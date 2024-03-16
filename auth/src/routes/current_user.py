from fastapi import APIRouter

router = APIRouter()

@router.get('/current-user')
async def get_current_user():
    return {"route":"current_user"}


