#!/usr/bin/env python3
"""
Extension CMD-AI pour gérer les plugins d'éditeurs d'images
Remplace l'ancien GIMP Clone Studio
"""

import os
import sys
from core.base_extension import BaseExtension

class UIPluginManager(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "UIPluginManager"
        self.version = "1.0.0"
        self.description = "Gestionnaire de plugins pour éditeurs d'images"
        
        self.plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
    
    def initialize(self):
        """Initialiser l'extension"""
        return True
    
    def execute(self, command, args=None):
        """Exécuter une commande du gestionnaire de plugins"""
        if command == "install":
            return self.install_plugins()
        elif command == "uninstall":
            return self.uninstall_plugins()
        elif command == "status":
            return self.check_status()
        elif command == "help":
            return self.get_help()
        else:
            return self.get_help()
    
    def install_plugins(self):
        """Installer les plugins dans les éditeurs détectés"""
        try:
            # Importer l'installateur
            sys.path.append(os.path.join(self.plugins_dir, "shared"))
            from plugin_installer import PluginInstaller
            
            installer = PluginInstaller()
            results = installer.install_all()
            
            response = "🔌 **Installation des plugins UI**\n\n"
            
            if results:
                response += "**Résultats:**\n"
                for software, success in results.items():
                    status = "✅ Installé" if success else "❌ Échec"
                    response += f"- {software.upper()}: {status}\n"
                
                response += "\n**Instructions:**\n"
                response += "1. Redémarrez vos logiciels d'édition\n"
                response += "2. Cherchez 'UI Generator' dans les menus\n"
                response += "3. Ouvrez une image et analysez-la\n"
                response += "4. Le code Python sera généré automatiquement\n"
            else:
                response += "❌ Aucun logiciel détecté\n"
                response += "Installez GIMP ou Krita pour utiliser les plugins"
            
            return response
            
        except Exception as e:
            return f"❌ Erreur installation: {str(e)}"
    
    def uninstall_plugins(self):
        """Désinstaller les plugins"""
        try:
            sys.path.append(os.path.join(self.plugins_dir, "shared"))
            from plugin_installer import PluginInstaller
            
            installer = PluginInstaller()
            installer.uninstall_all()
            
            return "🗑️ **Plugins désinstallés**\n\nRedémarrez vos logiciels pour appliquer les changements."
            
        except Exception as e:
            return f"❌ Erreur désinstallation: {str(e)}"
    
    def check_status(self):
        """Vérifier le statut des plugins"""
        try:
            sys.path.append(os.path.join(self.plugins_dir, "shared"))
            from plugin_installer import PluginInstaller
            
            installer = PluginInstaller()
            detected = installer.detect_software()
            
            response = "📊 **Statut des plugins UI**\n\n"
            
            if detected:
                response += "**Logiciels détectés:**\n"
                for software, path in detected.items():
                    response += f"✅ {software.upper()}: {path}\n"
                
                response += "\n**Fonctionnalités:**\n"
                response += "- Analyse automatique d'images\n"
                response += "- Détection de boutons, champs, labels\n"
                response += "- Génération code Tkinter/PyQt\n"
                response += "- Interface intégrée dans l'éditeur\n"
            else:
                response += "❌ Aucun logiciel compatible détecté\n"
                response += "\n**Logiciels supportés:**\n"
                response += "- GIMP (toutes versions)\n"
                response += "- Krita (4.0+)\n"
                response += "- Photoshop (en développement)\n"
            
            return response
            
        except Exception as e:
            return f"❌ Erreur vérification: {str(e)}"
    
    def get_help(self):
        """Obtenir l'aide"""
        return """🎨 **Gestionnaire de Plugins UI**

**Commandes disponibles:**
- `ext UIPluginManager install` - Installer les plugins
- `ext UIPluginManager uninstall` - Désinstaller les plugins  
- `ext UIPluginManager status` - Vérifier le statut
- `ext UIPluginManager help` - Afficher cette aide

**Workflow:**
1. Installez les plugins avec `install`
2. Ouvrez GIMP/Krita
3. Créez/ouvrez une image d'interface
4. Utilisez le plugin 'UI Generator'
5. Obtenez le code Python automatiquement

**Remplacement:**
Cette extension remplace l'ancien GIMP Clone Studio par des plugins intégrés directement dans les éditeurs d'images professionnels."""

# Enregistrement de l'extension
def get_extension():
    return UIPluginManager()