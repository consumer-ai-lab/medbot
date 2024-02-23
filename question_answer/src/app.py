from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
import google.generativeai as genai
import os
from langchain_core.messages import HumanMessage

load_dotenv(find_dotenv())
load_dotenv()
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
async def hello(req_body:GenerateRequest):
    print(req_body.query)
    print(os.getenv('GOOGLE_API_KEY'))
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5,convert_system_message_to_human=True)
    res=llm.invoke(
    [
        HumanMessage(
            content=req_body.query
        )
    ]
    )
    return {"ai_response":res.content}