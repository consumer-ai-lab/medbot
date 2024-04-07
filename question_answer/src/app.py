from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv
from .query_manager import get_query_manager, ApiQuery

load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/get-ai-response')
def query(query: ApiQuery):
    query_manager = get_query_manager()
    response = query_manager.get_response(query)
    return {"ai_response": response["response"]}

