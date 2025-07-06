import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class AboutDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("À propos de CMD-AI Ultra Reboot")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrer la fenêtre
        self.dialog.geometry("+{}+{}".format(
            parent.winfo_x() + 150,
            parent.winfo_y() + 100
        ))
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True)
        
        # Header avec logo
        header_frame = tk.Frame(main_frame, bg='#34495e')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        # Logo + titre
        try:
            logo_path = "ressources/logos/CMD-AI_Ultra_main.png"
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(image)
                logo_label = tk.Label(header_frame, image=self.logo_photo, bg='#34495e')
                logo_label.pack(side='left', padx=10)
        except:
            pass
        
        title_frame = tk.Frame(header_frame, bg='#34495e')
        title_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(title_frame, text="CMD-AI Ultra Reboot", 
                font=('Arial', 18, 'bold'), fg='white', bg='#34495e').pack(anchor='w')
        tk.Label(title_frame, text="Version 1.0.0", 
                font=('Arial', 12), fg='#bdc3c7', bg='#34495e').pack(anchor='w')
        tk.Label(title_frame, text="Application de chat IA modulaire", 
                font=('Arial', 10), fg='#95a5a6', bg='#34495e').pack(anchor='w')
        
        # Informations
        info_frame = tk.Frame(main_frame, bg='#2c3e50')
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        info_text = """🎨 Développement: Boris Vermaelen 
        (Github:Bambino-117)
⚙️ Équipe: CMD-AI Team
📅 Année: 2025

🚀 Fonctionnalités:
• Chat IA multi-modèles (OpenAI, Gemini, DeepSeek, Ollama)
• Extensions modulaires
• Interface graphique moderne
• Commandes système intégrées
• Compatible Windows/macOS/Linux (32/64-bit)

🔧 Technologies:
• Python 3.8+
• Tkinter (Interface)
• Pillow (Images)
• Requests (HTTP)

🙏 Remerciements spéciaux:
JimmyThree, Masturbain, Kisda, Sebinou, Le J, Fôv, CedB

© 2025 CMD-AI Team - Tous droits réservés"""
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=('Arial', 9), fg='#ecf0f1', bg='#2c3e50',
                             justify='left', anchor='nw')
        info_label.pack(fill='both', expand=True)
        
        # Bouton fermer
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        from ui.widgets.custom_button import create_button
        close_btn = create_button(btn_frame, "Fermer", self.close, width=8, symbol="❌")
        close_btn.pack(side='right')
    
    def close(self):
        self.dialog.destroy()