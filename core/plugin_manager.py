import json
import os
import requests
import zipfile
import tempfile
import shutil
from datetime import datetime
from core.logger import app_logger

class PluginManager:
    def __init__(self):
        self.plugins_dir = "extensions"
        self.marketplace_url = "https://raw.githubusercontent.com/bambino-117/CMD-AI_Extensions/main/marketplace.json"
        self.installed_plugins_file = "user/installed_plugins.json"
        self.installed_plugins = self._load_installed_plugins()
    
    def _load_installed_plugins(self):
        """Charge la liste des plugins installés"""
        try:
            if os.path.exists(self.installed_plugins_file):
                with open(self.installed_plugins_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement plugins: {e}", "PLUGIN_MANAGER")
        
        return {
            "plugins": [],
            "last_update": None
        }
    
    def _save_installed_plugins(self):
        """Sauvegarde la liste des plugins installés"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.installed_plugins_file, 'w', encoding='utf-8') as f:
                json.dump(self.installed_plugins, f, indent=2, ensure_ascii=False)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde plugins: {e}", "PLUGIN_MANAGER")
    
    def get_marketplace(self):
        """Récupère la liste des plugins disponibles"""
        try:
            response = requests.get(self.marketplace_url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            app_logger.error(f"Erreur marketplace: {e}", "PLUGIN_MANAGER")
        
        # Fallback local
        return self._get_default_marketplace()
    
    def _get_default_marketplace(self):
        """Marketplace par défaut si pas de connexion"""
        return {
            "plugins": [
                {
                    "id": "weather",
                    "name": "Weather",
                    "version": "1.0.0",
                    "description": "Extension météo avec géolocalisation",
                    "author": "CMD-AI Team",
                    "category": "Utility",
                    "download_url": "local://weather_extension.py",
                    "size": "15KB",
                    "rating": 4.8,
                    "downloads": 1250,
                    "tags": ["météo", "géolocalisation", "api"]
                },
                {
                    "id": "filemanager",
                    "name": "FileManager",
                    "version": "1.0.0",
                    "description": "Gestionnaire de fichiers avancé avec recherche et organisation",
                    "author": "CMD-AI Team",
                    "category": "Utility",
                    "download_url": "local://file_manager_extension.py",
                    "size": "25KB",
                    "rating": 4.9,
                    "downloads": 1850,
                    "tags": ["fichiers", "organisation", "recherche", "doublons"]
                },
                {
                    "id": "networktools",
                    "name": "NetworkTools",
                    "version": "1.2.0",
                    "description": "Outils réseau: ping, scan ports, vitesse, géolocalisation IP",
                    "author": "CMD-AI Team",
                    "category": "Network",
                    "download_url": "local://network_tools_extension.py",
                    "size": "30KB",
                    "rating": 4.7,
                    "downloads": 2100,
                    "tags": ["réseau", "ping", "scan", "vitesse", "ip"]
                },
                {
                    "id": "systemmonitor",
                    "name": "SystemMonitor",
                    "version": "1.1.0",
                    "description": "Monitoring système: CPU, RAM, disque, processus, température",
                    "author": "CMD-AI Team",
                    "category": "System",
                    "download_url": "local://system_monitor_extension.py",
                    "size": "28KB",
                    "rating": 4.8,
                    "downloads": 1650,
                    "tags": ["monitoring", "cpu", "ram", "processus", "température"]
                },
                {
                    "id": "texttools",
                    "name": "TextTools",
                    "version": "1.0.0",
                    "description": "Outils de traitement de texte: regex, hash, encode, format",
                    "author": "CMD-AI Team",
                    "category": "Text",
                    "download_url": "local://text_tools_extension.py",
                    "size": "22KB",
                    "rating": 4.6,
                    "downloads": 1200,
                    "tags": ["texte", "regex", "hash", "encodage", "formatage"]
                },
                {
                    "id": "translator",
                    "name": "Translator",
                    "version": "1.2.0",
                    "description": "Traduction multilingue avec Google Translate",
                    "author": "CMD-AI Team",
                    "category": "Language",
                    "download_url": "https://github.com/bambino-117/CMD-AI_Extensions/releases/download/translator-v1.2.0/translator.zip",
                    "size": "22KB",
                    "rating": 4.9,
                    "downloads": 2100,
                    "tags": ["traduction", "langues", "google"]
                },
                {
                    "id": "usbmanager",
                    "name": "USBManager",
                    "version": "2.0.0",
                    "description": "💾 Toolkit USB complet: bootable, formatage, firmware, identification",
                    "author": "CMD-AI Team",
                    "category": "System",
                    "download_url": "local://usb_manager_extension.py",
                    "size": "25KB",
                    "rating": 4.8,
                    "downloads": 1200,
                    "tags": ["usb", "bootable", "firmware", "formatage", "toolkit"]
                },
                {
                    "id": "securitytoolkit",
                    "name": "SecurityToolkit",
                    "version": "1.0.0",
                    "description": "🛡️ Boîte à outils de sécurité - KillRAM, BadUSB, USBKiller",
                    "author": "CMD-AI Team",
                    "category": "Security",
                    "download_url": "local://security_toolkit_extension.py",
                    "size": "22KB",
                    "rating": 4.5,
                    "downloads": 850,
                    "tags": ["🛡️ toolkit", "killram", "badusb", "usbkiller", "pentest"]
                },
                {
                    "id": "osint",
                    "name": "OSINT",
                    "version": "1.0.0",
                    "description": "🔍 Outils OSINT - Recherche et analyse de données publiques",
                    "author": "CMD-AI Team",
                    "category": "Security",
                    "download_url": "local://osint_extension.py",
                    "size": "28KB",
                    "rating": 4.6,
                    "downloads": 1150,
                    "tags": ["🔍 osint", "recherche", "investigation", "données publiques", "sécurité"]
                },
                {
                    "id": "calculator",
                    "name": "Calculator",
                    "version": "1.1.0",
                    "description": "Calculatrice avancée avec graphiques",
                    "author": "Community",
                    "category": "Math",
                    "download_url": "https://github.com/bambino-117/CMD-AI_Extensions/releases/download/calculator-v1.1.0/calculator.zip",
                    "size": "35KB",
                    "rating": 4.6,
                    "downloads": 890,
                    "tags": ["calcul", "mathématiques", "graphiques"]
                }
            ]
        }
    
    def list_available_plugins(self):
        """Liste les plugins disponibles"""
        marketplace = self.get_marketplace()
        result = "🔌 MARKETPLACE - Extensions disponibles\n\n"
        
        for plugin in marketplace.get("plugins", []):
            installed = self._is_plugin_installed(plugin["id"])
            status = "✅ Installé" if installed else "📥 Disponible"
            
            result += f"📦 {plugin['name']} v{plugin['version']} - {status}\n"
            result += f"   📝 {plugin['description']}\n"
            result += f"   👤 {plugin['author']} | 📂 {plugin['category']} | ⭐ {plugin['rating']}\n"
            result += f"   📊 {plugin['downloads']} téléchargements | 💾 {plugin['size']}\n"
            
            if not installed:
                result += f"   💡 Installation: plugin install {plugin['id']}\n"
            else:
                result += f"   🗑️ Désinstaller: plugin remove {plugin['id']}\n"
            result += "\n"
        
        return result
    
    def install_plugin(self, plugin_id):
        """Installe un plugin"""
        try:
            marketplace = self.get_marketplace()
            plugin_info = None
            
            for plugin in marketplace.get("plugins", []):
                if plugin["id"] == plugin_id:
                    plugin_info = plugin
                    break
            
            if not plugin_info:
                return f"❌ Plugin '{plugin_id}' non trouvé dans le marketplace"
            
            if self._is_plugin_installed(plugin_id):
                return f"⚠️ Plugin '{plugin_id}' déjà installé"
            
            download_url = plugin_info["download_url"]
            
            # Vérifier si c'est une extension locale
            if download_url.startswith("local://"):
                # Extension locale déjà présente
                extension_file = download_url.replace("local://", "")
                extension_path = os.path.join(self.plugins_dir, extension_file)
                
                if os.path.exists(extension_path):
                    # Marquer comme installé
                    self.installed_plugins["plugins"].append({
                        "id": plugin_id,
                        "name": plugin_info["name"],
                        "version": plugin_info["version"],
                        "installed_at": datetime.now().isoformat()
                    })
                    self._save_installed_plugins()
                    
                    return f"✅ Extension '{plugin_info['name']}' activée !\n💡 Redémarrez l'application pour l'utiliser"
                else:
                    return f"❌ Fichier d'extension manquant: {extension_file}"
            else:
                # Télécharger le plugin distant
                temp_file = self._download_plugin(download_url)
                
                if not temp_file:
                    return f"❌ Échec téléchargement de '{plugin_id}'"
                
                # Extraire et installer
                if self._extract_plugin(temp_file, plugin_id):
                    # Marquer comme installé
                    self.installed_plugins["plugins"].append({
                        "id": plugin_id,
                        "name": plugin_info["name"],
                        "version": plugin_info["version"],
                        "installed_at": datetime.now().isoformat()
                    })
                    self._save_installed_plugins()
                    
                    return f"✅ Plugin '{plugin_info['name']}' installé avec succès !\n💡 Redémarrez l'application pour l'activer"
                else:
                    return f"❌ Erreur installation de '{plugin_id}'"
                
        except Exception as e:
            app_logger.error(f"Erreur installation plugin {plugin_id}: {e}", "PLUGIN_MANAGER")
            return f"❌ Erreur: {e}"
    
    def remove_plugin(self, plugin_id):
        """Désinstalle un plugin"""
        try:
            if not self._is_plugin_installed(plugin_id):
                return f"⚠️ Plugin '{plugin_id}' non installé"
            
            # Supprimer le fichier
            plugin_file = os.path.join(self.plugins_dir, f"{plugin_id}_extension.py")
            if os.path.exists(plugin_file):
                os.remove(plugin_file)
            
            # Retirer de la liste
            self.installed_plugins["plugins"] = [
                p for p in self.installed_plugins["plugins"] 
                if p["id"] != plugin_id
            ]
            self._save_installed_plugins()
            
            return f"✅ Plugin '{plugin_id}' désinstallé\n💡 Redémarrez l'application pour appliquer"
            
        except Exception as e:
            app_logger.error(f"Erreur désinstallation plugin {plugin_id}: {e}", "PLUGIN_MANAGER")
            return f"❌ Erreur: {e}"
    
    def _is_plugin_installed(self, plugin_id):
        """Vérifie si un plugin est installé"""
        return any(p["id"] == plugin_id for p in self.installed_plugins["plugins"])
    
    def _download_plugin(self, download_url):
        """Télécharge un plugin"""
        try:
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            temp_file.write(response.content)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            app_logger.error(f"Erreur téléchargement: {e}", "PLUGIN_MANAGER")
            return None
    
    def _extract_plugin(self, zip_file, plugin_id):
        """Extrait et installe un plugin"""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Extraire dans un dossier temporaire
                temp_dir = tempfile.mkdtemp()
                zip_ref.extractall(temp_dir)
                
                # Chercher le fichier principal du plugin
                main_file = None
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('_extension.py'):
                            main_file = os.path.join(root, file)
                            break
                    if main_file:
                        break
                
                if main_file:
                    # Copier vers le dossier extensions
                    target_file = os.path.join(self.plugins_dir, f"{plugin_id}_extension.py")
                    shutil.copy2(main_file, target_file)
                    
                    # Nettoyer
                    shutil.rmtree(temp_dir)
                    os.unlink(zip_file)
                    
                    return True
                else:
                    shutil.rmtree(temp_dir)
                    return False
                    
        except Exception as e:
            app_logger.error(f"Erreur extraction: {e}", "PLUGIN_MANAGER")
            return False
    
    def get_installed_plugins(self):
        """Liste les plugins installés"""
        if not self.installed_plugins["plugins"]:
            return "📦 Aucun plugin installé\n💡 Utilisez 'plugin list' pour voir les plugins disponibles"
        
        result = "🔌 PLUGINS INSTALLÉS\n\n"
        for plugin in self.installed_plugins["plugins"]:
            result += f"✅ {plugin['name']} v{plugin['version']}\n"
            result += f"   📅 Installé le: {plugin['installed_at'][:10]}\n"
            result += f"   🗑️ Désinstaller: plugin remove {plugin['id']}\n\n"
        
        return result