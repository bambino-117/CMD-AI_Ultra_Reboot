import json
import os
from core.logger import app_logger

class ThemeManager:
    def __init__(self):
        self.themes_file = "user/themes.json"
        self.current_theme_file = "user/current_theme.json"
        self.themes = self._load_themes()
        self.current_theme = self._load_current_theme()
    
    def _load_themes(self):
        """Charge les thèmes disponibles"""
        default_themes = {
            "light": {
                "name": "Clair",
                "bg_color": "#FFFFFF",
                "text_color": "#000000",
                "input_bg": "#F5F5F5",
                "button_bg": "#E0E0E0",
                "button_fg": "#000000",
                "accent_color": "#0078D4"
            },
            "dark": {
                "name": "Sombre",
                "bg_color": "#2B2B2B",
                "text_color": "#FFFFFF",
                "input_bg": "#3C3C3C",
                "button_bg": "#404040",
                "button_fg": "#FFFFFF",
                "accent_color": "#0078D4"
            },
            "blue": {
                "name": "Bleu",
                "bg_color": "#1E3A8A",
                "text_color": "#FFFFFF",
                "input_bg": "#1E40AF",
                "button_bg": "#3B82F6",
                "button_fg": "#FFFFFF",
                "accent_color": "#60A5FA"
            },
            "green": {
                "name": "Vert",
                "bg_color": "#064E3B",
                "text_color": "#FFFFFF",
                "input_bg": "#065F46",
                "button_bg": "#059669",
                "button_fg": "#FFFFFF",
                "accent_color": "#34D399"
            }
        }
        
        try:
            if os.path.exists(self.themes_file):
                with open(self.themes_file, 'r', encoding='utf-8') as f:
                    custom_themes = json.load(f)
                default_themes.update(custom_themes)
        except Exception as e:
            app_logger.error(f"Erreur chargement thèmes: {e}", "THEME_MANAGER")
        
        return default_themes
    
    def _load_current_theme(self):
        """Charge le thème actuel"""
        try:
            if os.path.exists(self.current_theme_file):
                with open(self.current_theme_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("theme", "light")
        except Exception as e:
            app_logger.error(f"Erreur chargement thème actuel: {e}", "THEME_MANAGER")
        
        return "light"
    
    def _save_current_theme(self):
        """Sauvegarde le thème actuel"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.current_theme_file, 'w', encoding='utf-8') as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde thème: {e}", "THEME_MANAGER")
    
    def get_theme(self, theme_name=None):
        """Récupère un thème"""
        if not theme_name:
            theme_name = self.current_theme
        
        return self.themes.get(theme_name, self.themes["light"])
    
    def set_theme(self, theme_name):
        """Change le thème"""
        if theme_name not in self.themes:
            return f"❌ Thème '{theme_name}' non trouvé"
        
        self.current_theme = theme_name
        self._save_current_theme()
        
        return f"✅ Thème changé: {self.themes[theme_name]['name']}\n💡 Redémarrez l'application pour appliquer"
    
    def list_themes(self):
        """Liste les thèmes disponibles"""
        result = "🎨 THÈMES DISPONIBLES\n\n"
        
        for theme_id, theme_data in self.themes.items():
            current = " (ACTUEL)" if theme_id == self.current_theme else ""
            result += f"🎨 {theme_data['name']}{current}\n"
            result += f"   ID: {theme_id}\n"
            result += f"   💡 Appliquer: theme set {theme_id}\n\n"
        
        return result
    
    def get_shortcuts(self):
        """Récupère les raccourcis clavier"""
        return {
            "send_message": "Ctrl+Enter",
            "clear_input": "Ctrl+L",
            "toggle_theme": "Ctrl+T",
            "screenshot": "Ctrl+Shift+S",
            "save_conversation": "Ctrl+S",
            "help": "F1",
            "quit": "Ctrl+Q"
        }