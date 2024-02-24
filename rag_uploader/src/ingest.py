from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.globals import set_debug
from langchain.vectorstores.pgvector import PGVector
import os
from dotenv import find_dotenv, load_dotenv

set_debug(True)
load_dotenv(find_dotenv())

def generate_vector_store(file_path:str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    documents = text_splitter.split_documents(pages)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    COLLECTION_NAME = os.getenv('CONNECTION_NAME')

    PGVector.from_documents(
        documents,
        embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
    )

    print("Successfully created an index")


def test_query(query:str):

    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    COLLECTION_NAME = os.getenv('CONNECTION_NAME')

    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    )
    result = store.similarity_search(query=query)
    print(result)

if __name__=="__main__":
    pass