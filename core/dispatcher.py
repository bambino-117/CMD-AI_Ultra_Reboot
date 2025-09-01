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
from core.auto_repair import initialize_auto_repair, get_auto_repair_manager, auto_repair_decorator
from core.logger import app_logger
from core.smart_ux import SmartUX

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
        
        # Initialiser le système de réparation automatique
        self.auto_repair = initialize_auto_repair(config)
        app_logger.debug("Système de réparation automatique initialisé", "DISPATCHER")
        
        self.awaiting_installation_response = False
        self.awaiting_update_response = False
        self.pending_update_info = None
        self.awaiting_model_selection = False
        self.awaiting_api_key = False
        self.awaiting_token_help = False
        self.selected_model_info = None
        self.awaiting_elevation_confirm = False
        self.pending_elevated_command = None
        
        # Système UX intelligent
        self.smart_ux = SmartUX()
        self.awaiting_menu_choice = False
        self.current_menu_category = None
        
        # Charger les extensions
        app_logger.info("Chargement des extensions", "DISPATCHER")
        self.extension_manager.load_extensions()
        app_logger.info("Dispatcher initialisé", "DISPATCHER")

    @auto_repair_decorator
    def process(self, user_input):
        try:
            # Gestion des menus contextuels UX
            if self.awaiting_menu_choice:
                return self._handle_menu_choice(user_input)
            
            # Gestion des états d'installation
            if self.awaiting_installation_response:
                return self._handle_installation_response(user_input)
            elif self.awaiting_model_selection:
                return self._handle_model_selection(user_input)
            elif self.awaiting_api_key:
                return self._handle_api_key_input(user_input)
            elif self.awaiting_token_help:
                return self._handle_token_help_choice(user_input)
            elif self.awaiting_elevation_confirm:
                return self._handle_elevation_confirmation(user_input)
            elif self.awaiting_update_response:
                return self._handle_update_response(user_input)
            
            # Détection d'intention intelligente
            intent_result = self._check_smart_intent(user_input)
            if intent_result:
                return intent_result
        except Exception as e:
            # Auto-repair tentera de réparer automatiquement
            app_logger.error(f"Erreur dans process(): {e}", "DISPATCHER")
            if self.auto_repair and self.auto_repair.enabled:
                # Détecter et programmer une réparation
                error_type = type(e).__name__
                error_details = {'error': str(e), 'context': 'dispatcher_process'}
                if self.auto_repair.detect_and_repair(error_type, error_details):
                    return f"🔧 Erreur détectée, réparation automatique en cours...\n⚠️ Erreur: {e}"
            raise
        
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
        elif user_input.startswith("repair "):
            return self._handle_repair_command(user_input[7:])
        elif user_input.startswith("install "):
            return self._handle_install_command(user_input[8:])
        elif user_input.startswith("dismiss "):
            return self._handle_dismiss_command(user_input[8:])
        elif user_input.startswith("never "):
            return self._handle_never_command(user_input[6:])
        elif user_input.startswith("ext "):
            return self._handle_extension_command(user_input[4:])
        elif user_input.startswith("gimp ") or user_input.startswith("design "):
            return self._handle_gimp_clone_command(user_input)
        elif user_input.lower() in ["designer", "interface designer", "gimp clone"]:
            return self._handle_gimp_clone_command("gimp launch")
        
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
• repair status/history - Réparation automatique

🎨 DESIGN D'INTERFACE:
• gimp launch - Lance GIMP Clone Studio
• designer - Raccourci interface designer
• gimp help - Aide du designer

Exemples:
• ext AIchat setup - Configurer l'IA
• plugin list - Voir plugins disponibles
• theme toggle - Changer thème
• gimp launch - Créer une interface

🤖 ASSISTANT INTELLIGENT:
• "scanner mon système" - Analyse sécurité
• "analyser un fichier" - Vérification fichier
• "créer une clé USB" - Outils BadUSB
• "tester ma connexion" - Analyse réseau
• "rechercher des infos" - OSINT"""
    
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
        
        # Si une clé API est requise, proposer le menu d'aide
        if "requise" in response:
            self.awaiting_token_help = True
            self.selected_model_info = self._get_model_info(model_number)
            return self._show_token_help_menu()
        
        return response
    
    def _get_model_info(self, model_number):
        """Retourne les informations du modèle sélectionné"""
        models = {
            "1": {"name": "OpenAI GPT", "url": "https://platform.openai.com/api-keys", "guide": "openai"},
            "2": {"name": "Google Gemini", "url": "https://makersuite.google.com/app/apikey", "guide": "gemini"},
            "4": {"name": "Hugging Face", "url": "https://huggingface.co/settings/tokens", "guide": "huggingface"}
        }
        return models.get(model_number, {"name": "Modèle", "url": "", "guide": "general"})
    
    def _show_token_help_menu(self):
        """Affiche le menu d'aide pour obtenir le token API"""
        model_name = self.selected_model_info.get("name", "ce modèle") if self.selected_model_info else "ce modèle"
        
        return f"""🔑 **CONFIGURATION {model_name.upper()}**

Une clé API est requise pour utiliser {model_name}.

Comment souhaitez-vous procéder ?

[1] 📝 J'ai déjà ma clé API (la saisir directement)
[2] 🎯 Me guider pour créer ma clé API  
[3] 🌐 Ouvrir la page de création de clé
[4] ❌ Choisir un autre modèle

Tapez le numéro de votre choix :"""
    
    def _handle_token_help_choice(self, choice):
        """Gère le choix dans le menu d'aide token"""
        self.awaiting_token_help = False
        
        if choice == "1":
            self.awaiting_api_key = True
            return f"🔑 Parfait ! Collez votre clé API {self.selected_model_info.get('name', '') if self.selected_model_info else ''} ici :"
        
        elif choice == "2":
            return self._get_token_creation_guide()
        
        elif choice == "3":
            url = self.selected_model_info.get("url", "") if self.selected_model_info else ""
            if url:
                import webbrowser
                try:
                    webbrowser.open(url)
                    self.awaiting_api_key = True
                    return f"🌐 Page ouverte dans votre navigateur !\n\n📋 Une fois votre clé créée, collez-la ici :"
                except:
                    self.awaiting_api_key = True
                    return f"🌐 Ouvrez cette URL : {url}\n\n📋 Une fois votre clé créée, collez-la ici :"
            else:
                self.awaiting_api_key = True
                return "📋 Collez votre clé API ici une fois créée :"
        
        elif choice == "4":
            self.awaiting_model_selection = True
            return self.extension_manager.execute_extension_command("AIchat", "setup")
        
        else:
            self.awaiting_token_help = True
            return "❌ Choix non reconnu. Tapez 1, 2, 3 ou 4 :"
    
    def _get_token_creation_guide(self):
        """Retourne un guide détaillé pour créer le token"""
        model_name = self.selected_model_info.get("name", "") if self.selected_model_info else ""
        guide_type = self.selected_model_info.get("guide", "general") if self.selected_model_info else "general"
        url = self.selected_model_info.get("url", "") if self.selected_model_info else ""
        
        guides = {
            "openai": f"""🎯 **GUIDE CRÉATION CLÉ OPENAI**

📋 **Étapes détaillées :**
1. 🌐 Allez sur : {url}
2. 🔐 Connectez-vous à votre compte OpenAI
3. ➕ Cliquez sur "Create new secret key"
4. 📝 Donnez un nom à votre clé (ex: "CMD-AI")
5. 📋 Copiez la clé (elle ne sera plus visible !)
6. 💰 Vérifiez vos crédits sur platform.openai.com/usage

⚠️ **Important :** Gardez votre clé secrète !

📋 Une fois créée, collez votre clé ici :""",
            
            "gemini": f"""🎯 **GUIDE CRÉATION CLÉ GEMINI**

📋 **Étapes détaillées :**
1. 🌐 Allez sur : {url}
2. 🔐 Connectez-vous avec votre compte Google
3. ➕ Cliquez sur "Create API Key"
4. 📝 Choisissez un projet ou créez-en un
5. 📋 Copiez la clé générée
6. 🆓 Gemini a un quota gratuit généreux !

⚠️ **Important :** Gardez votre clé secrète !

📋 Une fois créée, collez votre clé ici :""",
            
            "huggingface": f"""🎯 **GUIDE CRÉATION TOKEN HUGGING FACE**

📋 **Étapes détaillées :**
1. 🌐 Allez sur : {url}
2. 🔐 Connectez-vous à votre compte Hugging Face
3. ➕ Cliquez sur "New token"
4. 📝 Nom: "CMD-AI" | Type: "Read"
5. 📋 Copiez le token généré
6. 🆓 Accès gratuit à de nombreux modèles !

⚠️ **Important :** Gardez votre token secret !

📋 Une fois créé, collez votre token ici :"""
        }
        
        guide = guides.get(guide_type, f"""🎯 **GUIDE CRÉATION CLÉ API**

📋 **Étapes générales :**
1. 🌐 Allez sur le site du fournisseur
2. 🔐 Connectez-vous à votre compte
3. ➕ Créez une nouvelle clé API
4. 📋 Copiez la clé générée

📋 Une fois créée, collez votre clé ici :""")
        
        self.awaiting_api_key = True
        return guide
    
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
    
    def _handle_repair_command(self, command):
        """Gère les commandes de réparation automatique"""
        parts = command.split(' ', 2)
        action = parts[0] if parts else ""
        
        if action == "status":
            return self._get_repair_status()
        elif action == "history":
            return self._get_repair_history()
        elif action == "manual" and len(parts) > 1:
            repair_type = parts[1]
            kwargs = {}
            if len(parts) > 2:
                # Parse arguments simples
                args_str = parts[2]
                if '=' in args_str:
                    for arg in args_str.split(','):
                        if '=' in arg:
                            key, value = arg.split('=', 1)
                            kwargs[key.strip()] = value.strip()
            return self.auto_repair.manual_repair(repair_type, **kwargs)
        elif action == "enable":
            self.auto_repair.enabled = True
            return "✅ Réparation automatique activée"
        elif action == "disable":
            self.auto_repair.enabled = False
            return "⏸️ Réparation automatique désactivée"
        else:
            return """🔧 COMMANDES RÉPARATION AUTOMATIQUE

• repair status - Statut du système
• repair history - Historique des réparations
• repair manual [type] - Réparation manuelle
• repair enable/disable - Activer/désactiver

Types de réparation manuelle:
• dependency_fix packages=nom1,nom2
• import_fix module=nom_module
• file_repair filepath=chemin
• config_reset config_file=fichier
• cache_clean

Exemples:
• repair manual dependency_fix packages=requests,numpy
• repair manual cache_clean"""
    
    def _get_repair_status(self):
        """Retourne le statut du système de réparation"""
        if not self.auto_repair:
            return "❌ Système de réparation non initialisé"
        
        status = "🔧 STATUT RÉPARATION AUTOMATIQUE\n\n"
        status += f"État: {'✅ Activé' if self.auto_repair.enabled else '⏸️ Désactivé'}\n"
        status += f"Worker: {'🔄 Actif' if self.auto_repair.worker.active else '⏹️ Arrêté'}\n"
        
        # Statistiques de la file d'attente
        queue_size = self.auto_repair.worker.task_queue.qsize()
        status += f"File d'attente: {queue_size} tâche(s)\n"
        
        # Historique récent
        history = self.auto_repair.get_repair_history()
        recent_repairs = len([r for r in history if r['result']['success']])
        failed_repairs = len([r for r in history if not r['result']['success']])
        
        status += f"Réparations réussies: {recent_repairs}\n"
        status += f"Réparations échouées: {failed_repairs}\n\n"
        
        if history:
            last_repair = history[-1]
            status += f"Dernière réparation:\n"
            status += f"  📅 {last_repair['timestamp'][:19]}\n"
            status += f"  🔧 {last_repair['task']['description']}\n"
            status += f"  {'✅' if last_repair['result']['success'] else '❌'} {last_repair['result'].get('message', 'N/A')}\n"
        
        return status
    
    def _check_smart_intent(self, user_input):
        """Vérifie si l'utilisateur exprime une intention reconnue"""
        intent = self.smart_ux.detect_intent(user_input)
        if intent:
            category, action = intent
            menu = self.smart_ux.create_contextual_menu(category)
            self.awaiting_menu_choice = True
            self.current_menu_category = category
            return menu
        return None
    
    def _handle_menu_choice(self, user_input):
        """Gère les choix dans les menus contextuels"""
        if user_input.lower() in ['annuler', 'cancel', 'exit', 'quit']:
            self.awaiting_menu_choice = False
            self.current_menu_category = None
            return "❌ Opération annulée. Que puis-je faire pour vous ?"
        
        if user_input.lower() == 'menu':
            if self.current_menu_category:
                return self.smart_ux.create_contextual_menu(self.current_menu_category)
            else:
                self.awaiting_menu_choice = False
                return "Quel type d'action souhaitez-vous effectuer ?"
        
        # Traiter le choix du menu
        if self.current_menu_category and user_input.isdigit():
            response = self.smart_ux.start_guided_workflow(self.current_menu_category, user_input)
            self.awaiting_menu_choice = False
            self.current_menu_category = None
            return response
        
        return "❌ Choix non reconnu. Tapez un numéro (1-4) ou 'annuler'"
    
    def _get_repair_history(self):
        """Retourne l'historique des réparations"""
        if not self.auto_repair:
            return "❌ Système de réparation non initialisé"
        
        history = self.auto_repair.get_repair_history()
        
        if not history:
            return "📋 Aucune réparation effectuée"
        
        result = "📋 HISTORIQUE DES RÉPARATIONS\n\n"
        
        # Afficher les 10 dernières réparations
        for repair in history[-10:]:
            timestamp = repair['timestamp'][:19].replace('T', ' ')
            task_desc = repair['task']['description']
            success = repair['result']['success']
            duration = repair['duration']
            
            status_icon = "✅" if success else "❌"
            result += f"{status_icon} {timestamp}\n"
            result += f"   🔧 {task_desc}\n"
            result += f"   ⏱️ {duration:.2f}s\n"
            
            if success:
                message = repair['result'].get('message', 'Réparation réussie')
                result += f"   💬 {message}\n"
            else:
                error = repair['result'].get('error', 'Erreur inconnue')
                result += f"   ❌ {error}\n"
            
            result += "\n"
        
        if len(history) > 10:
            result += f"... et {len(history) - 10} réparations plus anciennes\n"
        
        return result
    
    def _handle_gimp_clone_command(self, command):
        """Gère les commandes GIMP Clone Studio"""
        import subprocess
        import sys
        from pathlib import Path
        
        parts = command.lower().split()
        action = parts[1] if len(parts) > 1 else "launch"
        
        if action in ["launch", "start", "run"]:
            try:
                # Chemin vers GIMP Clone Studio
                gimp_path = Path(__file__).parent.parent / "gimp_clone_studio.py"
                
                if not gimp_path.exists():
                    return """❌ GIMP Clone Studio non trouvé

🔧 Pour l'installer:
• Assurez-vous que gimp_clone_studio.py existe
• Ou tapez 'gimp install' pour le créer

💡 GIMP Clone Studio permet de:
• Créer des interfaces visuellement
• Générer du code automatiquement
• Éditer en mode WYSIWYG
• Exporter en Tkinter, PyQt, HTML/CSS"""
                
                # Lancer GIMP Clone Studio
                subprocess.Popen([sys.executable, str(gimp_path)])
                
                return """🎨 GIMP Clone Studio lancé!

✨ FONCTIONNALITÉS:
• 🛠️ Outils de dessin style GIMP
• 📚 Système de calques
• 🎨 Palette de couleurs
• 💻 Génération de code automatique
• 👁️ Prévisualisation en temps réel
• 💾 Export vers différents formats

🚀 L'interface s'ouvre dans une nouvelle fenêtre.
Créez votre interface visuellement et le code sera généré automatiquement!"""
                
            except Exception as e:
                return f"""❌ Erreur lors du lancement: {e}

🔧 Solutions:
• Vérifiez que Python fonctionne
• Redémarrez l'application
• Tapez 'gimp install' pour réinstaller"""
                
        elif action == "install":
            return """🔧 Installation de GIMP Clone Studio

GIMP Clone Studio est déjà intégré à CMD-AI!

📁 Fichiers disponibles:
• gimp_clone_studio.py - Interface principale
• launch_gimp_clone.py - Lanceur

🚀 Pour lancer: tapez 'gimp launch' ou 'designer'"""

        elif action == "help":
            return """🎨 GIMP CLONE STUDIO - AIDE

🚀 COMMANDES:
• gimp launch - Lance l'interface
• gimp help - Cette aide
• designer - Raccourci de lancement

🛠️ OUTILS DISPONIBLES:
• Rectangle, Ellipse, Texte
• Boutons, Champs de saisie
• Cadres, Onglets, Listes
• Barres de progression

🎨 FONCTIONNALITÉS:
• Système de calques comme GIMP
• Palette de couleurs
• Propriétés en temps réel
• Génération de code automatique

💻 LANGAGES SUPPORTÉS:
• Tkinter (Python)
• PyQt5 (Python) 
• HTML/CSS
• Flutter (en développement)

💡 WORKFLOW:
1. Dessinez votre interface visuellement
2. Le code est généré automatiquement
3. Prévisualisez le résultat
4. Exportez vers votre projet

📖 Plus d'infos: Lancez l'interface et explorez les menus!"""

        else:
            return """🎨 GIMP CLONE STUDIO

COMMANDES:
• gimp launch - Lance l'interface de design
• gimp help - Aide détaillée
• designer - Raccourci

💡 Créez des interfaces visuellement avec génération de code automatique!"""
