import json
import os
import hashlib
from datetime import datetime, timedelta
from core.logger import app_logger

class OfflineManager:
    def __init__(self):
        self.cache_dir = "user/cache"
        self.responses_cache_file = os.path.join(self.cache_dir, "responses_cache.json")
        self.patterns_file = os.path.join(self.cache_dir, "common_patterns.json")
        self.offline_responses_file = os.path.join(self.cache_dir, "offline_responses.json")
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.responses_cache = self._load_cache()
        self.common_patterns = self._load_patterns()
        self.offline_responses = self._load_offline_responses()
        
    def _load_cache(self):
        """Charge le cache des réponses"""
        try:
            if os.path.exists(self.responses_cache_file):
                with open(self.responses_cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement cache: {e}", "OFFLINE_MANAGER")
        
        return {"responses": {}, "last_cleanup": None}
    
    def _save_cache(self):
        """Sauvegarde le cache"""
        try:
            with open(self.responses_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.responses_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde cache: {e}", "OFFLINE_MANAGER")
    
    def _load_patterns(self):
        """Charge les patterns communs"""
        try:
            if os.path.exists(self.patterns_file):
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement patterns: {e}", "OFFLINE_MANAGER")
        
        return self._get_default_patterns()
    
    def _get_default_patterns(self):
        """Patterns par défaut"""
        return {
            "greetings": {
                "patterns": ["bonjour", "salut", "hello", "hi", "bonsoir"],
                "responses": [
                    "Bonjour ! Comment puis-je vous aider ?",
                    "Salut ! Que puis-je faire pour vous ?",
                    "Hello ! Je suis là pour vous assister."
                ]
            },
            "thanks": {
                "patterns": ["merci", "thanks", "thank you", "merci beaucoup"],
                "responses": [
                    "De rien ! N'hésitez pas si vous avez d'autres questions.",
                    "Je vous en prie ! C'est un plaisir de vous aider.",
                    "Avec plaisir ! À votre service."
                ]
            },
            "help": {
                "patterns": ["aide", "help", "comment", "how to", "comment faire"],
                "responses": [
                    "Je suis là pour vous aider ! Posez-moi votre question.",
                    "Bien sûr ! Que voulez-vous savoir ?",
                    "Je peux vous expliquer. De quoi avez-vous besoin ?"
                ]
            },
            "programming": {
                "patterns": ["python", "code", "programmation", "script", "fonction"],
                "responses": [
                    "Je peux vous aider avec la programmation ! Quel langage vous intéresse ?",
                    "Excellent ! La programmation est passionnante. Que voulez-vous créer ?",
                    "Je connais plusieurs langages. Python, JavaScript, que préférez-vous ?"
                ]
            }
        }
    
    def _load_offline_responses(self):
        """Charge les réponses hors-ligne"""
        try:
            if os.path.exists(self.offline_responses_file):
                with open(self.offline_responses_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            app_logger.error(f"Erreur chargement offline: {e}", "OFFLINE_MANAGER")
        
        return {
            "system_info": {
                "question": "informations système",
                "response": "🖥️ Informations système disponibles via 'cmd: systeminfo' (Windows) ou 'cmd: uname -a' (Linux/Mac)"
            },
            "file_operations": {
                "question": "créer fichier",
                "response": "📁 Pour créer un fichier: 'cmd: touch fichier.txt' (Linux/Mac) ou 'cmd: echo. > fichier.txt' (Windows)"
            },
            "network": {
                "question": "réseau",
                "response": "🌐 Vérifiez votre connexion avec 'cmd: ping google.com' ou consultez les paramètres réseau"
            }
        }
    
    def cache_response(self, question, response, model="unknown"):
        """Met en cache une réponse"""
        try:
            question_hash = hashlib.md5(question.lower().encode()).hexdigest()
            
            cache_entry = {
                "question": question,
                "response": response,
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "usage_count": 1
            }
            
            if question_hash in self.responses_cache["responses"]:
                # Incrémenter le compteur d'usage
                self.responses_cache["responses"][question_hash]["usage_count"] += 1
            else:
                self.responses_cache["responses"][question_hash] = cache_entry
            
            self._save_cache()
            
        except Exception as e:
            app_logger.error(f"Erreur cache response: {e}", "OFFLINE_MANAGER")
    
    def get_cached_response(self, question):
        """Récupère une réponse du cache"""
        try:
            question_hash = hashlib.md5(question.lower().encode()).hexdigest()
            
            if question_hash in self.responses_cache["responses"]:
                entry = self.responses_cache["responses"][question_hash]
                
                # Vérifier si pas trop ancien (7 jours max)
                timestamp = datetime.fromisoformat(entry["timestamp"])
                if datetime.now() - timestamp < timedelta(days=7):
                    return f"💾 [CACHE] {entry['response']}"
            
            return None
            
        except Exception as e:
            app_logger.error(f"Erreur get cache: {e}", "OFFLINE_MANAGER")
            return None
    
    def get_pattern_response(self, question):
        """Trouve une réponse basée sur les patterns"""
        try:
            question_lower = question.lower()
            
            for category, data in self.common_patterns.items():
                for pattern in data["patterns"]:
                    if pattern in question_lower:
                        import random
                        response = random.choice(data["responses"])
                        return f"🤖 [PATTERN] {response}"
            
            return None
            
        except Exception as e:
            app_logger.error(f"Erreur pattern response: {e}", "OFFLINE_MANAGER")
            return None
    
    def get_offline_response(self, question):
        """Génère une réponse hors-ligne intelligente"""
        try:
            # 1. Vérifier le cache
            cached = self.get_cached_response(question)
            if cached:
                return cached
            
            # 2. Vérifier les patterns
            pattern_response = self.get_pattern_response(question)
            if pattern_response:
                return pattern_response
            
            # 3. Réponses spécialisées hors-ligne
            question_lower = question.lower()
            for key, data in self.offline_responses.items():
                if any(word in question_lower for word in data["question"].split()):
                    return f"📱 [OFFLINE] {data['response']}"
            
            # 4. Réponse générique
            return self._get_generic_offline_response(question)
            
        except Exception as e:
            app_logger.error(f"Erreur offline response: {e}", "OFFLINE_MANAGER")
            return "❌ Mode hors-ligne: Impossible de traiter la demande"
    
    def _get_generic_offline_response(self, question):
        """Réponse générique hors-ligne"""
        return f"""📱 MODE HORS-LIGNE ACTIF

❓ Votre question: "{question}"

🔌 Je ne peux pas accéder aux modèles IA en ligne actuellement.

💡 Suggestions:
• Vérifiez votre connexion internet
• Consultez le cache: cache list
• Utilisez les commandes système: cmd: [commande]
• Essayez plus tard quand la connexion sera rétablie

📚 Aide disponible: help"""
    
    def is_online(self):
        """Vérifie si on est en ligne"""
        try:
            import requests
            response = requests.get("https://httpbin.org/status/200", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def get_cache_stats(self):
        """Statistiques du cache"""
        try:
            total_responses = len(self.responses_cache["responses"])
            
            if total_responses == 0:
                return "📊 Cache vide - Aucune réponse en cache"
            
            # Calculer les stats
            total_usage = sum(entry["usage_count"] for entry in self.responses_cache["responses"].values())
            avg_usage = total_usage / total_responses
            
            # Réponses les plus utilisées
            popular = sorted(
                self.responses_cache["responses"].items(),
                key=lambda x: x[1]["usage_count"],
                reverse=True
            )[:3]
            
            result = f"""📊 STATISTIQUES DU CACHE

📦 Réponses en cache: {total_responses}
🔄 Utilisations totales: {total_usage}
📈 Moyenne d'usage: {avg_usage:.1f}

🏆 Top 3 des réponses:"""
            
            for i, (hash_key, entry) in enumerate(popular, 1):
                question = entry["question"][:50] + "..." if len(entry["question"]) > 50 else entry["question"]
                result += f"\n{i}. {question} ({entry['usage_count']} fois)"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur stats: {e}"
    
    def clear_cache(self):
        """Vide le cache"""
        try:
            self.responses_cache = {"responses": {}, "last_cleanup": datetime.now().isoformat()}
            self._save_cache()
            return "✅ Cache vidé avec succès"
        except Exception as e:
            return f"❌ Erreur vidage cache: {e}"
    
    def cleanup_old_cache(self, days=30):
        """Nettoie les anciennes entrées du cache"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            old_count = len(self.responses_cache["responses"])
            
            # Filtrer les entrées récentes
            self.responses_cache["responses"] = {
                k: v for k, v in self.responses_cache["responses"].items()
                if datetime.fromisoformat(v["timestamp"]) > cutoff_date
            }
            
            new_count = len(self.responses_cache["responses"])
            removed = old_count - new_count
            
            self.responses_cache["last_cleanup"] = datetime.now().isoformat()
            self._save_cache()
            
            return f"🧹 Nettoyage terminé: {removed} entrées supprimées (>{days} jours)"
            
        except Exception as e:
            return f"❌ Erreur nettoyage: {e}"