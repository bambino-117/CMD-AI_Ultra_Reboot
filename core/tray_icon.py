import tkinter as tk
from PIL import Image, ImageTk
import os
import threading
import time

class TrayIcon:
    def __init__(self, app_instance):
        self.app = app_instance
        self.enabled = False
        self.tray_window = None
        
    def enable(self):
        """Active l'icône de la barre système"""
        try:
            if self.enabled:
                return "⚠️ Icône déjà active"
            
            # Créer une fenêtre invisible pour l'icône
            self.tray_window = tk.Toplevel()
            self.tray_window.withdraw()  # Cacher la fenêtre
            self.tray_window.title("CMD-AI Ultra Reboot - Tray")
            
            # Configurer l'icône
            self._setup_tray_icon()
            
            self.enabled = True
            return "✅ Icône de la barre système activée"
            
        except Exception as e:
            return f"❌ Erreur icône système: {e}"
    
    def _setup_tray_icon(self):
        """Configure l'icône système"""
        try:
            # Charger l'icône
            icon_path = "ressources/logos/CMD-AI_Ultra_main.png"
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((16, 16), Image.Resampling.LANCZOS)
                self.icon = ImageTk.PhotoImage(img)
                self.tray_window.iconphoto(False, self.icon)
            
            # Menu contextuel simple
            self.tray_window.bind("<Button-3>", self._show_context_menu)
            
        except Exception as e:
            print(f"Erreur setup tray: {e}")
    
    def _show_context_menu(self, event):
        """Affiche le menu contextuel"""
        try:
            menu = tk.Menu(self.tray_window, tearoff=0)
            menu.add_command(label="🤖 Ouvrir CMD-AI", command=self._restore_window)
            menu.add_separator()
            menu.add_command(label="📊 Statut", command=self._show_status)
            menu.add_command(label="⚙️ Paramètres", command=self._show_settings)
            menu.add_separator()
            menu.add_command(label="❌ Quitter", command=self._quit_app)
            
            menu.tk_popup(event.x_root, event.y_root)
            
        except Exception as e:
            print(f"Erreur menu contextuel: {e}")
    
    def _restore_window(self):
        """Restaure la fenêtre principale"""
        if self.app and hasattr(self.app, 'root'):
            self.app.root.deiconify()
            self.app.root.lift()
    
    def _show_status(self):
        """Affiche le statut via notification"""
        if hasattr(self.app, 'dispatcher'):
            self.app.dispatcher.system_integration.send_notification(
                "CMD-AI Ultra Reboot",
                "Application active en arrière-plan"
            )
    
    def _show_settings(self):
        """Ouvre les paramètres"""
        self._restore_window()
        if hasattr(self.app, 'toggle_settings'):
            self.app.toggle_settings()
    
    def _quit_app(self):
        """Ferme l'application"""
        if self.app and hasattr(self.app, 'on_quit'):
            self.app.on_quit()
    
    def disable(self):
        """Désactive l'icône système"""
        try:
            if self.tray_window:
                self.tray_window.destroy()
                self.tray_window = None
            
            self.enabled = False
            return "✅ Icône système désactivée"
            
        except Exception as e:
            return f"❌ Erreur désactivation: {e}"
    
    def send_tray_notification(self, title, message):
        """Envoie une notification depuis la barre système"""
        if self.enabled and hasattr(self.app, 'dispatcher'):
            return self.app.dispatcher.system_integration.send_notification(title, message)
        return False