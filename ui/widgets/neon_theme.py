#!/usr/bin/env python3
"""
Widget pour le thème Neon avec coins coupés et effets lumineux
"""

import tkinter as tk
from tkinter import ttk
import json
import os

class NeonThemeApplier:
    def __init__(self, root):
        self.root = root
        self.neon_colors = {
            "bg": "#0A0A0A",
            "fg": "#00BFFF", 
            "accent": "#00FFFF",
            "input_bg": "#1A1A1A",
            "button_bg": "#001122",
            "border": "#00BFFF"
        }
        
    def apply_neon_theme(self):
        """Applique le thème néon à l'interface"""
        try:
            # Configuration de la fenêtre principale
            self.root.configure(bg=self.neon_colors["bg"])
            
            # Style TTK pour les widgets
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configuration des styles néon
            self._configure_neon_styles(style)
            
            # Appliquer aux widgets existants
            self._apply_to_existing_widgets()
            
            return True
        except Exception as e:
            print(f"Erreur application thème néon: {e}")
            return False
    
    def _configure_neon_styles(self, style):
        """Configure les styles TTK pour le thème néon"""
        
        # Style pour les boutons
        style.configure("Neon.TButton",
            background=self.neon_colors["button_bg"],
            foreground=self.neon_colors["fg"],
            borderwidth=1,
            focuscolor="none",
            relief="flat"
        )
        
        style.map("Neon.TButton",
            background=[('active', self.neon_colors["accent"]),
                       ('pressed', self.neon_colors["border"])],
            foreground=[('active', self.neon_colors["bg"]),
                       ('pressed', self.neon_colors["bg"])]
        )
        
        # Style pour les entrées de texte
        style.configure("Neon.TEntry",
            fieldbackground=self.neon_colors["input_bg"],
            foreground=self.neon_colors["fg"],
            borderwidth=1,
            insertcolor=self.neon_colors["accent"]
        )
        
        # Style pour les labels
        style.configure("Neon.TLabel",
            background=self.neon_colors["bg"],
            foreground=self.neon_colors["fg"]
        )
        
        # Style pour les frames
        style.configure("Neon.TFrame",
            background=self.neon_colors["bg"],
            borderwidth=1,
            relief="flat"
        )
    
    def _apply_to_existing_widgets(self):
        """Applique le thème aux widgets existants"""
        self._apply_recursive(self.root)
    
    def _apply_recursive(self, widget):
        """Applique récursivement le thème à tous les widgets"""
        try:
            widget_class = widget.winfo_class()
            
            if widget_class == "Button":
                widget.configure(
                    bg=self.neon_colors["button_bg"],
                    fg=self.neon_colors["fg"],
                    activebackground=self.neon_colors["accent"],
                    activeforeground=self.neon_colors["bg"],
                    bd=1,
                    relief="flat"
                )
            
            elif widget_class == "Entry":
                widget.configure(
                    bg=self.neon_colors["input_bg"],
                    fg=self.neon_colors["fg"],
                    insertbackground=self.neon_colors["accent"],
                    bd=1,
                    relief="flat"
                )
            
            elif widget_class == "Text":
                widget.configure(
                    bg=self.neon_colors["input_bg"],
                    fg=self.neon_colors["fg"],
                    insertbackground=self.neon_colors["accent"],
                    selectbackground=self.neon_colors["accent"],
                    selectforeground=self.neon_colors["bg"],
                    bd=1,
                    relief="flat"
                )
            
            elif widget_class == "Label":
                widget.configure(
                    bg=self.neon_colors["bg"],
                    fg=self.neon_colors["fg"]
                )
            
            elif widget_class == "Frame":
                widget.configure(
                    bg=self.neon_colors["bg"],
                    bd=1,
                    relief="flat"
                )
            
            elif widget_class == "Toplevel":
                widget.configure(bg=self.neon_colors["bg"])
            
            # Appliquer aux widgets TTK
            if hasattr(widget, 'configure'):
                if isinstance(widget, ttk.Button):
                    widget.configure(style="Neon.TButton")
                elif isinstance(widget, ttk.Entry):
                    widget.configure(style="Neon.TEntry")
                elif isinstance(widget, ttk.Label):
                    widget.configure(style="Neon.TLabel")
                elif isinstance(widget, ttk.Frame):
                    widget.configure(style="Neon.TFrame")
            
        except Exception as e:
            pass  # Ignorer les erreurs de widgets spécifiques
        
        # Appliquer récursivement aux enfants
        try:
            for child in widget.winfo_children():
                self._apply_recursive(child)
        except:
            pass

class CutCornerWidget(tk.Frame):
    """Widget avec coins coupés pour le thème néon"""
    
    def __init__(self, parent, corner_size=10, **kwargs):
        super().__init__(parent, **kwargs)
        self.corner_size = corner_size
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.bind('<Configure>', self._on_resize)
        
    def _on_resize(self, event=None):
        """Redessine le widget avec coins coupés"""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Créer le polygone avec coins coupés
        points = [
            self.corner_size, 0,  # Coin haut gauche coupé
            width - self.corner_size, 0,  # Haut
            width, self.corner_size,  # Coin haut droit coupé
            width, height - self.corner_size,  # Droite
            width - self.corner_size, height,  # Coin bas droit coupé
            self.corner_size, height,  # Bas
            0, height - self.corner_size,  # Coin bas gauche coupé
            0, self.corner_size  # Gauche
        ]
        
        # Dessiner le fond avec coins coupés
        self.canvas.create_polygon(
            points,
            fill="#001122",
            outline="#00BFFF",
            width=1
        )

def create_neon_button(parent, text, command=None, **kwargs):
    """Crée un bouton avec style néon et coins coupés"""
    frame = CutCornerWidget(parent, corner_size=8)
    
    button = tk.Button(
        frame.canvas,
        text=text,
        command=command,
        bg="#001122",
        fg="#00BFFF",
        activebackground="#00FFFF",
        activeforeground="#0A0A0A",
        bd=0,
        relief="flat",
        font=("Arial", 10, "bold"),
        **kwargs
    )
    
    # Positionner le bouton dans le canvas
    frame.canvas.create_window(
        frame.canvas.winfo_reqwidth()//2,
        frame.canvas.winfo_reqheight()//2,
        window=button
    )
    
    return frame

def monitor_theme_changes(root, theme_applier):
    """Surveille les changements de thème"""
    signal_file = "user/theme_update_signal.json"
    
    def check_theme_update():
        try:
            if os.path.exists(signal_file):
                with open(signal_file, 'r') as f:
                    data = json.load(f)
                
                if data.get("theme") == "neon":
                    theme_applier.apply_neon_theme()
                    os.remove(signal_file)  # Supprimer le signal
                    
        except Exception as e:
            pass
        
        # Vérifier à nouveau dans 1 seconde
        root.after(1000, check_theme_update)
    
    check_theme_update()

# Exemple d'utilisation
def example_neon_interface():
    """Exemple d'interface avec thème néon"""
    root = tk.Tk()
    root.title("CMD-AI Ultra Reboot - Thème Néon")
    root.geometry("600x400")
    
    # Appliquer le thème néon
    neon_applier = NeonThemeApplier(root)
    neon_applier.apply_neon_theme()
    
    # Surveiller les changements de thème
    monitor_theme_changes(root, neon_applier)
    
    # Interface d'exemple
    main_frame = tk.Frame(root, bg="#0A0A0A")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    title_label = tk.Label(
        main_frame,
        text="🤖 CMD-AI Ultra Reboot",
        font=("Arial", 16, "bold"),
        bg="#0A0A0A",
        fg="#00BFFF"
    )
    title_label.pack(pady=10)
    
    # Boutons avec coins coupés
    button_frame = tk.Frame(main_frame, bg="#0A0A0A")
    button_frame.pack(pady=20)
    
    neon_btn1 = create_neon_button(button_frame, "Scanner Système")
    neon_btn1.pack(side=tk.LEFT, padx=5)
    
    neon_btn2 = create_neon_button(button_frame, "Analyser Fichier")
    neon_btn2.pack(side=tk.LEFT, padx=5)
    
    # Zone de texte néon
    text_area = tk.Text(
        main_frame,
        bg="#1A1A1A",
        fg="#00BFFF",
        insertbackground="#00FFFF",
        selectbackground="#00FFFF",
        selectforeground="#0A0A0A",
        bd=1,
        relief="flat",
        font=("Consolas", 10)
    )
    text_area.pack(fill=tk.BOTH, expand=True, pady=10)
    text_area.insert("1.0", "Interface néon avec coins coupés activée !\\n")
    
    root.mainloop()

if __name__ == "__main__":
    example_neon_interface()