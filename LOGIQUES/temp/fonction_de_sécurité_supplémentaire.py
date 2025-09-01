class SecurityUtils:
    @staticmethod
    def obfuscate_code(code: str) -> str:
        """Obfuscation basique du code"""
        return base64.b64encode(code.encode()).decode()
    
    @staticmethod
    def deobfuscate_code(obfuscated: str) -> str:
        """Désobfuscation"""
        return base64.b64decode(obfuscated.encode()).decode()
    
    @staticmethod
    def generate_self_destruct_timer(seconds: int):
        """Timer d'autodestruction"""
        import threading
        import time
        
        def self_destruct():
            time.sleep(seconds)
            # Nettoyage sécurisé
            if hasattr(sys, 'last_traceback'):
                del sys.last_traceback
            # Réinitialisation des variables sensibles
            globals().clear()
            locals().clear()
        
        timer = threading.Thread(target=self_destruct, daemon=True)
        timer.start()