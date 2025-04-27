import speech_recognition as sr

def takecommand_with_timeout(timeout=10, phrase_time_limit=15):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening with timeout...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Recognizing...")
            query = r.recognize_google(audio)
            print("Heard:", query)
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out (timeout mode).")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio (timeout mode).")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return None

def takecommand():
    return takecommand_with_timeout(timeout=30, phrase_time_limit=15)
