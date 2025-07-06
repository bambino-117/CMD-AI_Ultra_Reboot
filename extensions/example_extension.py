from core.base_extension import BaseExtension

class ExampleExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "Exemple"
        self.version = "1.0.0"
        self.description = "Extension d'exemple pour démonstration"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        """Initialise l'extension"""
        self.app_context = app_context
        print(f"Extension {self.name} initialisée")
    
    def execute(self, command, args=None):
        """Exécute les commandes de l'extension"""
        if command == "hello":
            return f"Salut depuis l'extension {self.name}!"
        elif command == "info":
            return f"Extension: {self.name} v{self.version} - {self.description}"
        else:
            return f"Commande '{command}' non reconnue"
    
    def get_commands(self):
        """Retourne les commandes disponibles"""
        return ["hello", "info"]