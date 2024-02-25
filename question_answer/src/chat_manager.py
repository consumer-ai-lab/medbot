from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores.pgvector import PGVector
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv

from langchain.globals import set_debug

set_debug(True)

load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class ChatManager:
    def __init__(self, connection_string: str, collection_name: str):
        self.connection_string = connection_string
        self.collection_name = collection_name
    
    def get_custom_prompt(self):
        prompt_template = """
        As an advanced and reliable medical chatbot, your foremost priority is to furnish the user with precise, evidence-based health insights and guidance. It is of utmost importance that you strictly adhere to the context provided, without introducing assumptions or extrapolations beyond the given information. Your responses must be deeply rooted in verified medical knowledge and practices. Additionally, you are to underscore the necessity for users to seek direct consultation from healthcare professionals for personalized advice.

        In crafting your response, it is crucial to:
        - Confine your analysis and advice strictly within the parameters of the context provided by the user. Do not deviate or infer details not explicitly mentioned.
        - Identify the key medical facts or principles pertinent to the user's inquiry, applying them directly to the specifics of the provided context.
        - Offer general health information or clarifications that directly respond to the user's concerns, based solely on the context.
        - Discuss recognized medical guidelines or treatment options relevant to the question, always within the scope of general advice and clearly bounded by the context given.
        - Emphasize the critical importance of professional medical consultation for diagnoses or treatment plans, urging the user to consult a healthcare provider.
        - Where applicable, provide actionable health tips or preventive measures that are directly applicable to the context and analysis provided, clarifying these are not substitutes for professional advice.

        Your aim is to deliver a response that is not only informative and specific to the user's question but also responsibly framed within the limitations of non-personalized medical advice. Ensure accuracy, clarity, and a strong directive for the user to seek out professional medical evaluation and consultation. Through this approach, you will assist in enhancing the user's health literacy and decision-making capabilities, always within the context provided and without overstepping the boundaries of general medical guidance.

        context: {context}
        
        Question: {question}

        """

        prompt = PromptTemplate(template=prompt_template,input_variables=['question','history'])
        return prompt
    
    def get_retriever(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        store = PGVector(
            collection_name=self.collection_name,
            connection_string=self.connection_string,
            embedding_function=embeddings
        )
        return store.as_retriever()
    
    def get_retrival_qa_chain(self):
        prompt = self.get_custom_prompt()
        retriever = self.get_retriever()
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5, convert_system_message_to_human=True)
        qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, verbose=True, retriever=retriever)
        return qa_chain
    
    def get_chain_with_history(self):
        chain = self.get_retrival_qa_chain()
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: RedisChatMessageHistory(
                session_id=session_id, url="redis://redis-service:6379"
            ),
            input_messages_key="question",
            history_messages_key="chat_history"
        )
        return chain_with_history
    
    def get_response(self, query: str, session_id: str):
        config = {"configurable": {"session_id": session_id}}
        chain_with_history = self.get_chain_with_history()
        res = chain_with_history.invoke({"question": query}, config=config)
        return res["answer"]
    
def get_chat_manager():
    connection_string = os.getenv('CONNECTION_STRING')
    collection_name = os.getenv('CONNECTION_NAME')
    return ChatManager(connection_string, collection_name)