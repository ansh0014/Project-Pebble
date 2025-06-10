import os
import platform

def say(text):
    chunks = [s.strip() for s in text.split('.') if s.strip()]
    for chunk in chunks:
        if platform.system() == 'Darwin':
            os.system(f'say "{chunk}"')
        elif platform.system() == 'Windows':
            # Escape single quotes and backslashes for PowerShell
            safe_chunk = chunk.replace("'", "''").replace("\\", "\\\\")
            os.system(
                f'powershell -command "Add-Type -AssemblyName System.Speech; '
                f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{safe_chunk}\')"')
        else:
            os.system(f'espeak "{chunk}"')

# def ask()
