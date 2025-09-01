from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
import platform
import random

class DiagnostiqueSysteme(BaseExtension):
    """
    Une extension d'exemple qui effectue un diagnostique simulé du système.
    """
    NAME = "Diagnostique Système"
    DESCRIPTION = "Vérifie l'intégrité des modules principaux et la connectivité réseau."

    def execute(self, *args, **kwargs):
        # Simule une opération et retourne un résultat
        status = random.choice(["Opérationnel", "Instable", "Erreur Critique"])
        message = f"État du noyau ({platform.system()}): {status}"
        
        return {"status": "success", "message": message}