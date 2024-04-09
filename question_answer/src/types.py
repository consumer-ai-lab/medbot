import enum
import pydantic


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class Message(pydantic.BaseModel):
    role: MessageRole
    content: str

class ChatThread(pydantic.BaseModel):
    title: str
    id: str


# :skull https://stackoverflow.com/questions/77550506/what-is-the-right-way-to-do-system-prompting-with-ollama-in-langchain-using-pyth
class Model(str, enum.Enum):
    gemini_pro = "gemini-pro"
    gemini_pro_chat = "gemini-pro-chat"
    ollama_llama2 = "ollama-llama2"
    ollama_llama2_uncensored = "ollama-llama2-uncensored"

    # - [GroqCloud](https://console.groq.com/docs/models)
    groq_mistral_8x7b = "groq-mistral-8x7b"
    groq_llama2_70b = "groq-llama2-70b"
    groq_gemma_7b = "groq-gemma-7b"

    def model(self):
        match self:
            case Model.gemini_pro_chat | Model.gemini_pro:
                return "gemini-pro"
            case Model.ollama_llama2:
                return "llama2"
            case Model.ollama_llama2_uncensored:
                return "llama2-uncensored"
            case Model.groq_gemma_7b:
                return "gemma-7b-it"
            case Model.groq_llama2_70b:
                return "llama2-70b-4096"
            case Model.groq_mistral_8x7b:
                return "mixtral-8x7b-32768"
            case _:
                return self.value

class EmbeddingsModel(str, enum.Enum):
    gemini_pro = "gemini-pro"
    ollama_llama2 = "ollama-llama2"
    ollama_llama2_uncensored = "ollama-llama2-uncensored"

    def model(self):
        match self:
            case EmbeddingsModel.gemini_pro:
                return "gemini-pro"
            case EmbeddingsModel.ollama_llama2:
                return "llama2"
            case EmbeddingsModel.ollama_llama2_uncensored:
                return "llama2-uncensored"
            case _:
                return self.value

class Strategy(str, enum.Enum):
    medical_database = "medical-database"
    pubmed_search = "pubmed-search"
    web_search = "web-search"
    web_search_api = "web-search-api"

class Query(pydantic.BaseModel):
    prompt: str
    model: Model

class ApiThreadQuery(pydantic.BaseModel):
    thread_id: str

class ApiQuery(pydantic.BaseModel):
    thread_id: str
    model: Model
    embeddings_model: EmbeddingsModel
    strategy: Strategy
    prompt: str

class QaQuery(pydantic.BaseModel):
    model: Model
    embeddings_model: EmbeddingsModel
    strategy: Strategy
    prompt: str
    summary: str

class Related(str, enum.Enum):
    YES = "YES"
    NO = "NO"
    MAYBE = "MAYBE"
    ILLEGAL = "ILLEGAL"

class RelevanceResponse(pydantic.BaseModel):
    related: Related
    reason: str

    def is_related(self):
        match self.related:
            case "YES" | "MAYBE":
                return True
            case "NO" | "ILLEGAL":
                return False
            case _:
                return True

class QaResponse(pydantic.BaseModel):
    class Type(str, enum.Enum):
        # ERROR = "ERROR"
        OK = "OK"
        REJECTED = "REJECTED"

    type: Type
    response: str


