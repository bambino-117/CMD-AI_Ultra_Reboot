import json
import os
from datetime import datetime, timedelta
from core.logger import app_logger

class DailySuggestions:
    def __init__(self):
        self.suggestions_file = "user/daily_suggestions.json"
        self.suggestions_data = self._load_suggestions()
    
    def _load_suggestions(self):
        """Charge les données de suggestions"""
        try:
            if os.path.exists(self.suggestions_file):
                with open(self.suggestions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement suggestions: {e}", "DAILY_SUGGESTIONS")
        
        return {
            "last_shown": {},
            "installed_extensions": [],
            "dismissed_suggestions": []
        }
    
    def _save_suggestions(self):
        """Sauvegarde les données de suggestions"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.suggestions_file, 'w', encoding='utf-8') as f:
                json.dump(self.suggestions_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde suggestions: {e}", "DAILY_SUGGESTIONS")
    
    def should_show_screenshot_suggestion(self):
        """Vérifie si on doit proposer l'extension Screenshot"""
        # Vérifier si déjà installée
        if "Screenshot" in self.suggestions_data.get("installed_extensions", []):
            return False
        
        # Vérifier si suggestion rejetée définitivement
        if "screenshot_never" in self.suggestions_data.get("dismissed_suggestions", []):
            return False
        
        # Vérifier la dernière fois qu'on l'a proposée
        last_shown = self.suggestions_data.get("last_shown", {}).get("screenshot")
        if last_shown:
            last_date = datetime.fromisoformat(last_shown)
            if datetime.now() - last_date < timedelta(days=1):
                return False
        
        return True
    
    def get_screenshot_suggestion(self):
        """Retourne le message de suggestion pour Screenshot"""
        return """📸 NOUVELLE EXTENSION DISPONIBLE !

🎯 Extension Screenshot - Capture d'écran pour IA
• Capture plein écran ou sélective
• Envoi direct à votre IA pour analyse
• Compatible Windows/macOS/Linux

💡 Commandes:
• ext Screenshot capture - Capture plein écran
• ext Screenshot select - Capture sélective
• ext AIchat image screenshot.png Que vois-tu ?

❓ Voulez-vous installer cette extension ?
• Tapez: install screenshot (pour installer)
• Tapez: dismiss screenshot (pour reporter à demain)
• Tapez: never screenshot (pour ne plus proposer)"""
    
    def mark_screenshot_shown(self):
        """Marque la suggestion Screenshot comme affichée"""
        self.suggestions_data.setdefault("last_shown", {})["screenshot"] = datetime.now().isoformat()
        self._save_suggestions()
    
    def install_screenshot(self):
        """Marque Screenshot comme installée"""
        if "Screenshot" not in self.suggestions_data.get("installed_extensions", []):
            self.suggestions_data.setdefault("installed_extensions", []).append("Screenshot")
            self._save_suggestions()
            return "✅ Extension Screenshot installée ! Utilisez: ext Screenshot help"
        return "Extension déjà installée"
    
    def dismiss_screenshot(self, permanently=False):
        """Rejette la suggestion Screenshot"""
        if permanently:
            if "screenshot_never" not in self.suggestions_data.get("dismissed_suggestions", []):
                self.suggestions_data.setdefault("dismissed_suggestions", []).append("screenshot_never")
                self._save_suggestions()
                return "Extension Screenshot ne sera plus proposée"
        else:
            self.mark_screenshot_shown()  # Reporter à demain
            return "Extension Screenshot reportée à demain"
    
    def is_screenshot_installed(self):
        """Vérifie si Screenshot est installée"""
        return "Screenshot" in self.suggestions_data.get("installed_extensions", [])