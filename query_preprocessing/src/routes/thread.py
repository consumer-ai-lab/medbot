from fastapi import APIRouter, Depends,Response,status
from ..security import get_current_user, UserBase
from dotenv import find_dotenv, load_dotenv
from typing import List
from ..types import (
    Message,
    ApiThreadQuery,
)
from ..redis_manager import get_redis_manager
from ..security import get_current_user, UserBase
from typing import List
from ..types import (
    Message,
    ApiThreadQuery,
)
from ..redis_manager import get_redis_manager

router = APIRouter(
    tags=["chat_history_routes"]
)

@router.get("/get-threads")
def threads(current_user: UserBase = Depends(get_current_user)):
    chat_manager = get_redis_manager(current_user.user_id)
    threads = chat_manager.get_threads()
    return threads


@router.post("/thread")
def thread(
    query: ApiThreadQuery, current_user: UserBase = Depends(get_current_user)
) -> List[Message]:
    chat_manager = get_redis_manager(current_user.user_id)
    chat_history = chat_manager.get_chat(query.thread_id)
    return chat_history

@router.delete("/delete-thread")
def delete_thread(
    query: ApiThreadQuery, current_user: UserBase = Depends(get_current_user)
):
    try:
        chat_manager = get_redis_manager(current_user.user_id)
        chat_manager.delete_thread(query.thread_id)
        response = Response(
            content="Deleted", status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print(e)
        response = Response(
            content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
