from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv
from .query_manager import get_response
from .types import QaQuery, QaResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get-ai-response")
def query(query: QaQuery):
    response = get_response(query)
    return QaResponse(**{"type": QaResponse.Type.OK, "response": response["response"]})
