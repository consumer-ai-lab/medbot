from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

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
Rephrased Question: """
pubmed_query_prompt_template = PromptTemplate(
    template=pubmed_query_prompt, input_variables=["prompt"]
)

summarization_prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        SystemMessage(
            content="Summarise the chat. include as much detail as much details in the least words possible such that it is easy to understand the context."
            # content="You are an AI assistant with the capability to process summaries of conversations and related follow-up questions. Your task is to rephrase a given follow-up question so it can be understood as a standalone question, without needing additional context from the conversation summary. Ensure the rephrased question maintains the essence and specificity of the original query, allowing for clear and concise communication. Given below is the example of what kind of response is expected"
            # content="You are an AI assistant specialized in reading transcripts of conversation between human and AI. Your primary task is to provide brief, accurate summaries of these transcripts, ensuring no important details are omitted."
        ),
    ]
)
