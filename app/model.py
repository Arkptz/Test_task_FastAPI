from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "JWT tokens...."
            }
        }

class PostEditSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "JWT tokens...."
                }
        }


class PagePostSchema(BaseModel):
    num_page: int = Field(...)
    page_size: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "num_page": 1,
                "page_size": 50
            }
        }

class RemovePostSchema(BaseModel):
    id: int = Field()

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
            }
        }


class UserSchema(BaseModel):
    login: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "Enzensus",
                'email': 'example@example.com',
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "Enzensus",
                "password": "weakpassword"
            }
        }