import os
from dotenv import load_dotenv

def get_api_key():
    load_dotenv()
    key = os.getenv('GROQ_API_KEY')

    if not key:
        key = input("Please enter your GROQ API Key: ").strip()
        with open(".env", "a") as f:
            f.write(f"GROQ_API_KEY={key}\n")
        os.environ['GROQ_API_KEY'] = key

    return key

def get_model_name():
    load_dotenv()
    model = os.getenv('GROQ_MODEL_NAME')

    if not model:
        model = input("Please enter your GROQ Model Name (e.g., llama3-8b-8192): ").strip()
        with open(".env", "a") as f:
            f.write(f"GROQ_MODEL_NAME={model}\n")
        os.environ['GROQ_MODEL_NAME'] = model

    return model

# Load them when importing config
apikey = get_api_key()
modelname = get_model_name()
