#!/usr/bin/env python3
"""
Widget de menu contextuel pour l'interface graphique
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List

class ContextualMenu(tk.Toplevel):
    def __init__(self, parent, title: str, options: List[Dict], callback: Callable):
        super().__init__(parent)
        self.callback = callback
        self.result = None
        
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui(options)
        self.center_window()
        
    def setup_ui(self, options: List[Dict]):
        """Configure l'interface du menu"""
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="Que souhaitez-vous faire ?",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame pour les boutons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Créer les boutons d'options
        for i, option in enumerate(options, 1):
            self.create_option_button(
                buttons_frame, 
                f"[{i}] {option['icon']} {option['text']}", 
                option['description'],
                lambda opt=option: self.select_option(opt)
            )
        
        # Bouton annuler
        cancel_frame = ttk.Frame(main_frame)
        cancel_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = ttk.Button(
            cancel_frame,
            text="❌ Annuler",
            command=self.cancel
        )
        cancel_btn.pack(side=tk.RIGHT)
    
    def create_option_button(self, parent, text: str, description: str, command: Callable):
        """Crée un bouton d'option avec description"""
        # Frame pour l'option
        option_frame = ttk.Frame(parent)
        option_frame.pack(fill=tk.X, pady=5)
        
        # Bouton principal
        btn = ttk.Button(
            option_frame,
            text=text,
            command=command,
            width=40
        )
        btn.pack(fill=tk.X)
        
        # Description
        desc_label = ttk.Label(
            option_frame,
            text=description,
            font=("Arial", 8),
            foreground="gray"
        )
        desc_label.pack(fill=tk.X, padx=(10, 0))
    
    def select_option(self, option: Dict):
        """Sélectionne une option"""
        self.result = option
        self.callback(option)
        self.destroy()
    
    def cancel(self):
        """Annule la sélection"""
        self.result = None
        self.callback(None)
        self.destroy()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

class SmartMenuManager:
    """Gestionnaire de menus contextuels intelligents"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.menu_definitions = self._create_menu_definitions()
    
    def _create_menu_definitions(self) -> Dict:
        """Définit les menus disponibles"""
        return {
            "security_scan": {
                "title": "🛡️ Analyse Sécurité",
                "options": [
                    {
                        "icon": "🖥️",
                        "text": "Scanner tout le système",
                        "description": "Analyse complète : processus, fichiers, réseau",
                        "action": "system_scan"
                    },
                    {
                        "icon": "📁",
                        "text": "Analyser un fichier",
                        "description": "Vérification de sécurité d'un fichier spécifique",
                        "action": "file_scan"
                    },
                    {
                        "icon": "🌐",
                        "text": "Vérifier les connexions",
                        "description": "Analyse des connexions réseau actives",
                        "action": "network_scan"
                    },
                    {
                        "icon": "🔍",
                        "text": "Analyse complète",
                        "description": "Système + réseau + fichiers + rapport IA",
                        "action": "complete_scan"
                    }
                ]
            },
            
            "usb_tools": {
                "title": "🔌 Outils USB",
                "options": [
                    {
                        "icon": "⚡",
                        "text": "Créer un payload BadUSB",
                        "description": "Génération de payloads pour tests de sécurité",
                        "action": "badusb_create"
                    },
                    {
                        "icon": "📋",
                        "text": "Gérer les périphériques",
                        "description": "Liste et gestion des périphériques USB",
                        "action": "usb_manage"
                    },
                    {
                        "icon": "🔒",
                        "text": "Sécuriser une clé USB",
                        "description": "Chiffrement et protection d'une clé USB",
                        "action": "usb_secure"
                    },
                    {
                        "icon": "📊",
                        "text": "Analyser un périphérique",
                        "description": "Analyse de sécurité d'un périphérique USB",
                        "action": "usb_analyze"
                    }
                ]
            },
            
            "network_analysis": {
                "title": "🌐 Analyse Réseau",
                "options": [
                    {
                        "icon": "🔍",
                        "text": "Scanner le réseau local",
                        "description": "Découverte des appareils sur le réseau",
                        "action": "network_local_scan"
                    },
                    {
                        "icon": "📡",
                        "text": "Tester une connexion",
                        "description": "Test de ping vers une adresse",
                        "action": "ping_test"
                    },
                    {
                        "icon": "⚡",
                        "text": "Test de vitesse",
                        "description": "Mesure de la vitesse Internet",
                        "action": "speed_test"
                    },
                    {
                        "icon": "🕵️",
                        "text": "Analyser une IP",
                        "description": "Informations détaillées sur une adresse IP",
                        "action": "ip_analyze"
                    }
                ]
            },
            
            "osint_research": {
                "title": "🕵️ Recherche OSINT",
                "options": [
                    {
                        "icon": "🌐",
                        "text": "Recherche générale",
                        "description": "Recherche d'informations publiques",
                        "action": "osint_general"
                    },
                    {
                        "icon": "📧",
                        "text": "Analyser un email",
                        "description": "Informations sur une adresse email",
                        "action": "osint_email"
                    },
                    {
                        "icon": "🌍",
                        "text": "Analyser une IP",
                        "description": "Géolocalisation et informations IP",
                        "action": "osint_ip"
                    },
                    {
                        "icon": "🏢",
                        "text": "Rechercher un domaine",
                        "description": "Informations sur un nom de domaine",
                        "action": "osint_domain"
                    }
                ]
            },
            
            "file_management": {
                "title": "📁 Gestion Fichiers",
                "options": [
                    {
                        "icon": "🗂️",
                        "text": "Organiser automatiquement",
                        "description": "Tri automatique par type et date",
                        "action": "organize_files"
                    },
                    {
                        "icon": "🔍",
                        "text": "Rechercher des fichiers",
                        "description": "Recherche avancée de fichiers",
                        "action": "search_files"
                    },
                    {
                        "icon": "🧹",
                        "text": "Nettoyer les temporaires",
                        "description": "Suppression des fichiers temporaires",
                        "action": "cleanup_files"
                    },
                    {
                        "icon": "📊",
                        "text": "Analyser l'espace disque",
                        "description": "Analyse de l'utilisation du disque",
                        "action": "disk_analyze"
                    }
                ]
            }
        }
    
    def show_menu(self, category: str, callback: Callable):
        """Affiche un menu contextuel"""
        if category not in self.menu_definitions:
            callback(None)
            return
        
        menu_def = self.menu_definitions[category]
        
        menu = ContextualMenu(
            self.parent,
            menu_def["title"],
            menu_def["options"],
            callback
        )
        
        return menu
    
    def get_available_categories(self) -> List[str]:
        """Retourne les catégories de menus disponibles"""
        return list(self.menu_definitions.keys())

# Exemple d'utilisation
def example_usage():
    """Exemple d'utilisation du menu contextuel"""
    
    def handle_menu_selection(option):
        if option:
            print(f"Option sélectionnée: {option['action']}")
            print(f"Description: {option['description']}")
        else:
            print("Sélection annulée")
    
    # Dans l'interface principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale pour l'exemple
    
    menu_manager = SmartMenuManager(root)
    menu_manager.show_menu("security_scan", handle_menu_selection)
    
    root.mainloop()

if __name__ == "__main__":
    example_usage()