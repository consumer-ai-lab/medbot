from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
async def sign_up_user():
    return {"route":"sign_up_user"}


