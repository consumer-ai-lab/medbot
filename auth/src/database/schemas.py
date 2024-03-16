from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username:str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str
    token_type:str