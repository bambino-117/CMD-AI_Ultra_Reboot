import tkinter as tk
from tkinter import Canvas

class ImperialTile(tk.Frame):
    def __init__(self, parent, plugin, is_installed, bg_color, text_color, click_callback):
        super().__init__(parent, bg='#0D1117', width=240, height=180)
        self.pack_propagate(False)
        
        self.plugin = plugin
        self.is_installed = is_installed
        self.bg_color = bg_color
        self.text_color = text_color
        self.click_callback = click_callback
        
        self.create_imperial_design()
        self.setup_content()
        self.bind_events()
    
    def create_imperial_design(self):
        """Crée le design style caisse impériale avec coins coupés"""
        # Canvas principal pour le design personnalisé
        self.canvas = Canvas(
            self,
            width=240,
            height=180,
            bg='#0D1117',
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Dessiner la forme avec coins coupés
        self.draw_imperial_shape()
        
        # Ajouter les bandes croisées
        self.draw_cross_bands()
        
        # Ajouter l'indicateur de statut (point gris avec point vert)
        self.draw_status_indicator()
    
    def draw_imperial_shape(self):
        """Dessine la forme principale avec coins coupés"""
        # Coordonnées pour forme avec coins coupés (style Empire)
        points = [
            20, 10,   # Coin haut-gauche coupé
            220, 10,  # Haut
            230, 20,  # Coin haut-droite coupé
            230, 160, # Droite
            220, 170, # Coin bas-droite coupé
            20, 170,  # Bas
            10, 160,  # Coin bas-gauche coupé
            10, 20    # Gauche
        ]
        
        # Fond principal
        self.canvas.create_polygon(
            points,
            fill=self.bg_color,
            outline='#555555',
            width=2
        )
        
        # Effet de profondeur (ombre interne)
        shadow_points = [
            22, 12,
            218, 12,
            228, 22,
            228, 158,
            218, 168,
            22, 168,
            12, 158,
            12, 22
        ]
        
        self.canvas.create_polygon(
            shadow_points,
            fill='',
            outline='#333333',
            width=1
        )
    
    def draw_cross_bands(self):
        """Dessine les bandes qui se croisent au centre"""
        center_x, center_y = 120, 90
        
        # Bande horizontale
        self.canvas.create_rectangle(
            30, center_y - 3,
            210, center_y + 3,
            fill='#444444',
            outline='#666666'
        )
        
        # Bande verticale
        self.canvas.create_rectangle(
            center_x - 3, 30,
            center_x + 3, 150,
            fill='#444444',
            outline='#666666'
        )
        
        # Point central de croisement
        self.canvas.create_oval(
            center_x - 4, center_y - 4,
            center_x + 4, center_y + 4,
            fill='#666666',
            outline='#888888'
        )
    
    def draw_status_indicator(self):
        """Dessine l'indicateur de statut (point gris avec point vert)"""
        # Position sur le côté droit
        indicator_x, indicator_y = 200, 30
        
        # Point gris externe
        self.canvas.create_oval(
            indicator_x - 8, indicator_y - 8,
            indicator_x + 8, indicator_y + 8,
            fill='#666666',
            outline='#888888',
            width=1
        )
        
        # Point vert interne (plus petit)
        status_color = '#00FF00' if self.is_installed else '#FF6B6B'
        self.canvas.create_oval(
            indicator_x - 4, indicator_y - 4,
            indicator_x + 4, indicator_y + 4,
            fill=status_color,
            outline='#FFFFFF',
            width=1
        )
    
    def setup_content(self):
        """Configure le contenu textuel de la tuile"""
        # Frame pour le contenu par-dessus le canvas
        content_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        # Nom de l'extension (style impérial)
        name_label = tk.Label(
            content_frame,
            text=self.plugin['name'].upper(),
            font=('Arial', 11, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        name_label.pack(pady=(15, 2))
        
        # Version
        version_label = tk.Label(
            content_frame,
            text=f"v{self.plugin['version']}",
            font=('Arial', 8),
            fg=self.text_color,
            bg=self.bg_color
        )
        version_label.pack()
        
        # Statut
        status_text = "INSTALLÉ" if self.is_installed else "DISPONIBLE"
        status_label = tk.Label(
            content_frame,
            text=status_text,
            font=('Arial', 8, 'bold'),
            fg='#00FF00' if self.is_installed else '#FFD700',
            bg=self.bg_color
        )
        status_label.pack(pady=2)
        
        # Description courte
        desc_text = self.plugin['description'][:35] + "..." if len(self.plugin['description']) > 35 else self.plugin['description']
        desc_label = tk.Label(
            content_frame,
            text=desc_text,
            font=('Arial', 7),
            fg=self.text_color,
            bg=self.bg_color,
            wraplength=180,
            justify='center'
        )
        desc_label.pack(pady=5)
        
        # Rating et downloads (en bas)
        stats_label = tk.Label(
            content_frame,
            text=f"⭐ {self.plugin['rating']} | 📊 {self.plugin['downloads']}",
            font=('Arial', 7),
            fg=self.text_color,
            bg=self.bg_color
        )
        stats_label.pack(side='bottom', pady=5)
        
        # Placer le frame de contenu sur le canvas
        self.canvas.create_window(120, 90, window=content_frame)
        
        # Stocker les widgets pour les événements
        self.content_widgets = [content_frame, name_label, version_label, status_label, desc_label, stats_label]
    
    def bind_events(self):
        """Configure les événements de clic et hover"""
        # Bind sur le canvas et tous les widgets
        widgets_to_bind = [self, self.canvas] + self.content_widgets
        
        for widget in widgets_to_bind:
            widget.bind("<Button-1>", self.on_click)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
    
    def on_click(self, event=None):
        """Gère le clic sur la tuile"""
        if self.click_callback:
            self.click_callback(self.plugin, self.is_installed)
    
    def on_enter(self, event=None):
        """Effet hover - entrée"""
        self.configure(cursor="hand2")
        # Effet de surbrillance
        self.canvas.create_rectangle(
            8, 8, 232, 172,
            outline='#FFD700',
            width=2,
            tags="hover_effect"
        )
    
    def on_leave(self, event=None):
        """Effet hover - sortie"""
        self.configure(cursor="")
        # Supprimer l'effet de surbrillance
        self.canvas.delete("hover_effect")