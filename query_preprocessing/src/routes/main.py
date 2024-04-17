from fastapi import APIRouter
from .chat import router as chat_router
from .thread import router as thread_router


router = APIRouter()

router.include_router(router=chat_router)
router.include_router(router=thread_router)