"""Groq AI Integration Module for Pebble Voice Assistant."""

from groq import Groq
from config import apikey
from utils.listen import takecommand
from utils.speak import say
from Storedata_Groq import ConversationHistory


class GroqAssistant:
    """Handles communication with Groq LLM and conversation history."""

    def __init__(self):
        """Initialize Groq client and conversation history."""
        if not apikey:
            raise ValueError("GROQ_API_KEY is not set in the environment or config.")
        self.client = Groq(api_key=apikey)
        self.history = ConversationHistory()

    def get_completion(self, prompt):
        """
        Sends a prompt to the Groq model and returns the streamed response.

        Args:
            prompt (str): User's input prompt.

        Returns:
            str: AI-generated response text.
        """
        try:
            completion = self.client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Give brief, concise responses. "
                            "use commas instead of full-stops"
                            "Only ask follow-up questions if they are truly relevant or necessary."
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
    """
    Initialize and return a GroqAssistant instance.

    Returns:
        GroqAssistant: An instance of the GroqAssistant class.
    """
    return GroqAssistant()


def ask_groq(ai, question):
    """
    Sends a user question to Groq and speaks the response.

    Args:
        ai (GroqAssistant): Instance of the GroqAssistant.
        question (str): User's question as text.
    """
    try:
        response = ai.get_completion(question)
        if response:
            print("\nGroq AI Response:", response)
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            for sentence in sentences:
                say(sentence)
        else:
            say("I'm sorry, I couldn't get a response from Groq AI.")
    except Exception as error:
        print(f"Error processing Groq AI response: {error}")
        say("I encountered an error while processing your request.")


def groq_int():
    """
    Voice interface for querying Groq using microphone input.
    """
    say("What would you like to ask?")
    ai = init_ai()
    ai_query = takecommand()

    if ai_query != "None":
        say("Processing your request.")
        try:
            response = ai.get_completion(ai_query)
            if response:
                print("\nGroq AI Response:", response)
                sentences = [s.strip() for s in response.split('.') if s.strip()]
                for sentence in sentences:
                    say(sentence)
            else:
                say("I'm sorry, I couldn't get a response from Groq AI.")
        except Exception as error:
            print(f"Error during Groq interaction: {error}")
            say("There was an error while processing your request.")
    else:
        say("I couldn't hear your question.")
