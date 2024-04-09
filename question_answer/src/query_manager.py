from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.transform import BaseTransformOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
)
from langchain_core.runnables.base import RunnableEach
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.document_compressors import (
    EmbeddingsFilter,
    DocumentCompressorPipeline,
)
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.vectorstores.pgvector import PGVector

from langchain_community.tools.pubmed.tool import PubmedQueryRun

# from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from bs4 import BeautifulSoup

from langchain.globals import set_debug

import google.generativeai as genai
import os
from typing import List, Dict
import pprint
import json
import requests
import enum
import pydantic
from dotenv import find_dotenv, load_dotenv

from langchain.globals import set_debug

from .types import Model, QaQuery, Strategy, EmbeddingsModel
from .create_llm import CreateLLM

# set_debug(True)

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


chatbot_long_prompt = """"
As an advanced and reliable medical chatbot, your foremost priority is to furnish the user with precise, evidence-based health insights and guidance. It is of utmost importance that you strictly adhere to the context provided, without introducing assumptions or extrapolations beyond the given information. Your responses must be deeply rooted in verified medical knowledge and practices. Additionally, you are to underscore the necessity for users to seek direct consultation from healthcare professionals for personalized advice.

In crafting your response, it is crucial to:
- Confine your analysis and advice strictly within the parameters of the context provided by the user. Do not deviate or infer details not explicitly mentioned.
- Identify the key medical facts or principles pertinent to the user's inquiry, applying them directly to the specifics of the provided context.
- Offer general health information or clarifications that directly respond to the user's concerns, based solely on the context.
- Discuss recognized medical guidelines or treatment options relevant to the question, always within the scope of general advice and clearly bounded by the context given.
- Emphasize the critical importance of professional medical consultation for diagnoses or treatment plans, urging the user to consult a healthcare provider.
- Where applicable, provide actionable health tips or preventive measures that are directly applicable to the context and analysis provided, clarifying these are not substitutes for professional advice.

Your aim is to deliver a response that is not only informative and specific to the user's question but also responsibly framed within the limitations of non-personalized medical advice. Ensure accuracy, clarity, and a strong directive for the user to seek out professional medical evaluation and consultation. Through this approach, you will assist in enhancing the user's health literacy and decision-making capabilities, always within the context provided and without overstepping the boundaries of general medical guidance.

Context: {context}

Summary: {summary}

Question: {prompt}
"""
chatbot_long_prompt_template = PromptTemplate(
    template=chatbot_long_prompt,
    input_variables=["context", "prompt", "summary"],
)


chatbot_with_history_prompt = """
### System: provided the summary, context and a question, answer it using the given context without mentioning the existance of this context. you may offer medical advice. when context is not related to the question, just say that you don't know about it.

### Symmary: []

### Context: <CONTEXT ABOUT KNEE SPRAINS>

### Question: how do i treat brain damage?

### AI: I can't tell you about treating brain damage as i don't know about it.


### Summary: {summary}

### Context: {context}

### Question: {prompt}

"""
chatbot_with_history_promt_template = PromptTemplate(
    template=chatbot_with_history_prompt,
    input_variables=["context", "prompt", "summary"],
)

chatbot_prompt = """
### System:
provided the context and a question, answer it using the given context. you may offer medical advice. do not deviate from the given context. when context is not related to the question, just say that the context does not have the answer to the question.

### Context:
<INFO ABOUT COWS>

### Question:
How many legs do cows have?

### AI:
Cows have 4 legs.


### Context:
<INFO ABOUT DOGS>

### Question:
Are cats mammals?

### AI:
Context does not have any information about cats.


### Context:
[]

### Question:
Are cats mammals?

### AI:
No context provided


### Context:
{context}

### Question:
{prompt}

### AI:
"""
chatbot_promt_template = PromptTemplate(
    template=chatbot_prompt, input_variables=["context", "prompt"]
)

question_rephrase_prompt = """
### System: you are an AI. your job is to rephrase the question given below with given context (if required) such that it is possible to answer it without any context. do not change the meaning of question. write the question as if it was written by the user. DO NOT answer the question. just rephrase it. output the response in json format as a single follows {{ "question": <REPHRASED QUESTION>, "remarks": <ANY OTHER REMARKS (OPTIONAL)> }}

### Context: user wants to know about brain damage.
### Question: what is it?
### Rephrased Question: {{ "question": "What is Brain Damage?", "remarks": "Note: Treating brain damage is a very serious issue." }}

### Context: None
### Question: What is fractal?
### Rephrased Question: {{ "question": "What are Fractals?" }}

### Context: {summary}
### Question: {prompt}
### Rephrased Question: 
"""
question_rephrase_prompt_template = PromptTemplate(
    template=question_rephrase_prompt, input_variables=["summary", "prompt"]
)

search_query_prompt = """
System: you are an AI. your job is to generate 3 search queries that are most likely to get the most relevent results from search engines. do not change the meaning of query. DO NOT answer the query. you must output it as a list of strings in json format.

Context: user and ai are talking about mountains.
Question: what is the tallest one called?
Rephrased Question: ["tallest mountains in the world", "mountain heights", "highest peaks in the world"]

Context: {summary}
Question: {prompt}
Rephrased Question: 
"""
search_query_prompt_template = PromptTemplate(
    template=search_query_prompt, input_variables=["summary", "prompt"]
)

generic_chatbot_prompt = """
Context: {context}

Question: {prompt}

System: you are a helpful and smart AI chatbot. provided the context and a question, answer it using the given context. do not deviate from the given context. give detailed and helpful answers.

AI:
"""
generic_chatbot_promt_template = PromptTemplate(
    template=generic_chatbot_prompt, input_variables=["context", "prompt"]
)


pubmed_query_prompt = """
System: you are an AI. your job is to generate 3 search queries that are most likely to get the most relevent results from Pubmed search. Do not change the meaning of query. DO NOT answer the query. you must output it as a list of strings in json format.

Question: My brother has ashtama. how do i make sure he is cured?
Rephrased Question: ["asthama treatment", "asthama definition", "asthama medication"]

Question: {prompt}
Rephrased Question: 
"""
pubmed_query_prompt_template = PromptTemplate(
    template=pubmed_query_prompt, input_variables=["prompt"]
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

class QaService:

    """ prompt summary """
    def question_rephrase_chain(self, llm):
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

    """ context prompt """
    def medical_chatbot_prompt_chain(self, llm):
        return (
            chatbot_promt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
        )

    """ context prompt summary """
    def medical_chatbot_with_history_prompt_chain(self, llm):
        return (
            chatbot_with_history_promt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
        )

    """ prompt summary """
    def generic_chatbot_prompt_chain(self, llm):
        return (
            generic_chatbot_promt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
        )

    """ prompt summary """
    def generate_search_queries_chain(self, llm):
        return (
            search_query_prompt_template
            | llm
            | StrOutputParser()
            | printer
            | RunnableLambda(hacky_extract_json_list)
            | RunnableLambda(lambda x: json.loads(x))
        )

class VectorDbQaService(QaService):
    def qa_chain(self, llm, embeddings):
        db = PGVector(
            collection_name=os.getenv("CONNECTION_NAME"),
            connection_string=os.getenv("CONNECTION_STRING"),
            embedding_function=embeddings,
        )

        return (
            printer
            | RunnableParallel(
                prompt=self.question_rephrase_chain(llm),
                summary=lambda x: x["summary"],
            )
            | printer
            | RunnableParallel(
                prompt=lambda x: x["prompt"],
                summary=lambda x: x["summary"],
                context=lambda x: db.as_retriever().invoke(x["prompt"]),
            )
            | printer
            | RunnableParallel(
                response=self.medical_chatbot_prompt_chain(llm),
                context=lambda x: x["context"],
            )
            | printer
        )


class PubmedQaService(QaService):
    def genrate_search_queries_chain(self, llm):
        return (
            RunnableParallel(
                questions=(
                    # search_query_prompt_template
                    pubmed_query_prompt_template
                    | llm
                    | StrOutputParser()
                    | printer
                    | RunnableLambda(lambda x: json.loads(x))
                ),
                prompt=lambda x: x["prompt"],
            )
            | printer
            # | RunnableLambda(lambda x: [x["prompt"]] + x["questions"])
            | RunnableLambda(lambda x: x["questions"])
            | printer
        )

    def pubmed_context_chain(self, llm):
        return (
            self.genrate_search_queries_chain(llm)
            | RunnableEach(
                bound=(
                    RunnableParallel(
                        prompt=lambda x: x,
                        context=lambda x: Document(page_content=PubmedQueryRun().invoke(x)),
                    )
                )
            )
        )

    def qa_chain(self, llm, embeddings):
        return (
            printer
            | RunnableParallel(
                prompt=self.question_rephrase_chain(llm),
                summary=lambda x: x["summary"],
            )
            | printer
            | RunnableParallel(
                prompt=lambda x: x["prompt"],
                summary=lambda x: x["summary"],
                context=self.pubmed_context_chain(llm),
            )
            | printer
            | RunnableParallel(
                response=self.medical_chatbot_prompt_chain(llm),
                context=lambda x: x["context"],
            )
            | printer
        )

class InternetQaService(QaService):
    def __init__(self):
        self.session = None

    class UrlExtractionMethod(enum.Enum):
        CHROME = "chrome"
        REQUESTS = "requests"

    class AllDocsRetriever(BaseRetriever):
        docs: List[Document] = []

        def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
        ) -> List[Document]:
            return self.docs

    def url_content_extraction_chain(self, method: UrlExtractionMethod):
        tags = ["p", "h1", "h2", "h3", "h4", "h5", "span"]

        # TODO: make it work in docker
        def chrome_loader(urls):
            # loader = AsyncChromiumLoader(urls)
            # html = loader.load()
            # bs_transformer = BeautifulSoupTransformer()
            # docs_transformed = bs_transformer.transform_documents(
            #     html, tags_to_extract=tags
            # )
            # docs = []
            # for doc in docs_transformed:
            #     doc = {
            #         "page_content": doc.page_content,
            #         "source": doc.metadata["source"],
            #     }
            #     docs.append(doc)
            # return docs
            pass

        def requests_loader(urls):
            if self.session is None:
                self.session = requests.Session()

            docs = []
            for url in urls:
                response = self.session.get(url, timeout=4)
                soup = BeautifulSoup(
                    response.content, "lxml", from_encoding=response.encoding
                )
                text = ""
                for element in soup.find_all(tags):
                    text += element.text + "\n"
                doc = {
                    "page_content": text,
                    "source": url,
                }
                docs.append(doc)
            return docs
            pass

        if method == InternetQaService.UrlExtractionMethod.CHROME:
            loader = chrome_loader
        elif method == InternetQaService.UrlExtractionMethod.REQUESTS:
            loader = requests_loader
        else:
            raise RuntimeError("unknown url extraction method")

        return RunnableLambda(lambda x: loader(x["urls"]))

    def generate_questions_chain(self, llm):
        return (
            RunnableParallel(
                questions=self.generate_search_queries_chain(llm),
                prompt=lambda x: x["prompt"],
            )
            | printer
            | RunnableLambda(lambda x: [x["prompt"]] + x["questions"])
            | printer
        )

    def search_engine_chain(self):
        ddg = DuckDuckGoSearchAPIWrapper()

        def search(query):
            res = ddg.results(query, 3)
            # snippet title link
            return list(map(lambda x: x["link"], res))

        return RunnableLambda(search)

    def web_context_chain(self, llm, embeddings):
        def retriever(pages):
            # - [Contextual compression | 🦜️🔗 Langchain](https://python.langchain.com/docs/modules/data_connection/retrievers/contextual_compression/)
            # - [Retrievers | 🦜️🔗 Langchain](https://python.langchain.com/docs/modules/data_connection/retrievers/)

            docs = [
                Document(
                    page_content=d["page_content"], metadata={"source": d["source"]}
                )
                for d in pages
            ]
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100
            )

            # retriever = InternetQaService.AllDocsRetriever(docs=docs)
            # filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
            # compressor = DocumentCompressorPipeline(
            #     transformers=[splitter, filter]
            # )
            # # compressor = LLMChainExtractor.from_llm(llm)
            # contextual_retriever = ContextualCompressionRetriever(
            #     base_compressor=compressor, base_retriever=retriever
            # )
            # return contextual_retriever

            faiss = FAISS.from_documents(splitter.split_documents(docs), embeddings)
            retriever = faiss.as_retriever(search_kwargs={"k": 5})
            return retriever

        return (
            RunnableParallel(
                prompt=lambda x: x["prompt"],
                pages=(
                    self.generate_questions_chain(llm)
                    | RunnableEach(
                        bound=(
                            RunnableParallel(
                                prompt=lambda x: x,
                                urls=self.search_engine_chain(),
                            )
                            | RunnableParallel(
                                prompt=lambda x: x["prompt"],
                                pages=self.url_content_extraction_chain(
                                    InternetQaService.UrlExtractionMethod.REQUESTS
                                ),
                            )
                        )
                    )
                    # | printer
                    | RunnableLambda(lambda x: [d for docs in x for d in docs["pages"]])
                ),
            )
            # | printer
            | RunnableLambda(lambda x: retriever(x["pages"]).invoke(x["prompt"]))
            | RunnableLambda(
                lambda x: [
                    Document(page_content=d.page_content, metadata=d.metadata)
                    for d in x
                ]
            )
            | printer
        )

    def qa_chain(self, llm, embeddings):
        return (
            RunnableParallel(
                prompt=self.question_rephrase_chain(llm),
                summary=lambda x: x["summary"],
            )
            | printer
            | RunnableParallel(
                prompt=lambda x: x["prompt"],
                summary=lambda x: x["summary"],
                context=self.web_context_chain(llm, embeddings),
            )
            | printer
            | RunnableParallel(
                context=lambda x: x["context"],
                response=self.generic_chatbot_prompt_chain(llm),
            )
        )


def get_response(query: QaQuery) -> str:
    create_llm = CreateLLM(query.model, query.embeddings_model)
    llm = create_llm.getModel()
    embeddings = create_llm.get_embeddings()

    match query.strategy:
        case Strategy.web_search:
            strategy = InternetQaService()
        case Strategy.medical_database:
            strategy = VectorDbQaService()
        case Strategy.pubmed_search:
            strategy = PubmedQaService()
        case _:
            raise RuntimeError("unimplemented strategy")

    chain = strategy.qa_chain(llm, embeddings)
    res = chain.invoke(query.dict())
    return res
