from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class GuardRails:

  def __init__(self, message: str):
    self.message = message

  def gen_prompt(self):

    prompt_template = """
            You are an AI which is built to classify whether a given query is related to medical in any sense or not. Do not answer the query,
            just classify it as 'YES', 'NO', 'MAYBE', or 'ILLEGAL'. If you think the given query is related to medical then answer will be 'YES'.
            If you think the given query is not related to medical then output 'NO'. If you are are 70 percent sure that this can be related to medical
            by any sense like whether it requires any medical treatment or doctor supervision then output 'MAYBE' else your answer.
            You must output an JSON consisting of 2 parameters:- 1) related 2) reason. Output this :- {{{{"related":"YES", "reason":"<Insert-Your-Reason-Here>"}}}} or {{{{"related":"NO","reason":"<Insert-Your-Reason-Here">}}}}.
            The value of related will be either yes or no or maybe. The value of reason will the reason that will be inferred by you that why do you think
            that it's answer is yes, no or maybe. You should have a valid reason to judge the query. donot hallucinate. if you cannot infer anything just output 'MAYBE'.
            I will give you an example for the current situation.

            1. first situation:-
            query: I hurt myself while playing football
            AI response: {{{{"related":"YES", "reason": "User wants to know how to treat a wound they got while playing"}}}}

            2. second situation:-
            query: I want to know best restaurant near me.
            AI response: {{{{"related":"NO", "reason": "User is asking for restaurant, it is not related to medical field by any context"}}}}

            If user is asking you about wrong practices which are related to medical field but they illegal, then output 'ILLEGAL'.
            Wrong practices includes planning a murder of someone, asking about torturing someone using medical toolkits, something like this.

            3. third situation:-
            User: I want to take revenge with someone who always bully me in school. I want to set a trap for him like jigsaw and torture him with medical toolkits
            AI response: {{{{"related":"ILLEGAL", "reason": "User is asking for wrong practices. I donot support helping or promoting such actions"}}}}

            Query: {query}
            AI response:
        """

    guard_rails_template = PromptTemplate.from_template(prompt_template)

    return guard_rails_template

  def create_llm_chain(self):

    prompt = self.gen_prompt()

    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    chain = prompt | llm

    return chain

  def is_relevent(self):

    # Creating a llm chain
    chain = self.create_llm_chain()

    # Fetching response
    response = chain.invoke({"query": self.message})
    response = response[1:-1]

    # Converting response to json format
    response = json.loads(response)


    related = response["related"]
    reason = response["reason"]
    if related == "NO":
        return {"ai_response": f"The message you asked is out of context. Reason: {reason}", "is_relevant": "NO"}

    elif related == "ILLEGAL":
        return {"ai_response": f"The message you asked sounds like wrong practices to me. I refuse to support such practices. Reason I think it is malicious: {reason}", "is_relevant": "ILLEGAL"}
    else:
        return {"ai_response": "-", "is_relevant": "YES"}

