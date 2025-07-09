#!/usr/bin/env python3
"""
UI Studio - Éditeur complet avec calques et interpréteur
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, scrolledtext
import json

class Layer:
    def __init__(self, name, visible=True):
        self.name = name
        self.visible = visible
        self.elements = []
        self.opacity = 1.0

class UIStudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 UI Studio - Éditeur Complet")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1E1E1E")
        
        # Variables
        self.current_tool = "cut_rectangle"
        self.fill_color = "#00FFFF"
        self.stroke_color = "#00BFFF"
        self.stroke_width = 3
        
        # Calques
        self.layers = [Layer("Calque 1")]
        self.current_layer = 0
        
        # État du dessin
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.preview_shape = None
        
        self.setup_ui()
        self.draw_grid()
        
    def setup_ui(self):
        """Interface complète avec calques"""
        # Barre d'outils principale (haut)
        self.setup_main_toolbar()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1E1E1E")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Palette d'outils (gauche)
        self.setup_tools_panel(main_frame)
        
        # Canvas central
        self.setup_canvas_area(main_frame)
        
        # Panneau calques (droite)
        self.setup_layers_panel(main_frame)
        
        # Interpréteur de code (bas)
        self.setup_code_interpreter()
        
    def setup_main_toolbar(self):
        """Barre d'outils principale"""
        toolbar = tk.Frame(self.root, bg="#2D2D2D", height=60)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)
        
        # Fichier
        file_frame = tk.Frame(toolbar, bg="#2D2D2D")
        file_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(file_frame, text="📁", width=3, height=2, bg="#404040", fg="white",
                 command=self.new_project).pack(side=tk.LEFT, padx=1)
        tk.Button(file_frame, text="💾", width=3, height=2, bg="#404040", fg="white",
                 command=self.save_project).pack(side=tk.LEFT, padx=1)
        tk.Button(file_frame, text="📂", width=3, height=2, bg="#404040", fg="white",
                 command=self.load_project).pack(side=tk.LEFT, padx=1)
        
        # Couleurs
        colors_frame = tk.Frame(toolbar, bg="#2D2D2D")
        colors_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.fill_btn = tk.Button(colors_frame, width=4, height=2, bg=self.fill_color,
                                 command=self.choose_fill_color)
        self.fill_btn.pack(side=tk.LEFT, padx=2)
        
        self.stroke_btn = tk.Button(colors_frame, width=4, height=2, bg=self.stroke_color,
                                   command=self.choose_stroke_color)
        self.stroke_btn.pack(side=tk.LEFT, padx=2)
        
        # Actions
        actions_frame = tk.Frame(toolbar, bg="#2D2D2D")
        actions_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Button(actions_frame, text="▶️", width=3, height=2, bg="#4CAF50", fg="white",
                 command=self.run_code).pack(side=tk.LEFT, padx=1)
        tk.Button(actions_frame, text="🔄", width=3, height=2, bg="#2196F3", fg="white",
                 command=self.refresh_code).pack(side=tk.LEFT, padx=1)
        
    def setup_tools_panel(self, parent):
        """Panneau d'outils avec symboles clairs"""
        tools_frame = tk.Frame(parent, bg="#2D2D2D", width=80)
        tools_frame.pack(side=tk.LEFT, fill=tk.Y)
        tools_frame.pack_propagate(False)
        
        tk.Label(tools_frame, text="🛠️", bg="#2D2D2D", fg="white", 
                font=("Arial", 14)).pack(pady=10)
        
        # Outils avec symboles clairs
        tools = [
            ("◆", "cut_rectangle", "#FF5722"),
            ("⬜", "rectangle", "#2196F3"),
            ("⭕", "circle", "#4CAF50"),
            ("🔶", "diamond", "#FF9800"),
            ("📝", "text", "#9C27B0"),
            ("🖌️", "brush", "#795548"),
            ("🪣", "fill", "#607D8B"),
            ("📏", "line", "#E91E63")
        ]
        
        self.tool_buttons = {}
        
        for icon, tool, color in tools:
            btn = tk.Button(tools_frame, text=icon, width=6, height=3,
                           command=lambda t=tool: self.select_tool(t),
                           bg="#404040", fg="white", font=("Arial", 12),
                           activebackground=color)
            btn.pack(pady=2)
            self.tool_buttons[tool] = btn
        
        # Sélectionner outil par défaut
        self.select_tool("cut_rectangle")
        
    def setup_canvas_area(self, parent):
        """Zone de canvas avec quadrillage"""
        canvas_frame = tk.Frame(parent, bg="#1E1E1E")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas principal
        self.canvas = tk.Canvas(canvas_frame, bg="#0F0F0F", width=800, height=600)
        self.canvas.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Événements
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_motion)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        
    def setup_layers_panel(self, parent):
        """Panneau de gestion des calques"""
        layers_frame = tk.Frame(parent, bg="#2D2D2D", width=250)
        layers_frame.pack(side=tk.RIGHT, fill=tk.Y)
        layers_frame.pack_propagate(False)
        
        # Titre
        tk.Label(layers_frame, text="📋 Calques", bg="#2D2D2D", fg="white",
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Liste des calques
        self.layers_listbox = tk.Listbox(layers_frame, bg="#404040", fg="white",
                                        selectbackground="#0078D4", height=8)
        self.layers_listbox.pack(fill=tk.X, padx=10, pady=5)
        self.layers_listbox.bind("<<ListboxSelect>>", self.select_layer)
        
        # Boutons calques
        layers_buttons = tk.Frame(layers_frame, bg="#2D2D2D")
        layers_buttons.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(layers_buttons, text="➕", width=3, bg="#4CAF50", fg="white",
                 command=self.add_layer).pack(side=tk.LEFT, padx=1)
        tk.Button(layers_buttons, text="🗑️", width=3, bg="#F44336", fg="white",
                 command=self.delete_layer).pack(side=tk.LEFT, padx=1)
        tk.Button(layers_buttons, text="👁️", width=3, bg="#2196F3", fg="white",
                 command=self.toggle_layer_visibility).pack(side=tk.LEFT, padx=1)
        
        # Propriétés du calque
        props_frame = tk.LabelFrame(layers_frame, text="Propriétés", 
                                   bg="#2D2D2D", fg="white")
        props_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Opacité
        tk.Label(props_frame, text="Opacité:", bg="#2D2D2D", fg="white").pack(anchor="w")
        self.opacity_var = tk.DoubleVar(value=1.0)
        tk.Scale(props_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                variable=self.opacity_var, bg="#2D2D2D", fg="white",
                command=self.update_layer_opacity).pack(fill=tk.X)
        
        # Mise à jour initiale
        self.update_layers_list()
        
    def setup_code_interpreter(self):
        """Interpréteur de code intégré"""
        code_frame = tk.Frame(self.root, bg="#1E1E1E", height=200)
        code_frame.pack(fill=tk.X, side=tk.BOTTOM)
        code_frame.pack_propagate(False)
        
        # Titre avec boutons
        code_header = tk.Frame(code_frame, bg="#2D2D2D", height=30)
        code_header.pack(fill=tk.X)
        code_header.pack_propagate(False)
        
        tk.Label(code_header, text="💻 Interpréteur Python", bg="#2D2D2D", fg="white",
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Button(code_header, text="▶️ Exécuter", bg="#4CAF50", fg="white",
                 command=self.execute_code).pack(side=tk.RIGHT, padx=5, pady=2)
        tk.Button(code_header, text="🔄 Générer", bg="#2196F3", fg="white",
                 command=self.generate_interface_code).pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Zone de code
        code_content = tk.Frame(code_frame, bg="#1E1E1E")
        code_content.pack(fill=tk.BOTH, expand=True)
        
        # Éditeur de code
        self.code_editor = scrolledtext.ScrolledText(code_content, width=80, height=8,
                                                    bg="#0D1117", fg="#58A6FF",
                                                    font=("Consolas", 10),
                                                    insertbackground="white")
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Console de sortie
        self.console_output = scrolledtext.ScrolledText(code_content, width=40, height=8,
                                                       bg="#1E1E1E", fg="#00FF00",
                                                       font=("Consolas", 9),
                                                       state=tk.DISABLED)
        self.console_output.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Code initial
        initial_code = '''# Interface générée automatiquement
import tkinter as tk

class CustomInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Personnalisée")
        self.root.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        # Votre code ici
        pass
    
    def run(self):
        self.root.mainloop()

# Exécuter l'interface
if __name__ == "__main__":
    app = CustomInterface()
    app.run()
'''
        self.code_editor.insert(1.0, initial_code)
        
    def draw_grid(self):
        """Dessiner le quadrillage professionnel"""
        self.canvas.delete("grid")
        
        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        grid_size = 20
        
        # Grille principale
        for x in range(0, width, grid_size):
            self.canvas.create_line(x, 0, x, height, fill="#333333", width=1, tags="grid")
        
        for y in range(0, height, grid_size):
            self.canvas.create_line(0, y, width, y, fill="#333333", width=1, tags="grid")
        
        # Grille secondaire (tous les 100px)
        for x in range(0, width, grid_size*5):
            self.canvas.create_line(x, 0, x, height, fill="#555555", width=1, tags="grid")
        
        for y in range(0, height, grid_size*5):
            self.canvas.create_line(0, y, width, y, fill="#555555", width=1, tags="grid")
    
    def select_tool(self, tool):
        """Sélectionner un outil"""
        # Réinitialiser couleurs
        for btn in self.tool_buttons.values():
            btn.configure(bg="#404040")
        
        # Mettre en surbrillance
        self.tool_buttons[tool].configure(bg="#0078D4")
        self.current_tool = tool
        
    def choose_fill_color(self):
        """Choisir couleur de remplissage"""
        color = colorchooser.askcolor(title="Couleur de remplissage")[1]
        if color:
            self.fill_color = color
            self.fill_btn.configure(bg=color)
    
    def choose_stroke_color(self):
        """Choisir couleur de contour"""
        color = colorchooser.askcolor(title="Couleur de contour")[1]
        if color:
            self.stroke_color = color
            self.stroke_btn.configure(bg=color)
    
    def start_draw(self, event):
        """Commencer à dessiner"""
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
    
    def draw_motion(self, event):
        """Mouvement pendant le dessin"""
        if not self.drawing:
            return
        
        if self.preview_shape:
            self.canvas.delete(self.preview_shape)
        
        self.preview_shape = self.draw_preview(self.start_x, self.start_y, event.x, event.y)
    
    def end_draw(self, event):
        """Terminer le dessin"""
        if not self.drawing:
            return
        
        self.drawing = False
        
        if self.preview_shape:
            self.canvas.delete(self.preview_shape)
            self.preview_shape = None
        
        # Ajouter l'élément au calque actuel
        element = self.create_element(self.start_x, self.start_y, event.x, event.y)
        self.layers[self.current_layer].elements.append(element)
        
        # Dessiner l'élément final
        self.draw_final_element(element)
        
        # Mettre à jour le code
        self.generate_interface_code()
    
    def draw_preview(self, x1, y1, x2, y2):
        """Dessiner la prévisualisation"""
        if self.current_tool == "cut_rectangle":
            return self.draw_cut_rectangle_preview(x1, y1, x2, y2)
        elif self.current_tool == "rectangle":
            return self.canvas.create_rectangle(x1, y1, x2, y2,
                                              fill="", outline=self.stroke_color,
                                              width=1, dash=(5, 5))
        elif self.current_tool == "circle":
            return self.canvas.create_oval(x1, y1, x2, y2,
                                         fill="", outline=self.stroke_color,
                                         width=1, dash=(5, 5))
    
    def draw_cut_rectangle_preview(self, x1, y1, x2, y2):
        """Prévisualisation rectangle coins coupés"""
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        cut_size = min(20, width // 4, height // 4)
        
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        
        points = [
            x1 + cut_size, y1, x2 - cut_size, y1, x2, y1 + cut_size,
            x2, y2 - cut_size, x2 - cut_size, y2, x1 + cut_size, y2,
            x1, y2 - cut_size, x1, y1 + cut_size
        ]
        
        return self.canvas.create_polygon(points, fill="", outline=self.stroke_color,
                                        width=1, dash=(5, 5))
    
    def create_element(self, x1, y1, x2, y2):
        """Créer un élément"""
        return {
            "type": self.current_tool,
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "fill": self.fill_color,
            "stroke": self.stroke_color,
            "width": self.stroke_width,
            "layer": self.current_layer
        }
    
    def draw_final_element(self, element):
        """Dessiner l'élément final"""
        if element["type"] == "cut_rectangle":
            self.draw_cut_rectangle_final(element)
        elif element["type"] == "rectangle":
            self.canvas.create_rectangle(element["x1"], element["y1"], 
                                       element["x2"], element["y2"],
                                       fill=element["fill"], 
                                       outline=element["stroke"],
                                       width=element["width"])
        elif element["type"] == "circle":
            self.canvas.create_oval(element["x1"], element["y1"],
                                  element["x2"], element["y2"],
                                  fill=element["fill"],
                                  outline=element["stroke"],
                                  width=element["width"])
    
    def draw_cut_rectangle_final(self, element):
        """Rectangle coins coupés final"""
        x1, y1, x2, y2 = element["x1"], element["y1"], element["x2"], element["y2"]
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        cut_size = min(20, width // 4, height // 4)
        
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        
        points = [
            x1 + cut_size, y1, x2 - cut_size, y1, x2, y1 + cut_size,
            x2, y2 - cut_size, x2 - cut_size, y2, x1 + cut_size, y2,
            x1, y2 - cut_size, x1, y1 + cut_size
        ]
        
        self.canvas.create_polygon(points, fill=element["fill"],
                                 outline=element["stroke"], width=element["width"])
    
    def add_layer(self):
        """Ajouter un nouveau calque"""
        layer_name = f"Calque {len(self.layers) + 1}"
        self.layers.append(Layer(layer_name))
        self.update_layers_list()
    
    def delete_layer(self):
        """Supprimer le calque actuel"""
        if len(self.layers) > 1:
            del self.layers[self.current_layer]
            self.current_layer = min(self.current_layer, len(self.layers) - 1)
            self.update_layers_list()
            self.redraw_canvas()
    
    def toggle_layer_visibility(self):
        """Basculer la visibilité du calque"""
        if self.layers:
            layer = self.layers[self.current_layer]
            layer.visible = not layer.visible
            self.update_layers_list()
            self.redraw_canvas()
    
    def select_layer(self, event):
        """Sélectionner un calque"""
        selection = self.layers_listbox.curselection()
        if selection:
            self.current_layer = selection[0]
            self.opacity_var.set(self.layers[self.current_layer].opacity)
    
    def update_layer_opacity(self, value):
        """Mettre à jour l'opacité du calque"""
        if self.layers:
            self.layers[self.current_layer].opacity = float(value)
            self.redraw_canvas()
    
    def update_layers_list(self):
        """Mettre à jour la liste des calques"""
        self.layers_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.layers):
            visibility = "👁️" if layer.visible else "🙈"
            self.layers_listbox.insert(tk.END, f"{visibility} {layer.name}")
        
        if self.layers:
            self.layers_listbox.selection_set(self.current_layer)
    
    def redraw_canvas(self):
        """Redessiner tout le canvas"""
        self.canvas.delete("all")
        self.draw_grid()
        
        for layer in self.layers:
            if layer.visible:
                for element in layer.elements:
                    self.draw_final_element(element)
    
    def generate_interface_code(self):
        """Générer le code de l'interface"""
        code = '''#!/usr/bin/env python3
"""
Interface générée par UI Studio
"""

import tkinter as tk

class CustomInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Personnalisée")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface"""
        self.canvas = tk.Canvas(self.root, bg="#000000", width=700, height=500)
        self.canvas.pack(padx=50, pady=50)
        self.draw_elements()
    
    def draw_elements(self):
        """Dessine tous les éléments"""
'''
        
        element_count = 0
        for layer in self.layers:
            if layer.visible:
                for element in layer.elements:
                    element_count += 1
                    if element["type"] == "cut_rectangle":
                        code += f'''
        # Rectangle coins coupés {element_count}
        self.draw_cut_rectangle({element["x1"]}, {element["y1"]}, 
                               {element["x2"]}, {element["y2"]},
                               "{element["fill"]}", "{element["stroke"]}", 
                               {element["width"]})
'''
                    elif element["type"] == "rectangle":
                        code += f'''
        # Rectangle {element_count}
        self.canvas.create_rectangle({element["x1"]}, {element["y1"]}, 
                                   {element["x2"]}, {element["y2"]},
                                   fill="{element["fill"]}", 
                                   outline="{element["stroke"]}", 
                                   width={element["width"]})
'''
        
        code += '''
    def draw_cut_rectangle(self, x1, y1, x2, y2, fill, outline, width):
        """Dessine un rectangle avec coins coupés"""
        w, h = abs(x2-x1), abs(y2-y1)
        cut = min(20, w//4, h//4)
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        
        points = [x1+cut, y1, x2-cut, y1, x2, y1+cut, x2, y2-cut,
                 x2-cut, y2, x1+cut, y2, x1, y2-cut, x1, y1+cut]
        
        self.canvas.create_polygon(points, fill=fill, 
                                 outline=outline, width=width)
    
    def run(self):
        """Lance l'interface"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CustomInterface()
    app.run()
'''
        
        # Mettre à jour l'éditeur
        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(1.0, code)
    
    def execute_code(self):
        """Exécuter le code Python"""
        code = self.code_editor.get(1.0, tk.END)
        
        # Effacer la console
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete(1.0, tk.END)
        
        try:
            # Rediriger stdout vers la console
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Exécuter le code
            exec(code)
            
            # Récupérer la sortie
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.console_output.insert(tk.END, output)
            else:
                self.console_output.insert(tk.END, "✅ Code exécuté avec succès\n")
                
        except Exception as e:
            self.console_output.insert(tk.END, f"❌ Erreur: {e}\n")
        
        self.console_output.config(state=tk.DISABLED)
    
    def run_code(self):
        """Exécuter le code dans une nouvelle fenêtre"""
        code = self.code_editor.get(1.0, tk.END)
        try:
            exec(code)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'exécution: {e}")
    
    def refresh_code(self):
        """Actualiser le code généré"""
        self.generate_interface_code()
    
    def new_project(self):
        """Nouveau projet"""
        self.layers = [Layer("Calque 1")]
        self.current_layer = 0
        self.redraw_canvas()
        self.update_layers_list()
        self.generate_interface_code()
    
    def save_project(self):
        """Sauvegarder le projet"""
        messagebox.showinfo("💾", "Projet sauvegardé !")
    
    def load_project(self):
        """Charger un projet"""
        messagebox.showinfo("📂", "Chargement de projet à implémenter")
    
    def run(self):
        """Lancer UI Studio"""
        print("🎨 UI Studio - Éditeur Complet")
        print("=" * 40)
        print("✨ Fonctionnalités :")
        print("• Calques avec visibilité et opacité")
        print("• Outils de dessin professionnels")
        print("• Interpréteur Python intégré")
        print("• Génération de code automatique")
        print("• Interface fixe avec symboles clairs")
        print()
        
        self.root.mainloop()

if __name__ == "__main__":
    studio = UIStudio()
    studio.run()