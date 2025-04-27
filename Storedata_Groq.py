import json
import os
from pathlib import Path

class ConversationHistory:
    def __init__(self):
        self.history_file = Path(os.path.dirname(os.path.abspath(__file__))) / "conversation_history.json"
        self.ensure_history_file()

    def ensure_history_file(self):
        if not self.history_file.exists():
            self.history_file.write_text("[]")

    def load_conversations(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading conversations: {e}")
            return []

    def add_conversation(self, prompt, response):
        try:
            conversations = self.load_conversations()
            conversations.append({
                "prompt": prompt,
                "response": response
            })
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving conversation: {e}")
