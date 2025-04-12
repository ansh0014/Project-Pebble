import speech_recognition as sr
import os
import platform
import webbrowser
import subprocess
import datetime
# from api import GroqAPI
import os
from dotenv import load_dotenv
from groq import Groq
from config import apikey

def say(text):
    """Improved speech synthesis with text chunking"""
    # Split long text into sentences or chunks
    chunks = [s.strip() for s in text.split('.') if s.strip()]
    
    for chunk in chunks:
        if platform.system() == 'Darwin':  # macOS
            os.system(f'say "{chunk}"')
        elif platform.system() == 'Windows':  # Windows
            os.system(
                f'powershell -command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{chunk}\')"')
        else:  # Linux
            os.system(f'espeak "{chunk}"')


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


def get_time():
    """Function to get current time in 12-hour format"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.5
        
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Say that again please...")
            say("Can you repeat")
            return "None"
# def takecommand():
#     """Function to capture audio and convert to text using Whisper"""
#     # Initialize the recognizer
#     r = sr.Recognizer()
#     # Load Whisper model (you can choose different sizes: tiny, base, small, medium, large)
#     model = whisper.load_model("tiny")
    
#     with sr.Microphone() as source:
#         print('Listening...')
#         r.pause_threshold = 1
#         try:
#             # Capture audio
#             audio = r.listen(source)
#             # Convert speech recognition audio to numpy array
#             audio_data = np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0
            
#             # Transcribe using Whisper
#             result = model.transcribe(audio_data)
#             query = result["text"]
            
#             print(f"User said: {query}")
#             return query
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             print("Say that again please...")
#             say("Can you repeat")
# #             return "None"
# def takecommand():
#     try:
#         # Get model path and initialize Vosk model
#         model_path = "models/vosk-model-small-en-us-0.15"
#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"Model not found at {model_path}")
            
#         model = Model(model_path)
#         recognizer = KaldiRecognizer(model, 16000)
        
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print('Listening...')
#             r.pause_threshold = 1
#             audio = r.listen(source)
            
#             # Convert audio to raw data
#             raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            
#             if recognizer.AcceptWaveform(raw_data):
#                 result = json.loads(recognizer.Result())
#                 query = result["text"]
                
#                 if query.strip():  # Check if query is not empty
#                     print(f"User said: {query}")
#                     return query
#                 else:
#                     print("No speech detected")
#                     return "None"
            
#     except FileNotFoundError as e:
#         print(f"Error loading model: {str(e)}")
#     except sr.RequestError as e:
#         print(f"Could not connect to speech recognition service: {str(e)}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
    
#     print("Say that again please...")
#     say("Can you repeat")
#     return "None"

class GroqAssistant:
    def __init__(self):
        if not apikey:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=apikey)
    
    def get_completion(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )
            
            response_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    response_text += content
            return response_text
        except Exception as e:
            print(f"\nAPI Error: {str(e)}")
            return None

def init_ai():
    """Initialize AI components"""
    return GroqAssistant()

if __name__ == "__main__":
    print("AI Assistant is ready to work")
    say("Hi sir,I am Pedel")
    say("How i can  help you?")
    
    # Initialize AI
    ai = init_ai()
    
    while True:
        query = takecommand()
        
        # Skip the iteration if speech wasn't recognized
        if query == "None":
            continue
            
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
            open_codeditor()  # Fixed function call

        elif " time" in query_lower or "tell me the time" in query_lower:
            time_string = get_time()
            say(time_string)
            print(time_string)

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
      
        elif "open ai" in query_lower or "ask ai" in query_lower or "using ai" in query_lower:
            say("I'm listening to your question")
            say("What would you like to ask?")
            
            ai_query = takecommand()
            if ai_query != "None":
                say("Processing your request")
                try:
                    response = ai.get_completion(ai_query)
                    if response:
                        print("\nGroq AI Response:", response)
                        # Split response into smaller chunks for better speech synthesis
                        sentences = [s.strip() for s in response.split('.') if s.strip()]
                        for sentence in sentences:
                            say(sentence)
                    else:
                        say("I'm sorry, I couldn't get a response from Groq AI")
                except Exception as e:
                    print(f"Error processing Groq AI response: {e}")
                    say("I encountered an error while processing your request")
            else:
                say("I couldn't hear your question")

        elif "ok got it" in query_lower or "ok i got it" in query_lower or "ok understood" in query_lower:
            say("Goodbye! Have a great day!")
            break

        # elif "exit" in query_lower or "quit" in query_lower or "close" in query_lower:
        #     say("Goodbye!")
        #     break

