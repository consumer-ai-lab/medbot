from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Ollama

from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic

from .types import Model, EmbeddingsModel

load_dotenv(find_dotenv())


class CreateLLM:
    def __init__(self, model: Model, embeddings_model: EmbeddingsModel, temp=0):
        self.model = model
        self.embeddings_model = embeddings_model
        self.temp = temp
            
    def getModel(self):
        match self.model:
            case Model.gemini_pro:
                llm = GoogleGenerativeAI(
                    model=self.model.model(), google_api_key=os.getenv("GOOGLE_API_KEY")
                )
            case Model.gemini_pro_chat:
                llm = ChatGoogleGenerativeAI(
                    model=self.model.model(),
                    temperature=self.temp,
                    convert_system_message_to_human=True,
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                )
            case Model.ollama_llama2 | Model.ollama_llama2_uncensored:
                llm = Ollama(
                    base_url=os.getenv("OLLAMA_URL"),
                    model=self.model.model() + ":vram-34",
                    temperature=self.temp,
                )
            case Model.groq_mistral_8x7b | Model.groq_llama2_70b | Model.groq_gemma_7b:
                llm = ChatGroq(
                    model_name=self.model.model(),
                    temperature=self.temp,
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                )
            case Model.claude_3_opus:
                llm = ChatAnthropic(
                    model_name=self.model.model(),
                    temperature=self.temp,
                    anthropic_api_key=os.getenv("CLAUDE_API_KEY"),
                )
            case _:
                raise RuntimeError(message="Wrong llm name")
        return llm

    def get_embeddings(self):
        match self.embeddings_model:
            case EmbeddingsModel.gemini_pro:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            case EmbeddingsModel.ollama_llama2 | EmbeddingsModel.ollama_llama2_uncensored:
                embeddings = OllamaEmbeddings(model=self.embeddings_model.model() + ":vram-34")
            case _:
                raise RuntimeError("unknown embedding model")
        return embeddings
