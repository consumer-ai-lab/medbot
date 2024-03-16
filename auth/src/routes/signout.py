from fastapi import APIRouter

router = APIRouter()

@router.post("/signout")
async def sign_out_user():
    return {"route":"signout_user"}

