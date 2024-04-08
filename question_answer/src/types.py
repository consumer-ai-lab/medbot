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

class Query(pydantic.BaseModel):
    question: str
    model: Model

class ApiThreadQuery(pydantic.BaseModel):
    user_id: str
    thread_id: str

class ApiQuery(pydantic.BaseModel):
    user_id: str
    thread_id: str
    model: Model
    question: str

class QaQuery(pydantic.BaseModel):
    model: Model
    question: str
    summary: str


class QaResponse(pydantic.BaseModel):
    class Type(str, enum.Enum):
        # ERROR = "ERROR"
        OK = "OK"
        REJECTED = "REJECTED"

    type: Type
    response: str


