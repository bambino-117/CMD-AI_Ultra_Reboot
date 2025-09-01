import sys
import traceback
import datetime
import os
from core.logger import app_logger

class ErrorMonitor:
    def __init__(self):
        self.error_log_path = "user/error_reports.txt"
        self.install_handler()
    
    def install_handler(self):
        """Installe le gestionnaire d'erreurs global"""
        sys.excepthook = self.handle_exception
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Gère les exceptions non capturées"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Créer le rapport d'erreur
        error_report = self.create_error_report(exc_type, exc_value, exc_traceback)
        
        # Sauvegarder dans le fichier
        self.save_error_report(error_report)
        
        # Logger l'erreur
        app_logger.critical(f"Erreur non gérée: {exc_type.__name__}: {exc_value}", "ERROR_MONITOR")
        
        # Afficher l'erreur originale
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    def create_error_report(self, exc_type, exc_value, exc_traceback):
        """Crée un rapport d'erreur détaillé"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
=== RAPPORT D'ERREUR CMD-AI Ultra ===
Date: {timestamp}
Type: {exc_type.__name__}
Message: {exc_value}

=== TRACEBACK ===
{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}

=== INFORMATIONS SYSTÈME ===
Python: {sys.version}
Plateforme: {sys.platform}

=== FIN RAPPORT ===
"""
        return report
    
    def save_error_report(self, report):
        """Sauvegarde le rapport d'erreur"""
        try:
            os.makedirs("user", exist_ok=True)
            
            with open(self.error_log_path, "a", encoding="utf-8") as f:
                f.write(report)
                f.write("\n" + "="*50 + "\n")
            
            app_logger.info(f"Rapport d'erreur sauvegardé: {self.error_log_path}", "ERROR_MONITOR")
            
        except Exception as e:
            app_logger.error(f"Impossible de sauvegarder le rapport: {e}", "ERROR_MONITOR")
    
    def log_custom_error(self, error_msg, context="CUSTOM"):
        """Log une erreur personnalisée"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
=== ERREUR PERSONNALISÉE ===
Date: {timestamp}
Contexte: {context}
Message: {error_msg}
=== FIN ===
"""
        self.save_error_report(report)