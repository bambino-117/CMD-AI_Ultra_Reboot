import re
import os
from core.logger import app_logger

class TesterAuth:
    def __init__(self):
        self.tester_codes = self._load_tester_codes()
    
    def _load_tester_codes(self):
        """Charge les codes testeurs depuis le fichier"""
        codes = {}
        try:
            if os.path.exists("tester_codes.txt"):
                with open("tester_codes.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if ":" in line and not line.strip().startswith("#"):
                            name, code = line.strip().split(": ")
                            codes[code] = name
            app_logger.debug(f"Codes testeurs chargés: {len(codes)}", "TESTER_AUTH")
        except Exception as e:
            app_logger.error(f"Erreur chargement codes testeurs: {e}", "TESTER_AUTH")
        
        return codes
    
    def is_tester_code(self, pseudo):
        """Vérifie si le pseudo est un code testeur valide"""
        if not pseudo:
            return False
        
        # Format: 3 chiffres + 1 lettre (ex: 001Z)
        pattern = r'^\d{3}[A-Z]$'
        
        if re.match(pattern, pseudo.upper()):
            code = pseudo.upper()
            if code in self.tester_codes:
                app_logger.info(f"Testeur authentifié: {code}", "TESTER_AUTH")
                return True
            else:
                app_logger.warning(f"Code testeur invalide: {code}", "TESTER_AUTH")
        
        return False
    
    def get_tester_name(self, code):
        """Récupère le nom du testeur (pour logs internes uniquement)"""
        return self.tester_codes.get(code.upper(), "Testeur inconnu")
    
    def is_tester_mode_active(self, pseudo):
        """Détermine si le mode testeur doit être activé"""
        return self.is_tester_code(pseudo)
    
    def get_anonymous_id(self, code):
        """Retourne l'ID anonyme pour les rapports publics"""
        return code.upper()  # Le code lui-même est déjà anonyme