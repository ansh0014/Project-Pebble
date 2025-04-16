import platform
import webbrowser
from utils.listen import takecommand
from utils.speak import say
from command_router import run_command
from utils.History import HistoryManager

if __name__ == "__main__":
    history_manager = HistoryManager()
    say("Hi! I am Pebble")
    say("How can I help you?")

    while True:
        print("AI Assistant is ready to work")

        try:
            query = takecommand()
            if query in [None, ""]:
                continue

            query_lower = query.lower()

            if any(exit_kw in query_lower for exit_kw in ["ok got it", "exit", "quit", "shutdown"]):
                say("Goodbye! Have a great day!")
                break

            run_command(query_lower, history_manager)

        except Exception as e:
            print(f"Error occurred: {e}")
            say("Oops, something went wrong.")
