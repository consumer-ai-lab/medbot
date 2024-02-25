from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.globals import set_debug
from langchain.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import find_dotenv, load_dotenv

set_debug(True)
load_dotenv(find_dotenv())


class VectorStoreManager:
    def __init__(self):
        self.connection_string = os.getenv('CONNECTION_STRING')
        self.collection_name = os.getenv('CONNECTION_NAME')
        self.embedding_model = "models/embedding-001" 

    def generate_vector_store(self, file_path: str):
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = text_splitter.split_documents(pages)
        embeddings = GoogleGenerativeAIEmbeddings(model=self.embedding_model)

        PGVector.from_documents(
            documents,
            embeddings,
            collection_name=self.collection_name,
            connection_string=self.connection_string,
        )

        print("Successfully created an index")

    def test_query(self, query: str):
        embeddings=GoogleGenerativeAIEmbeddings(model=self.embedding_model)
        store = PGVector(
            collection_name=self.collection_name,
            connection_string=self.connection_string,
            embedding_function=embeddings
        )
        result = store.similarity_search(query=query)
        print(result)

def get_vector_store_manager():
    return VectorStoreManager()