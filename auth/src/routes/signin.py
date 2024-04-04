from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from ..security import authenticate_user,create_access_token
from ..database.schemas import Token
from pydantic import BaseModel
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPRIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPRIRE_MINUTES")

router = APIRouter()

@router.post('/token',response_model=Token)
def login_for_access_token(
    form_data:OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.email,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPRIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email},
        expires_delta=access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}
    

class SignInRequest(BaseModel):
    email:str
    password:str

@router.post('/signin')
def login_for_access_token(
    signin_request:SignInRequest
):
    user = authenticate_user(signin_request.email,signin_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPRIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email},
        expires_delta=access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}
    