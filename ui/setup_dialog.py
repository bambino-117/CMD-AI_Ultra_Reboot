import tkinter as tk
from tkinter import ttk, messagebox
from core.user_manager import UserManager
from core.system_detector import SystemDetector
from core.logger import app_logger

class SetupDialog:
    def __init__(self, parent=None):
        self.result = None
        self.user_manager = UserManager()
        self.system_detector = SystemDetector()
        
        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("Configuration initiale - CMD-AI Ultra")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        
        # Centrer
        self.dialog.geometry("+{}+{}".format(
            (self.dialog.winfo_screenwidth() // 2) - 200,
            (self.dialog.winfo_screenheight() // 2) - 125
        ))
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Bienvenue dans CMD-AI Ultra!", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Pseudo
        ttk.Label(main_frame, text="Choisissez votre pseudo:").pack(anchor='w')
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        username_entry.pack(pady=(5, 15), fill='x')
        username_entry.focus()
        
        # Info système
        info_label = ttk.Label(main_frame, 
                              text="Détection de votre environnement système...", 
                              font=('Arial', 9))
        info_label.pack(pady=(0, 20))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Annuler", 
                  command=self.cancel).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Continuer", 
                  command=self.save_and_continue).pack(side='right')
        
        # Bind Enter
        username_entry.bind('<Return>', lambda e: self.save_and_continue())
    
    def save_and_continue(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Attention", "Veuillez saisir un pseudo")
            return
        
        try:
            # Sauvegarder pseudo
            self.user_manager.set_username(username)
            
            # Détecter et sauvegarder système
            self.system_detector.save_system_info()
            
            self.result = True
            self.dialog.destroy()
            app_logger.info(f"Configuration initiale terminée pour {username}", "SETUP")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la configuration: {e}")
            app_logger.error(f"Erreur setup: {e}", "SETUP")
    
    def cancel(self):
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        self.dialog.grab_set()
        self.dialog.wait_window()
        return self.result