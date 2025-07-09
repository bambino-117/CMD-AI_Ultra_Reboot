#!/usr/bin/env python3
"""
Système de design d'interface personnalisée
Permet de créer des interfaces avec éditeur visuel
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import json
import os
from PIL import Image, ImageTk, ImageDraw
import io

class InterfaceDesigner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Designer d'Interface - CMD-AI Ultra Reboot")
        self.root.geometry("1200x800")
        
        self.current_design = {
            "name": "Interface Personnalisée",
            "background": "#000000",
            "elements": [],
            "theme_colors": {}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface du designer"""
        # Menu principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_design)
        file_menu.add_command(label="Ouvrir", command=self.open_design)
        file_menu.add_command(label="Sauvegarder", command=self.save_design)
        file_menu.add_separator()
        file_menu.add_command(label="Exporter PNG", command=self.export_png)
        file_menu.add_command(label="Générer Code", command=self.generate_code)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panneau d'outils (gauche)
        tools_frame = ttk.LabelFrame(main_frame, text="🛠️ Outils", width=250)
        tools_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        tools_frame.pack_propagate(False)
        
        self.setup_tools_panel(tools_frame)
        
        # Zone de design (centre)
        design_frame = ttk.LabelFrame(main_frame, text="🎨 Zone de Design")
        design_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.setup_design_area(design_frame)
        
        # Panneau propriétés (droite)
        props_frame = ttk.LabelFrame(main_frame, text="⚙️ Propriétés", width=250)
        props_frame.pack(side=tk.RIGHT, fill=tk.Y)
        props_frame.pack_propagate(False)
        
        self.setup_properties_panel(props_frame)
    
    def setup_tools_panel(self, parent):
        """Configure le panneau d'outils"""
        # Couleurs de base
        colors_frame = ttk.LabelFrame(parent, text="🎨 Couleurs")
        colors_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Fond
        bg_frame = ttk.Frame(colors_frame)
        bg_frame.pack(fill=tk.X, pady=2)
        ttk.Label(bg_frame, text="Fond:").pack(side=tk.LEFT)
        self.bg_color_btn = tk.Button(bg_frame, width=3, bg="#000000", command=self.choose_bg_color)
        self.bg_color_btn.pack(side=tk.RIGHT)
        
        # Texte
        text_frame = ttk.Frame(colors_frame)
        text_frame.pack(fill=tk.X, pady=2)
        ttk.Label(text_frame, text="Texte:").pack(side=tk.LEFT)
        self.text_color_btn = tk.Button(text_frame, width=3, bg="#FFFFFF", command=self.choose_text_color)
        self.text_color_btn.pack(side=tk.RIGHT)
        
        # Accent
        accent_frame = ttk.Frame(colors_frame)
        accent_frame.pack(fill=tk.X, pady=2)
        ttk.Label(accent_frame, text="Accent:").pack(side=tk.LEFT)
        self.accent_color_btn = tk.Button(accent_frame, width=3, bg="#00BFFF", command=self.choose_accent_color)
        self.accent_color_btn.pack(side=tk.RIGHT)
        
        # Éléments
        elements_frame = ttk.LabelFrame(parent, text="📦 Éléments")
        elements_frame.pack(fill=tk.X, padx=5, pady=5)
        
        elements = [
            ("📝 Zone de Texte", "textarea"),
            ("🔘 Bouton", "button"),
            ("📥 Champ de Saisie", "entry"),
            ("🏷️ Label", "label"),
            ("📋 Frame", "frame"),
            ("🖼️ Image", "image")
        ]
        
        for text, elem_type in elements:
            btn = ttk.Button(elements_frame, text=text, 
                           command=lambda t=elem_type: self.add_element(t))
            btn.pack(fill=tk.X, pady=1)
        
        # Styles
        styles_frame = ttk.LabelFrame(parent, text="✨ Styles")
        styles_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bordures
        border_frame = ttk.Frame(styles_frame)
        border_frame.pack(fill=tk.X, pady=2)
        ttk.Label(border_frame, text="Bordure:").pack(side=tk.LEFT)
        self.border_width = tk.IntVar(value=1)
        border_spin = ttk.Spinbox(border_frame, from_=0, to=10, width=5, textvariable=self.border_width)
        border_spin.pack(side=tk.RIGHT)
        
        # Coins
        corner_frame = ttk.Frame(styles_frame)
        corner_frame.pack(fill=tk.X, pady=2)
        ttk.Label(corner_frame, text="Coins:").pack(side=tk.LEFT)
        self.corner_radius = tk.IntVar(value=5)
        corner_spin = ttk.Spinbox(corner_frame, from_=0, to=50, width=5, textvariable=self.corner_radius)
        corner_spin.pack(side=tk.RIGHT)
        
        # Transparence
        trans_frame = ttk.Frame(styles_frame)
        trans_frame.pack(fill=tk.X, pady=2)
        ttk.Label(trans_frame, text="Opacité:").pack(side=tk.LEFT)
        self.opacity = tk.DoubleVar(value=1.0)
        opacity_scale = ttk.Scale(trans_frame, from_=0.1, to=1.0, variable=self.opacity, orient=tk.HORIZONTAL)
        opacity_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def setup_design_area(self, parent):
        """Configure la zone de design"""
        # Canvas pour le design
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#000000", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scroll.set)
        
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=h_scroll.set)
        
        # Événements
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        self.selected_element = None
        self.drag_start = None
    
    def setup_properties_panel(self, parent):
        """Configure le panneau des propriétés"""
        # Propriétés de l'élément sélectionné
        self.props_frame = ttk.Frame(parent)
        self.props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(self.props_frame, text="Sélectionnez un élément", font=("Arial", 10, "italic")).pack(pady=20)
        
        # Prévisualisation
        preview_frame = ttk.LabelFrame(parent, text="👁️ Aperçu")
        preview_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=200, height=150, bg="#f0f0f0")
        self.preview_canvas.pack(padx=5, pady=5)
        
        # Actions
        actions_frame = ttk.LabelFrame(parent, text="🎬 Actions")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(actions_frame, text="🔄 Actualiser", command=self.refresh_design).pack(fill=tk.X, pady=1)
        ttk.Button(actions_frame, text="🗑️ Supprimer", command=self.delete_selected).pack(fill=tk.X, pady=1)
        ttk.Button(actions_frame, text="📋 Dupliquer", command=self.duplicate_selected).pack(fill=tk.X, pady=1)
    
    def choose_bg_color(self):
        """Choisir la couleur de fond"""
        color = colorchooser.askcolor(title="Couleur de fond")[1]
        if color:
            self.bg_color_btn.configure(bg=color)
            self.canvas.configure(bg=color)
            self.current_design["background"] = color
    
    def choose_text_color(self):
        """Choisir la couleur de texte"""
        color = colorchooser.askcolor(title="Couleur de texte")[1]
        if color:
            self.text_color_btn.configure(bg=color)
            self.current_design["theme_colors"]["text"] = color
    
    def choose_accent_color(self):
        """Choisir la couleur d'accent"""
        color = colorchooser.askcolor(title="Couleur d'accent")[1]
        if color:
            self.accent_color_btn.configure(bg=color)
            self.current_design["theme_colors"]["accent"] = color
    
    def add_element(self, element_type):
        """Ajouter un élément au design"""
        element = {
            "type": element_type,
            "x": 50,
            "y": 50,
            "width": 100,
            "height": 30,
            "text": f"Nouvel {element_type}",
            "color": self.text_color_btn.cget("bg"),
            "bg_color": self.accent_color_btn.cget("bg"),
            "border_width": self.border_width.get(),
            "corner_radius": self.corner_radius.get(),
            "opacity": self.opacity.get()
        }
        
        self.current_design["elements"].append(element)
        self.draw_element(element)
    
    def draw_element(self, element):
        """Dessiner un élément sur le canvas"""
        x, y = element["x"], element["y"]
        w, h = element["width"], element["height"]
        
        if element["type"] == "button":
            # Dessiner un bouton avec coins arrondis
            self.canvas.create_rectangle(x, y, x+w, y+h, 
                                       fill=element["bg_color"], 
                                       outline=element["color"],
                                       width=element["border_width"],
                                       tags=f"element_{len(self.current_design['elements'])-1}")
            
            self.canvas.create_text(x+w//2, y+h//2, 
                                  text=element["text"], 
                                  fill=element["color"],
                                  tags=f"element_{len(self.current_design['elements'])-1}")
        
        elif element["type"] == "entry":
            self.canvas.create_rectangle(x, y, x+w, y+h, 
                                       fill="white", 
                                       outline=element["color"],
                                       width=element["border_width"],
                                       tags=f"element_{len(self.current_design['elements'])-1}")
        
        elif element["type"] == "label":
            self.canvas.create_text(x, y, 
                                  text=element["text"], 
                                  fill=element["color"],
                                  anchor="nw",
                                  tags=f"element_{len(self.current_design['elements'])-1}")
    
    def on_canvas_click(self, event):
        """Gestion du clic sur le canvas"""
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(clicked_item)
        
        if tags and tags[0].startswith("element_"):
            element_id = int(tags[0].split("_")[1])
            self.select_element(element_id)
            self.drag_start = (event.x, event.y)
    
    def select_element(self, element_id):
        """Sélectionner un élément"""
        self.selected_element = element_id
        self.show_element_properties(self.current_design["elements"][element_id])
    
    def show_element_properties(self, element):
        """Afficher les propriétés d'un élément"""
        # Nettoyer le panneau
        for widget in self.props_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.props_frame, text=f"Élément: {element['type']}", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Texte
        if element["type"] in ["button", "label"]:
            text_frame = ttk.Frame(self.props_frame)
            text_frame.pack(fill=tk.X, pady=2)
            ttk.Label(text_frame, text="Texte:").pack(side=tk.LEFT)
            text_var = tk.StringVar(value=element["text"])
            text_entry = ttk.Entry(text_frame, textvariable=text_var)
            text_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            text_var.trace("w", lambda *args: self.update_element_property("text", text_var.get()))
        
        # Position
        pos_frame = ttk.LabelFrame(self.props_frame, text="Position")
        pos_frame.pack(fill=tk.X, pady=5)
        
        x_frame = ttk.Frame(pos_frame)
        x_frame.pack(fill=tk.X, pady=1)
        ttk.Label(x_frame, text="X:").pack(side=tk.LEFT)
        x_var = tk.IntVar(value=element["x"])
        ttk.Spinbox(x_frame, from_=0, to=1000, textvariable=x_var, width=8).pack(side=tk.RIGHT)
        x_var.trace("w", lambda *args: self.update_element_property("x", x_var.get()))
        
        y_frame = ttk.Frame(pos_frame)
        y_frame.pack(fill=tk.X, pady=1)
        ttk.Label(y_frame, text="Y:").pack(side=tk.LEFT)
        y_var = tk.IntVar(value=element["y"])
        ttk.Spinbox(y_frame, from_=0, to=1000, textvariable=y_var, width=8).pack(side=tk.RIGHT)
        y_var.trace("w", lambda *args: self.update_element_property("y", y_var.get()))
    
    def update_element_property(self, prop, value):
        """Mettre à jour une propriété d'élément"""
        if self.selected_element is not None:
            self.current_design["elements"][self.selected_element][prop] = value
            self.refresh_design()
    
    def refresh_design(self):
        """Actualiser l'affichage du design"""
        self.canvas.delete("all")
        for element in self.current_design["elements"]:
            self.draw_element(element)
    
    def export_png(self):
        """Exporter le design en PNG"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            # Créer une image PIL
            width = int(self.canvas.cget("width"))
            height = int(self.canvas.cget("height"))
            
            img = Image.new("RGBA", (width, height), self.current_design["background"])
            draw = ImageDraw.Draw(img)
            
            # Dessiner les éléments
            for element in self.current_design["elements"]:
                x, y = element["x"], element["y"]
                w, h = element["width"], element["height"]
                
                if element["type"] == "button":
                    draw.rectangle([x, y, x+w, y+h], 
                                 fill=element["bg_color"], 
                                 outline=element["color"],
                                 width=element["border_width"])
            
            img.save(filename)
            messagebox.showinfo("✅", f"Design exporté : {filename}")
    
    def generate_code(self):
        """Générer le code Python pour l'interface"""
        code = f'''#!/usr/bin/env python3
"""
Interface générée par CMD-AI Interface Designer
"""

import tkinter as tk
from tkinter import ttk

class CustomInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("{self.current_design['name']}")
        self.root.configure(bg="{self.current_design['background']}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface"""
'''
        
        for i, element in enumerate(self.current_design["elements"]):
            if element["type"] == "button":
                code += f'''        
        # Bouton {i+1}
        btn_{i} = tk.Button(
            self.root,
            text="{element['text']}",
            bg="{element['bg_color']}",
            fg="{element['color']}",
            bd={element['border_width']}
        )
        btn_{i}.place(x={element['x']}, y={element['y']}, width={element['width']}, height={element['height']})
'''
        
        code += '''
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CustomInterface()
    app.run()
'''
        
        # Sauvegarder le code
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("✅", f"Code généré : {filename}")
    
    def new_design(self):
        """Nouveau design"""
        self.current_design = {
            "name": "Interface Personnalisée",
            "background": "#000000",
            "elements": [],
            "theme_colors": {}
        }
        self.canvas.delete("all")
        self.canvas.configure(bg="#000000")
    
    def save_design(self):
        """Sauvegarder le design"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_design, f, indent=2)
            messagebox.showinfo("✅", f"Design sauvegardé : {filename}")
    
    def open_design(self):
        """Ouvrir un design"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.current_design = json.load(f)
                self.refresh_design()
                messagebox.showinfo("✅", f"Design chargé : {filename}")
            except Exception as e:
                messagebox.showerror("❌", f"Erreur chargement : {e}")
    
    def delete_selected(self):
        """Supprimer l'élément sélectionné"""
        if self.selected_element is not None:
            del self.current_design["elements"][self.selected_element]
            self.selected_element = None
            self.refresh_design()
    
    def duplicate_selected(self):
        """Dupliquer l'élément sélectionné"""
        if self.selected_element is not None:
            element = self.current_design["elements"][self.selected_element].copy()
            element["x"] += 20
            element["y"] += 20
            self.current_design["elements"].append(element)
            self.refresh_design()
    
    def on_canvas_drag(self, event):
        """Gestion du glisser-déposer"""
        if self.selected_element is not None and self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            
            element = self.current_design["elements"][self.selected_element]
            element["x"] += dx
            element["y"] += dy
            
            self.drag_start = (event.x, event.y)
            self.refresh_design()
    
    def on_canvas_release(self, event):
        """Fin du glisser-déposer"""
        self.drag_start = None
    
    def run(self):
        """Lancer le designer"""
        self.root.mainloop()

def main():
    """Point d'entrée principal"""
    designer = InterfaceDesigner()
    designer.run()

if __name__ == "__main__":
    main()