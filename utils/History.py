from Storedata_Groq import ConversationHistory

class HistoryManager:
    def __init__(self):
        self.history = ConversationHistory()
    
    def show_history(self):
        recent = self.history.get_recent_conversations()
        if recent:
            print("\nRecent conversations:")
            for conv in recent:
                print(f"\nTime: {conv['timestamp']}")
                print(f"You: {conv['user_query']}")
                print(f"AI: {conv['ai_response']}")
            return True
        return False
    
    def search_history(self, search_term):
        results = self.history.search_history(search_term)
        if results:
            print(f"\nFound {len(results)} matching conversations:")
            for conv in results:
                print(f"\nTime: {conv['timestamp']}")
                print(f"You: {conv['user_query']}")
                print(f"AI: {conv['ai_response']}")
            return len(results)
        return 0
    
    def delete_history(self):
        try:
            success = self.history.clear_history()
            if success:
                print("History cleared successfully")
                return True
            else:
                print("Failed to clear history")
                return False
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
