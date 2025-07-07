import tkinter as tk
from tkinter import ttk
import random
import colorsys

class MarketplaceTiles:
    def __init__(self, parent, dispatcher):
        self.parent = parent
        self.dispatcher = dispatcher
        self.tiles_window = None
        self.colors_used = set()
    
    def generate_imperial_color(self):
        """Génère des couleurs style Empire (gris, bleus foncés, rouges sombres)"""
        imperial_colors = [
            '#2C3E50', '#34495E', '#1B2631', '#17202A',  # Gris Empire
            '#1F2937', '#374151', '#4B5563', '#6B7280',  # Gris modernes
            '#7F1D1D', '#991B1B', '#B91C1C', '#DC2626',  # Rouges sombres
            '#1E3A8A', '#1E40AF', '#2563EB', '#3B82F6',  # Bleus impériaux
            '#581C87', '#6B21A8', '#7C2D12', '#92400E'   # Violets/oranges sombres
        ]
        
        available_colors = [c for c in imperial_colors if c not in self.colors_used]
        if not available_colors:
            self.colors_used.clear()
            available_colors = imperial_colors
        
        color = random.choice(available_colors)
        self.colors_used.add(color)
        return color
    
    def get_contrasting_color(self, bg_color):
        """Retourne une couleur contrastante"""
        hex_color = bg_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return '#FFFFFF' if luminance < 0.5 else '#000000'
    
    def show_marketplace_tiles(self):
        """Affiche le marketplace avec des tuiles cliquables"""
        if self.tiles_window:
            self.tiles_window.destroy()
        
        # Créer une nouvelle fenêtre
        self.tiles_window = tk.Toplevel(self.parent.root)
        self.tiles_window.title("🔌 Marketplace - Extensions")
        self.tiles_window.geometry("800x600")
        self.tiles_window.configure(bg='#0D1117')  # Fond sombre style Empire
        
        # Frame principal avec scrollbar (fond noir)
        main_frame = tk.Frame(self.tiles_window, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(main_frame, bg='#0D1117', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Espace en haut (sans titre)
        spacer = tk.Frame(scrollable_frame, bg='#0D1117', height=10)
        spacer.pack()
        
        # Récupérer les extensions
        marketplace = self.dispatcher.plugin_manager.get_marketplace()
        plugins = marketplace.get('plugins', [])
        installed_plugins = {p['id'] for p in self.dispatcher.plugin_manager.installed_plugins['plugins']}
        
        # Créer les tuiles en grille (fond noir)
        tiles_frame = tk.Frame(scrollable_frame, bg='#000000')
        tiles_frame.pack(fill='both', expand=True)
        
        for i, plugin in enumerate(plugins):
            row = i // 3
            col = i % 3
            
            self.create_imperial_tile(tiles_frame, plugin, installed_plugins, row, col)
        
        # Pack le canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bouton fermer
        close_btn = tk.Button(
            self.tiles_window,
            text="❌ FERMER",
            command=self.tiles_window.destroy,
            bg='#7F1D1D',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=3
        )
        close_btn.pack(side='bottom', pady=10)
    
    def create_imperial_tile(self, parent, plugin, installed_plugins, row, col):
        """Crée une tuile style caisse impériale"""
        is_installed = plugin['id'] in installed_plugins
        bg_color = self.generate_imperial_color()
        text_color = self.get_contrasting_color(bg_color)
        
        # Créer la tuile impériale personnalisée
        from ui.imperial_tile_widget import ImperialTile
        
        tile = ImperialTile(
            parent, 
            plugin, 
            is_installed, 
            bg_color, 
            text_color,
            self.show_extension_detail
        )
        
        tile.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configurer le grid
        parent.grid_columnconfigure(col, weight=1)
    
    def on_tile_hover(self, widget, entering):
        """Effet hover sur les tuiles"""
        if entering:
            widget.configure(cursor="hand2")
        else:
            widget.configure(cursor="")
    
    def show_extension_detail(self, plugin, is_installed):
        """Affiche les détails d'une extension dans une fenêtre dédiée"""
        from ui.extension_detail_window import ExtensionDetailWindow
        
        detail_window = ExtensionDetailWindow(self.parent, plugin, is_installed, self.dispatcher)
        detail_window.show_detail_window()
    
    def get_extension_readme(self, plugin_id):
        """Génère un README pour l'extension"""
        readmes = {
            'weather': """🌤️ EXTENSION MÉTÉO

FONCTIONNALITÉS:
• Météo actuelle par ville
• Prévisions 3 jours
• Géolocalisation automatique
• Données météo détaillées

COMMANDES:
• ext Weather current [ville] - Météo actuelle
• ext Weather forecast [ville] - Prévisions
• ext Weather help - Aide complète

EXEMPLES:
• ext Weather current Paris
• ext Weather forecast London
• ext Weather current (utilise Paris par défaut)""",

            'filemanager': """📁 GESTIONNAIRE DE FICHIERS

FONCTIONNALITÉS:
• Recherche de fichiers par pattern
• Organisation automatique par type
• Détection de fichiers dupliqués
• Nettoyage des fichiers temporaires

COMMANDES:
• ext FileManager search [pattern] - Rechercher
• ext FileManager organize [dossier] - Organiser
• ext FileManager duplicate [dossier] - Doublons
• ext FileManager clean - Nettoyer

EXEMPLES:
• ext FileManager search "*.pdf"
• ext FileManager organize ~/Downloads
• ext FileManager duplicate .""",

            'networktools': """🌐 OUTILS RÉSEAU

FONCTIONNALITÉS:
• Test de connectivité (ping)
• Scan de ports réseau
• Test de vitesse internet
• Géolocalisation d'adresses IP
• Scan des réseaux WiFi

COMMANDES:
• ext NetworkTools ping [host] - Tester connexion
• ext NetworkTools scan [ip] - Scanner ports
• ext NetworkTools speed - Test vitesse
• ext NetworkTools ip [adresse] - Info IP
• ext NetworkTools wifi - Scanner WiFi

EXEMPLES:
• ext NetworkTools ping google.com
• ext NetworkTools scan 192.168.1.1
• ext NetworkTools speed""",

            'systemmonitor': """🖥️ MONITORING SYSTÈME

FONCTIONNALITÉS:
• Statut système complet
• Top des processus consommateurs
• Usage des disques
• Statistiques réseau
• Températures système
• Monitoring temps réel

COMMANDES:
• ext SystemMonitor status - Statut général
• ext SystemMonitor processes - Top processus
• ext SystemMonitor disk - Usage disques
• ext SystemMonitor network - Stats réseau
• ext SystemMonitor temp - Températures
• ext SystemMonitor monitor - Temps réel

EXEMPLES:
• ext SystemMonitor status
• ext SystemMonitor processes""",

            'texttools': """🔤 OUTILS DE TEXTE

FONCTIONNALITÉS:
• Recherche et remplacement regex
• Génération de hash (MD5, SHA256, etc.)
• Encodage/décodage (Base64, Hex, URL)
• Formatage de texte avancé
• Analyse et comptage de texte

COMMANDES:
• ext TextTools regex "pattern|texte" - Regex
• ext TextTools hash "texte|algo" - Hash
• ext TextTools encode "texte|format" - Encoder
• ext TextTools decode "texte|format" - Décoder
• ext TextTools format "texte|format" - Formater
• ext TextTools count "texte" - Analyser

EXEMPLES:
• ext TextTools hash "password|sha256"
• ext TextTools regex "\\d+|J'ai 25 ans"
• ext TextTools encode "Hello|base64" """
        }
        
        return readmes.get(plugin_id, f"""📖 README - {plugin_id.upper()}

Cette extension fait partie du marketplace CMD-AI Ultra Reboot.

Pour plus d'informations, utilisez:
ext {plugin_id} help

Consultez la documentation complète après installation.""")