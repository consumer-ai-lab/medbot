from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database.schemas import SignInUser,UserBase
from ..database.models import User
from ..database.config import get_db
from ..security import create_access_token,verify_password



router = APIRouter()


@router.post('/signin')
async def sign_in_user(
    user:SignInUser,
    db:Session=Depends(get_db)
):
    # check if user exists
    db_user = db.query(User).filter(User.email==user.email).first()
    if not user:
        return {"message":"User does not exist"}

    # check if password match
    if not verify_password(user.password,db_user.hashed_password):
        return {"message":"Invalid password"}
    
    # create jwt
    encoded_jwt=create_access_token(data={"sub":db_user.user_name, "email": db_user.email, "user_level": db_user.user_level})

    # set cookie
    user = UserBase(user_name=db_user.user_name,email=user.email,user_level=db_user.user_level)

    response = JSONResponse(content=user.model_dump(),status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="jwt",
        value=encoded_jwt,
    )
    return response
