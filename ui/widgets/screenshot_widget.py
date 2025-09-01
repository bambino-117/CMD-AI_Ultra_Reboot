import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ScreenshotWidget:
    def __init__(self, parent, on_screenshot_callback):
        self.parent = parent
        self.on_screenshot_callback = on_screenshot_callback
        self.current_screenshot = None
        
        # Frame pour la vignette
        self.thumbnail_frame = ttk.Frame(parent)
        self.thumbnail_label = None
        
    def show_thumbnail(self, image_path):
        """Affiche une vignette de l'image capturée"""
        try:
            # Charger et redimensionner l'image
            image = Image.open(image_path)
            image.thumbnail((60, 40), Image.Resampling.LANCZOS)
            
            # Convertir en PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Créer ou mettre à jour le label
            if self.thumbnail_label:
                self.thumbnail_label.destroy()
            
            self.thumbnail_label = tk.Label(
                self.thumbnail_frame, 
                image=photo,
                relief='solid',
                bd=1,
                cursor='hand2'
            )
            self.thumbnail_label.image = photo  # Garder une référence
            self.thumbnail_label.pack(side='left', padx=(0, 5))
            
            # Clic pour supprimer
            self.thumbnail_label.bind('<Button-1>', self.remove_thumbnail)
            
            # Afficher le frame
            self.thumbnail_frame.pack(side='left', padx=(0, 5))
            
            self.current_screenshot = image_path
            
        except Exception as e:
            print(f"Erreur affichage vignette: {e}")
    
    def remove_thumbnail(self, event=None):
        """Supprime la vignette"""
        if self.thumbnail_label:
            self.thumbnail_label.destroy()
            self.thumbnail_label = None
        
        self.thumbnail_frame.pack_forget()
        self.current_screenshot = None
    
    def get_screenshot_path(self):
        """Retourne le chemin de la capture actuelle"""
        return self.current_screenshot
    
    def take_screenshot(self):
        """Lance la capture d'écran"""
        try:
            from extensions.screenshot_extension import ScreenshotExtension
            from core.daily_suggestions import DailySuggestions
            
            # Vérifier si l'extension est installée
            daily_suggestions = DailySuggestions()
            if not daily_suggestions.is_screenshot_installed():
                return "❌ Extension Screenshot non installée. Allez dans Paramètres pour l'installer."
            
            # Prendre la capture
            screenshot_ext = ScreenshotExtension()
            screenshot_path = screenshot_ext._take_screenshot(fullscreen=False)
            
            if screenshot_path:
                self.show_thumbnail(screenshot_path)
                return f"📸 Capture ajoutée"
            else:
                return "❌ Erreur lors de la capture"
                
        except Exception as e:
            return f"❌ Erreur: {e}"