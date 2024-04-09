from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
import json
from dotenv import load_dotenv, find_dotenv
import pprint

from .create_llm import CreateLLM
from .types import Model, QaQuery, RelevanceResponse
from .proompter import printer, hacky_extract_json_dict
from .proompts import guard_prompt_template, guard_prompt2_template

load_dotenv(find_dotenv())


def guard_chain1(llm):
    return (
        RunnableParallel(context=lambda x: x["summary"], prompt=lambda x: x["prompt"])
        | printer
        | RunnableLambda(
            lambda x: PromptTemplate(
                template=guard_prompt_template.invoke(x).to_string(),
                input_variables=[],
            ).invoke({})
        )
        | printer
        | llm
        | printer
        | StrOutputParser()
    )


def guard_chain2(llm):
    return (
        RunnableParallel(prompt=lambda x: x["prompt"])
        | printer
        | RunnableLambda(
            lambda x: PromptTemplate(
                template=guard_prompt2_template.invoke(x).to_string(),
                input_variables=[],
            ).invoke({})
        )
        | printer
        | llm
        | printer
        | StrOutputParser()
    )


def relevance_chain(llm):
    chain = guard_chain1(llm)
    # chain = guard_chain2(llm)
    return (
        chain
        | RunnableLambda(lambda x: json.loads(x))
        | RunnableLambda(lambda x: RelevanceResponse(**x))
    )
