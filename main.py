# main.py
import platform
import webbrowser
from utils.listen import takecommand
from utils.speak import say
from command_router import run_command

if __name__ == "__main__":
    print("AI Assistant is ready to work")
    say("Hi! I am Pebble. How can I help you?")

    while True:
        query = takecommand()

        if query == "None":
            say("Could you please repeat that?")
            continue

        run_command(query.lower())


# TO-DOS

# Finalize the open app funcitionality
# fix the volume issues
# fix the issue of cmd opening in the terminal instead of pop-up window
