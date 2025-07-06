from .ollama_llm import OllamaLLM
from .fallback_llm import FallbackLLM
from .api_llm import APIBasedLLM
from .simple_llm import SimpleLLM
from core.logger import app_logger
from core.user_manager import UserManager

class LLMManager:
    """Gestionnaire des modèles de langage avec fallback automatique"""
    
    def __init__(self):
        self.llms = []
        self.current_llm = None
        self.user_manager = UserManager()
        self.available_models = {
            "1": {"name": "IA Gratuite", "provider": "simple", "model": "IA Simple"},
            "2": {"name": "ChatGPT", "provider": "openai", "model": "gpt-3.5-turbo"},
            "3": {"name": "Gemini", "provider": "gemini", "model": "gemini-pro"},
            "4": {"name": "DeepSeek", "provider": "deepseek", "model": "deepseek-chat"},
            "5": {"name": "Ollama (Local)", "provider": "ollama", "model": "phi3:mini"},
            "6": {"name": "Mode Hors-ligne", "provider": "fallback", "model": "fallback"}
        }
        self.initialize_llms()
    
    def initialize_llms(self):
        """Initialise les LLM selon la configuration utilisateur"""
        app_logger.info("Initialisation des LLM...", "LLM_MANAGER")
        
        # Charger la configuration utilisateur
        settings = self.user_manager.settings
        selected_model = settings.get('selected_llm')
        api_keys = settings.get('api_keys', {})
        
        # Créer les LLM selon les clés API disponibles
        for key, config in self.available_models.items():
            if config['provider'] == 'ollama':
                llm = OllamaLLM(config['model'])
                self.llms.append(llm)
            elif config['provider'] == 'fallback':
                llm = FallbackLLM()
                self.llms.append(llm)
            elif config['provider'] == 'simple':
                llm = SimpleLLM()
                self.llms.append(llm)
            else:
                api_key = api_keys.get(config['provider'])
                llm = APIBasedLLM(config['model'], api_key, config['provider'])
                self.llms.append(llm)
        
        # Sélectionner le modèle actuel
        if selected_model and self.switch_model_by_number(selected_model):
            app_logger.info(f"Modèle configuré: {selected_model}", "LLM_MANAGER")
        else:
            # IA Gratuite par défaut (modèle 1)
            if self.switch_model_by_number("1"):
                app_logger.info("IA Gratuite activée par défaut", "LLM_MANAGER")
            else:
                # Fallback en dernier recours
                fallback = next((llm for llm in self.llms if isinstance(llm, FallbackLLM)), None)
                if fallback:
                    self.current_llm = fallback
                    app_logger.warning("Mode fallback activé", "LLM_MANAGER")
    
    def get_response(self, prompt, max_tokens=150):
        """Génère une réponse avec le LLM actuel"""
        if not self.current_llm:
            return "Aucun modèle de langage disponible"
        
        try:
            response = self.current_llm.generate_response(prompt, max_tokens)
            app_logger.debug(f"Réponse générée par {self.current_llm.model_name}", "LLM_MANAGER")
            return response
        except Exception as e:
            app_logger.error(f"Erreur génération réponse: {e}", "LLM_MANAGER")
            # Basculer vers fallback en cas d'erreur
            if self.current_llm.__class__.__name__ != "FallbackLLM":
                fallback = next((llm for llm in self.llms if llm.__class__.__name__ == "FallbackLLM"), None)
                if fallback:
                    self.current_llm = fallback
                    return fallback.generate_response(prompt, max_tokens)
            return "Erreur lors de la génération de la réponse"
    
    def get_available_models(self):
        """Retourne la liste des modèles disponibles"""
        return [llm.get_model_info() for llm in self.llms if llm.is_available]
    
    def switch_model_by_number(self, model_number):
        """Change de modèle par numéro"""
        if model_number in self.available_models:
            config = self.available_models[model_number]
            for llm in self.llms:
                if (llm.model_name == config['model'] or 
                    (isinstance(llm, FallbackLLM) and config['provider'] == 'fallback') or
                    (hasattr(llm, '__class__') and llm.__class__.__name__ == 'SimpleLLM' and config['provider'] == 'simple')):
                    if llm.is_available:
                        self.current_llm = llm
                        # Sauvegarder le choix
                        self.user_manager.settings['selected_llm'] = model_number
                        self.user_manager.save_settings()
                        app_logger.info(f"Basculé vers {config['name']}", "LLM_MANAGER")
                        return True
        return False
    
    def configure_api_key(self, provider, api_key):
        """Configure une clé API"""
        if 'api_keys' not in self.user_manager.settings:
            self.user_manager.settings['api_keys'] = {}
        self.user_manager.settings['api_keys'][provider] = api_key
        self.user_manager.save_settings()
        
        # Recréer le LLM avec la nouvelle clé
        self.initialize_llms()
        app_logger.info(f"Clé API {provider} configurée", "LLM_MANAGER")
    
    def get_model_selection_menu(self):
        """Retourne le menu de sélection des modèles"""
        menu = "=== Sélection du modèle IA ===\n\n"
        for key, config in self.available_models.items():
            status = "✓" if self._is_model_configured(config) else "✗"
            menu += f"{key}. {config['name']} {status}\n"
        return menu
    
    def _is_model_configured(self, config):
        """Vérifie si un modèle est configuré"""
        if config['provider'] in ['ollama', 'fallback', 'simple']:
            return True
        api_keys = self.user_manager.settings.get('api_keys', {})
        return config['provider'] in api_keys
    
    def get_current_model_info(self):
        """Retourne les infos du modèle actuel"""
        return self.current_llm.get_model_info() if self.current_llm else None