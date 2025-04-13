# ai.py
from groq import Groq
from config import apikey

class GroqAssistant:
    def __init__(self):
        if not apikey:
            raise ValueError("GROQ_API_KEY not set")
        self.client = Groq(api_key=apikey)

    def get_completion(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True
            )
            response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
            return response
        except Exception as e:
            print("API Error:", str(e))
            return "Sorry, I couldn't get a response"
