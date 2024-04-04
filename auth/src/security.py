from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
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
ACCESS_TOKEN_EXPRIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPRIRE_MINUTES")

pwd_context = CryptContext(schemes=["brcypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


def create_access_token(*args,data:dict,expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+expires_delta
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPRIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()


def get_current_user(
    token:str = Depends(oauth2_scheme),
    db:Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email:str=payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db,email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

    