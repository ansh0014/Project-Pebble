from dotenv import load_dotenv
import os

def get_api_key():
    load_dotenv()
    key = os.getenv('GROQ_API_KEY')
    if not key:
        raise RuntimeError("Please set GROQ_API_KEY in your .env file")
    return key

apikey = get_api_key()


