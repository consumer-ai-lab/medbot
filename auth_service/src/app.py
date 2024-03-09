import os
import requests
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from .model import UserSchema, UserLoginSchema
from .auth_handler import signJWT
from .auth_bearer import JWTBearer

load_dotenv()

# TODO: protect cors in future
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    conversation_id:str
    content:str

@app.get("/")
def root():
    return {"message":"hello from auth_service"}


users = []
def check_user(user):
    for u in users:
        if u.email == user.email and u.password == user.password:
            return True
    return False

# TODO: add prisma client for handling db operations
@app.post("/auth/signup", tags=["authentication"])
def create_user(user: UserSchema = Body(...)):
    
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/auth/login", tags=["authentication"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }