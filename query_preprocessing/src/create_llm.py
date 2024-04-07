from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
import os
from dotenv import load_dotenv, find_dotenv

from .types import Model

load_dotenv(find_dotenv())

class CreateLLM:
    def __init__(self, model, temp=0):
        match model:
            case Model.gemini_pro:
                self.llm = GoogleGenerativeAI(
                    model=model.model(), google_api_key=os.getenv("GOOGLE_API_KEY")
                )
            case Model.gemini_pro_chat:
                self.llm = ChatGoogleGenerativeAI(
                    model=model.model(),
                    temperature=temp,
                    convert_system_message_to_human=True,
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                )
            case _:
                raise RuntimeError(message="Wrong llm name")
