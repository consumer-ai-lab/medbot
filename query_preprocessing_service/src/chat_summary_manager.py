from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.messages import HumanMessage, SystemMessage

from langchain.globals import set_debug
import os
from dotenv import find_dotenv, load_dotenv

set_debug(False)

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class ChatSummaryManager:
    def __init__(self, model, temperature):
        self.model = model
        self.temperature = temperature
        self.llm = ChatGoogleGenerativeAI(model=self.model, temperature=self.temperature, convert_system_message_to_human=True)

    def combine_messages(self,messages):
        return "\n".join(f"{msg['type']} message: {msg['content']}" for msg in messages)
    
    def summarize_chats(self,chats:list)->str:
        message_str = self.combine_messages(messages=chats)
        system_message=SystemMessage(content="You are an AI assistant specialized in reading transcripts of conversation between human and AI. Your primary task is to provide brief, accurate summaries of these transcripts, ensuring no important details are omitted.")
        human_message=HumanMessage(content=f"Summarize the below conversation\n{message_str}")
        res = self.llm.invoke([system_message,human_message])
        return res.content
    

    def generate_query(self,chats:list,new_query:str)->str:
        summary = self.summarize_chats(chats)
        system_message=SystemMessage(content="You are an AI assistant with the capability to process summaries of conversations and related follow-up questions. Your task is to rephrase a given follow-up question so it can be understood as a standalone question, without needing additional context from the conversation summary. Ensure the rephrased question maintains the essence and specificity of the original query, allowing for clear and concise communication. Given below is the example of what kind of response is expected\nEXAMPLE\nSummary: The conversation involves an AI assistant providing guidance on integrating a function into a project, including parameter passing, error handling, and thread-safety\nfollow-up question: can you give me an example of the above?\nResponse: Can you provide an example of how to integrate a function into a project, including how to pass parameters, handle errors, and ensure the function is thread-safe?'\nEXAMPLE ENDS\n")
        human_message=HumanMessage(content=f"Summary: {summary} follow up question: {new_query}")
        res = self.llm.invoke([system_message,human_message])
        return res.content
    

def get_chat_summary_manager(model:str=None,temperature:float=None)->ChatSummaryManager:
    _model = model if model is not None else "gemini-pro"
    _temperature = temperature if temperature is not None else 0.5
    return ChatSummaryManager(model=_model,temperature=_temperature)

    