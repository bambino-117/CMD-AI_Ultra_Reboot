import tkinter as tk

class CustomTextArea:
    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(self.root, state='disabled', wrap='word', height=20)
        self.text_area.pack(fill='both', expand=True, padx=10, pady=(10, 0))

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + '\n')
        self.text_area.see('end')
        self.text_area.config(state='disabled')