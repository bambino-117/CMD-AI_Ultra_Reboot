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
    "actif": 0.625,      # 62.5% de chance
    "inerte": 0.10,      # 10% de chance
    "bloqué": 0.1625,    # 16.25% de chance
    "contaminé": 0.1125  # 11.25% de chance
}
# On s'assure que la somme des probabilités est bien 1 (ou très proche)
assert sum(STATUS_CHOICES.values()) == 1.0, "La somme des probabilités des statuts doit être égale à 1."

# Le dossier de sortie pour les fichiers de conteneurs
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'CONTENEURS')

def generer_conteneurs():
    """Génère les fichiers de données pour les 64 conteneurs."""
    # 1. Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Répertoire de sortie '{OUTPUT_DIR}' assuré.")

    # --- Définition des conteneurs statiques/spécifiques ---
    osint_extension_data = {
        "id": 17,
        "name": "OSINT Aggregator",
        "version": "1.0.0",
        "author": "Anonyme",
        "type": "extension",
        "status": "actif",
        "description": "Un outil puissant pour agréger des informations open-source sur une cible donnée. Combine plusieurs moteurs de recherche et analyse les résultats.",
        "payload": {
            "entry_point_template": "osint_tool.html"
        }
    }
    STATIC_CONTAINERS = {17: osint_extension_data}

    # 2. Sélectionner aléatoirement les IDs pour les conteneurs spéciaux
    # On exclut les IDs des conteneurs statiques pour ne pas leur assigner un type aléatoire.
    ids_disponibles = [i for i in range(TOTAL_CONTENEURS) if i not in STATIC_CONTAINERS]
    ids_speciaux = random.sample(ids_disponibles, k=CONTENEURS_SPECIAUX)

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
        # Vérifier si c'est un conteneur statique
        if i in STATIC_CONTAINERS:
            data_conteneur = STATIC_CONTAINERS[i]
        else:
            # Sinon, générer un conteneur standard/aléatoire
            if i in ids_furtifs:
                type_conteneur = TYPE_FURTIF
            elif i in ids_blindes:
                type_conteneur = TYPE_BLINDE
            else:
                type_conteneur = TYPE_STANDARD

            # Choisir un statut aléatoirement selon les poids
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