# Mégastructure // CMD-AI Ultra Reboot

Une interface de bureau cyberpunk immersive construite avec Python, Flask et pywebview.

## Concept

Ce projet est une application de bureau qui simule une interface informatique d'un univers cyberpunk. Elle combine une interface utilisateur riche et thématique avec des fonctionnalités backend, y compris une connexion à diverses API d'IA, la gestion de fichiers locaux et un système d'extensions.

## Fonctionnalités

-   **Interface Immersive**: Une UI inspirée du cyberpunk avec des animations, des effets sonores et une typographie stylisée.
-   **Logicateur (IA)**: Intégration avec plusieurs fournisseurs d'IA (DeepSeek, OpenAI, Google, Groq, Ollama) pour une assistance conversationnelle.
-   **Bunker Sécurisé**: Un espace utilisateur local pour stocker des fichiers, protégé par un mot de passe.
-   **Système de Niveaux**: Navigation entre différents "niveaux" de l'application, chacun avec sa propre fonction.
    -   Mécanique de navigation avec animation de défilement du terminal d'arrière-plan.
-   **Sondeur Administratif**: Un outil (maintenant intégré à l'extension OSINT) pour rechercher des jeux de données sur les portails de données ouverts des gouvernements.
-   **Conteneurs Blindés**: Des conteneurs spéciaux protégés par un mini-jeu de déchiffrement avec un clavier dynamique.
-   **Configurateur**: Une page de paramètres pour personnaliser l'expérience (mode d'affichage, clés API, etc.).
-   **Éléments Narratifs**: Des secrets et des événements scriptés pour enrichir l'univers.

## Roadmap / Plan d'Action - Outil de Recherche Complet (OSINT)

L'objectif est de faire évoluer le "Centre d'Analyse" vers un outil OSINT multifonction, installable et puissant.

### Phase 1 : Intégration et Dynamisme (Terminée)

-   **[FAIT] Étape 1 : Interface Dynamique**
    -   `centre_analyse.html` a été modifié pour remplacer le contenu statique par une interface interactive.
    -   L'interface permet de lancer des scans, de voir les journaux en temps réel, d'afficher les résultats et de sauvegarder les rapports.
    -   La liste des rapports sauvegardés dans le Bunker est chargée dynamiquement.

-   **[FAIT] Étape 2 : Consultation des Rapports**
    -   L'interface liste et affiche les rapports OSINT déjà sauvegardés au format Markdown.

### Phase 2 : Transformation en Extension (En cours)

-   **[FAIT] Étape 3 : Transformation en Extension Installable**
    -   Le conteneur 17 est maintenant assigné à l'extension OSINT via le script de génération `generateur_conteneurs.py`.
    -   Le `payload` pointe vers le template `osint_tool.html`.

-   **[FAIT] Étape 4 : Navigation Conditionnelle**
    -   Supprimer le lien direct vers `/centre_analyse` depuis le menu statique de `terminaux.html`.
    -   L'accès au Centre d'Analyse se fera via le menu des extensions installées, qui apparaît dynamiquement après l'installation depuis le Portail Conteneur.
    -   Le niveau 500 deviendra un niveau d'ambiance (comme le 241) tant que l'extension n'est pas installée.

### Phase 3 : Évolution vers un Outil Complet (Futures Améliorations)

-   **[FAIT] Étape 5 : Diversification des Sources**
    -   Le scan des réseaux sociaux utilise maintenant la bibliothèque `sherlock-project` pour des résultats réels.
    -   La recherche en base de données est connectée à l'API "Have I Been Pwned" pour des résultats réels.

-   **[FAIT] Étape 6 : Analyse par IA**
    -   Ajout d'un bouton "Analyser avec le Logicateur" sur les résultats d'un scan pour obtenir un résumé synthétique, identifier les entités clés et les relations potentielles via l'API d'IA configurée.

-   **[À FAIRE] Étape 7 : Amélioration de l'Interface et de l'Export**
    -   Ajouter des options de filtrage et de tri pour les résultats de scan.
    -   Permettre l'exportation des rapports dans différents formats (JSON, TXT).
    -   **NOUVEAU : Ajout d'une sélection de modules de scan.**
        -   **Question :** Comment pourrait-on ajouter une option dans le Hub OSINT pour choisir les modules à inclure dans un scan (Web, Social, etc.) ?
        -   **Réponse (Concept) :**
            1.  **Interface (`osint_tool.html`) :** Dans l'onglet "Scan & Analyse", on ajouterait une série de cases à cocher (checkboxes) ou d'interrupteurs (toggles) avant le bouton "Lancer le Scan". Chaque case correspondrait à un module : "Recherche Web", "Scan Social", etc.
            2.  **Logique JavaScript :** Au moment de lancer le scan, le script JavaScript récupérerait la liste des modules cochés.
            3.  **API Backend (`conteneur_monde.py`) :** La fonction `run_osint_scan` serait modifiée pour accepter cette liste de modules en plus de la cible.
            4.  **Logique de l'Extension (`osint_aggregator.py`) :** La méthode `execute_scan` recevrait la liste des modules à exécuter. Elle lancerait alors conditionnellement les fonctions de recherche (`_search_duckduckgo`, `search_social_media`, etc.) uniquement si elles sont présentes dans la liste. Cela rendrait les scans plus rapides et plus ciblés selon les besoins de l'utilisateur.

-   **[FAIT] Étape 8 : Refactoring et Nettoyage**
    -   Suppression des fichiers de templates obsolètes (`centre_analyse.html`, `deep_social_preview.html`, `sondeur_administratif.html`) après leur intégration dans le hub OSINT.
    -   Renommage des modules logiques pour une meilleure clarté.

## Installation

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/bambino-117/CMD-AI_Ultra_Reboot.git
    cd CMD-AI_Ultra_Reboot
    ```

2.  **Créer un environnement virtuel et l'activer**
    ```bash
    # Pour macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # Pour Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer l'application**
    -   Si le fichier `INTERFACES/config.json` n'existe pas, copiez `INTERFACES/config.example.json` et renommez-le en `config.json`.
    -   Ouvrez `INTERFACES/config.json` pour le modifier.
    -   **Configuration IA** : Dans la section `ai.providers`, ajoutez vos clés API pour chaque service que vous souhaitez utiliser (ex: `openai`, `deepseek`, `google`, etc.). L'application utilisera la clé correspondant au modèle sélectionné dans les paramètres de l'application.
    -   **Chemin du Bunker** : Modifiez `user_folder_path` pour définir où les données utilisateur seront stockées. Laissez vide pour utiliser le chemin par défaut (`Documents/Megastructure_Data`).
    -   **Clé API OSINT** : Pour utiliser la recherche de fuites de données, obtenez une clé API sur haveibeenpwned.com/API et ajoutez-la dans `config.json` à l'emplacement `user.api_keys.hibp_api_key`.

## Lancement

Pour démarrer l'application, exécutez le script principal :

```bash
python conteneur_monde.py
```

## Structure du Projet

-   `conteneur_monde.py`: Script principal de l'application (backend Flask et logique pywebview).
-   `INTERFACES/`: Contient les ressources front-end.
-   `LOGIQUES/`: Contient la logique métier plus complexe.
-   `RESSOURCES/`: Fichiers divers utilisés par l'application.