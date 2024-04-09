from jose import JWTError, jwt
from fastapi import  HTTPException, Request,status
import os
from dotenv import load_dotenv
import enum
import pydantic

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

class UserLevel(str,enum.Enum):
    admin = "admin"
    user = "user"


class UserBase(pydantic.BaseModel):
    user_id:str
    email:str
    user_name:str
    user_level:UserLevel = UserLevel.user


def get_current_user(request:Request):
    jwt_token  = request.cookies.get("jwt")
    if jwt_token is None:
        print("No JWT")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload.get("sub"))
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return UserBase(user_id=payload.get("sub"),user_name=payload.get("user_name"),email=payload.get("email"),user_level=payload.get("user_level"))

