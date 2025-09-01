import os
from datetime import datetime
from core.system_detector import SystemDetector
from core.user_manager import UserManager

class SystemReport:
    def __init__(self):
        self.system_detector = SystemDetector()
        self.user_manager = UserManager()
    
    def generate_report(self):
        """Génère un rapport système en markdown"""
        info = self.system_detector.detect_system_info()
        username = self.user_manager.get_username()
        
        report = f"""# Rapport Système - {username}

**Pseudo utilisateur:** {username}  
**Date de génération:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

## Détection Matérielle

- **Système:** {info.get('system', 'Inconnu')} {info.get('release', '')}
- **Version OS:** {info.get('version', 'Inconnue')}
- **Architecture:** {info.get('machine', 'Inconnue')}
- **Processeur:** {info.get('processor', 'Inconnu')}
- **Cœurs CPU:** {info.get('cpu_count', 'Inconnu')}
- **Mémoire RAM:** {info.get('memory_gb', 'Inconnue')} GB
- **Python:** {info.get('python_version', 'Inconnue')}

## Configuration {username}

- **Modèle IA actuel:** {self._get_current_model()}
- **Extensions installées:** AIchat
- **Historique conversations:** Activé

---
*Rapport personnalisé pour {username} - CMD-AI Ultra*
"""
        return report
    
    def save_report(self):
        """Sauvegarde le rapport dans user/"""
        report = self.generate_report()
        report_path = "user/rapport_systeme.md"
        
        os.makedirs("user", exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_path
    
    def _get_current_model(self):
        try:
            from language_models.llm_manager import LLMManager
            llm = LLMManager()
            current = llm.get_current_model_info()
            return current['name'] if current else 'Non configuré'
        except:
            return 'Non configuré'