import tkinter as tk
from ui.widgets.syntax_highlighter import SyntaxHighlighter

class CustomTextArea:
    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(self.root, state='disabled', wrap='word', height=20, font=('Consolas', 10))
        self.text_area.pack(fill='both', expand=True, padx=10, pady=(10, 0))
        
        # Initialiser la coloration syntaxique
        self.highlighter = SyntaxHighlighter(self.text_area)
        self.syntax_enabled = True

    def display_message(self, message):
        self.text_area.config(state='normal')
        
        # Insérer le message
        start_pos = self.text_area.index('end-1c')
        self.text_area.insert('end', message + '\n')
        
        # Appliquer la coloration syntaxique si activée
        if self.syntax_enabled and self._contains_code(message):
            self.highlighter.detect_and_highlight(message)
        
        self.text_area.see('end')
        self.text_area.config(state='disabled')
    
    def _contains_code(self, text):
        """Détecte si le texte contient du code"""
        code_indicators = [
            '```', 'def ', 'class ', 'import ', 'from ', 'print(', 
            'function', 'var ', 'const ', '<html>', '<?php'
        ]
        return any(indicator in text for indicator in code_indicators)
    
    def toggle_syntax_highlighting(self):
        """Active/désactive la coloration syntaxique"""
        self.syntax_enabled = not self.syntax_enabled
        return "🎨 Coloration activée" if self.syntax_enabled else "🎨 Coloration désactivée"