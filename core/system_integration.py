import os
import platform
import subprocess
import json
from datetime import datetime
from core.logger import app_logger

class SystemIntegration:
    def __init__(self):
        self.system = platform.system()
        self.settings_file = "user/system_settings.json"
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Charge les paramètres d'intégration"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement settings: {e}", "SYSTEM_INTEGRATION")
        
        return {
            "notifications_enabled": True,
            "startup_enabled": False,
            "context_menu_enabled": False,
            "tray_icon_enabled": False
        }
    
    def _save_settings(self):
        """Sauvegarde les paramètres"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde settings: {e}", "SYSTEM_INTEGRATION")
    
    def send_notification(self, title, message, icon="info"):
        """Envoie une notification système"""
        if not self.settings.get("notifications_enabled", True):
            return False
        
        try:
            if self.system == "Windows":
                return self._notify_windows(title, message, icon)
            elif self.system == "Darwin":  # macOS
                return self._notify_macos(title, message, icon)
            else:  # Linux
                return self._notify_linux(title, message, icon)
        except Exception as e:
            app_logger.error(f"Erreur notification: {e}", "SYSTEM_INTEGRATION")
            return False
    
    def _notify_windows(self, title, message, icon):
        """Notification Windows"""
        try:
            import win32gui
            import win32con
            
            # Utiliser win32api pour notification
            win32gui.MessageBox(0, message, title, win32con.MB_ICONINFORMATION)
            return True
        except ImportError:
            # Fallback PowerShell
            try:
                ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.ShowBalloonTip(5000, "{title}", "{message}", [System.Windows.Forms.ToolTipIcon]::Info)
Start-Sleep -Seconds 6
$notify.Dispose()
'''
                subprocess.run(["powershell", "-Command", ps_script], 
                             capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                return True
            except:
                return False
    
    def _notify_macos(self, title, message, icon):
        """Notification macOS"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], capture_output=True)
            return True
        except:
            return False
    
    def _notify_linux(self, title, message, icon):
        """Notification Linux"""
        try:
            # Essayer notify-send
            subprocess.run(["notify-send", title, message], capture_output=True)
            return True
        except:
            try:
                # Fallback zenity
                subprocess.run(["zenity", "--info", "--title", title, "--text", message], 
                             capture_output=True)
                return True
            except:
                return False
    
    def enable_startup(self):
        """Active le démarrage automatique"""
        try:
            if self.system == "Windows":
                return self._startup_windows()
            elif self.system == "Darwin":
                return self._startup_macos()
            else:
                return self._startup_linux()
        except Exception as e:
            app_logger.error(f"Erreur startup: {e}", "SYSTEM_INTEGRATION")
            return f"❌ Erreur: {e}"
    
    def _startup_windows(self):
        """Démarrage automatique Windows"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "CMD-AI_Ultra_Reboot"
            app_path = os.path.abspath("main.py")
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'python "{app_path}"')
            winreg.CloseKey(key)
            
            self.settings["startup_enabled"] = True
            self._save_settings()
            
            return "✅ Démarrage automatique activé (Windows)"
        except Exception as e:
            return f"❌ Erreur Windows startup: {e}"
    
    def _startup_macos(self):
        """Démarrage automatique macOS"""
        try:
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cmdai.ultrareboot</string>
    <key>ProgramArguments</key>
    <array>
        <string>python</string>
        <string>{os.path.abspath("main.py")}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
            
            plist_path = os.path.expanduser("~/Library/LaunchAgents/com.cmdai.ultrareboot.plist")
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            subprocess.run(["launchctl", "load", plist_path])
            
            self.settings["startup_enabled"] = True
            self._save_settings()
            
            return "✅ Démarrage automatique activé (macOS)"
        except Exception as e:
            return f"❌ Erreur macOS startup: {e}"
    
    def _startup_linux(self):
        """Démarrage automatique Linux"""
        try:
            desktop_content = f'''[Desktop Entry]
Type=Application
Name=CMD-AI Ultra Reboot
Exec=python {os.path.abspath("main.py")}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
'''
            
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            
            desktop_path = os.path.join(autostart_dir, "cmd-ai-ultra-reboot.desktop")
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            
            os.chmod(desktop_path, 0o755)
            
            self.settings["startup_enabled"] = True
            self._save_settings()
            
            return "✅ Démarrage automatique activé (Linux)"
        except Exception as e:
            return f"❌ Erreur Linux startup: {e}"
    
    def disable_startup(self):
        """Désactive le démarrage automatique"""
        try:
            if self.system == "Windows":
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, "CMD-AI_Ultra_Reboot")
                winreg.CloseKey(key)
            
            elif self.system == "Darwin":
                plist_path = os.path.expanduser("~/Library/LaunchAgents/com.cmdai.ultrareboot.plist")
                subprocess.run(["launchctl", "unload", plist_path])
                if os.path.exists(plist_path):
                    os.remove(plist_path)
            
            else:  # Linux
                desktop_path = os.path.expanduser("~/.config/autostart/cmd-ai-ultra-reboot.desktop")
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
            
            self.settings["startup_enabled"] = False
            self._save_settings()
            
            return "✅ Démarrage automatique désactivé"
            
        except Exception as e:
            return f"❌ Erreur désactivation: {e}"
    
    def add_context_menu(self):
        """Ajoute au menu contextuel"""
        try:
            if self.system == "Windows":
                return self._context_menu_windows()
            else:
                return "⚠️ Menu contextuel disponible uniquement sur Windows"
        except Exception as e:
            return f"❌ Erreur menu contextuel: {e}"
    
    def _context_menu_windows(self):
        """Menu contextuel Windows"""
        try:
            import winreg
            
            # Clé pour le menu contextuel des fichiers
            key_path = r"*\shell\CMD-AI_Ultra"
            app_path = os.path.abspath("main.py")
            
            # Créer la clé principale
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
            winreg.SetValue(key, "", winreg.REG_SZ, "Analyser avec CMD-AI")
            winreg.CloseKey(key)
            
            # Créer la commande
            cmd_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path + r"\command")
            winreg.SetValue(cmd_key, "", winreg.REG_SZ, f'python "{app_path}" --file "%1"')
            winreg.CloseKey(cmd_key)
            
            self.settings["context_menu_enabled"] = True
            self._save_settings()
            
            return "✅ Menu contextuel ajouté (Windows)"
        except Exception as e:
            return f"❌ Erreur menu contextuel: {e}"
    
    def get_system_info(self):
        """Récupère les informations système"""
        try:
            import psutil
            
            # Informations de base
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
            }
            
            # Informations système
            info.update({
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_total": round(psutil.virtual_memory().total / (1024**3), 2),
                "memory_available": round(psutil.virtual_memory().available / (1024**3), 2),
                "disk_usage": round(psutil.disk_usage('/').percent, 1) if self.system != "Windows" else round(psutil.disk_usage('C:').percent, 1)
            })
            
            return info
        except Exception as e:
            app_logger.error(f"Erreur system info: {e}", "SYSTEM_INTEGRATION")
            return {"error": str(e)}
    
    def get_integration_status(self):
        """Statut des intégrations système"""
        return f"""⚙️ INTÉGRATION SYSTÈME

🖥️ Système: {self.system} {platform.release()}
📱 Notifications: {"✅ Activées" if self.settings.get("notifications_enabled") else "❌ Désactivées"}
🚀 Démarrage auto: {"✅ Activé" if self.settings.get("startup_enabled") else "❌ Désactivé"}
📋 Menu contextuel: {"✅ Activé" if self.settings.get("context_menu_enabled") else "❌ Désactivé"}

💡 Commandes:
• system notify "Titre" "Message" - Tester notification
• system startup enable/disable - Démarrage automatique
• system context enable - Menu contextuel (Windows)
• system info - Informations détaillées"""