from core.base_extension import BaseExtension
import requests
import json

class WeatherExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "Weather"
        self.version = "1.0.0"
        self.description = "Extension météo avec géolocalisation"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "current":
            return self.get_current_weather(args)
        elif command == "forecast":
            return self.get_forecast(args)
        elif command == "help":
            return self.show_help()
        else:
            return "Commandes: current, forecast, help"
    
    def get_current_weather(self, location=None):
        """Récupère la météo actuelle"""
        if not location:
            location = "Paris"
        
        try:
            # API gratuite OpenWeatherMap (nécessite clé)
            # Pour la démo, on simule
            return f"""🌤️ MÉTÉO ACTUELLE - {location.title()}

🌡️ Température: 22°C (ressenti 24°C)
☁️ Conditions: Partiellement nuageux
💨 Vent: 15 km/h Nord-Est
💧 Humidité: 65%
👁️ Visibilité: 10 km

💡 Usage: ext Weather current [ville]
📊 Prévisions: ext Weather forecast [ville]"""
        
        except Exception as e:
            return f"❌ Erreur météo: {e}"
    
    def get_forecast(self, location=None):
        """Récupère les prévisions"""
        if not location:
            location = "Paris"
        
        return f"""📅 PRÉVISIONS 3 JOURS - {location.title()}

🌅 Demain: 25°C / 18°C - Ensoleillé
⛅ Après-demain: 23°C / 16°C - Nuageux
🌧️ Dans 3 jours: 19°C / 14°C - Pluie

💡 Météo détaillée: ext Weather current {location}"""
    
    def show_help(self):
        """Affiche l'aide"""
        return """🌤️ EXTENSION MÉTÉO

📌 Commandes disponibles:
• ext Weather current [ville] - Météo actuelle
• ext Weather forecast [ville] - Prévisions 3 jours
• ext Weather help - Cette aide

💡 Exemples:
• ext Weather current Paris
• ext Weather forecast London
• ext Weather current (utilise Paris par défaut)

🔑 Note: Version démo avec données simulées"""
    
    def get_commands(self):
        return ["current", "forecast", "help"]