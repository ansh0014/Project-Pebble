import os
from groq import Groq
from config import apikey

client = Groq(api_key=apikey)  # reuse client

def get_ai_response(prompt):
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
            stream=False  # set to False for debug
        )
        response_text = completion.choices[0].message.content
        print(f"\n=== Response for: {prompt} ===\n{response_text}")
        return response_text

    except Exception as e:
        print(f"\nAPI Error: {str(e)}")
        return None
