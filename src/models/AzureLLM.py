from src.constants.constant import AZURE_CONFIG
from src.logger.logger import setup_logger
from langchain_openai import AzureChatOpenAI
class AzureLLM:
    def __init__(self):
        self.AZURE_CONFIG=AZURE_CONFIG
        self.logger=setup_logger()
        
    def get_llm(self):
        self.logger.info("entered into the get_llm function")
        
        llm = AzureChatOpenAI(
            openai_api_key=AZURE_CONFIG["api_key"],
            openai_api_version=AZURE_CONFIG["api_version"],
            azure_endpoint=AZURE_CONFIG["azure_endpoint"],
            deployment_name=AZURE_CONFIG["deployment_name"],
            temperature=0.1,
            streaming=False
        )
        return llm
        


'''
obj=AzureLLM()
llm=obj.get_llm()
print(llm.invoke("hii"))

'''