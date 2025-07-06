import json
import datetime
import os
from core.logger import app_logger
from core.tester_auth import TesterAuth
from core.user_manager import UserManager

class ExitReporter:
    def __init__(self):
        self.tester_auth = TesterAuth()
        self.user_manager = UserManager()
        self.session_data = {
            "start_time": datetime.datetime.now(),
            "commands_used": [],
            "errors_encountered": [],
            "features_tested": []
        }
    
    def log_command(self, command):
        """Enregistre une commande utilisée"""
        self.session_data["commands_used"].append({
            "command": command,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def log_error(self, error_type, error_msg):
        """Enregistre une erreur rencontrée"""
        self.session_data["errors_encountered"].append({
            "type": error_type,
            "message": error_msg,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def log_feature_used(self, feature):
        """Enregistre une fonctionnalité utilisée"""
        if feature not in self.session_data["features_tested"]:
            self.session_data["features_tested"].append(feature)
    
    def generate_exit_report(self):
        """Génère le rapport de fin de session pour les testeurs"""
        current_pseudo = self.user_manager.get_username()
        
        if not self.tester_auth.is_tester_code(current_pseudo):
            return False  # Pas un testeur, pas de rapport
        
        try:
            # Calculer la durée de session
            session_duration = datetime.datetime.now() - self.session_data["start_time"]
            
            report = {
                "tester_id": current_pseudo,
                "session_start": self.session_data["start_time"].isoformat(),
                "session_end": datetime.datetime.now().isoformat(),
                "session_duration_minutes": int(session_duration.total_seconds() / 60),
                "commands_used": self.session_data["commands_used"],
                "errors_encountered": self.session_data["errors_encountered"],
                "features_tested": self.session_data["features_tested"],
                "total_commands": len(self.session_data["commands_used"]),
                "total_errors": len(self.session_data["errors_encountered"]),
                "app_version": "1.0.0"
            }
            
            # Sauvegarder le rapport
            os.makedirs("user/session_reports", exist_ok=True)
            filename = f"user/session_reports/session_{current_pseudo}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            app_logger.info(f"Rapport de session généré: {filename}", "EXIT_REPORTER")
            return filename
            
        except Exception as e:
            app_logger.error(f"Erreur génération rapport de session: {e}", "EXIT_REPORTER")
            return False