from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from ..database.schemas import UserBase,UserInDB,RegisterUser
from ..database.models import User
from ..database.config import get_db
from ..security import get_password_hash,create_access_token
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/signup")
async def sign_up_user(
    user:RegisterUser,
    db:Session=Depends(get_db)
):
    # check if user exists
    existing_user = db.query(User).filter(User.email==user.email).first()
    if existing_user:
        return {"message":"User already exists"}
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(email=user.email,user_name=user.user_name,hashed_password=hashed_password)

    # create user
    db_user = User(**user_in_db.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # create jwt
    encoded_jwt=create_access_token(data={"sub":str(db_user.id),"user_name":db_user.user_name, "email": db_user.email, "user_level": db_user.user_level})

    # set cookie
    created_user = UserBase(user_name=db_user.user_name,email=db_user.email,user_level=db_user.user_level)
    response = JSONResponse(content=created_user.model_dump(),status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="jwt",
        value=encoded_jwt,
    )
    return response


    


