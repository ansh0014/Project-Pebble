# utils/listen.py
import speech_recognition as sr
from utils.speak import say

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception:
            say("Can you repeat?")
            return "None"
