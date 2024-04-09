from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .security import get_current_user,UserBase
import requests
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import find_dotenv, load_dotenv
from typing import List

from .gaurdrails import is_relevent
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
from .chat_summary_manager import get_chat_summary_manager
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


@app.post("/generate")
async def get_ai_message(query: ApiQuery,current_user: UserBase=Depends(get_current_user)):
    # llm = CreateLLM(query.model).getModel()

    chat_manager = get_redis_manager(current_user.user_id)
    if not chat_manager.has_thread(query.thread_id):
        chat_manager.add_thread(
            ChatThread(id=query.thread_id, title=query.prompt)
        )
    chat_history = chat_manager.get_chat(query.thread_id)

    chat_manager.add_message(
        query.thread_id, Message(role=MessageRole.user, content=query.prompt)
    )

    # TODO
    # summary_manager = get_chat_summary_manager(llm)
    # summary = summary_manager.summarize_chats(history=chat_history)

    qa_query = QaQuery(**(query.dict() | {"summary": "no previous chat history"}))
    # qa_query = QaQuery(**(query.dict()))
    # if not is_relevent(llm, qa_query):
    if True:
        resp = QaResponse(
            **{
                "type": QaResponse.Type.REJECTED,
                "response": "I am sorry, I am not able to answer this question. Please ask something else related to medicine.",
            }
        )

        # TODO: add the message to the chat history
        chat_manager.add_message(
            query.thread_id,
            Message(role=MessageRole.assistant, content=resp.response),
        )

        async def generator():
            for chunk in resp.response.split():
                yield f"{chunk} " 
                await asyncio.sleep(0.1)

        response_messages=generator()

        return StreamingResponse(response_messages, media_type="text/event-stream")

    

    try:
        response = requests.post(
            "http://qa-service:8000/get-ai-response", json=qa_query.dict()
        )
        response.raise_for_status()
        ai_response = response.json()
    except requests.exceptions.RequestException as e:
        # return QaResponse(**{"type": QaResponse.Type.ERROR, "response": e})
        raise HTTPException(status_code=418, detail=e)
    else:
        chat_manager.add_message(
            query.thread_id,
            Message(role=MessageRole.assistant, content=ai_response.get("ai_response")),
        )
        return QaResponse(
            **{
                "type": QaResponse.Type.OK,
                "response": ai_response.get("ai_response"),
            }
        )


@app.post("/get-threads")
def threads(current_user: UserBase=Depends(get_current_user)) :
    chat_manager = get_redis_manager(current_user.user_id)
    threads = chat_manager.get_threads()
    return threads



@app.post("/thread")
def thread(query: ApiThreadQuery,current_user: UserBase=Depends(get_current_user)) -> List[Message]:
    chat_manager = get_redis_manager(current_user.user_id)
    chat_history = chat_manager.get_chat(query.thread_id)
    return chat_history


## I will test it when frontend is ready, till then donot use

# @app.post('/generate')
# def get_ai_message(req_body: Message):
#     return StreamingResponse(gen_streaming_response(req_body))

# def gen_streaming_response(req_body:Message):
#     chat_manager = get_redis_manager(req_body.conversation_id)
#     chat_history = chat_manager.get_messages()
#     summary_manager = get_chat_summary_manager(temperature=0.2)

#     # Generate a standalone query for question answer service.
#     query=summary_manager.generate_query(chats=chat_history,new_query=req_body.content)
#     try:
#         response = requests.post(
#             f'http://qa-service:8000/get-ai-response',
#             json={"query": query}
#         )
#         response.raise_for_status()
#         ai_response = response.json()
#     except requests.exceptions.RequestException as e:
#         chat_manager.add_user_message(req_body.content)
#         yield {"error": f"Request to qa_service failed: {e}"}
#     else:
#         chat_manager.add_user_message(req_body.content)
#         chat_manager.add_ai_message(ai_response.get('ai_response'))
#         yield {"ai_response":ai_response.get("ai_response")}
