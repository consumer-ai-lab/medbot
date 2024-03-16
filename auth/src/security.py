from datetime import datetime,timedelta,timezone
from fastapi import Depends, HTTPException, Request, status, APIRouter
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from typing import Optional,Dict
from sqlalchemy.orm import Session
from .database.crud import get_user_by_email
from .database.config import get_db
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPRIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPRIRE_MINUTES")
COOKIE_NAME=os.getenv("COOKIE_NAME")


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl:str,
        schema_name:Optional[str]=None,
        scopes:Optional[Dict[str,str]]=None,
        auto_error:bool = True
    ):
        if not scopes:
            scopes={}
            flows = OAuthFlowsModel(password={"tokenUrl":tokenUrl,"scopes":scopes})
            super().__init__(flows=flows,scheme_name=schema_name,auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization:str = request.cookies.get("access_token")

        schema,param = get_authorization_scheme_param(authorization)
        if not authorization or schema.lower()!='bearer':
            return None
        return param
        

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_schema = OAuth2PasswordBearerWithCookie(tokenUrl="signin")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta: timedelta|None=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta 
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=50)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user =  get_user_by_email(db=db,email=email)
    if user is None:
        raise credentials_exception
    return user

   
        