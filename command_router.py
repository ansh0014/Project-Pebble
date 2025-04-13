import os
import platform
import subprocess
import webbrowser
from datetime import datetime, date
import socket
import shutil
import psutil
import logging
import pyautogui
from pathlib import Path
import ctypes
import re
import winreg
import glob

from utils.speak import say
import utils.get_paths as get_paths
from utils.get_paths import KNOWN_FOLDER_IDS
from utils.open_apps import open_app

# === SCREENSHOT ===
def take_screenshot():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Pictures"])
        screenshots_dir = Path(base_dir) / "Pebble"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        path = screenshots_dir / f"screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(str(path))

        say("Screenshot saved successfully.")

        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':
            subprocess.call(["open", str(path)])
        else:
            subprocess.call(["xdg-open", str(path)])

        print(f'Screenshot saved at: {path}')
        logging.info(f"Screenshot saved at: {path}")

    except pyautogui.FailSafeException:
        say("Screenshot failed due to a failsafe exception.")
        logging.error("Screenshot error: FailSafeException")

    except PermissionError:
        say("Permission denied while creating the screenshots directory.")
        logging.error("PermissionError: Unable to create screenshots directory.")

    except Exception as e:
        say("Failed to take screenshot.")
        logging.exception(f"Unexpected error during screenshot: {e}")
        print("Screenshot error:", e)

# === SYSTEM INFO ===
def show_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "not available"

        info = f"CPU usage is {cpu}%. Memory usage is {memory}%. Battery level is {battery_percent}."
        print(info)
        say(info)
    except Exception as e:
        say("Unable to retrieve system information.")
        print("System info error:", e)

# === VOLUME ===
def adjust_volume(units):
    if platform.system() == 'Windows':
        try:
            import pycaw.pycaw as pycaw
            # Placeholder for more precise volume management if pycaw is used
            for _ in range(abs(units)):
                key = 0xA0000 if units < 0 else 0x90000
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, key)
        except Exception as e:
            say("Unable to adjust volume on Windows.")
            logging.error(f"Volume adjust error: {e}")
    elif platform.system() == 'Darwin':
        step = 1 if units > 0 else -1
        for _ in range(abs(units)):
            os.system(f"osascript -e 'set volume output volume (output volume of (get volume settings) + {step})'")
    else:
        if units > 0:
            os.system(f"amixer -D pulse sset Master {units * 3}%+")
        else:
            os.system(f"amixer -D pulse sset Master {abs(units) * 3}%-")

def mute_volume():
    if platform.system() == 'Windows':
        os.system("nircmd.exe mutesysvolume 1")
    elif platform.system() == 'Darwin':
        os.system("osascript -e 'set volume output muted true'")
    else:
        os.system("amixer set Master mute")

def unmute_volume():
    if platform.system() == 'Windows':
        os.system("nircmd.exe mutesysvolume 0")
    elif platform.system() == 'Darwin':
        os.system("osascript -e 'set volume output muted false'")
    else:
        os.system("amixer set Master unmute")

# === MUSIC AND APP LAUNCH ===
# def play_music():
#     music_dir = Path(get_paths.get_known_folder(KNOWN_FOLDER_IDS["Music"]))
#     if music_dir.exists():
#         for file in music_dir.iterdir():
#             if file.suffix.lower() in ['.mp3', '.wav', '.m4a']:
#                 os.startfile(file)
#                 say("Playing music.")
#                 break
#     else:
#         say("No music directory found.")

# === DATE & TIME ===
def get_time():
    current_time = datetime.now().strftime("%I:%M %p")
    say(f"The time is {current_time}")

def get_date():
    today = date.today()
    say(f"Today is {today.strftime('%A, %B %d, %Y')}")

# === INTERNET ===
def open_browser():
    webbrowser.open("https://www.google.com")

def search_query(command):
    query = command.replace("search", "").strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    say("Searching your query.")

# === SYSTEM NAVIGATION ===
def open_terminal():
    if platform.system() == 'Windows':
        os.system("start cmd")
    elif platform.system() == 'Darwin':
        os.system("open -a Terminal")
    else:
        subprocess.Popen(["x-terminal-emulator"])

def open_downloads():
    downloads = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Downloads"])
    if platform.system() == 'Windows':
        os.startfile(downloads)
    elif platform.system() == 'Darwin':
        subprocess.call(["open", str(downloads)])
    else:
        subprocess.call(["xdg-open", str(downloads)])

def open_documents():
    docs = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Documents"])
    if platform.system() == 'Windows':
        os.startfile(docs)
    elif platform.system() == 'Darwin':
        subprocess.call(["open", str(docs)])
    else:
        subprocess.call(["xdg-open", str(docs)])

# === SYSTEM CONTROL ===
def lock_screen():
    if platform.system() == 'Windows':
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif platform.system() == 'Darwin':
        os.system("pmset displaysleepnow")
    else:
        os.system("gnome-screensaver-command -l")

def shutdown_system():
    if platform.system() == 'Windows':
        os.system("shutdown /s /t 1")
    elif platform.system() == 'Darwin':
        os.system("sudo shutdown -h now")
    else:
        os.system("shutdown now")

def restart_system():
    if platform.system() == 'Windows':
        os.system("shutdown /r /t 1")
    elif platform.system() == 'Darwin':
        os.system("sudo shutdown -r now")
    else:
        os.system("reboot")

def log_out():
    if platform.system() == 'Windows':
        os.system("shutdown -l")
    elif platform.system() == 'Darwin':
        os.system("osascript -e 'tell application \"System Events\" to log out'")
    else:
        os.system("gnome-session-quit --logout --no-prompt")

def empty_recycle_bin():
    if platform.system() == 'Windows':
        os.system("PowerShell.exe -Command Clear-RecycleBin -Force")
    elif platform.system() == 'Darwin':
        os.system("rm -rf ~/.Trash/*")
    else:
        os.system("rm -rf ~/.local/share/Trash/* ~/.local/share/Trash/files/*")

# === NETWORK & STORAGE ===
def show_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    say(f"Your IP address is {ip}")
    print(f"Your IP address is {ip}")

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    say(f"Disk space: Used {used // (2**30)}GB, Free {free // (2**30)}GB out of {total // (2**30)}GB")

def run_cleanup():
    if platform.system() == 'Windows':
        os.system("cleanmgr")
    else:
        say("Cleanup not available on this system yet.")

# === ROUTER ===
def run_command(command: str):
    command = command.lower()

    if "screenshot" in command:
        take_screenshot()
    elif "system info" in command:
        show_system_info()
    elif "mute" in command and "unmute" not in command:
        mute_volume()
    elif "unmute" in command:
        unmute_volume()
    elif "increase volume" in command or "decrease volume" in command:
        match = re.search(r"(increase|decrease) volume( by (\d+))?", command)
        if match:
            direction = 1 if match.group(1) == "increase" else -1
            units = int(match.group(3)) if match.group(3) else 1
            adjust_volume(direction * units)
    elif "time" in command:
        get_time()
    elif "date" in command or "today" in command:
        get_date()
    elif "open browser" in command:
        open_browser()
    elif "search" in command:
        search_query(command)
    elif "terminal" in command:
        open_terminal()
    elif "downloads" in command:
        open_downloads()
    elif "documents" in command:
        open_documents()
    elif " lock" in command:
        lock_screen()
    elif "shut down" in command:
        shutdown_system()
    elif "restart" in command:
        restart_system()
    elif "log out" in command:
        log_out()
    elif "empty recycle" in command or "clear trash" in command:
        empty_recycle_bin()
    elif "ip address" in command:
        show_ip()
    elif "disk space" in command:
        check_disk_space()
    elif "cleanup" in command:
        run_cleanup()
    # elif "play music" or "music" in command:
    #     play_music()
    elif command.startswith("open "):
        app_name = command.replace("open", "").strip()
        open_app(app_name)
    else:
        print("Command not recognized:", command)
        say("Sorry, I don't recognize that command.")