from abc import ABC, abstractmethod

class BaseExtension(ABC):
    def __init__(self):
        self.name = "Extension"
        self.version = "1.0.0"
        self.description = "Extension de base"
        self.author = "Inconnu"
        self.enabled = True
    
    @abstractmethod
    def initialize(self, app_context):
        """Initialise l'extension avec le contexte de l'application"""
        pass
    
    @abstractmethod
    def execute(self, command, args=None):
        """Exécute une commande de l'extension"""
        pass
    
    def get_commands(self):
        """Retourne la liste des commandes supportées par l'extension"""
        return []
    
    def get_info(self):
        """Retourne les informations de l'extension"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'enabled': self.enabled,
            'commands': self.get_commands()
        }
    
    def enable(self):
        """Active l'extension"""
        self.enabled = True
    
    def disable(self):
        """Désactive l'extension"""
        self.enabled = False