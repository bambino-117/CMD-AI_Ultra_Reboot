import json
import os
from datetime import datetime
from core.logger import app_logger

class ChatHistory:
    def __init__(self, history_path='user/chat_history.json'):
        self.history_path = history_path
        self.sessions = self.load_history()
        self.current_session = self.create_new_session()
    
    def load_history(self):
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"sessions": []}
        except Exception as e:
            app_logger.error(f"Erreur chargement historique: {e}", "CHAT_HISTORY")
            return {"sessions": []}
    
    def save_history(self):
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde historique: {e}", "CHAT_HISTORY")
    
    def create_new_session(self):
        session = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "messages": []
        }
        return session
    
    def add_message(self, user_message, ai_response, model_name):
        message = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response,
            "model": model_name
        }
        self.current_session["messages"].append(message)
        self.save_session()
    
    def save_session(self):
        # Ajouter session actuelle si elle a des messages
        if self.current_session["messages"]:
            # Vérifier si session existe déjà
            existing = next((s for s in self.sessions["sessions"] 
                           if s["id"] == self.current_session["id"]), None)
            if existing:
                existing["messages"] = self.current_session["messages"]
            else:
                self.sessions["sessions"].append(self.current_session.copy())
            self.save_history()
    
    def get_recent_messages(self, count=5):
        if self.current_session["messages"]:
            return self.current_session["messages"][-count:]
        return []