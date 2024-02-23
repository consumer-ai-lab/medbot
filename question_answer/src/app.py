from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/chat/')
def hello():
    return {"message":"Hello, from k8s cluster"}