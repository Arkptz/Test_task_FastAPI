from app.model import PostSchema
from fastapi import FastAPI, Body, Depends, HTTPException, Request
from app.model import PostSchema, UserSchema, UserLoginSchema, RemovePostSchema, PagePostSchema, PostEditSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import token_response
from Utils.db_conn import db_users, db_posts

app = FastAPI()





@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Engine!"}


@app.post("/posts", tags=["posts"])
async def get_posts(page:PagePostSchema) -> dict:
    return {"data": db_posts.get_list_posts(page)}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    # replace with db call, making sure to hash the password first
    if db_users.check_user(user):
        _user = db_users.create_user(user)
        return token_response(_user.current_token)
    raise HTTPException(status_code=403, detail='Such a user already exists!')


@app.post("/user/login", tags=["user"])
async def login(user: UserLoginSchema = Body(...)):
    # replace with db call, making sure to hash the password first
    _user = db_users.login(user)
    if _user:
        return token_response(_user.current_token)
    raise HTTPException(status_code=403, detail='There is no such user')


@app.put("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema, r :Request) -> dict:
    token = r.headers.get('authorization')
    _post = db_posts.create_post(post, db_users.get_user_from_token(token))
    return {
        "data": "post added."
    }


@app.delete("/posts/{id}", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def del_post(id: int, r :Request) -> dict:
    token = r.headers.get('authorization')
    user = db_users.get_user_from_token(token)
    _post = db_posts.get_post(id)
    if not _post:
        raise HTTPException(status_code=403, detail='There is no such publication.')
    if user.uuid == _post.user_uuid:
        db_posts.delete_post(_post)
        return {
            "data": "post deleted."
        }
    raise HTTPException(status_code=403, detail='You have no rights to delete this post!')

@app.patch("/posts/{id}", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def edit_post(id: int, r :Request, post:PostEditSchema) -> dict:
    token = r.headers.get('authorization')
    user = db_users.get_user_from_token(token)
    _post = db_posts.get_post(id)
    if not _post:
        raise HTTPException(status_code=403, detail='There is no such publication.')
    if user.uuid == _post.user_uuid:
        db_posts.update_post(post, id)
        return {
            "data": "post edited."
        }
    raise HTTPException(status_code=403, detail='You have no rights to delete this post!')
