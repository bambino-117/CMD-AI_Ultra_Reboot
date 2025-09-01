import tkinter as tk
from tkinter import ttk
from core.kaamelott_responses import KaamelottResponses

class InactivityEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.last_activity = None
        self.inactivity_timer = None
        self.kaamelott_active = False
        self.original_value = ""
        
        # Surveiller l'activité
        self.bind('<Key>', self.on_activity)
        self.bind('<Button-1>', self.on_activity)
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        
        self.start_inactivity_timer()
    
    def on_activity(self, event=None):
        """Réinitialise le timer d'inactivité"""
        if self.kaamelott_active:
            self.clear_kaamelott()
        self.reset_inactivity_timer()
    
    def on_focus_in(self, event=None):
        """Quand le champ reçoit le focus"""
        if self.kaamelott_active:
            self.clear_kaamelott()
        self.reset_inactivity_timer()
    
    def on_focus_out(self, event=None):
        """Quand le champ perd le focus"""
        self.reset_inactivity_timer()
    
    def start_inactivity_timer(self):
        """Démarre le timer d'inactivité (60 secondes)"""
        if self.inactivity_timer:
            self.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.after(60000, self.show_kaamelott)  # 60 secondes
    
    def reset_inactivity_timer(self):
        """Remet à zéro le timer d'inactivité"""
        self.start_inactivity_timer()
    
    def show_kaamelott(self):
        """Affiche une phrase de Kaamelott"""
        if not self.kaamelott_active and not self.get().strip():
            self.original_value = self.get()
            phrase = KaamelottResponses.get_impatience()
            self.delete(0, 'end')
            self.insert(0, phrase)
            self.config(foreground='orange')
            self.kaamelott_active = True
            
            # Programmer la prochaine phrase dans 60 secondes
            self.inactivity_timer = self.after(60000, self.update_kaamelott)
    
    def update_kaamelott(self):
        """Met à jour la phrase de Kaamelott"""
        if self.kaamelott_active:
            phrase = KaamelottResponses.get_impatience()
            self.delete(0, 'end')
            self.insert(0, phrase)
            # Programmer la prochaine mise à jour
            self.inactivity_timer = self.after(60000, self.update_kaamelott)
    
    def clear_kaamelott(self):
        """Efface la phrase de Kaamelott"""
        if self.kaamelott_active:
            self.delete(0, 'end')
            self.insert(0, self.original_value)
            self.config(foreground='black')
            self.kaamelott_active = False
    
    def get(self):
        """Override get() pour ignorer les phrases Kaamelott"""
        value = super().get()
        if self.kaamelott_active:
            return self.original_value
        return value