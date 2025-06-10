import re
from groq import Groq
from config import apikey, modelname
from utils.speak import say
from Storedata_Groq import ConversationHistory
from utils.terminator_integration import terminator_manager
from utils.listen import takecommand_with_timeout

def clean_response(text):
    """Clean AI response to remove invalid characters and think tags."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.replace('.', ',')
    return text.strip()


class GroqAssistant:
    def __init__(self):
        if not apikey:
            raise ValueError("GROQ_API_KEY is not set in the environment or config.")
        self.client = Groq(api_key=apikey)
        self.history = ConversationHistory()

    def get_completion(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model=modelname,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Give brief, concise responses, "
                            "use commas ',' instead of full-stops '.', only at the end of the sentences "
                            "only ask follow-up questions if necessary."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
            )

            response_text = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    response_text += content

            self.history.add_conversation(prompt, response_text)
            return response_text

        except Exception as error:
            print(f"\nAPI Error: {error}")
            return None

def init_ai():
    return GroqAssistant()
def ask_groq(ai, initial_question):
    """Handles Groq conversation with improved natural waiting."""
    try:
        current_question = initial_question
        while True:
            response = ai.get_completion(current_question)
            if response:
                response = clean_response(response)
                response = response.replace('.', ',')  # Replace full stops with commas
                print("\nGroq AI Response:", response)

                sentences = [s.strip() for s in response.split(',') if s.strip()]
                for sentence in sentences:
                    say(sentence)

                print("Waiting for response [30]")
                user_input = takecommand_with_timeout(timeout=10)

                if user_input and user_input.strip().lower() != "none":
                    current_question = user_input
                    continue  # continue asking Groq
                else:
                    say("No further input detected, ending AI conversation.")
                    break
            else:
                say("I'm sorry, I couldn't get a response from Groq AI.")
                break

    except Exception as error:
        print(f"Error processing Groq AI response: {error}")
        say("I encountered an error while processing your request.")
