from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from .query_manager import get_query_manager

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

@app.post('/get-ai-response')
def query(req_body:GenerateRequest):
    query_manager = get_query_manager()
    response = query_manager.get_response(query=req_body.query)
    return {"ai_response":response}

