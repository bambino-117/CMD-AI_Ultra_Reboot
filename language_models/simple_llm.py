import random
from .base_llm import BaseLLM

class SimpleLLM(BaseLLM):
    """LLM simple avec réponses intelligentes sans API"""
    
    def __init__(self):
        super().__init__("IA Simple")
        self.is_available = True
        
        self.patterns = {
            'salut': ['Salut ! Comment puis-je t\'aider ?', 'Hello ! Que veux-tu savoir ?'],
            'bonjour': ['Bonjour ! Ravi de te parler !', 'Bonjour ! Comment ça va ?'],
            'comment': ['Bonne question ! Peux-tu être plus précis ?', 'Ça dépend du contexte...'],
            'pourquoi': ['C\'est complexe à expliquer...', 'Il y a plusieurs raisons possibles.'],
            'python': ['Python est un langage génial !', 'Python est parfait pour débuter en programmation.'],
            'code': ['Le code, c\'est de la logique pure !', 'Programmer, c\'est créer des solutions.'],
            'aide': ['Je suis là pour t\'aider !', 'Dis-moi ce dont tu as besoin.'],
            'merci': ['De rien !', 'Avec plaisir !', 'Content d\'avoir pu aider !'],
            'au revoir': ['À bientôt !', 'Au revoir !', 'Bonne journée !']
        }
        
        self.default_responses = [
            'Intéressant ! Peux-tu m\'en dire plus ?',
            'Je vois... Continue !',
            'C\'est une perspective intéressante.',
            'Hmm, laisse-moi réfléchir à ça.',
            'Bonne observation !',
            'Ça mérite réflexion.',
            'Je comprends ton point de vue.'
        ]
    
    def is_model_available(self):
        return True
    
    def generate_response(self, prompt, max_tokens=150):
        prompt_lower = prompt.lower()
        
        # Chercher des mots-clés
        for keyword, responses in self.patterns.items():
            if keyword in prompt_lower:
                return random.choice(responses)
        
        # Réponse par défaut
        return random.choice(self.default_responses)