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
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever, SearchDepth
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
from .proompter import Proompter, printer, hacky_extract_json_list
from .proompts import pubmed_query_prompt_template

# set_debug(True)

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class VectorDbQaService(Proompter):
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


class PubmedQaService(Proompter):
    def genrate_search_queries_chain(self, llm):
        return (
            RunnableParallel(
                questions=(
                    # search_query_prompt_template
                    pubmed_query_prompt_template
                    | printer
                    | llm
                    | StrOutputParser()
                    | printer
                    | RunnableLambda(hacky_extract_json_list)
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
        return self.genrate_search_queries_chain(llm) | RunnableEach(
            bound=(
                RunnableParallel(
                    prompt=lambda x: x,
                    context=lambda x: Document(page_content=PubmedQueryRun().invoke(x)),
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


class TavilyQaService(Proompter):
    def tavily_chain(self):
        return TavilySearchAPIRetriever(
            k=1,
            api_key=os.getenv("TAVILY_AI_API_KEY"),
            search_depth=SearchDepth.ADVANCED,
            include_generated_answer=True,
        )

    def web_context_chain(self, llm, embeddings):
        return (
            self.generate_search_queries_chain(llm)
            | RunnableEach(
                bound=(
                    RunnableParallel(
                        prompt=lambda x: x,
                        urls=self.tavily_chain(),
                    )
                )
            )
            | printer
            | RunnableLambda(lambda x: [d for d in x])
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


class InternetQaService(Proompter):
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
                try:
                    response = self.session.get(url, timeout=6)
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
                except Exception as e:
                    print(f"ERROR while searching url {url}: ", e)
                    continue
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
        case Strategy.web_search_api:
            strategy = TavilyQaService()
        case _:
            raise RuntimeError("unimplemented strategy")

    chain = strategy.qa_chain(llm, embeddings)
    res = chain.invoke(query.dict())
    return res


if __name__ == "__main__":
    query = QaQuery(
        **{
            "model": Model.groq_mistral_8x7b,
            "embeddings_model": EmbeddingsModel.gemini_pro,
            "strategy": Strategy.web_search_api,
            "prompt": "what medicines do i take for headache?",
            "summary": "None",
        }
    )

    resp = get_response(query)
    print(resp)
