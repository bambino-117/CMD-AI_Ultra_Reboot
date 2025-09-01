import json
import os
from core.logger import app_logger

class UserManager:
    def __init__(self, settings_path='user/settings.json'):
        self.settings_path = settings_path
        self.settings = self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            app_logger.error(f"Erreur chargement settings: {e}", "USER_MANAGER")
            return {}
    
    def save_settings(self):
        try:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            app_logger.info("Settings sauvegardés", "USER_MANAGER")
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde settings: {e}", "USER_MANAGER")
    
    def get_username(self):
        return self.settings.get('username', '')
    
    def set_username(self, username):
        self.settings['username'] = username
        self.save_settings()
        app_logger.info(f"Pseudo défini: {username}", "USER_MANAGER")
    
    def has_username(self):
        return bool(self.get_username())