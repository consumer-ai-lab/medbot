from pydantic import BaseModel
from typing import Optional
from enum import Enum



class UserLevel(str,Enum):
    admin = "admin"
    user = "user"


class SignInUser(BaseModel):
    email:str
    password:str


class UserBase(BaseModel):
    email:str
    user_name:str
    user_level:UserLevel = UserLevel.user

class RegisterUser(UserBase):
    password:str

class UserInDB(UserBase):
    hashed_password:str

class TokenData(BaseModel):
    email:Optional[str] = None
    user_level:Optional[UserLevel] = None

class Token(BaseModel):
    access_token:str
    token_type:str