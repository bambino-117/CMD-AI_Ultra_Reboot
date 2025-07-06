import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time

class SplashScreen:
    def __init__(self, duration=3):
        self.duration = duration
        self.splash = tk.Toplevel()
        self.splash.title("CMD-AI Ultra Reboot")
        self.splash.geometry("600x400")
        self.splash.resizable(False, False)
        
        # Centrer la fenêtre
        self.splash.geometry("+{}+{}".format(
            (self.splash.winfo_screenwidth() // 2) - 300,
            (self.splash.winfo_screenheight() // 2) - 200
        ))
        
        # Supprimer la barre de titre
        self.splash.overrideredirect(True)
        
        # Frame principal
        main_frame = tk.Frame(self.splash, bg='#2c3e50', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True)
        
        # Frame horizontal pour crédits + logo
        content_frame = tk.Frame(main_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Rectangle crédits à gauche
        credits_rect = tk.Frame(content_frame, bg='#34495e', relief='solid', bd=1)
        credits_rect.pack(side='left', fill='y', padx=(0, 10))
        
        credits_text = """Remerciements à JimmyThree, Masturbain, Kisda, Sebinou, Le J, Fôv, CedB.

Toucher rectal à M.Lepen, E.Zemmour, V.Orban, V.Poutine, D.Trump.

Invitation à aller niquer sa mère à JD.Vance, JL Mélenchon, Ayatola Khamenei, Joseph Kabila.

Nous souhaitons un joyeux malaise vagal Paul Biya, M. Kagamé & Sergei Lavrov, B.Nethanyahu"""
        
        credits_label = tk.Label(credits_rect, text=credits_text, 
                                font=('Arial', 7), 
                                fg='#ecf0f1', bg='#34495e',
                                justify='left', wraplength=180,
                                padx=8, pady=8)
        credits_label.pack()
        
        # Logo à droite
        logo_frame = tk.Frame(content_frame, bg='#2c3e50')
        logo_frame.pack(side='right', expand=True, fill='both')
        
        self.load_logo(logo_frame)
        
        # Titre
        title_label = tk.Label(main_frame, text="CMD-AI Ultra Reboot", 
                              font=('Arial', 16, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=(5, 5))
        
        # Version
        version_label = tk.Label(main_frame, text="Version 1.0.0", 
                                font=('Arial', 10), 
                                fg='#bdc3c7', bg='#2c3e50')
        version_label.pack()
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(pady=20, padx=50, fill='x')
        
        # Status
        self.status_label = tk.Label(main_frame, text="Chargement...", 
                                    font=('Arial', 9), 
                                    fg='#ecf0f1', bg='#2c3e50')
        self.status_label.pack(pady=(0, 10))
        
        # Crédits développement en bas
        dev_frame = tk.Frame(main_frame, bg='#2c3e50')
        dev_frame.pack(pady=(0, 5))
        
        dev_label = tk.Label(dev_frame, text="🎨 Design & Développement: Boris - ⚙️ CMD-AI Team", 
                            font=('Arial', 8), 
                            fg='#95a5a6', bg='#2c3e50')
        dev_label.pack()
    
    def load_logo(self, parent):
        try:
            logo_path = "ressources/logos/CMD-AI_Ultra_Full.png"
            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                image = image.resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(parent, image=self.logo_photo, bg='#2c3e50')
                logo_label.pack(pady=20)
            else:
                # Logo par défaut si fichier non trouvé
                logo_label = tk.Label(parent, text="CMD-AI", 
                                     font=('Arial', 24, 'bold'), 
                                     fg='#3498db', bg='#2c3e50')
                logo_label.pack(pady=40)
        except Exception as e:
            # Logo de fallback
            logo_label = tk.Label(parent, text="CMD-AI", 
                                 font=('Arial', 24, 'bold'), 
                                 fg='#3498db', bg='#2c3e50')
            logo_label.pack(pady=40)
    
    def show(self, callback=None):
        self.splash.lift()
        self.splash.attributes('-topmost', True)
        self.progress.start(10)
        
        # Simulation du chargement
        def loading_sequence():
            steps = [
                "Initialisation...",
                "Chargement des modules...",
                "Chargement des extensions...",
                "Finalisation..."
            ]
            
            step_duration = self.duration / len(steps)
            
            for step in steps:
                self.status_label.config(text=step)
                self.splash.update()
                time.sleep(step_duration)
            
            self.progress.stop()
            self.splash.destroy()
            
            if callback:
                callback()
        
        # Lancer le chargement dans un thread
        threading.Thread(target=loading_sequence, daemon=True).start()
    
    def destroy(self):
        if self.splash.winfo_exists():
            self.splash.destroy()