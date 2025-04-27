import logging
from pathlib import Path
from datetime import datetime
from utils.speak import say
import pyautogui  # Fallback for basic functionality

class TerminatorManager:
    def __init__(self):
        self.using_fallback = True
        self.term = None
        
        try:
            from terminator import Terminator
            self.term = Terminator()
            self.using_fallback = False
            logging.info("Successfully initialized Terminator")
        except ImportError:
            pass
        except Exception as e:
            logging.error(f"Failed to initialize Terminator: {e}")

    def take_screenshot(self, screenshots_dir: Path) -> Path:
        """Take a screenshot using Terminator or pyautogui fallback"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = screenshots_dir / f"screenshot_{timestamp}.png"
            
            if not self.using_fallback:
                screen = self.term.screen()
                screen.capture().save(str(path))
            else:
                screenshot = pyautogui.screenshot()
                screenshot.save(str(path))
            
            return path
        except Exception as e:
            logging.error(f"Screenshot error: {e}")
            raise

    def click_button(self, button_text: str):
        """Find and click a button with the specified text"""
        if self.using_fallback:
            say("Advanced UI automation requires Terminator installation")
            return
            
        try:
            button = self.term.find_element(text=button_text, role="button")
            button.click()
            say(f"Clicked button {button_text}")
        except Exception as e:
            logging.error(f"Failed to click button {button_text}: {e}")
            say(f"Could not find or click button {button_text}")

    def type_text(self, text: str, element_identifier: str):
        """Type text into an input field"""
        if self.using_fallback:
            say("Advanced UI automation requires Terminator installation")
            return
            
        try:
            input_field = self.term.find_element(identifier=element_identifier, role="textbox")
            input_field.type(text)
            say(f"Typed text into {element_identifier}")
        except Exception as e:
            logging.error(f"Failed to type text: {e}")
            say(f"Could not type text into {element_identifier}")

    def find_and_focus_window(self, window_title: str):
        """Find and focus a window by its title"""
        if self.using_fallback:
            say("Advanced UI automation requires Terminator installation")
            return None
            
        try:
            window = self.term.find_window(title=window_title)
            if window:
                window.focus()
                say(f"Found and focused window: {window_title}")
                return window
            else:
                say(f"Could not find window: {window_title}")
                return None
        except Exception as e:
            logging.error(f"Window interaction error: {e}")
            say(f"Error interacting with window {window_title}")
            return None

    def close_window(self, window_title: str):
        """Close a window by its title"""
        if self.using_fallback:
            say("Advanced UI automation requires Terminator installation")
            return
            
        try:
            window = self.term.find_window(title=window_title)
            if window:
                window.close()
                say(f"Closed window: {window_title}")
            else:
                say(f"Could not find window: {window_title}")
        except Exception as e:
            logging.error(f"Failed to close window: {e}")
            say(f"Error closing window {window_title}")

    def open_notepad_and_write(self, text: str):
        """Open Notepad and write the given text using Terminator or fallback."""
        if self.using_fallback:
            print("[DEBUG] Using fallback for Notepad writing.")
            say("Using fallback for Notepad writing.")
            import subprocess, time
            subprocess.Popen(['notepad.exe'])
            try:
                pyautogui.typewrite(text, interval=0.03)
                say("Wrote text to Notepad (fallback mode)")
            except Exception as e:
                print(f"[ERROR] Fallback Notepad write failed: {e}")
                say(f"Fallback Notepad write failed: {e}")
            return
        try:
            print("[DEBUG] Using Terminator for Notepad writing.")
            say("Using Terminator for Notepad writing.")
            self.term.open_application('notepad')
            import time
            # time.sleep(1.5)
            editor = self.term.find_element(window_title='Notepad', role='textbox')
            editor.type(text)
            say("Wrote text to Notepad using Terminator")
        except Exception as e:
            print(f"[ERROR] Terminator Notepad write failed: {e}")
            say(f"Could not write to Notepad: {e}")

    def start_screen_recording(self, output_path: str):
        """Start screen recording using Terminator or ffmpeg fallback."""
        if self.using_fallback:
            print("[DEBUG] Using fallback (ffmpeg) for screen recording.")
            say("Using fallback for screen recording.")
            import subprocess
            try:
                cmd = [
                    'ffmpeg', '-y', '-f', 'gdigrab', '-framerate', '15', '-i', 'desktop',
                    '-vcodec', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', output_path
                ]
                self._ffmpeg_proc = subprocess.Popen(cmd)
                say("Started screen recording (fallback mode)")
            except Exception as e:
                print(f"[ERROR] Fallback screen recording failed: {e}")
                say(f"Fallback screen recording failed: {e}")
            return
        try:
            print("[DEBUG] Using Terminator for screen recording.")
            say("Using Terminator for screen recording.")
            self.term.start_screen_recording(output_path)
            say("Started screen recording using Terminator")
        except Exception as e:
            print(f"[ERROR] Terminator screen recording failed: {e}")
            say(f"Could not start screen recording: {e}")

    def stop_screen_recording(self):
        """Stop screen recording using Terminator or ffmpeg fallback."""
        if self.using_fallback:
            print("[DEBUG] Using fallback (ffmpeg) to stop screen recording.")
            say("Using fallback to stop screen recording.")
            if hasattr(self, '_ffmpeg_proc'):
                self._ffmpeg_proc.terminate()
                self._ffmpeg_proc = None
                say("Stopped screen recording (fallback mode)")
            else:
                say("No screen recording in progress (fallback mode)")
            return
        try:
            print("[DEBUG] Using Terminator to stop screen recording.")
            say("Using Terminator to stop screen recording.")
            self.term.stop_screen_recording()
            say("Stopped screen recording using Terminator")
        except Exception as e:
            print(f"[ERROR] Terminator stop screen recording failed: {e}")
            say(f"Could not stop screen recording: {e}")

# Initialize the global Terminator manager
terminator_manager = TerminatorManager() 