from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from .chat_manager import get_chat_manager

load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    query: str
    conversation_id:str


@app.post('/get-ai-response')
def query(req_body:GenerateRequest):
    chat_manager = get_chat_manager()
    # response = chat_manager.get_response(query=req_body.query,session_id=req_body.conversation_id)
    return {"ai_response":"response"}

