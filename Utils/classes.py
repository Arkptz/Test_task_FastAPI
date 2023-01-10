from dataclasses import dataclass

@dataclass
class User:
    uuid:str
    login:str
    email:str
    password:str
    current_token:str


@dataclass
class Post:
    id:int
    title:str
    content:str
    user_uuid:str