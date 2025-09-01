import json
from typing import Any

# Importe la classe de base depuis son nouveau fichier
from .boite_conteneur import BoiteConteneur

class ConteneurSerialisable(BoiteConteneur):
    def to_json(self) -> str:
        return json.dumps({
            'capacite_max': self.capacite_max,
            'contenu': self.contenu
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ConteneurSerialisable':
        data = json.loads(json_str)
        conteneur = cls(data['capacite_max'])
        for element in data['contenu']:
            conteneur.ajouter(element)
        return conteneur

# Exemple de sérialisation (commenté pour ne pas s'exécuter à l'import)
if __name__ == '__main__':
    conteneur = ConteneurSerialisable(3)
    conteneur.ajouter("donnée1")
    conteneur.ajouter("donnée2")
    json_data = conteneur.to_json()
    print("JSON:", json_data)
    # Reconstruction depuis JSON
    nouveau_conteneur = ConteneurSerialisable.from_json(json_data)
    print("Reconstruit:", nouveau_conteneur)