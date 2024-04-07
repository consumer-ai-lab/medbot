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
    gemini_pro_chat = "gemini-pro-chat"
    gemini_pro = "gemini-pro"
    llama2 = "llama2"
    llama2_uncensored = "llama2-uncensored"

    def model(self):
        match self:
            case Model.gemini_pro_chat:
                return "gemini-pro"
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


