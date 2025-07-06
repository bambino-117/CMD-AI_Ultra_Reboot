import sys
import tkinter.messagebox as messagebox
from core.error_reporter import ErrorReporter

class ExceptionHandler:
    def __init__(self, error_reporter=None):
        self.error_reporter = error_reporter or ErrorReporter()
        self.original_excepthook = sys.excepthook
        
    def install(self):
        """Installe le gestionnaire d'exceptions global"""
        sys.excepthook = self.handle_exception
    
    def uninstall(self):
        """Désinstalle le gestionnaire d'exceptions"""
        sys.excepthook = self.original_excepthook
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Gestionnaire d'exceptions personnalisé"""
        # Afficher l'erreur dans la console
        self.original_excepthook(exc_type, exc_value, exc_traceback)
        
        # Envoyer le rapport d'erreur
        if self.error_reporter:
            self.error_reporter.report_error(exc_value, f"Exception non gérée: {exc_type.__name__}")
        
        # Afficher une boîte de dialogue à l'utilisateur
        error_msg = f"Une erreur inattendue s'est produite:\n\n{exc_type.__name__}: {exc_value}\n\nUn rapport d'erreur a été envoyé automatiquement."
        
        try:
            messagebox.showerror("Erreur", error_msg)
        except:
            print(error_msg)