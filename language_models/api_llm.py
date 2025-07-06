import requests
from .base_llm import BaseLLM
from core.logger import app_logger

class APIBasedLLM(BaseLLM):
    """LLM générique basé sur API"""
    
    def __init__(self, model_name, api_key=None, provider="generic"):
        super().__init__(model_name)
        self.api_key = api_key
        self.provider = provider
        self.is_available = bool(api_key)
    
    def is_model_available(self):
        return bool(self.api_key)
    
    def generate_response(self, prompt, max_tokens=150):
        if not self.is_available:
            return f"Erreur: Clé API {self.provider} requise"
        
        if self.provider == "openai":
            return self._openai_request(prompt, max_tokens)
        elif self.provider == "gemini":
            return self._gemini_request(prompt, max_tokens)
        elif self.provider == "deepseek":
            return self._deepseek_request(prompt, max_tokens)
        else:
            return "Provider non supporté"
    
    def _openai_request(self, prompt, max_tokens):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"Erreur OpenAI: {response.status_code}"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def _gemini_request(self, prompt, max_tokens):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
            params = {"key": self.api_key}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url, params=params, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return f"Erreur Gemini: {response.status_code}"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def _deepseek_request(self, prompt, max_tokens):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
            response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"Erreur DeepSeek: {response.status_code}"
        except Exception as e:
            return f"Erreur: {str(e)}"