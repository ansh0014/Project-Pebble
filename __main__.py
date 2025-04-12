import speech_recognition as sr
import os
import platform
import webbrowser
import subprocess
import openai

def say(text):
    # Check the operating system and use appropriate command
    if platform.system() == 'Darwin':  # macOS
        os.system(f'say "{text}"')
    elif platform.system() == 'Windows':  # Windows
        # Using PowerShell's speech synthesis
        os.system(
            f'powershell -command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
    else:  # Linux (might need espeak to be installed)
        os.system(f'espeak "{text}"')


def open_spotify():
    """Function to open Spotify based on operating system"""
    system = platform.system()

    if system == 'Windows':
        try:
            # Try to open Spotify using the Start command
            os.system('start spotify:')
        except:
            # Alternative method using the full path (you might need to adjust this path)
            try:
                subprocess.Popen(['C:\\Users\\YourUsername\\AppData\\Roaming\\Spotify\\Spotify.exe'])
            except:
                say("I couldn't open Spotify. Please make sure it's installed.")

    elif system == 'Darwin':  # macOS
        os.system('open -a Spotify')

    elif system == 'Linux':
        subprocess.Popen(['spotify'])

    else:
        say("Sorry, I don't know how to open Spotify on your operating system.")


def open_codeditor():
    """Function to open Visual Studio Code based on operating system"""
    system = platform.system()

    if system == 'Windows':
        try:
            # Using the command that should work if VS Code is in PATH
            os.system('start code')
        except:
            # Alternative methods
            try:
                subprocess.Popen(['code'])
            except:
                try:
                    # Common installation path for VS Code on Windows
                    subprocess.Popen(['C:\\Users\\%username%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'],
                                     shell=True)
                except:
                    say("I couldn't open VS Code. Please make sure it's installed.")

    elif system == 'Darwin':  # macOS
        os.system('open -a "Visual Studio Code"')

    elif system == 'Linux':
        subprocess.Popen(['code'])

    else:
        say("Sorry, I don't know how to open VS Code on your operating system.")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            # print(e)
            print("Say that again please...")
            return "Some error occured.Sorry"


if __name__ == "__main__":
    print("AI Assistant is ready to work")
    say("Hello I am Pedel")
    while True:
        # print("listening")
        query = takecommand()
        # say(query)

        # Convert query to lowercase for easier matching
        query_lower = query.lower()

        if "open youtube" in query_lower:
            say("Opening YouTube")
            webbrowser.open("https://www.youtube.com/")

        elif "play music" in query_lower or "open spotify" in query_lower:
            say("Opening Spotify")
            open_spotify()

        elif "open discord" in query_lower:
            say("Opening Discord")
            # For Windows, using a more direct approach that should work if Discord is in PATH
            if platform.system() == 'Windows':
                try:
                    subprocess.Popen(["discord"])

                except:
                    try:
                        os.system("start Discord")
                    except:
                        say("I couldn't open Discord. Please make sure it's installed correctly.")
            else:
                # Use the general approach for other operating systems
                if platform.system() == 'Darwin':  # macOS
                    os.system('open -a Discord')
                elif platform.system() == 'Linux':
                    subprocess.Popen(['discord'])

        elif "open vs code" in query_lower or "open visual studio code" in query_lower or "open vscode" in query_lower:
            say("Opening Visual Studio Code")
            open_vscode()

        elif "open chatgpt" in query_lower or "chatgpt" in query_lower:
            say("Opening ChatGPT")
            webbrowser.open("https://chat.openai.com/")

        elif "open deepseek" in query_lower or "deepseek" in query_lower:
            say("Opening DeepSeek")
            # The correct URL for DeepSeek's chat interface
            webbrowser.open("https://chat.deepseek.com/")

        elif "open google" in query_lower:
            say("Opening Google")
            webbrowser.open("https://www.google.com/")

        elif "open stackoverflow" in query_lower:
            say("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com/")

        elif "open github" in query_lower:
            say("Opening GitHub")
            webbrowser.open("https://github.com/")

        elif "open gmail" in query_lower:
            say("Opening Gmail")
            webbrowser.open("https://mail.google.com/")

        elif "exit" in query_lower or "quit" in query_lower:
            say("Goodbye!")
            break