from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.globals import set_debug
from util import get_absolute_path
import os


genai.configure(api_key="AIzaSyCbtMQhFYEr8s6GcHl_RchUgdvcfnV2NP8")
set_debug(True)
