# Incogni-Me Extension

## Description
Incogni-Me est une extension qui vous aide à gérer votre empreinte numérique en ligne. Elle vous permet de :
- Rechercher vos informations personnelles sur différentes plateformes
- Suivre où vos données personnelles apparaissent
- Gérer les demandes de suppression de vos informations
- Protéger votre vie privée en ligne

Extension FastAPI pour l'effacement et l'anonymisation de l'identité numérique.

## Fonctionnalités principales
- API REST pour gérer les utilisateurs, identités, requêtes de suppression
- Scraping et automatisation pour la suppression de traces
- Authentification JWT

## Installation

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Configurez la base de données dans un fichier `.env` (voir `database.py`)
3. Lancez le serveur :
   ```bash
   uvicorn main:app --reload
   ```

## Utilisation
- Accédez à la documentation interactive sur `/docs` après lancement.
- Personnalisez les scrapers et services selon vos besoins.

## Auteur
boris
