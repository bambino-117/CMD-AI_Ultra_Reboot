import requests
import json
import datetime
import platform
import sys
from core.logger import app_logger
from core.user_manager import UserManager

class GitHubReporter:
    def __init__(self, repo_owner="votre-username", repo_name="CMD-AI_Ultra_Reboot"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.user_manager = UserManager()
    
    def send_bug_report(self, error_type, error_message, traceback_str, description=""):
        """Envoie automatiquement un rapport de bug à GitHub"""
        try:
            from core.tester_auth import TesterAuth
            tester_auth = TesterAuth()
            current_pseudo = self.user_manager.get_username()
            
            # Préparer les données
            report_data = {
                "error_type": error_type,
                "description": description,
                "error_traceback": traceback_str,
                "logs": self._get_recent_logs(),
                "system": self._get_system_info(),
                "user_pseudo": tester_auth.get_anonymous_id(current_pseudo) if tester_auth.is_tester_code(current_pseudo) else current_pseudo,
                "is_tester": tester_auth.is_tester_code(current_pseudo),
                "user_level": self._detect_user_level(),
                "first_time": self._is_first_time(),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Envoyer via repository_dispatch
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/dispatches"
            
            payload = {
                "event_type": "tester-report",
                "client_payload": report_data
            }
            
            # Note: En production, utiliser un token GitHub
            # headers = {"Authorization": f"token {github_token}"}
            
            app_logger.info("Rapport de bug préparé pour envoi GitHub", "GITHUB_REPORTER")
            
            # Pour les testeurs novices, sauvegarder localement aussi
            self._save_local_backup(report_data)
            
            return True
            
        except Exception as e:
            app_logger.error(f"Erreur envoi rapport GitHub: {e}", "GITHUB_REPORTER")
            return False
    
    def send_simple_feedback(self, rating, comments, features_tested):
        """Envoie un feedback simple pour testeurs novices"""
        try:
            feedback_data = {
                "type": "feedback",
                "rating": rating,
                "comments": comments,
                "features_tested": features_tested,
                "user_pseudo": self.user_manager.get_username(),
                "system": self._get_system_info(),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Sauvegarder localement pour récupération manuelle
            self._save_feedback_backup(feedback_data)
            
            app_logger.info("Feedback sauvegardé localement", "GITHUB_REPORTER")
            return True
            
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde feedback: {e}", "GITHUB_REPORTER")
            return False
    
    def _get_system_info(self):
        """Collecte les informations système"""
        return {
            "os": f"{platform.system()} {platform.release()}",
            "python": sys.version,
            "app_version": "1.0.0",
            "arch": platform.machine()
        }
    
    def _get_recent_logs(self):
        """Récupère les logs récents"""
        try:
            with open("logs/app.log", "r", encoding="utf-8") as f:
                lines = f.readlines()
                return "".join(lines[-20:])  # 20 dernières lignes
        except:
            return "Logs non disponibles"
    
    def _detect_user_level(self):
        """Détecte le niveau technique de l'utilisateur"""
        # Heuristique simple basée sur l'usage
        settings = self.user_manager.settings
        
        if settings.get('api_keys'):
            return "Avancé"
        elif len(settings.get('command_history', [])) > 10:
            return "Intermédiaire"
        else:
            return "Débutant"
    
    def _is_first_time(self):
        """Détecte si c'est la première utilisation"""
        return not self.user_manager.settings.get('first_launch_done', False)
    
    def _save_local_backup(self, data):
        """Sauvegarde locale pour récupération manuelle"""
        import os
        os.makedirs("user/github_reports", exist_ok=True)
        
        filename = f"user/github_reports/bug_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_feedback_backup(self, data):
        """Sauvegarde feedback local"""
        import os
        os.makedirs("user/github_reports", exist_ok=True)
        
        filename = f"user/github_reports/feedback_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)