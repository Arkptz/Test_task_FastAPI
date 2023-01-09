from app.model import PostSchema
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

app = FastAPI()


posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Engine!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    print(user)
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.login)

@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    print(post.dict())
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }