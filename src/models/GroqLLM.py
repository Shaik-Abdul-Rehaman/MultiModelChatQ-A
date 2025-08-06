from src.constants.constant import GROQ_CONFIG
from src.logger.logger import setup_logger
from langchain_groq import ChatGroq
class GroqLLM:
    def __init__(self):
        self.AZURE_CONFIG=GROQ_CONFIG
        self.logger=setup_logger()
        
    def get_llm(self):
        self.logger.info("entered into the get_llm function")
        
        llm = ChatGroq(model="gemma2-9b-it",api_key=GROQ_CONFIG["api_key"])
        return llm
        


'''
obj=GroqLLM()
llm=obj.get_llm()
print(llm.invoke("hii"))
'''