import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    def __init__(self, parent, placeholder="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['foreground']
        
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        
        self.put_placeholder()
        self.start_blink()
    
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color
    
    def focus_in(self, *args):
        if self['foreground'] == self.placeholder_color:
            self.delete('0', 'end')
            self['foreground'] = self.default_fg_color
    
    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()
    
    def start_blink(self):
        if self['foreground'] == self.placeholder_color:
            current_color = self['foreground']
            new_color = 'lightgrey' if current_color == 'grey' else 'grey'
            self['foreground'] = new_color
        self.after(800, self.start_blink)
    
    def get(self):
        value = super().get()
        if value == self.placeholder:
            return ""
        return value