from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from ..database.models import User
from ..security import get_current_user

router = APIRouter()

@router.get('/current-user')
async def get_current_user(current_user:User=Depends(get_current_user)):
    return  JSONResponse(content=current_user.model_dump(),status_code=status.HTTP_200_OK)


