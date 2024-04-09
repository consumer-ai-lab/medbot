from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import pprint
import json

from .proompts import (
    question_rephrase_prompt_template,
    chatbot_with_history_promt_template,
    chatbot_promt_template,
    generic_chatbot_promt_template,
    search_query_prompt_template,
)


def printer_print(x):
    print()
    pprint.pprint(x)
    print()
    return x


printer = RunnableLambda(printer_print)


def hacky_extract_json_dict(x):
    if "{" not in x:
        raise RuntimeError(f"string does not contain a json object: {x}")

    inside = x.split("{")[1]
    inside = inside.split("}")[0]
    return "{" + inside + "}"


def hacky_extract_json_list(x):
    if "[" not in x:
        raise RuntimeError(f"string does not contain a json object: {x}")

    inside = x.split("[")[1]
    inside = inside.split("]")[0]
    return "[" + inside + "]"


class Proompter:
    def question_rephrase_chain(self, llm):
        """prompt summary"""
        return (
            question_rephrase_prompt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
            | RunnableLambda(hacky_extract_json_dict)
            | printer
            | RunnableLambda(lambda x: json.loads(x))
            | RunnableLambda(lambda x: x["question"])
        )

    def medical_chatbot_prompt_chain(self, llm):
        """context prompt"""
        return chatbot_promt_template | printer | llm | printer | StrOutputParser()

    def medical_chatbot_with_history_prompt_chain(self, llm):
        """context prompt summary"""
        return (
            chatbot_with_history_promt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
        )

    def generic_chatbot_prompt_chain(self, llm):
        """prompt summary"""
        return (
            generic_chatbot_promt_template | printer | llm | printer | StrOutputParser()
        )

    def generate_search_queries_chain(self, llm):
        """prompt summary"""
        return (
            search_query_prompt_template
            | llm
            | StrOutputParser()
            | printer
            | RunnableLambda(hacky_extract_json_list)
            | RunnableLambda(lambda x: json.loads(x))
        )
