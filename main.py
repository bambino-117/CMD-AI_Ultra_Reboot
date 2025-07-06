from core.safe_loader import SafeLoader
from core.fallback_components import FallbackDispatcher, FallbackTextArea, FallbackSettings
from core.logger import app_logger
from core.user_manager import UserManager
from core.system_detector import SystemDetector

# Patch de compatibilité 32-bit
try:
    import compatibility_patch
except ImportError:
    pass

# Moniteur d'erreurs
try:
    from core.error_monitor import ErrorMonitor
    error_monitor = ErrorMonitor()
except ImportError:
    error_monitor = None

# Initialisation du chargeur sécurisé
safe_loader = SafeLoader()

# Imports sécurisés
AppUI = None
Dispatcher = None
AppConfig = None
ExceptionHandler = None
ErrorReporter = None

try:
    from ui.interface import AppUI
    from core.dispatcher import Dispatcher
    from core.config import AppConfig
    from core.exception_handler import ExceptionHandler
    from core.error_reporter import ErrorReporter
    app_logger.info("Tous les imports réussis - Mode normal", "MAIN")
except Exception as e:
    app_logger.error(f"Erreur d'import critique: {e}", "MAIN")
    safe_loader.enable_fallback_mode()

def main():
    app_logger.info("Démarrage de CMD-AI Ultra Reboot", "MAIN")
    
    # Vérifier si c'est le premier lancement
    user_manager = UserManager()
    system_detector = SystemDetector()
    
    if not user_manager.has_username() or not system_detector.is_system_detected():
        app_logger.info("Premier lancement détecté - Configuration initiale", "MAIN")
        # Configuration automatique avec valeurs par défaut
        if not user_manager.has_username():
            user_manager.set_username("Utilisateur")
        if not system_detector.is_system_detected():
            system_detector.save_system_info()
    
    try:
        # Configuration du système de rapport d'erreurs si disponible
        if ErrorReporter and ExceptionHandler:
            app_logger.debug("Configuration du système de rapport d'erreurs", "MAIN")
            error_reporter = ErrorReporter(
                github_repo="votre-username/CMD-AI_Ultra_Reboot",
                github_token=None
            )
            exception_handler = ExceptionHandler(error_reporter)
            exception_handler.install()
            app_logger.info("Système de rapport d'erreurs configuré", "MAIN")
        else:
            app_logger.warning("Système de rapport d'erreurs non disponible", "MAIN")
        
        # Création des instances principales si disponibles
        if AppConfig and Dispatcher and AppUI:
            app_logger.debug("Création des instances principales", "MAIN")
            config = AppConfig('user/settings.json')
            app_logger.debug("Configuration chargée", "MAIN")
            
            dispatcher = Dispatcher(config)
            app_logger.debug("Dispatcher créé", "MAIN")
            
            app_ui = AppUI(dispatcher)
            app_logger.info("Interface utilisateur créée", "MAIN")
            
            app_logger.info("Lancement de l'interface", "MAIN")
            app_ui.run()
        else:
            app_logger.error("Classes principales non disponibles", "MAIN")
            raise Exception("Imports critiques échoués")
        
    except Exception as e:
        app_logger.critical(f"Erreur critique: {e}", "MAIN")
        app_logger.warning("Démarrage en mode dégradé", "MAIN")
        run_fallback_mode()

def run_fallback_mode():
    """Lance l'application en mode dégradé"""
    import tkinter as tk
    from tkinter import ttk
    
    root = tk.Tk()
    root.title("CMD-AI Ultra Reboot - Mode Dégradé")
    root.geometry("500x300")
    
    # Interface minimale
    label = tk.Label(root, text="Application en mode dégradé", font=('Arial', 14, 'bold'))
    label.pack(pady=20)
    
    text_area = FallbackTextArea(root)
    text_area.display_message("Mode dégradé activé - Fonctionnalités limitées")
    text_area.display_message("Modules échoués: " + str(safe_loader.get_failed_modules()))
    
    # Champ de saisie basique
    input_frame = ttk.Frame(root)
    input_frame.pack(fill='x', padx=10, pady=10)
    
    input_var = tk.StringVar()
    input_entry = ttk.Entry(input_frame, textvariable=input_var)
    input_entry.pack(side='left', fill='x', expand=True)
    
    def on_send():
        user_input = input_var.get().strip()
        if user_input:
            text_area.display_message(f"> {user_input}")
            text_area.display_message(f"Echo: {user_input}")
            input_var.set("")
    
    send_btn = ttk.Button(input_frame, text="Envoyer", command=on_send)
    send_btn.pack(side='left', padx=(5, 0))
    
    input_entry.bind('<Return>', lambda e: on_send())
    
    root.mainloop()

if __name__ == "__main__":
    main()