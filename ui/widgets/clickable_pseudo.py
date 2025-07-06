import tkinter as tk
from tkinter import ttk
from core.user_manager import UserManager

class ClickablePseudo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_manager = UserManager()
        self.dropdown_visible = False
        
        # Label pseudo cliquable
        self.pseudo_label = ttk.Label(self, text=f"👤 {self.user_manager.get_username()}", 
                                     cursor="hand2", foreground="blue")
        self.pseudo_label.pack(side='left')
        self.pseudo_label.bind("<Button-1>", self.toggle_dropdown)
        
        # Frame dropdown (caché par défaut)
        self.dropdown_frame = ttk.Frame(self, relief='raised', borderwidth=1)
        
        # Champ de saisie
        self.new_pseudo_var = tk.StringVar()
        self.pseudo_entry = ttk.Entry(self.dropdown_frame, textvariable=self.new_pseudo_var, width=15)
        self.pseudo_entry.pack(padx=5, pady=2)
        
        # Boutons
        btn_frame = ttk.Frame(self.dropdown_frame)
        btn_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Button(btn_frame, text="✓", command=self.save_pseudo, width=3).pack(side='left')
        ttk.Button(btn_frame, text="✗", command=self.cancel_edit, width=3).pack(side='left', padx=(2,0))
        
        # Bind pour fermer en cliquant ailleurs
        self.bind_all("<Button-1>", self.check_click_outside)
    
    def toggle_dropdown(self, event=None):
        if self.dropdown_visible:
            self.hide_dropdown()
        else:
            self.show_dropdown()
    
    def show_dropdown(self):
        self.new_pseudo_var.set(self.user_manager.get_username())
        self.dropdown_frame.pack(side='left', padx=(10, 0))
        self.pseudo_entry.focus()
        self.pseudo_entry.select_range(0, 'end')
        self.dropdown_visible = True
    
    def hide_dropdown(self):
        self.dropdown_frame.pack_forget()
        self.dropdown_visible = False
    
    def save_pseudo(self):
        new_pseudo = self.new_pseudo_var.get().strip()
        if new_pseudo:
            self.user_manager.set_username(new_pseudo)
            self.pseudo_label.config(text=f"👤 {new_pseudo}")
        self.hide_dropdown()
    
    def cancel_edit(self):
        self.hide_dropdown()
    
    def check_click_outside(self, event):
        if self.dropdown_visible:
            # Vérifier si le clic est en dehors du dropdown
            widget = event.widget
            if widget not in [self.dropdown_frame, self.pseudo_entry]:
                try:
                    # Vérifier si c'est un enfant du dropdown
                    parent = widget
                    while parent:
                        if parent == self.dropdown_frame:
                            return
                        parent = parent.master
                    self.hide_dropdown()
                except:
                    self.hide_dropdown()