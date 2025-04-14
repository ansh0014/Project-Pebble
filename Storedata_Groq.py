import json
import os
from datetime import datetime

class ConversationHistory:
    def __init__(self):
        self.history_file = os.path.join(os.path.dirname(__file__), 'conversation_history.json')
        self.load_history()

    def load_history(self):
        """Load existing conversation history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []

    def save_history(self):
        """Save conversation history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_conversation(self, user_query, ai_response):
        """Add new conversation to history"""
        conversation = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_query': user_query,
            'ai_response': ai_response
        }
        self.history.append(conversation)
        self.save_history()

    def get_recent_conversations(self, limit=5):
        """Get recent conversations"""
        return self.history[-limit:] if self.history else []

    def search_history(self, keyword):
        """Search conversations by keyword"""
        return [
            conv for conv in self.history 
            if keyword.lower() in conv['user_query'].lower() 
            or keyword.lower() in conv['ai_response'].lower()
        ]

    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        self.save_history()
