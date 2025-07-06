from core.text_interpreter import TextInterpreter, CommandType
from core.extension_manager import ExtensionManager
from core.installation_manager import InstallationManager
from core.system_executor import SystemExecutor
from core.daily_suggestions import DailySuggestions
from core.updater import AppUpdater
from core.logger import app_logger

class Dispatcher:
    def __init__(self, config):
        app_logger.debug("Initialisation du Dispatcher", "DISPATCHER")
        self.config = config
        self.interpreter = TextInterpreter()
        app_logger.debug("Interpréteur de texte créé", "DISPATCHER")
        
        self.extension_manager = ExtensionManager()
        app_logger.debug("Gestionnaire d'extensions créé", "DISPATCHER")
        
        self.installation_manager = InstallationManager()
        app_logger.debug("Gestionnaire d'installation créé", "DISPATCHER")
        
        self.daily_suggestions = DailySuggestions()
        app_logger.debug("Suggestions quotidiennes créées", "DISPATCHER")
        
        self.updater = AppUpdater()
        app_logger.debug("Système de mise à jour créé", "DISPATCHER")
        
        self.awaiting_installation_response = False
        self.awaiting_update_response = False
        self.pending_update_info = None
        self.awaiting_model_selection = False
        self.awaiting_api_key = False
        self.awaiting_elevation_confirm = False
        self.pending_elevated_command = None
        
        # Charger les extensions
        app_logger.info("Chargement des extensions", "DISPATCHER")
        self.extension_manager.load_extensions()
        app_logger.info("Dispatcher initialisé", "DISPATCHER")

    def process(self, user_input):
        # Gestion des états d'installation
        if self.awaiting_installation_response:
            return self._handle_installation_response(user_input)
        elif self.awaiting_model_selection:
            return self._handle_model_selection(user_input)
        elif self.awaiting_api_key:
            return self._handle_api_key_input(user_input)
        elif self.awaiting_elevation_confirm:
            return self._handle_elevation_confirmation(user_input)
        elif self.awaiting_update_response:
            return self._handle_update_response(user_input)
        
        command_type, processed_text = self.interpreter.interpret(user_input)
        
        # Vérifier les commandes de mise à jour
        if user_input.startswith("update "):
            return self._handle_update_command(user_input[7:])
        
        # Vérifier les commandes de suggestion
        if user_input.startswith("install "):
            return self._handle_install_command(user_input[8:])
        elif user_input.startswith("dismiss "):
            return self._handle_dismiss_command(user_input[8:])
        elif user_input.startswith("never "):
            return self._handle_never_command(user_input[6:])
        
        # Vérifier les commandes d'extension
        if user_input.startswith("ext "):
            return self._handle_extension_command(user_input[4:])
        
        if command_type == CommandType.SYSTEM_COMMAND:
            return self._handle_system_command(processed_text)
        elif command_type == CommandType.AI_CHAT:
            return self._handle_ai_chat(processed_text)
        elif command_type == CommandType.HELP:
            return self._handle_help(processed_text)
        else:
            return "Commande non reconnue. Tapez 'help' pour l'aide."
    
    def _handle_system_command(self, command):
        os_type = self.interpreter.get_os_type()
        
        # Vérifier si élévation nécessaire
        needs_elevation = SystemExecutor.needs_elevation(command)
        
        if needs_elevation:
            self.awaiting_elevation_confirm = True
            self.pending_elevated_command = command
            confirmation = f"[SYSTÈME {os_type.upper()}] Commande avec privilèges: {command}\n⚠️ Confirmer exécution ? (oui/non)"
            return confirmation
        else:
            # Exécuter directement
            result = SystemExecutor.execute_command(command, elevated=False)
            return f"[SYSTÈME {os_type.upper()}]\n{result}"
    
    def _handle_ai_chat(self, text):
        return f"[CHAT IA] Question: {text}\n(Modèle IA à implémenter)"
    
    def _handle_help(self, query):
        if not query:
            return self._get_general_help()
        return f"[AIDE] Recherche pour: {query}\n(Aide contextuelle à implémenter)"
    
    def _handle_extension_command(self, command):
        parts = command.split(" ", 2)
        if len(parts) < 2:
            return "Usage: ext [extension] [commande] [args]"
        
        ext_name, ext_command = parts[0], parts[1]
        args = parts[2] if len(parts) > 2 else None
        
        return self.extension_manager.execute_extension_command(ext_name, ext_command, args)
    
    def _handle_installation_response(self, response):
        if response.lower() in ['y', 'yes', 'oui']:
            self.awaiting_installation_response = False
            self.awaiting_model_selection = True
            return self.extension_manager.execute_extension_command("AIchat", "setup")
        else:
            self.awaiting_installation_response = False
            self.installation_manager.mark_extension_suggested("AIchat")
            return "Elle te sert à quoi l'appli si tu mets de modèle de langage pauvre idiot!"
    
    def _handle_model_selection(self, model_number):
        self.awaiting_model_selection = False
        response = self.extension_manager.execute_extension_command("AIchat", "select", model_number)
        
        if "requise" in response:
            self.awaiting_api_key = True
        
        return response
    
    def _handle_api_key_input(self, api_key):
        self.awaiting_api_key = False
        self.installation_manager.mark_first_run_complete()
        return self.extension_manager.execute_extension_command("AIchat", "apikey", api_key)
    
    def get_startup_message(self):
        app_logger.debug("Récupération du message de démarrage", "DISPATCHER")
        message = self.installation_manager.get_installation_prompt()
        app_logger.info(f"Message de démarrage: {message is not None}", "DISPATCHER")
        return message
    
    def set_awaiting_installation(self):
        self.awaiting_installation_response = True
    
    def _get_general_help(self):
        help_text = """CMD-AI Ultra Reboot - Aide
        
Préfixes disponibles:
• cmd:, exec:, $, >, run: - Commandes système
• chat:, ai:, ?, ask: - Chat avec IA
• help, aide, /?, --help - Aide
• ext [extension] [commande] - Extensions

Exemples:
• cmd: dir (Windows) ou ls (macOS)
• chat: Comment créer un fichier?
• ext AIchat setup - Configurer l'IA"""
        
        # Ajouter les extensions disponibles
        extensions = self.extension_manager.list_extensions()
        if extensions:
            help_text += "\n\nExtensions chargées: " + ", ".join(extensions)
        
        return help_text
    
    def _handle_elevation_confirmation(self, response):
        """Gère la confirmation d'élévation de privilèges"""
        self.awaiting_elevation_confirm = False
        
        if response.lower() in ['oui', 'yes', 'y', 'o']:
            result = SystemExecutor.execute_command(self.pending_elevated_command, elevated=True)
            self.pending_elevated_command = None
            return f"[SYSTÈME ÉLEVÉ]\n{result}"
        else:
            self.pending_elevated_command = None
            return "Exécution annulée par l'utilisateur."
    
    def _handle_install_command(self, extension_name):
        """Gère l'installation d'extensions"""
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.install_screenshot()
        return f"Extension '{extension_name}' non reconnue"
    
    def _handle_dismiss_command(self, extension_name):
        """Gère le report de suggestions"""
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.dismiss_screenshot(permanently=False)
        return f"Suggestion '{extension_name}' non reconnue"
    
    def _handle_never_command(self, extension_name):
        """Gère le rejet définitif de suggestions"""
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.dismiss_screenshot(permanently=True)
        return f"Suggestion '{extension_name}' non reconnue"
    
    def get_daily_suggestion(self):
        """Récupère la suggestion quotidienne"""
        if self.daily_suggestions.should_show_screenshot_suggestion():
            self.daily_suggestions.mark_screenshot_shown()
            return self.daily_suggestions.get_screenshot_suggestion()
        return None
    
    def _handle_update_command(self, command):
        """Gère les commandes de mise à jour"""
        if command == "check":
            update_info = self.updater.check_for_updates(force=True)
            if update_info:
                self.pending_update_info = update_info
                self.awaiting_update_response = True
                return self.updater.get_update_message(update_info)
            else:
                return f"✅ Vous avez la dernière version (v{self.updater.current_version})"
        
        elif command == "download":
            if self.pending_update_info:
                return self._download_update()
            else:
                return "❌ Aucune mise à jour en attente"
        
        elif command == "later":
            self.awaiting_update_response = False
            self.pending_update_info = None
            return "🕰️ Mise à jour reportée"
        
        elif command == "never":
            # TODO: Implémenter désactivation permanente
            self.awaiting_update_response = False
            self.pending_update_info = None
            return "❌ Vérifications de mise à jour désactivées"
        
        else:
            return "Commandes: update check, update download, update later, update never"
    
    def _handle_update_response(self, response):
        """Gère les réponses aux mises à jour"""
        self.awaiting_update_response = False
        
        if response.lower() in ['download', 'oui', 'yes', 'y']:
            return self._download_update()
        elif response.lower() in ['later', 'plus tard']:
            self.pending_update_info = None
            return "🕰️ Mise à jour reportée"
        else:
            self.pending_update_info = None
            return "❌ Mise à jour annulée"
    
    def _download_update(self):
        """Télécharge et installe la mise à jour"""
        if not self.pending_update_info:
            return "❌ Aucune mise à jour en attente"
        
        try:
            download_url = self.pending_update_info["download_url"]
            
            # Téléchargement
            file_path = self.updater.download_update(download_url)
            
            if file_path:
                # Installation
                if self.updater.install_update(file_path):
                    return f"✅ Mise à jour téléchargée !\n\n🚀 L'installation va commencer.\n⚠️ Fermez l'application après installation."
                else:
                    return f"⚠️ Téléchargement réussi mais installation manuelle requise.\n📁 Fichier: {file_path}"
            else:
                return "❌ Échec du téléchargement"
                
        except Exception as e:
            app_logger.error(f"Erreur download update: {e}", "DISPATCHER")
            return f"❌ Erreur: {e}"
        finally:
            self.pending_update_info = None
    
    def check_startup_update(self):
        """Vérifie les mises à jour au démarrage"""
        update_info = self.updater.check_for_updates()
        if update_info:
            self.pending_update_info = update_info
            self.awaiting_update_response = True
            return self.updater.get_update_message(update_info)
        return None
