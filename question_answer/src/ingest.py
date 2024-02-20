from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.globals import set_debug
from util import get_absolute_path
from langchain.vectorstores.pgvector import PGVector
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
set_debug(True)

def generate_vector_store():
    loader = DirectoryLoader(
    "./knowledge_base", glob="**/*.txt", loader_cls=TextLoader, show_progress=True
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    CONNECTION_STRING = "postgresql+psycopg2://admin:admin@127.0.0.1:5433/vectordb"
    COLLECTION_NAME = "vectordb"

    store=PGVector.from_documents(
        documents,
        embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
    )

    docs = store.similarity_search("it works?")
    print(docs[0])
    print("Successfully created an index")


if __name__=="__main__":
    generate_vector_store()