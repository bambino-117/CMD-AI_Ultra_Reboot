import requests
from .base_llm import BaseLLM
from core.logger import app_logger

class HuggingFaceLLM(BaseLLM):
    """LLM gratuit via Hugging Face Inference API"""
    
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        super().__init__(model_name)
        self.base_url = "https://api-inference.huggingface.co/models"
        self.is_available = True  # Toujours disponible
    
    def is_model_available(self):
        return True
    
    def generate_response(self, prompt, max_tokens=150):
        try:
            url = f"{self.base_url}/{self.model_name}"
            payload = {"inputs": prompt, "parameters": {"max_length": max_tokens}}
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "Pas de réponse").replace(prompt, "").strip()
                return "Réponse générée"
            elif response.status_code == 503:
                return "Modèle en cours de chargement, réessayez dans 30s"
            else:
                return f"Erreur HF: {response.status_code}"
                
        except Exception as e:
            app_logger.error(f"Erreur HuggingFace: {e}", "HF_LLM")
            return "Erreur de connexion - Mode hors-ligne activé"