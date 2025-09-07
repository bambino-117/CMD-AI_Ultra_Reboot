import os
import json
import random

# --- INSTRUCTIONS D'INTÉGRATION DES EXTENSIONS ---
# Pour ajouter une nouvelle extension au système de conteneurs :
# 1. Créer la classe d'extension dans LOGIQUES/EXTENSIONS/
# 2. L'importer ici
# 3. Ajouter son conteneur dans STATIC_CONTAINERS avec un ID libre
# 4. Relancer ce générateur pour mettre à jour tous les conteneurs

# --- Importations des classes d'extension ---
# from LOGIQUES.EXTENSIONS.votre_extension import VotreExtension

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
# NOUVEAU : Chemin vers le dossier des templates d'extensions
EXTENSIONS_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, '..', 'INTERFACES', 'templates', 'extensions')

def generer_conteneurs():
    """Génère les fichiers de données pour les 64 conteneurs."""
    # 1. Créer les répertoires de sortie s'ils n'existent pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # NOUVEAU : S'assurer que le dossier pour les templates d'extension existe
    os.makedirs(EXTENSIONS_TEMPLATE_DIR, exist_ok=True)
    print(f"Répertoire de sortie '{OUTPUT_DIR}' assuré.")

    # --- CONTENEURS D'EXTENSIONS STATIQUES ---
    # Chaque extension a un conteneur fixe avec un ID spécifique
    STATIC_CONTAINERS = {
        # Extension VPN (Conteneur 1)
        1: {
            "id": 1,
            "type": "extension",
            "name": "VPN Vénère Natif",
            "description": "Visualiseur de connexion VPN avec intégration de proxy.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "vpn_visualization.html"}
        },
        # Extension OSINT (Conteneur 17 - existant)
        17: {
            "id": 17,
            "type": "extension",
            "name": "OSINT Aggregator",
            "description": "Outil puissant pour agréger des informations open-source.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "osint_aggregator.html"}
        },
        # Extension Centre d'Analyse (Conteneur 40)
        40: {
            "id": 40,
            "type": "extension",
            "name": "Centre d'Analyse",
            "description": "Consultation de rapports d'OSINT et de pentesting.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "centre_analyse.html"}
        },
        # Extension Chargeur Universel (Conteneur 60)
        60: {
            "id": 60,
            "type": "extension",
            "name": "Chargeur d'Applications Universel",
            "description": "Sandbox Docker pour applications isolées.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "universal_loader.html"}
        },
        # Extension Diagnostic (Conteneur 61)
        61: {
            "id": 61,
            "type": "extension",
            "name": "Diagnostic Système",
            "description": "Monitoring des performances sandbox.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "diagnostic_systeme.html"}
        },
        # Extension Deep Social (Conteneur 62)
        62: {
            "id": 62,
            "type": "extension",
            "name": "Deep Social Scanner",
            "description": "Analyse approfondie des réseaux sociaux.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "deep_social.html"}
        },
        # Extension Database Search (Conteneur 63)
        63: {
            "id": 63,
            "type": "extension",
            "name": "Database Search Engine",
            "description": "Recherche dans bases de données administratives.",
            "version": "1.0.0",
            "author": "Cygnus X-1",
            "status": "actif",
            "payload": {"entry_point_template": "database_search.html"}
        }
    }

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

        # --- NOUVEAU : Création automatique du template pour les extensions ---
        if data_conteneur.get("type") == "extension":
            payload = data_conteneur.get("payload", {})
            template_name = payload.get("entry_point_template")
            if template_name:
                template_path = os.path.join(EXTENSIONS_TEMPLATE_DIR, template_name)
                if not os.path.exists(template_path):
                    # Crée un fichier placeholder simple
                    placeholder_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Placeholder pour {data_conteneur.get('name')}</title>
</head>
<body>
    <h1>Template pour {data_conteneur.get('name')}</h1>
    <p>Ce fichier a été généré automatiquement. Remplacez son contenu par l'interface de l'extension.</p>
</body>
</html>
"""
                    with open(template_path, 'w', encoding='utf-8') as tpl_f:
                        tpl_f.write(placeholder_content.strip())
                    print(f"  -> Template placeholder créé : {template_name}")

    print(f"Génération terminée. {TOTAL_CONTENEURS} fichiers créés dans {OUTPUT_DIR}.")
    print(f"Extensions intégrées : {len(STATIC_CONTAINERS)}")
    print(f"Conteneurs libres : {TOTAL_CONTENEURS - len(STATIC_CONTAINERS)}")
    print(f"IDs d'extensions : {sorted(STATIC_CONTAINERS.keys())}")
    print("\n--- MÉTHODE D'INTÉGRATION ---")
    print("Pour ajouter une extension :")
    print("1. Choisir un ID libre (0-63)")
    print("2. Ajouter l'entrée dans STATIC_CONTAINERS")
    print("3. Relancer ce générateur")
    print("4. L'extension apparaîtra dans le Portail Conteneur")
    print("\nIDs disponibles :", [i for i in range(64) if i not in STATIC_CONTAINERS][:10], "...")

if __name__ == '__main__':
    generer_conteneurs()