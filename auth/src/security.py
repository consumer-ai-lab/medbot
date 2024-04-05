from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .database.config import get_db
from .database.models import *
from .database.schemas import *

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(request:Request):
    jwt_token = request.cookies.get("jwt")
    if jwt_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return UserBase(user_name=payload.get("sub"),email=payload.get("email"),user_level=payload.get("user_level"))


def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)

def authenticate_user(email:str,password:str,db:Session = Depends(get_db)):
    db = get_db()
    user = db.query(User).filter(User.email==email).first()
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()



    