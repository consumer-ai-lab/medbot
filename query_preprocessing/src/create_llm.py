from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CreateLLM:
    def __init__(self, model, llm_name, temp=0):
        self.llm = None
        if llm_name == "ChatGoogleGenerativeAI":
            self.llm = ChatGoogleGenerativeAI(model=model, temperature=temp, convert_system_message_to_human=True, google_api_key=os.getenv("GOOGLE_API_KEY"))
        elif llm_name == "GoogleGenerativeAI":
            self.llm = GoogleGenerativeAI(model=model, google_api_key=os.getenv("GOOGLE_API_KEY"))
        else:
            raise RuntimeError(message="Wrong llm name")

    @staticmethod
    def get_llm(model, llm_name, temp=0):
        return CreateLLM(model, llm_name, temp)