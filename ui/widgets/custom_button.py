import tkinter as tk

class CustomButton(tk.Button):
    """Bouton minimaliste"""
    
    def __init__(self, parent, text="", command=None, width=8, symbol="•", **kwargs):
        # Formatage avec symbole à gauche
        formatted_text = f"{symbol} {text}"
        
        # Obtenir la couleur de fond
        try:
            bg_color = parent.cget('bg')
        except:
            bg_color = '#f0f0f0'  # Couleur par défaut
        
        super().__init__(parent, 
                        text=formatted_text, 
                        command=command,
                        width=width,
                        font=('Arial', 7),
                        relief='flat',
                        bd=0,
                        bg=bg_color,
                        fg='black',
                        activebackground='#e8e8e8',
                        **kwargs)

def create_button(parent, text, command=None, width=8, symbol="•"):
    """Fonction helper pour créer des boutons uniformes"""
    return CustomButton(parent, text=text, command=command, width=width, symbol=symbol)