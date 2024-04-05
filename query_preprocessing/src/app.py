from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from .redis_manager import get_redis_manager
from .chat_summary_manager import get_chat_summary_manager
from pydantic import BaseModel

app = FastAPI(root_path="/api/chat")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    conversation_id:str
    content:str

@app.get("/")
def root():
    return {"message":"hello from query_preprocessing_service"}


@app.post('/generate')
def get_ai_message(req_body:Message):
    chat_manager = get_redis_manager(req_body.conversation_id)
    chat_history = chat_manager.get_messages()
    summary_manager = get_chat_summary_manager(temperature=0.2)

    # Generate a standalone query for question answer service.
    query=summary_manager.generate_query(chats=chat_history,new_query=req_body.content)
    try:
        response = requests.post(
            f'http://qa-service:8000/get-ai-response',
            json={"query": query}
        )
        response.raise_for_status()
        ai_response = response.json()
    except requests.exceptions.RequestException as e:
        chat_manager.add_user_message(req_body.content)
        return {"error": f"Request to qa_service failed: {e}"}
    else:
        chat_manager.add_user_message(req_body.content)
        chat_manager.add_ai_message(ai_response.get('ai_response'))
        return {"ai_response":ai_response.get("ai_response")}