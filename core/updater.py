import requests
import json
import os
import subprocess
import tempfile
from datetime import datetime
from core.logger import app_logger

class AppUpdater:
    def __init__(self):
        self.current_version = "1.1.0"
        self.github_api = "https://api.github.com/repos/bambino-117/CMD-AI_Ultra_Reboot"
        self.update_check_file = "user/last_update_check.json"
        
    def check_for_updates(self, force=False):
        """Vérifie les mises à jour disponibles"""
        try:
            # Vérifier si on doit checker (max 1x par jour)
            if not force and not self._should_check_update():
                return None
            
            # Appel API GitHub
            response = requests.get(f"{self.github_api}/releases/latest", timeout=10)
            if response.status_code != 200:
                return None
            
            release_data = response.json()
            latest_version = release_data["tag_name"].replace("v", "")
            
            # Sauvegarder la dernière vérification
            self._save_update_check()
            
            if self._is_newer_version(latest_version):
                return {
                    "version": latest_version,
                    "current": self.current_version,
                    "release_notes": release_data.get("body", ""),
                    "download_url": self._get_download_url(release_data),
                    "published_at": release_data.get("published_at", "")
                }
            
            return None
            
        except Exception as e:
            app_logger.error(f"Erreur vérification mise à jour: {e}", "UPDATER")
            return None
    
    def _should_check_update(self):
        """Vérifie si on doit checker les mises à jour"""
        try:
            if not os.path.exists(self.update_check_file):
                return True
            
            with open(self.update_check_file, 'r') as f:
                data = json.load(f)
            
            last_check = datetime.fromisoformat(data.get("last_check", "2000-01-01"))
            return (datetime.now() - last_check).days >= 1
            
        except:
            return True
    
    def _save_update_check(self):
        """Sauvegarde la date de dernière vérification"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.update_check_file, 'w') as f:
                json.dump({"last_check": datetime.now().isoformat()}, f)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde update check: {e}", "UPDATER")
    
    def _is_newer_version(self, latest_version):
        """Compare les versions"""
        try:
            current_parts = [int(x) for x in self.current_version.split('.')]
            latest_parts = [int(x) for x in latest_version.split('.')]
            
            # Égaliser les longueurs
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)
            
            return latest_parts > current_parts
        except:
            return False
    
    def _get_download_url(self, release_data):
        """Récupère l'URL de téléchargement selon l'OS"""
        import platform
        system = platform.system()
        
        assets = release_data.get("assets", [])
        
        for asset in assets:
            name = asset["name"].lower()
            if system == "Windows" and ".exe" in name:
                return asset["browser_download_url"]
            elif system == "Darwin" and (".dmg" in name or ".app" in name):
                return asset["browser_download_url"]
            elif system == "Linux" and (".tar.gz" in name or "linux" in name):
                return asset["browser_download_url"]
        
        return release_data.get("html_url")  # Fallback vers page GitHub
    
    def download_update(self, download_url, progress_callback=None):
        """Télécharge la mise à jour"""
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Nom du fichier
            filename = download_url.split('/')[-1]
            if not filename or '.' not in filename:
                filename = "update.exe" if os.name == 'nt' else "update.tar.gz"
            
            # Téléchargement
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            return file_path
            
        except Exception as e:
            app_logger.error(f"Erreur téléchargement: {e}", "UPDATER")
            return None
    
    def install_update(self, file_path):
        """Lance l'installation de la mise à jour"""
        try:
            import platform
            system = platform.system()
            
            if system == "Windows":
                # Lancer l'exécutable
                subprocess.Popen([file_path])
                return True
            elif system == "Darwin":
                # Ouvrir le DMG
                subprocess.Popen(["open", file_path])
                return True
            else:
                # Linux - ouvrir le dossier
                subprocess.Popen(["xdg-open", os.path.dirname(file_path)])
                return True
                
        except Exception as e:
            app_logger.error(f"Erreur installation: {e}", "UPDATER")
            return False
    
    def get_update_message(self, update_info):
        """Génère le message de mise à jour"""
        return f"""🔄 MISE À JOUR DISPONIBLE !

📦 Version actuelle : v{update_info['current']}
🆕 Nouvelle version : v{update_info['version']}

📋 Nouveautés :
{update_info['release_notes'][:200]}...

💡 Voulez-vous télécharger la mise à jour ?
• Tapez: update download (pour télécharger)
• Tapez: update later (pour reporter)
• Tapez: update never (pour désactiver)"""