import os
import threading
import keyboard
import traceback
from utils.listen import takecommand
from utils.speak import say
from command_router import run_command
from utils.ai_integration import init_ai, ask_groq
from Storedata_Groq import ConversationHistory

main_p_running = False
main_p_thread = None

def main_p():
    global main_p_running
    exit_keywords = ["ok got it", "exit", "quit", "shutdown", "stop", "bye"]
    error_count = 0
    MAX_ERRORS = 5

    while main_p_running:
        print("AI Assistant is ready to work")

        try:
            query = takecommand()
            if not query or not query.strip():
                continue

            query = query.strip().lower()

            if any(exit_kw in query for exit_kw in exit_keywords):
                say("Goodbye! Have a great day!")
                main_p_running = False
                break

            if "open ai" in query:
                ai = init_ai()
                say("What would you like to ask the AI?")
                user_input = takecommand()
                if user_input and user_input.lower() != "none":
                    ask_groq(ai, user_input)
                else:
                    say("I couldn't catch that. Please try again.")
                continue

            run_command(query)
            error_count = 0

        except Exception as e:
            print("Error occurred:")
            traceback.print_exc()
            say("Oops, something went wrong.")
            error_count += 1

            if error_count >= MAX_ERRORS:
                say("Too many errors occurred. Shutting down for now.")
                main_p_running = False
                break

    say("Assistant has stopped listening.")

def toggle_main_p():
    global main_p_running, main_p_thread

    def listener():
        global main_p_running, main_p_thread

        while True:
            keyboard.wait("win+f11")
            main_p_running = not main_p_running

            if main_p_running:
                say("Assistant activated.")
                main_p_thread = threading.Thread(target=main_p, daemon=True)
                main_p_thread.start()
            else:
                say("Assistant deactivated.")

    threading.Thread(target=listener, daemon=True).start()

if __name__ == "__main__":
    toggle_main_p()

    try:
        while True:
            os.system("timeout /t 1 >nul" if os.name == "nt" else "sleep 1")
    except KeyboardInterrupt:
        say("Assistant shutting down.")
        os._exit(0)