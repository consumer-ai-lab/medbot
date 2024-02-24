from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from .redis_manager import RedisManager
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
    chat_manager = RedisManager(req_body.conversation_id)
    chat_manager.add_user_message(req_body.content)
    try:
        response = requests.post(
            f'http://qa-service:8000/get-ai-response',
            json={"query": req_body.content,"conversation_id":req_body.conversation_id}
        )
        response.raise_for_status()
        ai_response = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request to qa_service failed: {e}"}
    else:
        chat_manager.add_ai_message(ai_response.get('ai_response'))
        return {"ai_response":ai_response.get("ai_response")}
    