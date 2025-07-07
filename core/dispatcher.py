from core.text_interpreter import TextInterpreter, CommandType
from core.extension_manager import ExtensionManager
from core.installation_manager import InstallationManager
from core.system_executor import SystemExecutor
from core.daily_suggestions import DailySuggestions
from core.updater import AppUpdater
from core.plugin_manager import PluginManager
from core.conversation_manager import ConversationManager
from core.offline_manager import OfflineManager
from core.theme_manager import ThemeManager
from core.system_integration import SystemIntegration
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
        
        self.plugin_manager = PluginManager()
        app_logger.debug("Gestionnaire de plugins créé", "DISPATCHER")
        
        self.conversation_manager = ConversationManager()
        app_logger.debug("Gestionnaire de conversations créé", "DISPATCHER")
        
        self.offline_manager = OfflineManager()
        app_logger.debug("Gestionnaire hors-ligne créé", "DISPATCHER")
        
        self.theme_manager = ThemeManager()
        app_logger.debug("Gestionnaire de thèmes créé", "DISPATCHER")
        
        self.system_integration = SystemIntegration()
        app_logger.debug("Intégration système créée", "DISPATCHER")
        
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
        
        # Vérifier les commandes spécialisées
        if user_input.startswith("update "):
            return self._handle_update_command(user_input[7:])
        elif user_input.startswith("plugin "):
            return self._handle_plugin_command(user_input[7:])
        elif user_input.startswith("conv "):
            return self._handle_conversation_command(user_input[5:])
        elif user_input.startswith("cache "):
            return self._handle_cache_command(user_input[6:])
        elif user_input.startswith("theme "):
            return self._handle_theme_command(user_input[6:])
        elif user_input.startswith("system "):
            return self._handle_system_integration_command(user_input[7:])
        elif user_input.startswith("install "):
            return self._handle_install_command(user_input[8:])
        elif user_input.startswith("dismiss "):
            return self._handle_dismiss_command(user_input[8:])
        elif user_input.startswith("never "):
            return self._handle_never_command(user_input[6:])
        elif user_input.startswith("ext "):
            return self._handle_extension_command(user_input[4:])
        
        # Commandes génériques
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
        needs_elevation = SystemExecutor.needs_elevation(command)
        
        if needs_elevation:
            self.awaiting_elevation_confirm = True
            self.pending_elevated_command = command
            return f"[SYSTÈME {os_type.upper()}] Commande avec privilèges: {command}\n⚠️ Confirmer exécution ? (oui/non)"
        else:
            result = SystemExecutor.execute_command(command, elevated=False)
            return f"[SYSTÈME {os_type.upper()}]\n{result}"
    
    def _handle_ai_chat(self, text):
        if self.offline_manager.is_online():
            response = self.extension_manager.execute_extension_command("AIchat", "chat", text)
            if not response.startswith("❌"):
                self.offline_manager.cache_response(text, response)
            return response
        else:
            return self.offline_manager.get_offline_response(text)
    
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
    
    def get_startup_message(self):
        app_logger.debug("Récupération du message de démarrage", "DISPATCHER")
        message = self.installation_manager.get_installation_prompt()
        app_logger.info(f"Message de démarrage: {message is not None}", "DISPATCHER")
        return message
    
    def set_awaiting_installation(self):
        self.awaiting_installation_response = True
    
    def get_daily_suggestion(self):
        if self.daily_suggestions.should_show_screenshot_suggestion():
            self.daily_suggestions.mark_screenshot_shown()
            return self.daily_suggestions.get_screenshot_suggestion()
        return None
    
    def check_startup_update(self):
        update_info = self.updater.check_for_updates()
        if update_info:
            self.pending_update_info = update_info
            self.awaiting_update_response = True
            return self.updater.get_update_message(update_info)
        return None
    
    def _get_general_help(self):
        return """CMD-AI Ultra Reboot - Aide

Préfixes disponibles:
• cmd:, exec:, $, >, run: - Commandes système
• chat:, ai:, ?, ask: - Chat avec IA
• help, aide, /?, --help - Aide
• ext [extension] [commande] - Extensions

Nouvelles commandes:
• plugin list/install/remove - Gestion plugins
• conv save/load/pdf - Conversations
• cache status/clear - Cache hors-ligne
• theme set/toggle - Thèmes interface
• system notify/startup - Intégration OS

Exemples:
• ext AIchat setup - Configurer l'IA
• plugin list - Voir plugins disponibles
• theme toggle - Changer thème"""
    
    # Méthodes de gestion simplifiées
    def _handle_installation_response(self, response):
        if response.lower() in ['y', 'yes', 'oui']:
            self.awaiting_installation_response = False
            self.awaiting_model_selection = True
            return self.extension_manager.execute_extension_command("AIchat", "setup")
        else:
            self.awaiting_installation_response = False
            self.installation_manager.mark_extension_suggested("AIchat")
            return "Configuration IA annulée"
    
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
    
    def _handle_elevation_confirmation(self, response):
        self.awaiting_elevation_confirm = False
        if response.lower() in ['oui', 'yes', 'y', 'o']:
            result = SystemExecutor.execute_command(self.pending_elevated_command, elevated=True)
            self.pending_elevated_command = None
            return f"[SYSTÈME ÉLEVÉ]\n{result}"
        else:
            self.pending_elevated_command = None
            return "Exécution annulée par l'utilisateur."
    
    def _handle_install_command(self, extension_name):
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.install_screenshot()
        return f"Extension '{extension_name}' non reconnue"
    
    def _handle_dismiss_command(self, extension_name):
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.dismiss_screenshot(permanently=False)
        return f"Suggestion '{extension_name}' non reconnue"
    
    def _handle_never_command(self, extension_name):
        if extension_name.lower() == "screenshot":
            return self.daily_suggestions.dismiss_screenshot(permanently=True)
        return f"Suggestion '{extension_name}' non reconnue"
    
    # Handlers simplifiés pour les nouvelles fonctionnalités
    def _handle_update_command(self, command):
        if command == "check":
            update_info = self.updater.check_for_updates(force=True)
            if update_info:
                self.pending_update_info = update_info
                self.awaiting_update_response = True
                return self.updater.get_update_message(update_info)
            else:
                return f"✅ Vous avez la dernière version (v{self.updater.current_version})"
        return "Commandes: update check"
    
    def _handle_update_response(self, response):
        self.awaiting_update_response = False
        self.pending_update_info = None
        return "Mise à jour gérée"
    
    def _handle_plugin_command(self, command):
        parts = command.split(' ', 1)
        action = parts[0] if parts else ""
        
        if action == "list":
            return self.plugin_manager.list_available_plugins()
        elif action == "installed":
            return self.plugin_manager.get_installed_plugins()
        elif action == "install" and len(parts) > 1:
            return self.plugin_manager.install_plugin(parts[1])
        elif action == "remove" and len(parts) > 1:
            return self.plugin_manager.remove_plugin(parts[1])
        else:
            return "Commandes: plugin list, plugin installed, plugin install [id], plugin remove [id]"
    
    def _handle_conversation_command(self, command):
        parts = command.split(' ', 1)
        action = parts[0] if parts else ""
        
        if action == "list":
            return self.conversation_manager.list_conversations()
        elif action == "save":
            title = parts[1] if len(parts) > 1 else None
            return self.conversation_manager.save_conversation([], title)
        else:
            return "Commandes: conv list, conv save [titre]"
    
    def _handle_cache_command(self, command):
        parts = command.split(' ', 1)
        action = parts[0] if parts else ""
        
        if action == "status":
            return self.offline_manager.get_cache_stats()
        elif action == "clear":
            return self.offline_manager.clear_cache()
        else:
            return "Commandes: cache status, cache clear"
    
    def _handle_theme_command(self, command):
        parts = command.split(' ', 1)
        action = parts[0] if parts else ""
        
        if action == "list":
            return self.theme_manager.list_themes()
        elif action == "set" and len(parts) > 1:
            return self.theme_manager.set_theme(parts[1])
        elif action == "toggle":
            current = self.theme_manager.current_theme
            new_theme = "dark" if current == "light" else "light"
            return self.theme_manager.set_theme(new_theme)
        else:
            return "Commandes: theme list, theme set [nom], theme toggle"
    
    def _handle_system_integration_command(self, command):
        parts = command.split(' ', 2)
        action = parts[0] if parts else ""
        
        if action == "notify" and len(parts) >= 3:
            title = parts[1].strip('"')
            message = parts[2].strip('"')
            success = self.system_integration.send_notification(title, message)
            return "✅ Notification envoyée" if success else "❌ Erreur notification"
        elif action == "info":
            info = self.system_integration.get_system_info()
            return f"🖥️ Système: {info.get('system', 'N/A')} - CPU: {info.get('cpu_count', 'N/A')} cœurs"
        else:
            return "Commandes: system notify [titre] [message], system info"
