import tkinter as tk
from tkinter import ttk, messagebox
from core.user_manager import UserManager
from ui.widgets.custom_button import create_button

class SimplePseudoEditor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_manager = UserManager()
        
        # Label pseudo avec détection testeur
        from core.tester_auth import TesterAuth
        tester_auth = TesterAuth()
        current_pseudo = self.user_manager.get_username()
        
        if tester_auth.is_tester_code(current_pseudo):
            label_text = f"🧪 Testeur: {current_pseudo} (Mode testeur actif)"
        else:
            label_text = f"👤 Pseudo: {current_pseudo}"
        
        ttk.Label(self, text=label_text).pack(anchor='w')
        
        # Frame pour champ + bouton
        edit_frame = ttk.Frame(self)
        edit_frame.pack(fill='x', pady=(2, 0))
        
        self.pseudo_var = tk.StringVar()
        self.pseudo_entry = ttk.Entry(edit_frame, textvariable=self.pseudo_var, width=15, font=('Arial', 8))
        self.pseudo_entry.pack(side='left')
        self.pseudo_entry.insert(0, "changer pseudo?")
        self.pseudo_entry.config(foreground='grey')
        
        # Events pour placeholder et Enter
        self.pseudo_entry.bind('<FocusIn>', self.on_focus_in)
        self.pseudo_entry.bind('<FocusOut>', self.on_focus_out)
        self.pseudo_entry.bind('<Return>', lambda e: self.save_pseudo())
        
        self.save_btn = create_button(edit_frame, "Enregistrer", self.save_pseudo, width=10, symbol="💾")
        self.save_btn.pack(side='left', padx=(5, 0))
    
    def on_focus_in(self, event):
        if self.pseudo_entry.get() == "changer pseudo?":
            self.pseudo_entry.delete(0, 'end')
            self.pseudo_entry.config(foreground='black')
    
    def on_focus_out(self, event):
        if not self.pseudo_entry.get():
            self.pseudo_entry.insert(0, "changer pseudo?")
            self.pseudo_entry.config(foreground='grey')
    
    def save_pseudo(self):
        pseudo = self.pseudo_var.get().strip()
        if pseudo and pseudo != "changer pseudo?":
            self.user_manager.set_username(pseudo)
            messagebox.showinfo("✅", f"Pseudo changé en: {pseudo}")
            # Vider le champ et remettre placeholder
            self.pseudo_entry.delete(0, 'end')
            self.pseudo_entry.insert(0, "changer pseudo?")
            self.pseudo_entry.config(foreground='grey')
            # Mettre à jour le label
            self.winfo_children()[0].config(text=f"👤 Pseudo: {pseudo}")
        else:
            messagebox.showwarning("⚠️", "Entrez un nouveau pseudo !")