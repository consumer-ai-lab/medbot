from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from ..security import get_current_user, UserBase
import requests
from ..guard_rails import RelevenceProompter
from ..types import (
    ApiQuery,
    QaQuery,
    QaResponse,
    Message,
    MessageRole,
    ChatThread,
)
from ..redis_manager import get_redis_manager
from ..chat_summary_manager import SummaryProompter
from ..create_llm import CreateLLM
import asyncio
from ..tokenbucket import get_token_bucket

router = APIRouter()

async def generator(resp):
    for chunk in resp.response.split():
        yield f"{chunk} "
        await asyncio.sleep(0.1)

token_bucket = None
@router.post("/generate")
async def get_ai_message(
    query: ApiQuery, current_user: UserBase = Depends(get_current_user)
):
    try:
        global token_bucket
        print(f"{current_user=}")
        token_bucket = get_token_bucket(key=current_user.user_id, sizeof_bucket=11) if token_bucket is None else token_bucket
        if token_bucket.size() == 1 and token_bucket.exists():
            raise HTTPException(
                status_code=429,
                detail="Too many API requests. Please wait for some time.",
            )
        elif not token_bucket.exists():
            token_bucket = get_token_bucket(key=current_user.user_id, sizeof_bucket=11)

        token_bucket.consume()
        llm = CreateLLM(query.model, query.embeddings_model).getModel()

        chat_manager = get_redis_manager(current_user.user_id)
        if not chat_manager.has_thread(query.thread_id):
            chat_manager.add_thread(ChatThread(id=query.thread_id, title=query.prompt))
        chat_history = chat_manager.get_chat(query.thread_id)

        chat_manager.add_message(
            query.thread_id, Message(role=MessageRole.user, content=query.prompt)
        )

        summarizer = SummaryProompter()
        summary = summarizer.get_summary(llm, chat_history)

        qa_query = QaQuery(**(query.dict() | {"summary": summary}))
        relevance = RelevenceProompter()
        guard_chain = relevance.relevance_chain(llm)
        resp = guard_chain.invoke(qa_query.dict())
        if not resp.is_related():
            resp = QaResponse(
                **{
                    "type": QaResponse.Type.REJECTED,
                    "response": resp.reason,
                }
            )

            chat_manager.add_message(
                query.thread_id,
                Message(role=MessageRole.assistant, content=resp.response),
            )

            return StreamingResponse(generator(resp), media_type="text/event-stream")

        response = requests.post(
            "http://qa-service:8000/get-ai-response", json=qa_query.dict()
        )
        response.raise_for_status()
        response = response.json()
        response = QaResponse(**response)
    except requests.exceptions.RequestException as e:
        # return QaResponse(**{"type": QaResponse.Type.ERROR, "response": e})
        raise HTTPException(status_code=418, detail=str(e))
    else:
        chat_manager.add_message(
            query.thread_id,
            Message(role=MessageRole.assistant, content=response.response),
        )
        return StreamingResponse(generator(response), media_type="text/event-stream")



