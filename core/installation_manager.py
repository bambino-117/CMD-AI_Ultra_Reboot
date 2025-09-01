import os
import json

class InstallationManager:
    def __init__(self, config_file="user/installation.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Charge la configuration d'installation"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"first_run": True, "suggested_extensions": ["AIchat"]}
    
    def _save_config(self):
        """Sauvegarde la configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def is_first_run(self):
        """Vérifie si c'est le premier lancement"""
        return self.config.get("first_run", True)
    
    def mark_first_run_complete(self):
        """Marque le premier lancement comme terminé"""
        self.config["first_run"] = False
        self._save_config()
    
    def get_suggested_extensions(self):
        """Retourne les extensions suggérées"""
        return self.config.get("suggested_extensions", [])
    
    def mark_extension_suggested(self, extension_name):
        """Marque une extension comme déjà suggérée"""
        if "suggested_extensions" in self.config:
            if extension_name in self.config["suggested_extensions"]:
                self.config["suggested_extensions"].remove(extension_name)
                self._save_config()
    
    def get_installation_prompt(self):
        """Retourne le message de suggestion d'installation"""
        # Vérifier si c'est vraiment le premier lancement
        if self.is_first_run():
            return "🤖 Bienvenue dans CMD-AI Ultra Reboot!\n\n💡 Voulez-vous configurer l'IA maintenant? (Y/N)"
        return None