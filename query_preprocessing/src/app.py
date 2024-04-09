from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .security import get_current_user, UserBase
import requests
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import find_dotenv, load_dotenv
from typing import List

from .guard_rails import RelevenceProompter
from .types import (
    ApiQuery,
    QaQuery,
    QaResponse,
    Message,
    MessageRole,
    ChatThread,
    ApiThreadQuery,
)
from .redis_manager import get_redis_manager
from .chat_summary_manager import SummaryProompter
from .create_llm import CreateLLM
import asyncio

load_dotenv(find_dotenv())
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

app = FastAPI(root_path="/api/chat")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "hello from query_preprocessing_service"}


async def generator(resp):
    for chunk in resp.response.split():
        yield f"{chunk} "
        await asyncio.sleep(0.1)


@app.post("/generate")
async def get_ai_message(
    query: ApiQuery, current_user: UserBase = Depends(get_current_user)
):
    llm = CreateLLM(query.model, query.embeddings_model).getModel()

    chat_manager = get_redis_manager(current_user.user_id)
    if not chat_manager.has_thread(query.thread_id):
        chat_manager.add_thread(ChatThread(id=query.thread_id, title=query.prompt))
    chat_history = chat_manager.get_chat(query.thread_id)

    chat_manager.add_message(
        query.thread_id, Message(role=MessageRole.user, content=query.prompt)
    )

    try:
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


@app.get("/get-threads")
def threads(current_user: UserBase = Depends(get_current_user)):
    chat_manager = get_redis_manager(current_user.user_id)
    threads = chat_manager.get_threads()
    return threads


@app.post("/thread")
def thread(
    query: ApiThreadQuery, current_user: UserBase = Depends(get_current_user)
) -> List[Message]:
    chat_manager = get_redis_manager(current_user.user_id)
    chat_history = chat_manager.get_chat(query.thread_id)
    return chat_history

