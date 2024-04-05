from fastapi import APIRouter
from .signin import router as signin_router
from .signup import router as signup_router
from .signout import router as signout_router
from .current_user import router as current_user_router

router = APIRouter(
    tags=["auth_routes"]
)
router.include_router(router=signin_router)
router.include_router(router=signup_router)
router.include_router(router=signout_router)
router.include_router(router=current_user_router)
