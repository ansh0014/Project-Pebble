# main.py
import platform
import webbrowser
from utils.listen import takecommand
from utils.speak import say
from command_router import run_command
from ai import GroqAssistant

def init_ai():
    return GroqAssistant()

if __name__ == "__main__":
    print("AI Assistant is ready to work")
    say("Hi! I am Pebble")
    say("How can I help you?")

    ai = init_ai()

    while True:
        query = takecommand()

        if query == "None":
            continue

        query_lower = query.lower()

        if any(kw in query_lower for kw in ["ask ai", "using ai", "open ai"]):
            say("I'm listening to your question")
            ai_query = takecommand()
            if ai_query != "None":
                say("Processing your request")
                response = ai.get_completion(ai_query)
                if response:
                    say(response)
        elif any(exit_kw in query_lower for exit_kw in ["ok got it", "exit", "quit"]):
            say("Goodbye! Have a great day!")
            break
        else:
            run_command(query_lower)
