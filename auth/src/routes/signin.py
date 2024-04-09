from fastapi import APIRouter,Depends,status,HTTPException
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
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # check if password match
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    # create jwt
    encoded_jwt=create_access_token(data={"sub":str(db_user.id),"user_name":db_user.user_name, "email": db_user.email, "user_level": db_user.user_level})

    # set cookie
    user = UserBase(
        user_id=str(db_user.id),
        user_name=db_user.user_name,
        email=db_user.email,
        user_level=db_user.user_level
    )
    response = JSONResponse(content=user.model_dump(),status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="jwt",
        value=encoded_jwt,
    )
    return response
