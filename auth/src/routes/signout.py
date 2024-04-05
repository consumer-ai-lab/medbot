from fastapi import APIRouter,status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/signout")
async def sign_out_user():
    response = JSONResponse(content={"message":"User signed out successfully"},status_code=status.HTTP_200_OK)
    response.delete_cookie("jwt")
    return response

