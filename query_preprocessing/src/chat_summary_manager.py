import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import find_dotenv, load_dotenv
from typing import List

import os
import pprint

from .types import Message, MessageRole
from .proompts import summarization_prompt_template
from .proompter import printer

# set_debug(True)

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def summary_chain(llm):
    summarization_chain = (
        RunnableLambda(
            lambda x: PromptTemplate(
                template=summarization_prompt_template.invoke(x).to_string(),
                input_variables=[],
            ).invoke({})
        )
        | printer
        | llm
        | printer
        | StrOutputParser()
    )

    def get_summary(x):
        def get_history_object(mesg):
            if mesg.role == MessageRole.assistant:
                return AIMessage(mesg.content)
            else:
                return HumanMessage(mesg.content)

        history = x["history"]

        if len(history) > 0:
            return summarization_chain.invoke(
                {"history": list(map(get_history_object, history))}
            )
        else:
            return "None"

    return RunnableLambda(get_summary)


class ChatSummaryManager:
    def __init__(self, llm):
        self.llm = llm

    def summarize_chats(self, history: List[Message]) -> str:
        chain = summary_chain(self.llm)
        return chain.invoke({"history": history})


def get_chat_summary_manager(llm) -> ChatSummaryManager:
    llm = llm
    return ChatSummaryManager(llm=llm)
