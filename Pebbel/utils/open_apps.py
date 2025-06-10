import os
import subprocess
import platform

def say(text):
    print(text)  # Replace with your TTS or GUI if needed

def find_and_open_app(app_name):
    search_paths = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.path.expandvars(r"%LocalAppData%"),
        os.path.expandvars(r"%AppData%"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    ]

    app_name_clean = app_name.lower().replace(" ", "").replace("-", "").replace("_", "")

    for path in search_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_lower = file.lower()
                    filename_noext = os.path.splitext(file_lower)[0]
                    filename_noext_clean = filename_noext.replace(" ", "").replace("-", "").replace("_", "")

                    if (filename_noext_clean == app_name_clean) and (file_lower.endswith(".exe") or file_lower.endswith(".lnk")):
                        try:
                            full_path = os.path.join(root, file)
                            if file.endswith(".lnk"):
                                os.startfile(full_path)
                            else:
                                subprocess.Popen(full_path)
                            return True
                        except Exception as e:
                            print(f"Error opening {file}: {e}")
                            continue
    return False

def open_app(app_name):
    system = platform.system()
    app_key = app_name.lower().strip()

    # Special handling for VS Code
    if app_key in ["code editor", "vs code", "vscode", "vs"]:
        try:
            if system == 'Windows':
                possible_paths = [
                    r"C:\Program Files\Microsoft VS Code\Code.exe",
                    r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                    os.path.expandvars(r"%LocalAppData%\Programs\Microsoft VS Code\Code.exe")
                ]
                for path in possible_paths:
                    expanded = os.path.expandvars(path)
                    if os.path.exists(expanded):
                        subprocess.Popen([expanded])
                        return
                subprocess.Popen(["code"])  # Try launcher
                return
            elif system == 'Darwin':
                os.system('open -a "Visual Studio Code"')
                return
            elif system == 'Linux':
                subprocess.Popen(["code"])
                return
        except Exception as e:
            say(f"Something went wrong trying to open VS Code: {e}")
            return

    try:
        if system == 'Windows':
            # 1. Try direct open first
            try:
                subprocess.Popen([app_name])
                return
            except Exception:
                pass

            # 2. Try finding manually
            if find_and_open_app(app_name):
                return

            # 3. Try Shell Execute (Windows Search way)
            try:
                os.startfile(app_name)
                return
            except Exception:
                pass

            # 4. Try using Powershell Start-Process
            try:
                subprocess.Popen(["powershell", "Start-Process", app_name])
                return
            except Exception:
                pass

            # If all fail
            say(f"Sorry, I couldn't find or open '{app_name}'. Please make sure it's installed.")
        
        elif system == 'Darwin':  # macOS
            os.system(f'open -a "{app_name}"')
        elif system == 'Linux':
            subprocess.Popen([app_name])
        else:
            say("Sorry, I don't know how to open apps on your operating system.")
    
    except Exception as e:
        say(f"Something went wrong trying to open {app_name}: {e}")
