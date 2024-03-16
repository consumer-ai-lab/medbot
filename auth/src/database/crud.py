from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from ..security import verify_password


def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()

def authenticate_user(db:Session,email:str,password):
    db_user=get_user_by_email(db=db,email=email)
    if not db_user:
        return False
    if not verify_password(password,db_user.hashed_password):
        return False
    return db_user


def create_user(db:Session,user:UserCreate):
    db_user = User(email=user.email,hashed_password=user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        return None
    return db_user

