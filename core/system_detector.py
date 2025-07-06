import platform
import psutil
import json
import os
from core.logger import app_logger

class SystemDetector:
    def __init__(self, settings_path='user/settings.json'):
        self.settings_path = settings_path
    
    def detect_system_info(self):
        try:
            info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(),
                'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'python_version': platform.python_version()
            }
            app_logger.info("Détection système terminée", "SYSTEM_DETECTOR")
            return info
        except Exception as e:
            app_logger.error(f"Erreur détection système: {e}", "SYSTEM_DETECTOR")
            return {}
    
    def save_system_info(self):
        try:
            # Charger settings existants
            settings = {}
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            # Ajouter infos système
            settings['system_info'] = self.detect_system_info()
            settings['system_detected'] = True
            
            # Sauvegarder
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            app_logger.info("Infos système sauvegardées", "SYSTEM_DETECTOR")
            return True
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde système: {e}", "SYSTEM_DETECTOR")
            return False
    
    def is_system_detected(self):
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                return settings.get('system_detected', False)
            return False
        except:
            return False