import os
from groq import Groq
from config import apikey

def setup_api_client():
    if not apikey:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return Groq(api_key=apikey)

def get_ai_response(prompt):
    client = setup_api_client()
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None
        )
        
        print(f"\n=== Response for: {prompt} ===\n")
        response_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response_text += content
                print(content, end="", flush=True)
        
        return response_text

    except Exception as e:
        print(f"\nAPI Error: {str(e)}")
        return None

if __name__ == "__main__":
    prompt = input("Enter your question: ")
    response = get_ai_response(prompt)
    if response:
        print("\n\n=== Response saved successfully ===")
