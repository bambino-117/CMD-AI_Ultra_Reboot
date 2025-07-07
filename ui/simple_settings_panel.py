import tkinter as tk
from tkinter import ttk
import json
import os

class SimpleSettingsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.settings_file = "user/ui_settings.json"
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Charge les paramètres UI"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "extensions_enabled": True,
            "notifications_enabled": True,
            "auto_save": True,
            "theme": "light"
        }
    
    def _save_settings(self):
        """Sauvegarde les paramètres"""
        try:
            os.makedirs("user", exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde paramètres: {e}")
    
    def show(self):
        """Affiche le panneau de paramètres simplifié"""
        if self.frame:
            self.frame.destroy()
        
        # Frame principal
        self.frame = ttk.Frame(self.parent, relief='raised', borderwidth=2)
        self.frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Titre
        title_label = ttk.Label(
            self.frame,
            text="⚙️ PARAMÈTRES",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=10)
        
        # Séparateur
        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=5)
        
        # Switch Extensions
        ext_frame = ttk.Frame(self.frame)
        ext_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(ext_frame, text="🔌 Extensions:", font=('Arial', 10)).pack(anchor='w')
        
        self.ext_var = tk.BooleanVar(value=self.settings.get("extensions_enabled", True))
        ext_switch = ttk.Checkbutton(
            ext_frame,
            text="Activer les extensions",
            variable=self.ext_var,
            command=self._toggle_extensions
        )
        ext_switch.pack(anchor='w', pady=2)
        
        # Switch Notifications
        notif_frame = ttk.Frame(self.frame)
        notif_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(notif_frame, text="🔔 Notifications:", font=('Arial', 10)).pack(anchor='w')
        
        self.notif_var = tk.BooleanVar(value=self.settings.get("notifications_enabled", True))
        notif_switch = ttk.Checkbutton(
            notif_frame,
            text="Activer les notifications",
            variable=self.notif_var,
            command=self._toggle_notifications
        )
        notif_switch.pack(anchor='w', pady=2)
        
        # Switch Auto-save
        save_frame = ttk.Frame(self.frame)
        save_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(save_frame, text="💾 Sauvegarde:", font=('Arial', 10)).pack(anchor='w')
        
        self.save_var = tk.BooleanVar(value=self.settings.get("auto_save", True))
        save_switch = ttk.Checkbutton(
            save_frame,
            text="Sauvegarde automatique",
            variable=self.save_var,
            command=self._toggle_auto_save
        )
        save_switch.pack(anchor='w', pady=2)
        
        # Sélecteur de thème
        theme_frame = ttk.Frame(self.frame)
        theme_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(theme_frame, text="🎨 Thème:", font=('Arial', 10)).pack(anchor='w')
        
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["light", "dark", "blue", "green"],
            state="readonly",
            width=15
        )
        theme_combo.pack(anchor='w', pady=2)
        theme_combo.bind('<<ComboboxSelected>>', self._change_theme)
        
        # Séparateur
        separator2 = ttk.Separator(self.frame, orient='horizontal')
        separator2.pack(fill='x', padx=10, pady=15)
        
        # Boutons d'action
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill='x', padx=15, pady=5)
        
        # Bouton Reset
        reset_btn = ttk.Button(
            action_frame,
            text="🔄 Reset",
            command=self._reset_settings,
            width=12
        )
        reset_btn.pack(pady=2)
        
        # Bouton Marketplace
        marketplace_btn = ttk.Button(
            action_frame,
            text="🔌 Marketplace",
            command=self._open_marketplace,
            width=12
        )
        marketplace_btn.pack(pady=2)
        
        # Statut
        status_frame = ttk.Frame(self.frame)
        status_frame.pack(fill='x', padx=15, pady=10)
        
        status_text = f"""📊 Statut:
Extensions: {'✅' if self.ext_var.get() else '❌'}
Notifications: {'✅' if self.notif_var.get() else '❌'}
Auto-save: {'✅' if self.save_var.get() else '❌'}
Thème: {self.theme_var.get()}"""
        
        self.status_label = ttk.Label(
            status_frame,
            text=status_text,
            font=('Arial', 8),
            justify='left'
        )
        self.status_label.pack(anchor='w')
    
    def hide(self):
        """Cache le panneau"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
    
    def _toggle_extensions(self):
        """Active/désactive les extensions"""
        self.settings["extensions_enabled"] = self.ext_var.get()
        self._save_settings()
        self._update_status()
        
        status = "activées" if self.ext_var.get() else "désactivées"
        print(f"Extensions {status}")
    
    def _toggle_notifications(self):
        """Active/désactive les notifications"""
        self.settings["notifications_enabled"] = self.notif_var.get()
        self._save_settings()
        self._update_status()
    
    def _toggle_auto_save(self):
        """Active/désactive la sauvegarde automatique"""
        self.settings["auto_save"] = self.save_var.get()
        self._save_settings()
        self._update_status()
    
    def _change_theme(self, event=None):
        """Change le thème"""
        self.settings["theme"] = self.theme_var.get()
        self._save_settings()
        self._update_status()
        print(f"Thème changé: {self.theme_var.get()}")
    
    def _reset_settings(self):
        """Remet les paramètres par défaut"""
        self.settings = {
            "extensions_enabled": True,
            "notifications_enabled": True,
            "auto_save": True,
            "theme": "light"
        }
        self._save_settings()
        
        # Mettre à jour l'interface
        self.ext_var.set(True)
        self.notif_var.set(True)
        self.save_var.set(True)
        self.theme_var.set("light")
        self._update_status()
        
        print("Paramètres remis par défaut")
    
    def _open_marketplace(self):
        """Ouvre le marketplace"""
        # Accéder à l'interface parent pour ouvrir le marketplace
        try:
            # Remonter jusqu'à l'interface principale
            app_ui = self.parent
            while hasattr(app_ui, 'parent') and app_ui.parent:
                app_ui = app_ui.parent
            
            if hasattr(app_ui, 'show_marketplace'):
                app_ui.show_marketplace()
            else:
                print("Marketplace non accessible")
        except Exception as e:
            print(f"Erreur ouverture marketplace: {e}")
    
    def _update_status(self):
        """Met à jour le statut affiché"""
        if hasattr(self, 'status_label'):
            status_text = f"""📊 Statut:
Extensions: {'✅' if self.ext_var.get() else '❌'}
Notifications: {'✅' if self.notif_var.get() else '❌'}
Auto-save: {'✅' if self.save_var.get() else '❌'}
Thème: {self.theme_var.get()}"""
            
            self.status_label.config(text=status_text)