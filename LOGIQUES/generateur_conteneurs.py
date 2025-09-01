import os
import json
import random

# --- Configuration ---
TOTAL_CONTENEURS = 64
CONTENEURS_SPECIAUX = 16
TYPE_FURTIF = "furtif"
TYPE_BLINDE = "blindé"
TYPE_STANDARD = "standard"

# --- NOUVEAU : Configuration des statuts ---
STATUS_CHOICES = {
    "actif": 0.60,       # 60% de chance
    "inerte": 0.25,      # 25% de chance
    "bloqué": 0.10,      # 10% de chance
    "contaminé": 0.05    # 5% de chance
}
# On s'assure que la somme des probabilités est bien 1 (ou très proche)
assert sum(STATUS_CHOICES.values()) == 1.0, "La somme des probabilités des statuts doit être égale à 1."

# Le dossier de sortie pour les fichiers de conteneurs
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'CONTENEURS')

def generer_conteneurs():
    """
    Génère les fichiers de données pour les 64 conteneurs avec des statuts variés.
    """
    # 1. Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Répertoire de sortie '{OUTPUT_DIR}' assuré.")

    # 2. Sélectionner aléatoirement les IDs pour les conteneurs spéciaux
    tous_les_ids = list(range(TOTAL_CONTENEURS))
    ids_speciaux = random.sample(tous_les_ids, k=CONTENEURS_SPECIAUX)

    # 3. Diviser les IDs spéciaux en deux groupes : furtifs et blindés
    # On utilise des sets pour une recherche rapide (O(1) en moyenne)
    moitie = CONTENEURS_SPECIAUX // 2
    ids_furtifs = set(ids_speciaux[:moitie])
    ids_blindes = set(ids_speciaux[moitie:])

    print(f"Génération de {TOTAL_CONTENEURS} fichiers de conteneurs...")

    # Préparer les listes pour la sélection aléatoire pondérée
    statuts = list(STATUS_CHOICES.keys())
    poids = list(STATUS_CHOICES.values())

    # 4. Boucler pour créer chaque fichier de conteneur
    for i in range(TOTAL_CONTENEURS):
        # Déterminer le type du conteneur
        if i in ids_furtifs:
            type_conteneur = TYPE_FURTIF
        elif i in ids_blindes:
            type_conteneur = TYPE_BLINDE
        else:
            type_conteneur = TYPE_STANDARD

        # NOUVEAU : Choisir un statut aléatoirement selon les poids
        status_conteneur = random.choices(statuts, weights=poids, k=1)[0]

        # Créer la structure de données
        data_conteneur = {
            "id": i,
            "nom": f"Conteneur #{i:02d}",
            "type": type_conteneur,
            "status": status_conteneur
        }

        # Écrire les données dans un fichier JSON
        nom_fichier = f"conteneur_{i:02d}.json"
        chemin_fichier = os.path.join(OUTPUT_DIR, nom_fichier)
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            json.dump(data_conteneur, f, indent=4)

    print(f"Génération terminée. {TOTAL_CONTENEURS} fichiers créés dans {OUTPUT_DIR}.")

if __name__ == '__main__':
    generer_conteneurs()