import tkinter as tk

class UserSettings:
    def __init__(self, root):
        self.root = root
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Paramètres")

        # Code pour créer les éléments de la fenêtre de paramètres
        self.create_settings_widgets()

    def create_settings_widgets(self):
        # Code pour créer les éléments de la fenêtre de paramètres
        pass

    def show_settings(self):
        self.settings_window.deiconify()

    def hide_settings(self):
        self.settings_window.withdraw()