import os
import importlib.util
import sys
from core.base_extension import BaseExtension

class ExtensionManager:
    def __init__(self, extensions_dir="extensions"):
        self.extensions_dir = extensions_dir
        self.loaded_extensions = {}
        self.app_context = None
    
    def set_app_context(self, context):
        """Définit le contexte de l'application pour les extensions"""
        self.app_context = context
    
    def load_extensions(self):
        """Charge toutes les extensions du dossier extensions"""
        if not os.path.exists(self.extensions_dir):
            return
        
        for filename in os.listdir(self.extensions_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                self._load_extension(filename)
    
    def _load_extension(self, filename):
        """Charge une extension spécifique"""
        try:
            extension_path = os.path.join(self.extensions_dir, filename)
            module_name = filename[:-3]  # Retire .py
            
            spec = importlib.util.spec_from_file_location(module_name, extension_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Cherche une classe qui hérite de BaseExtension
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseExtension) and 
                    attr != BaseExtension):
                    
                    extension_instance = attr()
                    if self.app_context:
                        extension_instance.initialize(self.app_context)
                    
                    self.loaded_extensions[extension_instance.name] = extension_instance
                    print(f"Extension chargée: {extension_instance.name}")
                    break
                    
        except Exception as e:
            print(f"Erreur lors du chargement de {filename}: {e}")
    
    def get_extension(self, name):
        """Récupère une extension par son nom"""
        return self.loaded_extensions.get(name)
    
    def list_extensions(self):
        """Liste toutes les extensions chargées"""
        return list(self.loaded_extensions.keys())
    
    def execute_extension_command(self, extension_name, command, args=None):
        """Exécute une commande d'extension"""
        extension = self.get_extension(extension_name)
        if extension and extension.enabled:
            return extension.execute(command, args)
        return f"Extension '{extension_name}' non trouvée ou désactivée"
    
    def get_all_commands(self):
        """Récupère toutes les commandes de toutes les extensions"""
        commands = {}
        for name, extension in self.loaded_extensions.items():
            if extension.enabled:
                commands[name] = extension.get_commands()
        return commands
    
    def enable_extension(self, name):
        """Active une extension"""
        if name in self.loaded_extensions:
            self.loaded_extensions[name].enable()
            return True
        return False
    
    def disable_extension(self, name):
        """Désactive une extension"""
        if name in self.loaded_extensions:
            self.loaded_extensions[name].disable()
            return True
        return False