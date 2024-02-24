from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import find_dotenv,load_dotenv
import os

load_dotenv(find_dotenv())


app = FastAPI(root_path='/api/rag')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def process_uploaded_file(file: UploadFile):
  loader = PyPDFLoader(file)
  pages = loader.load_and_split()
  print(pages[0])

@app.get("/")
def root():
    return {"message":"hello from rag_uploader"}


@app.post('/upload')
async def upload_file(file:UploadFile=File(...)):
    try:
        await process_uploaded_file(file)
    except:
        return {"error":"There was an error while saving the file"}