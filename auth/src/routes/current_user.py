from fastapi import APIRouter,Depends
from ..database.models import User
from ..security import get_current_user
from ..database.schemas import UserBase

router = APIRouter()

@router.get('/current-user')
async def get_current_user(current_user:User=Depends(get_current_user)):
    user = UserBase(user_name=current_user.user_name,email=current_user.email)


