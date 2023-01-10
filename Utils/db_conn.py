import sqlite3 as sl
from typing import Union
from dataclasses import dataclass
from app.model import PostSchema, UserSchema, UserLoginSchema, RemovePostSchema, PagePostSchema, PostEditSchema
from app.auth.auth_handler import signJWT
from config import db_path
from .classes import User, Post
from uuid import uuid4


@dataclass
class Base:
    db: sl.Connection
    cursor: sl.Cursor


class UsersDatabaseConnector(Base):
    """connector to database w/ users"""

    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                uuid TEXT,
                                login TEXT,
                                email TEXT,
                                password TEXT,
                                current_token TEXT
                                )''')
        self.db.commit()

    def create_user(self, user: UserSchema) -> User:
        jwt = signJWT(user.login)
        data = [str(uuid4()), user.login, user.email, user.password, jwt]
        self.cursor.execute('INSERT INTO User VALUES(?,?,?,?,?)', data)
        self.db.commit()
        return User(*data)

    def update_user(self, user: User) -> None:
        data = list(user.__dict__.values())[1:]
        data.append(user.uuid)
        self.cursor.execute(
            'UPDATE User SET login=?, email=?, password=?, current_token=? WHERE uuid=?', data)
        self.db.commit()

    def check_user(self, user: UserSchema) -> bool:
        data_login = self.cursor.execute(
            'SELECT * FROM User WHERE login=?', [user.login]).fetchall()
        data_email = self.cursor.execute(
            'SELECT * FROM User WHERE email=?', [user.email]).fetchall()
        if len(data_login) == 0 and len(data_email) == 0:
            return True
        return False

    def login(self, user: UserLoginSchema) -> Union[bool, User]:
        data = self.cursor.execute(
            'SELECT * FROM User WHERE login=? AND password=?', [user.login, user.password]).fetchall()
        if len(data) == 0:
            return False
        _user = User(*data[0])
        jwt = signJWT(user.login)
        _user.current_token = jwt
        self.update_user(_user)
        return _user

    def get_user_from_token(self, jwt: str) -> User:
        jwt = jwt.replace('Bearer ', '')
        data = self.cursor.execute(
            'SELECT * FROM User WHERE current_token=?', [jwt]).fetchone()
        return User(*data)


class PostsDatabaseConnector(Base):
    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Post (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                content TEXT,
                                user_uuid TEXT
                                )''')
        self.db.commit()

    def create_post(self, post: PostSchema, user: User) -> Post:
        data = [
            post.title,
            post.content,
            user.uuid
        ]
        self.cursor.execute(
            'INSERT INTO Post (title, content, user_uuid) VALUES(?,?,?)', data)
        id = self.cursor.execute('SELECT MAX(id) FROM Post').fetchone()[0]
        self.db.commit()
        return Post(id, *data)

    def get_list_posts(self, page: PagePostSchema) -> list[Post]:
        num = page.page_size * (page.num_page-1)
        data = self.cursor.execute(
            'SELECT * FROM Post WHERE id=2').fetchall()[num:num+page.page_size]
        return [Post(*i).__dict__ for i in data]

    def get_post(self, id: int) -> Post:
        data = self.cursor.execute(
            'SELECT * FROM Post WHERE id=?', [id]).fetchall()
        if len(data) == 0:
            return None
        return Post(*data[0])


    def update_post(self, edit:PostEditSchema, id:int):
        self.cursor.execute('UPDATE Post SET title=?, content=? WHERE id=?', [edit.title, edit.content, id])
        self.db.commit()

    def delete_post(self, post: Post) -> None:
        self.cursor.execute('DELETE FROM Post WHERE id=?', [post.id])
        self.db.commit()


connect = sl.connect(db_path)
cursor = sl.Cursor(connect)
db_users = UsersDatabaseConnector(connect, cursor)
db_posts = PostsDatabaseConnector(connect, cursor)
for i in [db_users, db_posts]:
    i.create_table()
