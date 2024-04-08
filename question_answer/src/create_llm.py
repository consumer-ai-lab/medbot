from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq

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
            case Model.ollama_llama2 | Model.ollama_llama2_uncensored:
                self.llm = Ollama(
                    base_url=os.getenv("OLLAMA_URL"),
                    model=model.value + ":vram-34",
                    temperature=temp,
                )
            case Model.groq_mistral_8x7b | Model.groq_llama2_70b | Model.groq_gemma_7b:
                self.llm = ChatGroq(
                    model_name=model.model(),
                    temperature=temp,
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                )
            case _:
                raise RuntimeError(message="Wrong llm name")
