import requests
import json
from .base_llm import BaseLLM
from core.logger import app_logger

class OllamaLLM(BaseLLM):
    """LLM utilisant Ollama (ultra léger, local)"""
    
    def __init__(self, model_name="phi3:mini", host="http://localhost:11434"):
        super().__init__(model_name)
        self.host = host
        self.is_available = self.is_model_available()
    
    def is_model_available(self):
        try:
            # Vérifier si Ollama est en cours d'exécution
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m['name'] for m in models]
                if self.model_name in available_models:
                    app_logger.info(f"Ollama {self.model_name} disponible", "OLLAMA_LLM")
                    return True
                else:
                    app_logger.warning(f"Modèle {self.model_name} non trouvé dans Ollama", "OLLAMA_LLM")
            return False
        except Exception as e:
            # app_logger.debug(f"Ollama non disponible: {e}", "OLLAMA_LLM")  # Trop verbeux
            pass
            return False
    
    def generate_response(self, prompt, max_tokens=150):
        if not self.is_available:
            return "Erreur: Ollama non disponible"
        
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Pas de réponse')
            else:
                return f"Erreur Ollama: {response.status_code}"
                
        except Exception as e:
            app_logger.error(f"Erreur génération Ollama: {e}", "OLLAMA_LLM")
            return f"Erreur: {str(e)}"