import os
import subprocess
import platform

def say(text):
    print(text)  # Replace with your TTS or response function

def find_and_open_app(app_name):
    search_paths = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.path.expandvars(r"%LocalAppData%"),
        os.path.expandvars(r"%AppData%"),
    ]

    for path in search_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().startswith(app_name.lower()) and file.endswith(".exe"):
                        try:
                            subprocess.Popen(os.path.join(root, file))
                            return True
                        except Exception:
                            continue
    return False

def open_app(app_name):
    """Opens a generic application based on app name"""
    system = platform.system()

    try:
        if system == 'Windows':
            try:
                subprocess.Popen([app_name])
            except:
                if not find_and_open_app(app_name):
                    say(f"I couldn't find or open {app_name}. Please make sure it's installed.")
        elif system == 'Darwin':  # macOS
            os.system(f'open -a "{app_name}"')
        elif system == 'Linux':
            subprocess.Popen([app_name])
        else:
            say("Sorry, I don't know how to open apps on your operating system.")
    except Exception as e:
        say(f"Something went wrong trying to open {app_name}: {e}")
