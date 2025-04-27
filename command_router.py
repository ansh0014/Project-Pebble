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

from Storedata_Groq import *
from utils.ai_integration import init_ai, ask_groq
from utils.speak import say
from utils.listen import takecommand, takecommand_with_timeout
import utils.get_paths as get_paths
from utils.get_paths import KNOWN_FOLDER_IDS
from utils.open_apps import open_app
from utils.terminator_integration import terminator_manager

# === BASIC FUNCTIONS ===
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
        os.startfile(path)
    except Exception as e:
        say("Failed to take screenshot.")
        print("Screenshot error:", e)

def show_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "not available"
        info = f"CPU usage is {cpu}%. Memory usage is {memory}%. Battery level is {battery_percent}%."
        say(info)
        print(info)
    except Exception as e:
        say("Unable to retrieve system information.")
        print(e)

def adjust_volume(units):
    if platform.system() == 'Windows':
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = min(max(current_volume + (units * 0.05), 0.0), 1.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
        except Exception as e:
            print("Volume control error:", e)
    else:
        if units > 0:
            os.system(f"amixer -D pulse sset Master {units * 3}%+")
        else:
            os.system(f"amixer -D pulse sset Master {abs(units) * 3}%-")

def mute_volume():
    os.system("nircmd.exe mutesysvolume 1")

def unmute_volume():
    os.system("nircmd.exe mutesysvolume 0")

def get_time():
    current_time = datetime.now().strftime("%I:%M %p")
    say(f"The time is {current_time}")

def get_date():
    today = date.today()
    say(f"Today is {today.strftime('%A, %B %d, %Y')}")

def open_browser():
    webbrowser.open("https://www.google.com")

def search_query(command):
    query = command.replace("search", "").strip().replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    say("Searching your query.")

def open_terminal():
    os.system("start cmd")

def open_downloads():
    downloads = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Downloads"])
    os.startfile(downloads)

def open_documents():
    docs = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Documents"])
    os.startfile(docs)

def open_pictures():
    pics = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Pictures"])
    os.startfile(pics)

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown_system():
    os.system("shutdown /s /t 1")

def restart_system():
    os.system("shutdown /r /t 1")

def log_out():
    os.system("shutdown -l")

def empty_recycle_bin():
    os.system("PowerShell.exe -Command Clear-RecycleBin -Force")

def show_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    say(f"Your IP address is {ip}")

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    say(f"Disk space: Used {used // (2**30)}GB, Free {free // (2**30)}GB out of {total // (2**30)}GB")

def run_cleanup():
    os.system("cleanmgr")

def speech_to_text():
    say("Please start speaking, I am listening...")
    spoken_text = takecommand_with_timeout(timeout=45)
    if spoken_text:
        base_dir = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Documents"])
        save_dir = Path(base_dir) / "PebbleTranscripts"
        save_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_path = save_dir / f"speech_{timestamp}.txt"
        with open(text_path, "w", encoding="utf-8") as file:
            file.write(spoken_text)
        say("Your speech has been saved successfully.")
        os.startfile(text_path)
    else:
        say("I couldn't hear anything properly.")

def start_screen_recording():
    try:
        base_dir = get_paths.get_known_folder(KNOWN_FOLDER_IDS["Videos"])
        save_dir = Path(base_dir) / "PebbleRecordings"
        save_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(save_dir / f"recording_{timestamp}.mp4")
        terminator_manager.start_screen_recording(output_path)
    except Exception as e:
        print("Start screen recording error:", e)
        say("Failed to start screen recording.")

def stop_screen_recording():
    try:
        terminator_manager.stop_screen_recording()
    except Exception as e:
        print("Stop screen recording error:", e)
        say("Failed to stop screen recording.")

def show_history():
    try:
        history = ConversationHistory()
        conversations = history.load_conversations()  # Changed from get_all_conversations to load_conversations
        if not conversations:
            say("No conversation history found.")
            return
        
        say("Here are your recent conversations with AI:")
        # Show last 5 conversations if available
        recent_conversations = conversations[-5:] if len(conversations) > 5 else conversations
        for i, conv in enumerate(recent_conversations, 1):
            print(f"\nConversation {i}:")
            print(f"You: {conv['prompt']}")
            print(f"AI: {conv['response']}")
            say(f"Conversation {i}: You asked: {conv['prompt']}")
            say(f"AI responded: {conv['response']}")
    except Exception as e:
        print(f"Error showing history: {e}")
        say("Sorry, I couldn't retrieve the conversation history.")

# === MAIN ROUTER ===
def run_command(command: str):
    command = command.lower()

    # First handle AI-related commands
    if "show history" in command:
        show_history()
        return
    
    if any(trigger in command for trigger in ['ask ai', 'ai', 'open ai', 'ascii']):
        if 'open ai' in command:
            ai = init_ai()
            say("What would you like to ask the AI?")
            user_input = takecommand()
            if user_input and user_input.lower() != "none":
                ask_groq(ai, user_input)
            else:
                say("I couldn't catch that. Please try again.")
        else:
            # For other AI triggers, extract the prompt after the trigger word
            for trigger in ['ask ai', 'ai', 'ascii']:
                if trigger in command:
                    prompt = command.split(trigger, 1)[-1].strip()
                    if prompt:
                        ai = init_ai()
                        ask_groq(ai, prompt)
                    else:
                        say("You didn't ask anything.")
                    break
        return

    # Handle other non-AI commands
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
    elif "pictures" in command:
        open_pictures()
    elif "lock" in command:
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
    elif "speech to text" in command or "save my speech" in command:
        speech_to_text()
    elif "start screen recording" in command:
        start_screen_recording()
    elif "stop screen recording" in command:
        stop_screen_recording()
    elif command.startswith("open "):
        app_name = command.replace("open", "").strip()
        open_app(app_name)
    else:
        say("Sorry, I don't recognize that command.")
