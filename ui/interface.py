# imports des dépendances
import tkinter as tk
# imports des fichiers
from tkinter import ttk
from core.logger import app_logger

try:
    from ui.widgets.custom_text_area import CustomTextArea
    app_logger.debug("CustomTextArea importé", "UI")
except ImportError:
    from core.fallback_components import FallbackTextArea as CustomTextArea
    app_logger.warning("Utilisation de FallbackTextArea", "UI")

try:
    from ui.widgets.settings_panel import SettingsPanel
    app_logger.debug("SettingsPanel importé", "UI")
except ImportError:
    from core.fallback_components import FallbackSettings as SettingsPanel
    app_logger.warning("Utilisation de FallbackSettings", "UI")

try:
    from ui.splash_screen import SplashScreen
    app_logger.debug("SplashScreen importé", "UI")
except ImportError:
    SplashScreen = None
    app_logger.warning("SplashScreen non disponible", "UI")

class AppUI:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.root = tk.Tk()
        
        # Rapport de session pour testeurs
        from core.exit_reporter import ExitReporter
        self.exit_reporter = ExitReporter()
        # Titre avec détection mode testeur
        from core.tester_auth import TesterAuth
        from core.user_manager import UserManager
        
        tester_auth = TesterAuth()
        user_manager = UserManager()
        current_pseudo = user_manager.get_username()
        
        if tester_auth.is_tester_code(current_pseudo):
            self.root.title(f"CMD-AI Ultra Reboot - TESTEUR {current_pseudo}")
        else:
            self.root.title("CMD-AI Ultra Reboot")
        self.root.geometry("960x720")  # +20% (800->960, 600->720)
        self.root.minsize(720, 480)  # Taille minimale +20%
        
        # Icône de l'application
        self.set_icon()
        
        # Créer l'interface
        self.setup_ui()
        
        # Affichage marketplace avec tuiles
        from ui.marketplace_tiles import MarketplaceTiles
        self.marketplace_tiles = MarketplaceTiles(self, self.dispatcher)
        
        # Système de thèmes
        self._setup_theme_system()
    
    def set_icon(self):
        """Configure l'icône de l'application"""
        try:
            import os
            import platform
            from PIL import Image, ImageTk
            
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            if platform.system() == "Windows":
                # Windows : utiliser .ico
                icon_path = os.path.join(base_path, "ressources", "icons", "CMD-AI_Ultra_main.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    return
            
            # Linux/macOS : utiliser PNG converti
            png_path = os.path.join(base_path, "ressources", "logos", "CMD-AI_Ultra_main.png")
            if os.path.exists(png_path):
                # Méthode 1: iconphoto
                try:
                    img = Image.open(png_path)
                    img = img.resize((64, 64), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.root.iconphoto(False, photo)
                    self.root._icon_photo = photo
                    app_logger.debug("Icône PNG chargée via iconphoto", "UI")
                    return
                except:
                    pass
                
                # Méthode 2: wm_iconbitmap (fallback)
                try:
                    self.root.wm_iconbitmap('@' + png_path)
                    app_logger.debug("Icône PNG chargée via wm_iconbitmap", "UI")
                    return
                except:
                    pass
                
        except Exception as e:
            app_logger.debug(f"Icône non chargée: {e}", "UI")
        
        # Dernier recours: titre avec emoji
        self.root.title("🤖 CMD-AI Ultra Reboot")
        
        # Import pour la surveillance des thèmes
        import json
        import os
    
    def _setup_theme_system(self):
        """Configure le système de thèmes"""
        try:
            from core.theme_applier import get_theme_applier
            self.theme_applier = get_theme_applier(self.root)
            
            # Surveiller les changements de thème
            self._monitor_theme_changes()
            
            app_logger.debug("Système de thèmes configuré", "UI")
        except Exception as e:
            app_logger.debug(f"Système de thèmes non configuré: {e}", "UI")
    
    def _monitor_theme_changes(self):
        """Surveille les changements de thème"""
        def check_theme_signal():
            signal_file = "user/theme_update_signal.json"
            try:
                if os.path.exists(signal_file):
                    with open(signal_file, 'r') as f:
                        data = json.load(f)
                    
                    # Appliquer le thème
                    if self.theme_applier:
                        self.theme_applier.apply_theme_immediately(data['data'])
                    
                    # Supprimer le signal
                    os.remove(signal_file)
                    app_logger.info(f"Thème {data['theme']} appliqué", "UI")
                    
            except Exception as e:
                pass
            
            # Vérifier à nouveau dans 1 seconde
            self.root.after(1000, check_theme_signal)
        
        # Démarrer la surveillance
        check_theme_signal()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal avec panneau latéral
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Zone de chat (droite)
        self.chat_frame = ttk.Frame(main_frame)
        self.chat_frame.pack(side='right', fill='both', expand=True)

        # Création de l'instance de CustomTextArea
        self.text_area = CustomTextArea(self.chat_frame)
        
        # Panneau de paramètres (créé à la demande)
        self.settings_panel = None
        self.settings_visible = False

        # Menu "Fichier"
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        fichier_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Fichier", menu=fichier_menu)

        fichier_menu.add_command(label="⚙️ Paramètres", command=self.toggle_settings)
        fichier_menu.add_separator()
        fichier_menu.add_command(label="❌ Quitter", command=self.on_quit)
        
        # Menu Marketplace
        marketplace_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="🔌 Marketplace", menu=marketplace_menu)
        
        marketplace_menu.add_command(label="📦 Extensions disponibles", command=self.show_marketplace)
        marketplace_menu.add_command(label="✅ Extensions installées", command=self.show_installed_extensions)
        marketplace_menu.add_separator()
        marketplace_menu.add_command(label="🔄 Actualiser marketplace", command=self.refresh_marketplace)
        
        # Menu Aide
        aide_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Aide", menu=aide_menu)
        
        aide_menu.add_command(label="📖 Guide d'utilisation", command=self.show_help)
        aide_menu.add_command(label="⌨️ Commandes", command=self.show_commands)
        aide_menu.add_separator()
        aide_menu.add_command(label="ℹ️ À propos", command=self.show_about)

        # Frame pour la saisie
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Frame pour les boutons et vignettes
        controls_frame = ttk.Frame(input_frame)
        controls_frame.pack(fill='x', pady=(0, 5))
        
        # Widget de capture d'écran
        from ui.widgets.screenshot_widget import ScreenshotWidget
        self.screenshot_widget = ScreenshotWidget(controls_frame, self.on_screenshot_taken)

        # Frame pour l'entrée de texte
        text_input_frame = ttk.Frame(input_frame)
        text_input_frame.pack(fill='x')
        
        # Import du widget d'inactivité
        try:
            from ui.widgets.inactivity_entry import InactivityEntry
            self.input_var = tk.StringVar()
            self.input_entry = InactivityEntry(text_input_frame, textvariable=self.input_var)
            self.input_entry.pack(side='left', fill='x', expand=True)
            self.input_entry.bind('<Return>', self.on_send)
        except ImportError:
            # Fallback vers Entry normal
            self.input_var = tk.StringVar()
            self.input_entry = ttk.Entry(text_input_frame, textvariable=self.input_var)
            self.input_entry.pack(side='left', fill='x', expand=True)
            self.input_entry.bind('<Return>', self.on_send)

        from ui.widgets.custom_button import create_button
        
        # Bouton capture d'écran
        screenshot_btn = create_button(text_input_frame, "Capture", self.on_screenshot, width=8, symbol="📷")
        screenshot_btn.pack(side='left', padx=(5, 0))
        
        # Bouton coloration syntaxique
        syntax_btn = create_button(text_input_frame, "Code", self.toggle_syntax, width=6, symbol="🎨")
        syntax_btn.pack(side='left', padx=(5, 0))
        
        # Bouton envoyer
        send_btn = create_button(text_input_frame, "Envoyer", self.on_send, width=8, symbol="✈️")
        send_btn.pack(side='left', padx=(5, 0))

    def on_send(self, event=None):
        user_input = self.input_var.get().strip()
        screenshot_path = self.screenshot_widget.get_screenshot_path()
        
        if user_input or screenshot_path:
            # Logger la commande pour les testeurs
            if user_input:
                self.exit_reporter.log_command(user_input)
            
            # Construire la commande avec image si nécessaire
            if screenshot_path and user_input:
                full_command = f"ext AIchat image {screenshot_path} {user_input}"
                display_input = f"> 📷 {user_input}"
            elif screenshot_path:
                full_command = f"ext AIchat image {screenshot_path} Que vois-tu sur cette image ?"
                display_input = "> 📷 Que vois-tu sur cette image ?"
            else:
                full_command = user_input
                display_input = f"> {user_input}"
            
            self.text_area.display_message(display_input)
            response = self.dispatcher.process(full_command)
            self.text_area.display_message(response)
            
            # Nettoyer
            self.input_var.set("")
            self.screenshot_widget.remove_thumbnail()
    
    def on_screenshot(self):
        """Gère la capture d'écran"""
        result = self.screenshot_widget.take_screenshot()
        if result.startswith("❌"):
            self.text_area.display_message(result)
    
    def on_screenshot_taken(self, screenshot_path):
        """Callback quand une capture est prise"""
        self.exit_reporter.log_feature_used("Screenshot")
    
    def toggle_syntax(self):
        """Active/désactive la coloration syntaxique"""
        result = self.text_area.toggle_syntax_highlighting()
        self.text_area.display_message(result)
        self.exit_reporter.log_feature_used("SyntaxHighlighting")
    
    def show_startup_message(self):
        # Forcer l'affichage du message au premier lancement
        self.root.after(100, self._delayed_startup_message)
    
    def _delayed_startup_message(self):
        app_logger.debug("Demande de message de démarrage", "UI")
        startup_msg = self.dispatcher.get_startup_message()
        app_logger.info(f"Message reçu: {startup_msg}", "UI")
        
        if startup_msg:
            app_logger.info("Affichage du message de démarrage", "UI")
            self.text_area.display_message(startup_msg)
            self.dispatcher.set_awaiting_installation()
        else:
            # Messages de suggestion par défaut
            self.text_area.display_message("🤖 CMD-AI Ultra Reboot - Prêt !")
            self.text_area.display_message("💡 Suggestions:")
            self.text_area.display_message("   • ext AIchat setup - Configurer l'IA")
            self.text_area.display_message("   • ext AIchat chat Bonjour - Parler à l'IA")
            self.text_area.display_message("   • help - Aide générale")
            app_logger.debug("Messages de suggestion affichés", "UI")
            
            # Vérifier les suggestions quotidiennes
            daily_suggestion = self.dispatcher.get_daily_suggestion()
            if daily_suggestion:
                self.text_area.display_message("")
                self.text_area.display_message(daily_suggestion)
            
            # Vérifier les mises à jour
            update_message = self.dispatcher.check_startup_update()
            if update_message:
                self.text_area.display_message("")
                self.text_area.display_message(update_message)

    def toggle_settings(self):
        if self.settings_visible:
            if self.settings_panel:
                self.settings_panel.hide()
            self.settings_visible = False
        else:
            # Panneau de paramètres simplifié
            from ui.simple_settings_panel import SimpleSettingsPanel
            self.settings_panel = SimpleSettingsPanel(self.root.winfo_children()[0])  # main_frame
            self.settings_panel.show()
            self.settings_visible = True
            # Ajouter bouton fermer
            from ui.widgets.custom_button import create_button
            close_frame = ttk.Frame(self.settings_panel.frame)
            close_frame.pack(fill='x', pady=5)
            create_button(close_frame, "Fermer", self.toggle_settings, width=6, symbol="❌").pack(side='right')

    def show_help(self):
        """Affiche le guide d'utilisation"""
        # Guide de base
        help_text = """📖 GUIDE D'UTILISATION CMD-AI Ultra Reboot

🚀 Démarrage rapide:
1. Configurez votre IA: ext AIchat setup
2. Commencez à chatter: ext AIchat chat Bonjour
3. Explorez le marketplace: 🔌 Marketplace > Extensions disponibles
4. Installez des extensions: plugin install [nom]

🔌 MARKETPLACE D'EXTENSIONS:
• 🔌 Marketplace > Extensions disponibles - Voir toutes les extensions
• 🔌 Marketplace > Extensions installées - Gérer vos extensions
• plugin install [id] - Installer une extension
• plugin remove [id] - Désinstaller une extension

💬 NOUVELLES FONCTIONNALITÉS:
• conv save [titre] - Sauvegarder conversations
• conv pdf [titre] - Exporter en PDF
• theme toggle - Changer de thème
• cache status - Mode hors-ligne
• system info - Informations système

⚙️ Configuration:
• Fichier > Paramètres pour configurer
• Choisir modèle IA (1-6)
• Ajouter clés API si nécessaire

📝 Commandes système:
• Tapez directement les commandes
• Élévation automatique si nécessaire
• Confirmation pour actions sensibles"""
        
        # Ajouter les guides des extensions installées
        installed_extensions = self.dispatcher.plugin_manager.installed_plugins.get('plugins', [])
        if installed_extensions:
            help_text += "\n\n🔌 EXTENSIONS INSTALLÉES:\n"
            for ext in installed_extensions:
                ext_id = ext['id']
                ext_name = ext['name']
                help_text += f"\n📦 {ext_name}:\n"
                help_text += f"   • ext {ext_name} help - Aide complète\n"
                
                # Ajouter des exemples spécifiques selon l'extension
                if ext_id == 'filemanager':
                    help_text += f"   • ext {ext_name} search \"*.pdf\" - Rechercher fichiers\n"
                    help_text += f"   • ext {ext_name} organize ~/Downloads - Organiser dossier\n"
                elif ext_id == 'networktools':
                    help_text += f"   • ext {ext_name} ping google.com - Tester connexion\n"
                    help_text += f"   • ext {ext_name} speed - Test de vitesse\n"
                elif ext_id == 'systemmonitor':
                    help_text += f"   • ext {ext_name} status - Statut système\n"
                    help_text += f"   • ext {ext_name} processes - Top processus\n"
                elif ext_id == 'texttools':
                    help_text += f"   • ext {ext_name} hash \"texte|sha256\" - Générer hash\n"
                    help_text += f"   • ext {ext_name} regex \"\\\\d+|texte avec nombres\" - Regex\n"
                elif ext_id == 'weather':
                    help_text += f"   • ext {ext_name} current Paris - Météo actuelle\n"
                    help_text += f"   • ext {ext_name} forecast - Prévisions\n"
        
        self.text_area.display_message(help_text)
    
    def show_commands(self):
        """Affiche la liste des commandes"""
        commands_text = """⌨️ COMMANDES DISPONIBLES

🔌 MARKETPLACE & EXTENSIONS:
• plugin list - Voir extensions disponibles
• plugin install [id] - Installer extension
• plugin remove [id] - Désinstaller extension
• plugin installed - Extensions installées
• ext [nom] [commande] - Utiliser extension

🤖 EXTENSIONS PRINCIPALES:
• ext AIchat setup - Configurer l'IA
• ext AIchat chat [message] - Parler à l'IA
• ext Screenshot take - Capture d'écran

💬 CONVERSATIONS:
• conv save [titre] - Sauvegarder conversation
• conv list - Lister conversations
• conv pdf [titre] - Exporter en PDF
• conv html [titre] - Exporter en HTML

🎨 INTERFACE:
• theme list - Lister thèmes
• theme set [nom] - Changer thème
• theme toggle - Basculer clair/sombre
• theme neon - Activer thème Néon
• theme neon - Activer thème Néon (coins coupés)

💾 CACHE & HORS-LIGNE:
• cache status - Statut connexion
• cache stats - Statistiques cache
• cache clear - Vider cache

⚙️ SYSTÈME:
• system info - Informations système
• system notify "titre" "message" - Notification
• update check - Vérifier mises à jour

💻 COMMANDES OS:
• ls / dir - Lister fichiers
• cd [dossier] - Changer répertoire
• whoami - Utilisateur actuel
• [commande] - Exécuter commande système

⚠️ Note: Commandes avec privilèges demandent confirmation"""
        
        self.text_area.display_message(commands_text)
    
    def show_about(self):
        """Affiche la fenêtre à propos"""
        from ui.about_dialog import AboutDialog
        AboutDialog(self.root)
    
    def on_quit(self):
        """Gère la fermeture de l'application"""
        # Générer le rapport de session pour les testeurs
        report_file = self.exit_reporter.generate_exit_report()
        if report_file:
            app_logger.info(f"Rapport de session testeur généré: {report_file}", "UI")
            
            # Proposer l'envoi du rapport
            from tkinter import messagebox
            result = messagebox.askyesno(
                "📄 Rapport de test généré",
                f"Votre rapport de session a été créé !\n\n📁 Fichier: {report_file.split('/')[-1]}\n\n📧 Voulez-vous envoyer ce rapport au développeur ?\n\n(Cela aide à améliorer l'application)"
            )
            
            if result:
                self._send_tester_report(report_file)
        
        # Fermer l'application
        self.root.quit()
        self.root.destroy()
    
    def _send_tester_report(self, report_file):
        """Envoie le rapport testeur"""
        try:
            from core.github_reporter import GitHubReporter
            from tkinter import messagebox
            import json
            
            # Lire le rapport
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # Envoyer via GitHubReporter
            github_reporter = GitHubReporter()
            success = github_reporter.send_simple_feedback(
                rating=8,  # Note par défaut
                comments=f"Rapport de session automatique - {report_data['session_duration_minutes']} minutes",
                features_tested=report_data['features_tested']
            )
            
            if success:
                messagebox.showinfo(
                    "✅ Rapport envoyé",
                    "Merci ! Votre rapport a été sauvegardé.\n\nLe développeur le récupérera pour améliorer l'application."
                )
            else:
                messagebox.showwarning(
                    "⚠️ Sauvegarde locale",
                    "Le rapport a été sauvegardé localement.\n\nVous pouvez le transmettre manuellement si nécessaire."
                )
                
        except Exception as e:
            app_logger.error(f"Erreur envoi rapport: {e}", "UI")
            from tkinter import messagebox
            messagebox.showerror(
                "❌ Erreur",
                f"Impossible d'envoyer le rapport.\n\nErreur: {e}\n\nLe rapport reste disponible localement."
            )
    
    def run(self):
        # Afficher le splash screen si disponible
        if SplashScreen:
            try:
                splash = SplashScreen(duration=3)
                
                def after_splash():
                    self.root.deiconify()
                    self.show_startup_message()
                
                self.root.withdraw()
                splash.show(callback=after_splash)
            except Exception as e:
                print(f"Erreur splash screen: {e}")
                self.show_startup_message()
        else:
            self.show_startup_message()
        
        # Configurer la fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.mainloop()

    def show_marketplace(self):
        """Affiche le marketplace avec tuiles cliquables"""
        self.marketplace_tiles.show_marketplace_tiles()

    def show_installed_extensions(self):
        """Affiche les extensions installées"""
        result = self.dispatcher.plugin_manager.get_installed_plugins()
        self.text_area.display_message(result)

    def refresh_marketplace(self):
        """Actualise le marketplace"""
        self.text_area.display_message("🔄 Marketplace actualisé !")
        self.show_marketplace()