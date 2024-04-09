from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import pprint
import json

from .proompts import (
    question_rephrase_prompt_template,
    chatbot_with_history_promt_template,
    chatbot_promt_template,
    generic_chatbot_promt_template,
    search_query_prompt_template,
)


def printer_print(x):
    print()
    pprint.pprint(x)
    print()
    return x


printer = RunnableLambda(printer_print)


class HackyJsonExtractor:
    def __init__(self, string):
        self.string = string
        self.pos = 0

    def peek_char(self):
        if self.pos+1 >= len(self.string):
            return None
        return self.string[self.pos+1]

    def next_string(self):
        start = None
        end = None

        while self.pos < len(self.string):
            c = self.string[self.pos]

            if start is None:
                if c in [' ', '\n', '\t', ':', ',']:
                    self.pos += 1
                    continue

            if c == "\\":
                if self.peek_char() == '"':
                    self.pos += 2
                    continue
                
            if c == '"':
                if start is None:
                    start = self.pos
                    self.pos += 1
                else:
                    end = self.pos
                    self.pos += 1
                    break
            else:
                self.pos += 1

        if end is None:
            return None

        return self.string[start+1:end]

    def march_to_colon_before_new_stirng(self):
        pos = self.pos
        while pos < len(self.string):
            c = self.string[pos]
            if c == '"':
                return False
            if c == ':':
                self.pos = pos+1
                return True
            pos += 1
        return False
                

    def list_of_strings(self):
        if "[" not in self.string:
            raise RuntimeError(f"string does not contain a json object: {self.string}")
        
        x0, x1 = self.string.split("[")
        inside, _ = x1.split("]")
        self.string = inside
        self.pos = 0
        strings = []

        while s := self.next_string():
            strings.append(s)

        return strings

    def string_dict(self):
        if "{" not in self.string:
            raise RuntimeError(f"string does not contain a json object: {self.string}")
        
        x0, x1 = self.string.split("{")
        inside, _ = x1.split("}")
        self.string = inside
        self.pos = 0

        d = {}
        k = None
        while s := self.next_string():
            if k is None:
                k = s
                continue

            # OOF: just assume it is a value
            _ = self.march_to_colon_before_new_stirng()
            d[k] = s
            k = None

        return d

# # specialize for { string: string }
# def hacky_extract_json_dict(x):
#     if "{" not in x:
#         raise RuntimeError(f"string does not contain a json object: {x}")

#     inside = x.split("{")[1]
#     inside = inside.split("}")[0]
#     return "{" + inside + "}"


# # specialized for list of strings
# def hacky_extract_json_list(x):
#     if "[" not in x:
#         raise RuntimeError(f"string does not contain a json object: {x}")

#     inside = x.split("[")[1]
#     inside = inside.split("]")[0]
#     return "[" + inside + "]"


class Proompter:
    def question_rephrase_chain(self, llm):
        """prompt summary"""
        return (
            question_rephrase_prompt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
            | self.hacky_string_dict_chain()
            | printer
            | RunnableLambda(lambda x: x["question"])
        )

    def medical_chatbot_prompt_chain(self, llm):
        """context prompt"""
        return chatbot_promt_template | printer | llm | printer | StrOutputParser()

    def medical_chatbot_with_history_prompt_chain(self, llm):
        """context prompt summary"""
        return (
            chatbot_with_history_promt_template
            | printer
            | llm
            | printer
            | StrOutputParser()
        )

    def generic_chatbot_prompt_chain(self, llm):
        """prompt summary"""
        return (
            generic_chatbot_promt_template | printer | llm | printer | StrOutputParser()
        )

    def generate_search_queries_chain(self, llm):
        """prompt summary"""
        return (
            search_query_prompt_template
            | llm
            | StrOutputParser()
            | printer
            | self.hacky_list_of_strings_chain()
        )

    def hacky_list_of_strings_chain(self):
        return printer | RunnableLambda(lambda x: HackyJsonExtractor(x).list_of_strings()) | printer
        # return RunnableLambda(lambda x: hacky_extract_json_list(x)) | RunnableLambda(lambda x: json.loads(x))

    def hacky_string_dict_chain(self):
        return printer | RunnableLambda(lambda x: HackyJsonExtractor(x).string_dict()) | printer
        # return RunnableLambda(lambda x: hacky_extract_json_dict(x)) | RunnableLambda(lambda x: json.loads(x))
