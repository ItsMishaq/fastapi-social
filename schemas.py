from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint
# import time




class PostBase(BaseModel):
    title : str
    content : str
    # published: bool=True   


class PostCreate(PostBase):
    pass   

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner:UserOut
    class Config: #use to convert sqlalchemy to dictionary shape as pydantic models reads only dictionaries
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


 
class UserCreate(BaseModel):
    email : EmailStr
    password : str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    