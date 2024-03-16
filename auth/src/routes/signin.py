from fastapi import APIRouter

router = APIRouter()

@router.post('/signin')
async def signin():
    return {"route":"signin"}