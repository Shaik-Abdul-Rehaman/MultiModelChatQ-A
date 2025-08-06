from dotenv import load_dotenv
load_dotenv()
import os

AZURE_CONFIG = {
    'api_key': os.getenv("AZURE_OPENAI_API_KEY"),
    'api_version': os.getenv("AZURE_OPENAI_API_VERSION"),
    'azure_endpoint': os.getenv("AZURE_OPENAI_ENDPOINT"),
    'deployment_name': os.getenv("AZURE_OPENAI_DEPLOYMENT")
}

GROQ_CONFIG={
    'api_key':os.getenv("GROQ_API_KEY")
}

if __name__ =="__main__":
    print(AZURE_CONFIG)




