import traceback
import sys
import platform
import requests
import json
from datetime import datetime

class ErrorReporter:
    def __init__(self, github_repo="votre-username/CMD-AI_Ultra_Reboot", github_token=None):
        self.github_repo = github_repo
        self.github_token = github_token
        self.enabled = True
    
    def report_error(self, error, context=""):
        """Envoie automatiquement un rapport d'erreur sur GitHub"""
        if not self.enabled:
            return
        
        try:
            error_info = self._collect_error_info(error, context)
            self._send_to_github(error_info)
        except Exception as e:
            print(f"Erreur lors de l'envoi du rapport: {e}")
    
    def _collect_error_info(self, error, context):
        """Collecte les informations sur l'erreur"""
        return {
            "title": f"Erreur automatique: {type(error).__name__}",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "platform": platform.platform(),
                "python_version": sys.version,
                "os": platform.system()
            }
        }
    
    def _send_to_github(self, error_info):
        """Envoie le rapport d'erreur comme issue GitHub"""
        if not self.github_token:
            print("Token GitHub manquant pour le rapport d'erreur")
            return
        
        url = f"https://api.github.com/repos/{self.github_repo}/issues"
        
        body = f"""## Rapport d'erreur automatique

**Type d'erreur:** {error_info['error_type']}
**Message:** {error_info['error_message']}
**Contexte:** {error_info['context']}
**Timestamp:** {error_info['timestamp']}

### Informations système
- **Plateforme:** {error_info['system_info']['platform']}
- **Python:** {error_info['system_info']['python_version']}
- **OS:** {error_info['system_info']['os']}

### Traceback
```python
{error_info['traceback']}
```

*Rapport généré automatiquement par CMD-AI Ultra Reboot*
"""
        
        data = {
            "title": error_info['title'],
            "body": body,
            "labels": ["bug", "auto-report"]
        }
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            issue_url = response.json()['html_url']
            print(f"Rapport d'erreur envoyé: {issue_url}")
        else:
            print(f"Échec de l'envoi du rapport: {response.status_code}")
    
    def enable(self):
        """Active les rapports d'erreur"""
        self.enabled = True
    
    def disable(self):
        """Désactive les rapports d'erreur"""
        self.enabled = False