import tkinter as tk
from tkinter import ttk

class FallbackTextArea:
    """Zone de texte de fallback simple"""
    def __init__(self, parent):
        self.text_widget = tk.Text(parent, wrap=tk.WORD)
        self.text_widget.pack(fill='both', expand=True, padx=10, pady=10)
    
    def display_message(self, message):
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.see(tk.END)

class FallbackSettings:
    """Paramètres de fallback minimal"""
    def __init__(self, parent):
        self.parent = parent
    
    def show_settings(self):
        tk.messagebox.showinfo("Paramètres", "Paramètres en mode dégradé")

class FallbackDispatcher:
    """Dispatcher de fallback minimal"""
    def __init__(self, config=None):
        self.config = config
    
    def process(self, user_input):
        return f"Mode dégradé - Echo: {user_input}"
    
    def get_startup_message(self):
        return "Application en mode dégradé - Fonctionnalités limitées"
    
    def set_awaiting_installation(self):
        pass

class FallbackExtensionManager:
    """Gestionnaire d'extensions de fallback"""
    def __init__(self):
        pass
    
    def load_extensions(self):
        print("Extensions désactivées en mode dégradé")
    
    def list_extensions(self):
        return []