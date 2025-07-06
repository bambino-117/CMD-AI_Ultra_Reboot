import re
import tkinter as tk

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.setup_tags()
    
    def setup_tags(self):
        """Configure les tags de coloration"""
        # Python
        self.text_widget.tag_config("keyword", foreground="#0066CC", font=("Consolas", 10, "bold"))
        self.text_widget.tag_config("string", foreground="#008000")
        self.text_widget.tag_config("comment", foreground="#808080", font=("Consolas", 10, "italic"))
        self.text_widget.tag_config("function", foreground="#800080", font=("Consolas", 10, "bold"))
        self.text_widget.tag_config("number", foreground="#FF6600")
        self.text_widget.tag_config("operator", foreground="#CC0000")
        
        # Code block background
        self.text_widget.tag_config("code_block", background="#F5F5F5", font=("Consolas", 10))
    
    def highlight_python(self, start_line, end_line):
        """Colore le code Python entre les lignes spécifiées"""
        # Mots-clés Python
        keywords = [
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 
            'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'break', 
            'continue', 'pass', 'and', 'or', 'not', 'in', 'is', 'lambda', 'True', 
            'False', 'None', 'self', 'super', 'print'
        ]
        
        for line_num in range(start_line, end_line + 1):
            line_start = f"{line_num}.0"
            line_end = f"{line_num}.end"
            line_text = self.text_widget.get(line_start, line_end)
            
            # Supprimer les anciens tags
            for tag in ["keyword", "string", "comment", "function", "number", "operator"]:
                self.text_widget.tag_remove(tag, line_start, line_end)
            
            # Commentaires (priorité haute)
            comment_match = re.search(r'#.*$', line_text)
            if comment_match:
                start_col = comment_match.start()
                end_col = comment_match.end()
                self.text_widget.tag_add("comment", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                continue
            
            # Strings
            for match in re.finditer(r'(["\'])(?:(?!\1)[^\\]|\\.)*\1', line_text):
                start_col = match.start()
                end_col = match.end()
                self.text_widget.tag_add("string", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
            
            # Nombres
            for match in re.finditer(r'\b\d+\.?\d*\b', line_text):
                start_col = match.start()
                end_col = match.end()
                self.text_widget.tag_add("number", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
            
            # Fonctions (def nom_fonction)
            func_match = re.search(r'def\s+(\w+)', line_text)
            if func_match:
                start_col = func_match.start(1)
                end_col = func_match.end(1)
                self.text_widget.tag_add("function", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
            
            # Mots-clés
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                for match in re.finditer(pattern, line_text):
                    start_col = match.start()
                    end_col = match.end()
                    self.text_widget.tag_add("keyword", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
            
            # Opérateurs
            for match in re.finditer(r'[+\-*/%=<>!&|^~]', line_text):
                start_col = match.start()
                end_col = match.end()
                self.text_widget.tag_add("operator", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
    
    def detect_and_highlight(self, text):
        """Détecte et colore les blocs de code dans le texte"""
        lines = text.split('\n')
        current_line = 1
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Détection bloc Python ```python
            if line.startswith('```python'):
                start_line = current_line + 1
                i += 1
                current_line += 1
                
                # Chercher la fin du bloc
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    i += 1
                    current_line += 1
                
                end_line = current_line - 1
                
                # Appliquer le background du bloc
                self.text_widget.tag_add("code_block", f"{start_line}.0", f"{end_line}.end")
                
                # Colorer le Python
                self.highlight_python(start_line, end_line)
            
            # Détection code inline (heuristique simple)
            elif any(keyword in line for keyword in ['def ', 'class ', 'import ', 'from ', 'print(']):
                self.text_widget.tag_add("code_block", f"{current_line}.0", f"{current_line}.end")
                self.highlight_python(current_line, current_line)
            
            i += 1
            current_line += 1