from core.base_extension import BaseExtension
import os
import platform
import subprocess
import tempfile
from datetime import datetime

class ScreenshotExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "Screenshot"
        self.version = "1.0.0"
        self.description = "Capture d'écran pour IA"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "capture":
            return self.capture_screen(args)
        elif command == "select":
            return self.capture_selection(args)
        elif command == "help":
            return self.show_help(args)
        else:
            return "Commandes: capture, select, help"
    
    def get_commands(self):
        return ["capture", "select", "help"]
    
    def capture_screen(self, args=""):
        """Capture plein écran"""
        try:
            screenshot_path = self._take_screenshot(fullscreen=True)
            if screenshot_path:
                return f"📸 Capture d'écran sauvegardée: {screenshot_path}\n💡 Utilisez: ext AIchat image {screenshot_path} [votre question]"
            else:
                return "❌ Erreur lors de la capture d'écran"
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def capture_selection(self, args=""):
        """Capture sélective"""
        try:
            screenshot_path = self._take_screenshot(fullscreen=False)
            if screenshot_path:
                return f"📸 Capture sélective sauvegardée: {screenshot_path}\n💡 Utilisez: ext AIchat image {screenshot_path} [votre question]"
            else:
                return "❌ Erreur lors de la capture sélective"
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def show_help(self, args=""):
        """Affiche l'aide"""
        return """📸 EXTENSION SCREENSHOT
        
🖥️ Commandes disponibles:
• ext Screenshot capture - Capture plein écran
• ext Screenshot select - Capture sélective
• ext Screenshot help - Cette aide

💡 Utilisation avec IA:
1. Faites une capture: ext Screenshot capture
2. Envoyez à l'IA: ext AIchat image chemin/image.png Que vois-tu ?

📁 Les captures sont sauvées dans: user/screenshots/"""
    
    def _take_screenshot(self, fullscreen=True):
        """Prend une capture d'écran selon l'OS"""
        # Créer le dossier screenshots
        screenshots_dir = "user/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Nom du fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        system = platform.system()
        
        try:
            if system == "Windows":
                return self._screenshot_windows(filepath, fullscreen)
            elif system == "Darwin":  # macOS
                return self._screenshot_macos(filepath, fullscreen)
            else:  # Linux
                return self._screenshot_linux(filepath, fullscreen)
        except Exception as e:
            print(f"Erreur capture: {e}")
            return None
    
    def _screenshot_windows(self, filepath, fullscreen):
        """Capture Windows avec PowerShell"""
        if fullscreen:
            cmd = f'''powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen.Bounds | ForEach-Object {{ $bmp = New-Object System.Drawing.Bitmap($_.Width, $_.Height); $graphics = [System.Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($_.X, $_.Y, 0, 0, $bmp.Size); $bmp.Save('{filepath}'); $graphics.Dispose(); $bmp.Dispose() }}"'''
        else:
            # Utiliser l'outil Snipping Tool ou équivalent
            cmd = f'powershell -command "Start-Process SnippingTool -Wait; Start-Sleep 2"'
            subprocess.run(cmd, shell=True)
            return None  # L'utilisateur doit sauver manuellement
        
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return filepath if result.returncode == 0 else None
    
    def _screenshot_macos(self, filepath, fullscreen):
        """Capture macOS avec screencapture"""
        if fullscreen:
            cmd = ["screencapture", "-x", filepath]
        else:
            cmd = ["screencapture", "-s", filepath]  # -s pour sélection
        
        result = subprocess.run(cmd, capture_output=True)
        return filepath if result.returncode == 0 else None
    
    def _screenshot_linux(self, filepath, fullscreen):
        """Capture Linux avec plusieurs alternatives"""
        tools = [
            # Format: (commande_plein_écran, commande_sélection)
            (["gnome-screenshot", "-f", filepath], ["gnome-screenshot", "-a", "-f", filepath]),
            (["scrot", filepath], ["scrot", "-s", filepath]),
            (["import", filepath], ["import", filepath]),  # ImageMagick
            (["spectacle", "-f", "-b", "-o", filepath], ["spectacle", "-r", "-b", "-o", filepath]),  # KDE
            (["flameshot", "full", "-p", os.path.dirname(filepath)], ["flameshot", "gui", "-p", os.path.dirname(filepath)])
        ]
        
        for full_cmd, select_cmd in tools:
            try:
                cmd = full_cmd if fullscreen else select_cmd
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                
                if result.returncode == 0 and os.path.exists(filepath):
                    return filepath
                    
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        # Dernier recours : utiliser Python PIL + tkinter
        try:
            return self._screenshot_python_fallback(filepath, fullscreen)
        except:
            return None
    
    def _screenshot_python_fallback(self, filepath, fullscreen):
        """Capture avec Python pur (fallback)"""
        try:
            import tkinter as tk
            from PIL import ImageGrab
            
            if fullscreen:
                # Capture plein écran
                screenshot = ImageGrab.grab()
                screenshot.save(filepath)
                return filepath
            else:
                # Pour la sélection, on fait une capture pleine et on demande à l'utilisateur
                screenshot = ImageGrab.grab()
                screenshot.save(filepath)
                return filepath
                
        except Exception as e:
            print(f"Erreur capture Python: {e}")
            return None