from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
import json
from dotenv import load_dotenv, find_dotenv
import pprint

from .create_llm import CreateLLM
from .types import Model, QaQuery, RelevanceResponse
from .proompter import printer, Proompter
from .proompts import guard_prompt_template, guard_prompt2_template

load_dotenv(find_dotenv())


class RelevenceProompter(Proompter):
    def guard_chain1(self, llm):
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


    def guard_chain2(self, llm):
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

    def relevance_chain(self, llm):
        chain = self.guard_chain1(llm)
        # chain = guard_chain2(llm)
        return (
            chain
            | self.hacky_string_dict_chain()
            | RunnableLambda(lambda x: RelevanceResponse(**x))
        )
