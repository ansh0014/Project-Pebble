# utils/speak.py
import os
import platform

def say(text):
    chunks = [s.strip() for s in text.split('.') if s.strip()]
    for chunk in chunks:
        if platform.system() == 'Darwin':
            os.system(f'say "{chunk}"')
        elif platform.system() == 'Windows':
            os.system(
                f'powershell -command "Add-Type -AssemblyName System.Speech; '
                f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{chunk}\')"')
        else:
            os.system(f'espeak "{chunk}"')

# def ask()
