import random
from .base_llm import BaseLLM
from core.logger import app_logger

class FallbackLLM(BaseLLM):
    """LLM de fallback - réponses prédéfinies quand aucun autre LLM n'est disponible"""
    
    def __init__(self):
        super().__init__("fallback")
        self.is_available = True
        
        self.responses = {
            "salut": ["Salut ! Comment puis-je t'aider ?", "Hello ! Que puis-je faire pour toi ?"],
            "bonjour": ["Bonjour ! Comment allez-vous ?", "Bonjour ! Ravi de vous voir !"],
            "aide": ["Je suis là pour vous aider ! Posez-moi vos questions.", "Comment puis-je vous assister ?"],
            "merci": ["De rien !", "Avec plaisir !", "C'est normal !"],
            "au revoir": ["Au revoir !", "À bientôt !", "Bonne journée !"],
            "comment": ["C'est une bonne question !", "Intéressant...", "Laissez-moi réfléchir..."],
            "pourquoi": ["Bonne question !", "C'est complexe...", "Il y a plusieurs raisons..."],
            "default": [
                "Je comprends votre question.",
                "C'est intéressant comme point de vue.",
                "Pouvez-vous me donner plus de détails ?",
                "Je vais essayer de vous aider avec ça.",
                "C'est un sujet fascinant !",
                "Hmm, laissez-moi y réfléchir...",
                "Je vois ce que vous voulez dire."
            ]
        }
    
    def is_model_available(self):
        return True
    
    def generate_response(self, prompt, max_tokens=150):
        try:
            prompt_lower = prompt.lower()
            
            # Chercher des mots-clés
            for keyword, responses in self.responses.items():
                if keyword in prompt_lower and keyword != "default":
                    response = random.choice(responses)
                    app_logger.debug(f"Réponse fallback pour '{keyword}': {response}", "FALLBACK_LLM")
                    return response
            
            # Réponse par défaut
            response = random.choice(self.responses["default"])
            app_logger.debug(f"Réponse fallback par défaut: {response}", "FALLBACK_LLM")
            return response
            
        except Exception as e:
            app_logger.error(f"Erreur fallback LLM: {e}", "FALLBACK_LLM")
            return "Je suis désolé, je ne peux pas répondre pour le moment."