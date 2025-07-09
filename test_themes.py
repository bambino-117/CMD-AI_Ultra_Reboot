#!/usr/bin/env python3
"""
Test des thèmes en temps réel
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.theme_manager import ThemeManager
from core.theme_applier import ThemeApplier

class ThemeTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Test des Thèmes - CMD-AI Ultra Reboot")
        self.root.geometry("600x400")
        
        self.theme_manager = ThemeManager()
        self.theme_applier = ThemeApplier(self.root)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de test"""
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(main_frame, text="Test des Thèmes", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Boutons de thèmes
        themes_frame = tk.Frame(main_frame)
        themes_frame.pack(pady=10)
        
        themes = ["light", "dark", "blue", "green", "neon"]
        for theme in themes:
            btn = tk.Button(
                themes_frame,
                text=f"Thème {theme.title()}",
                command=lambda t=theme: self.apply_theme(t),
                width=12
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Zone de test avec différents widgets
        test_frame = tk.LabelFrame(main_frame, text="Zone de Test")
        test_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10, ipady=10)
        
        # Label
        test_label = tk.Label(test_frame, text="Ceci est un label de test")
        test_label.pack(pady=5)
        
        # Entry
        test_entry = tk.Entry(test_frame, width=30)
        test_entry.pack(pady=5)
        test_entry.insert(0, "Champ de saisie de test")
        
        # Boutons
        buttons_frame = tk.Frame(test_frame)
        buttons_frame.pack(pady=10)
        
        test_btn1 = tk.Button(buttons_frame, text="Bouton 1")
        test_btn1.pack(side=tk.LEFT, padx=5)
        
        test_btn2 = tk.Button(buttons_frame, text="Bouton 2")
        test_btn2.pack(side=tk.LEFT, padx=5)
        
        # Zone de texte
        text_area = tk.Text(test_frame, height=8, width=50)
        text_area.pack(pady=5)
        text_area.insert("1.0", "Zone de texte de test\\nLes thèmes devraient s'appliquer à tous ces éléments.\\n\\nTestez les différents thèmes avec les boutons ci-dessus.")
        
        # Statut
        self.status_label = tk.Label(main_frame, text="Prêt - Sélectionnez un thème", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=5)
        
    def apply_theme(self, theme_name):
        """Applique un thème"""
        try:
            # Changer le thème via le manager
            result = self.theme_manager.set_theme(theme_name)
            
            # Récupérer les données du thème
            theme_data = self.theme_manager.get_theme(theme_name)
            
            # Appliquer immédiatement
            success = self.theme_applier.apply_theme_immediately(theme_data)
            
            if success:
                self.status_label.config(text=f"✅ Thème '{theme_name}' appliqué avec succès")
                print(f"✅ Thème {theme_name} appliqué")
            else:
                self.status_label.config(text=f"❌ Erreur application thème '{theme_name}'")
                print(f"❌ Erreur thème {theme_name}")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Erreur: {e}")
            print(f"❌ Erreur: {e}")
    
    def run(self):
        """Lance l'application de test"""
        print("🎨 Test des Thèmes CMD-AI Ultra Reboot")
        print("=" * 40)
        print("Thèmes disponibles:")
        for theme_id, theme_data in self.theme_manager.themes.items():
            print(f"  • {theme_id}: {theme_data['name']}")
        print()
        print("Cliquez sur les boutons pour tester les thèmes.")
        print("L'interface devrait changer instantanément.")
        print()
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemeTestApp()
    app.run()