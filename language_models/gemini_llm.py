import requests
from .base_llm import BaseLLM
from core.logger import app_logger

class GeminiLLM(BaseLLM):
    """Google Gemini API"""
    
    def __init__(self, model_name="gemini-pro", api_key=None):
        super().__init__(model_name)
        self.api_key = api_key
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        self.is_available = self.is_model_available()
    
    def is_model_available(self):
        return bool(self.api_key)
    
    def generate_response(self, prompt, max_tokens=150):
        if not self.is_available:
            return "Erreur: Clé API Gemini requise"
        
        try:
            params = {"key": self.api_key}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": max_tokens}
            }
            
            response = requests.post(f"{self.base_url}", params=params, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"Erreur Gemini: {response.status_code}"
                
        except Exception as e:
            app_logger.error(f"Erreur Gemini: {e}", "GEMINI_LLM")
            return f"Erreur: {str(e)}"