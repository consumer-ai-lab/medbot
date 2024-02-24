from fastapi import FastAPI,Path as PathParam, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel,Field
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import google.generativeai as genai
import os
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import PyPDFLoader

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


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

@app.post('/generate')
async def query(req_body:GenerateRequest):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5,convert_system_message_to_human=True)
    res=llm.invoke(
    [
        HumanMessage(
            content=req_body.query
        )
    ]
    )
    return {"ai_response":res.content}

async def process_uploaded_file(file: UploadFile):
  loader = PyPDFLoader(file)
  pages = loader.load_and_split()
  print(pages[0])


@app.post('/upload')
async def upload_file(file:UploadFile=File(...)):
    try:
        await process_uploaded_file(file)
    except:
        return {"error":"There was an error while saving the file"}
    
