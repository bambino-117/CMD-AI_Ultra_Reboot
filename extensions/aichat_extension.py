from core.base_extension import BaseExtension
from language_models.llm_manager import LLMManager
from core.chat_history import ChatHistory
from core.kaamelott_responses import KaamelottResponses

class AIChatExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "AIchat"
        self.version = "1.0.0"
        self.description = "Extension de chat avec modèles de langage"
        self.author = "CMD-AI Team"
        self.llm_manager = LLMManager()
        self.chat_history = ChatHistory()
        self.setup_mode = None
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "setup":
            return self._start_setup()
        elif command == "select":
            return self._select_model(args)
        elif command == "apikey":
            return self._set_api_key(args)
        elif command == "chat":
            return self._chat(args)
        elif command == "image":
            return self._chat_with_image(args)
        elif command == "history":
            return self._show_history()
        elif command == "status":
            return self._get_status()
        else:
            return f"Commandes: setup, select, apikey, chat, history, status"
    
    def _start_setup(self):
        self.setup_mode = "model_selection"
        result = self.llm_manager.get_model_selection_menu()
        result += "\nChoisissez: ext AIchat select [1-6]"
        return result
    
    def _select_model(self, model_number):
        if not model_number:
            return f"Usage: ext AIchat select [1-6]\n\n{KaamelottResponses.get_impatience()}"
        
        config = self.llm_manager.available_models.get(model_number)
        if not config:
            return "Numéro invalide (1-6)"
        
        if config['provider'] not in ['ollama', 'fallback', 'simple']:
            api_keys = self.llm_manager.user_manager.settings.get('api_keys', {})
            if config['provider'] not in api_keys:
                self.setup_mode = f"api_key_{config['provider']}"
                return f"Clé API {config['provider']} requise.\nUsage: ext AIchat apikey [votre_clé]"
        
        if self.llm_manager.switch_model_by_number(model_number):
            self.setup_mode = None
            return f"{config['name']} activé ! Usage: ext AIchat chat [message]"
        else:
            return f"Erreur activation {config['name']}"
    
    def _set_api_key(self, api_key):
        if not self.setup_mode or not self.setup_mode.startswith("api_key_"):
            return "Aucune config API en cours"
        
        provider = self.setup_mode.replace("api_key_", "")
        if not api_key:
            return f"Usage: ext AIchat apikey [clé_{provider}]\n\n{KaamelottResponses.get_impatience()}"
        
        self.llm_manager.configure_api_key(provider, api_key)
        self.setup_mode = None
        return f"Clé {provider} OK ! Usage: ext AIchat setup"
    
    def _chat(self, message):
        if not message:
            return f"Usage: ext AIchat chat [message]\n\n{KaamelottResponses.get_impatience()}"
        
        current_model = self.llm_manager.get_current_model_info()
        if not current_model:
            return f"Aucun modèle. Usage: ext AIchat setup\n\n{KaamelottResponses.get_error()}"
        
        response = self.llm_manager.get_response(message)
        self.chat_history.add_message(message, response, current_model['name'])
        
        return f"[{current_model['name']}] {response}"
    
    def _chat_with_image(self, args):
        """Chat avec une image"""
        if not args:
            return "Usage: ext AIchat image [chemin_image] [question]\n\nExemple: ext AIchat image screenshot.png Que vois-tu ?"
        
        parts = args.split(' ', 1)
        if len(parts) < 2:
            return "Usage: ext AIchat image [chemin_image] [question]"
        
        image_path, question = parts
        
        # Vérifier si le fichier existe
        import os
        if not os.path.exists(image_path):
            return f"❌ Image non trouvée: {image_path}"
        
        current_model = self.llm_manager.get_current_model_info()
        if not current_model:
            return f"Aucun modèle. Usage: ext AIchat setup\n\n{KaamelottResponses.get_error()}"
        
        # Pour l'instant, simuler l'analyse d'image
        response = f"[ANALYSE IMAGE] {image_path}\n\nJe vois une image, mais l'analyse d'image n'est pas encore implémentée pour ce modèle.\n\nVotre question: {question}\n\n🚧 Fonctionnalité en développement - Prochaine mise à jour !"
        
        self.chat_history.add_message(f"[IMAGE] {question}", response, current_model['name'])
        
        return f"[{current_model['name']}] {response}"
    
    def _show_history(self):
        recent = self.chat_history.get_recent_messages(3)
        if not recent:
            return "Aucun historique"
        
        result = "=== Historique ===\n"
        for msg in recent:
            result += f"Vous: {msg['user'][:40]}...\n"
            result += f"[{msg['model']}]: {msg['ai'][:40]}...\n\n"
        return result
    
    def _get_status(self):
        current = self.llm_manager.get_current_model_info()
        if not current:
            return "Aucun modèle configuré"
        return f"Modèle actuel: {current['name']} ({current['type']})"
    
    def get_commands(self):
        return ["setup", "select", "apikey", "chat", "image", "history", "status"]