from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Interface de base pour tous les modèles de langage"""
    
    def __init__(self, model_name="default"):
        self.model_name = model_name
        self.is_available = False
    
    @abstractmethod
    def generate_response(self, prompt, max_tokens=150):
        """Génère une réponse à partir d'un prompt"""
        pass
    
    @abstractmethod
    def is_model_available(self):
        """Vérifie si le modèle est disponible"""
        pass
    
    def get_model_info(self):
        """Retourne les infos du modèle"""
        return {
            "name": self.model_name,
            "available": self.is_available,
            "type": self.__class__.__name__
        }