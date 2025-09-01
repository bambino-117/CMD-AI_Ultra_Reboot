import tkinter as tk
from tkinter import ttk
import random
import colorsys

class MarketplaceDisplay:
    def __init__(self, parent, dispatcher):
        self.parent = parent
        self.dispatcher = dispatcher
        self.colors_used = set()
    
    def generate_random_color(self):
        """Génère une couleur aléatoire non utilisée"""
        while True:
            # Générer une couleur HSV pour plus de variété
            hue = random.random()
            saturation = random.uniform(0.6, 1.0)
            value = random.uniform(0.4, 0.8)
            
            # Convertir en RGB
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            
            if hex_color not in self.colors_used:
                self.colors_used.add(hex_color)
                return hex_color
    
    def get_contrasting_color(self, bg_color):
        """Retourne une couleur contrastante (noir ou blanc)"""
        # Convertir hex en RGB
        hex_color = bg_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculer la luminance
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        
        # Retourner noir ou blanc selon la luminance
        return '#000000' if luminance > 0.5 else '#FFFFFF'
    
    def show_marketplace_grid(self):
        """Affiche le marketplace sous forme de grille colorée"""
        try:
            # Récupérer les extensions du marketplace
            marketplace = self.dispatcher.plugin_manager.get_marketplace()
            plugins = marketplace.get('plugins', [])
            
            if not plugins:
                self.parent.text_area.display_message("❌ Aucune extension disponible dans le marketplace")
                return
            
            # Créer le message d'en-tête
            header = "🔌 MARKETPLACE - EXTENSIONS DISPONIBLES\n"
            header += "=" * 50 + "\n\n"
            
            # Créer les cases colorées pour chaque extension
            grid_display = ""
            installed_plugins = {p['id'] for p in self.dispatcher.plugin_manager.installed_plugins['plugins']}
            
            for i, plugin in enumerate(plugins):
                # Générer une couleur aléatoire
                bg_color = self.generate_random_color()
                text_color = self.get_contrasting_color(bg_color)
                
                # Statut d'installation
                status = "✅ INSTALLÉ" if plugin['id'] in installed_plugins else "📥 DISPONIBLE"
                
                # Créer la case colorée (simulation textuelle)
                box_content = f"""
╔══════════════════════════════════════╗
║ {plugin['name']:<36} ║
║ {plugin['version']:<36} ║
║ {status:<36} ║
║                                      ║
║ {plugin['description'][:34]:<34}{'...' if len(plugin['description']) > 34 else '  '} ║
║                                      ║
║ 👤 {plugin['author']:<32} ║
║ 📂 {plugin['category']:<32} ║
║ ⭐ {plugin['rating']} | 📊 {plugin['downloads']:<20} ║
║                                      ║
║ 💡 plugin install {plugin['id']:<18} ║
╚══════════════════════════════════════╝
"""
                grid_display += box_content + "\n"
            
            # Afficher dans la zone de texte
            full_message = header + grid_display
            full_message += "\n💡 Commandes disponibles:\n"
            full_message += "• plugin list - Voir toutes les extensions\n"
            full_message += "• plugin install [id] - Installer une extension\n"
            full_message += "• plugin installed - Voir les extensions installées\n"
            
            self.parent.text_area.display_message(full_message)
            
        except Exception as e:
            self.parent.text_area.display_message(f"❌ Erreur affichage marketplace: {e}")
    
    def show_installed_extensions_grid(self):
        """Affiche les extensions installées"""
        try:
            installed = self.dispatcher.plugin_manager.installed_plugins['plugins']
            
            if not installed:
                self.parent.text_area.display_message("📦 Aucune extension installée\n💡 Utilisez le marketplace pour installer des extensions")
                return
            
            header = "✅ EXTENSIONS INSTALLÉES\n"
            header += "=" * 30 + "\n\n"
            
            grid_display = ""
            
            for plugin in installed:
                # Générer une couleur pour chaque extension installée
                bg_color = self.generate_random_color()
                
                box_content = f"""
╔════════════════════════════════╗
║ ✅ {plugin['name']:<26} ║
║ 📦 Version: {plugin['version']:<18} ║
║ 📅 Installé: {plugin['installed_at'][:10]:<16} ║
║                                ║
║ 🗑️ plugin remove {plugin['id']:<12} ║
╚════════════════════════════════╝
"""
                grid_display += box_content + "\n"
            
            full_message = header + grid_display
            full_message += f"\n📊 Total: {len(installed)} extension(s) installée(s)\n"
            full_message += "\n💡 Commandes:\n"
            full_message += "• plugin remove [id] - Désinstaller une extension\n"
            full_message += "• ext [nom] help - Aide d'une extension\n"
            
            self.parent.text_area.display_message(full_message)
            
        except Exception as e:
            self.parent.text_area.display_message(f"❌ Erreur affichage extensions installées: {e}")
    
    def refresh_marketplace_display(self):
        """Actualise l'affichage du marketplace"""
        self.colors_used.clear()  # Reset des couleurs
        self.parent.text_area.display_message("🔄 Actualisation du marketplace...")
        self.show_marketplace_grid()