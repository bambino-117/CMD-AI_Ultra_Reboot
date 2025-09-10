# Mégastructure // CMD-AI Ultra Reboot

Une interface de bureau cyberpunk immersive construite avec Python, Flask et pywebview.

## Concept

Ce projet est une application de bureau qui simule une interface informatique d'un univers cyberpunk. Elle combine une interface utilisateur riche et thématique avec des fonctionnalités backend, y compris une connexion à diverses API d'IA, la gestion de fichiers locaux et un système d'extensions.

## Fonctionnalités

-   **Interface Immersive**: Une UI inspirée du cyberpunk avec des animations, des effets sonores et une typographie stylisée.
-   **Logicateur (IA)**: Intégration avec plusieurs fournisseurs d'IA (DeepSeek, OpenAI, Google, Groq, Ollama) pour une assistance conversationnelle.
-   **Bunker Sécurisé**: Un espace utilisateur local pour stocker, créer, renommer et supprimer des fichiers/dossiers, avec une gestion par glisser-déposer.
-   **Système d'Extensions Modulaire**: Une architecture robuste permettant d'installer et de désinstaller des fonctionnalités via le "Portail Conteneur".
-   **Système d'Authentification Avancé**: Gestion de 3 rôles (Concepteur, Testeur, Utilisateur) avec des privilèges distincts et mots de passe hachés (bcrypt).
-   **Système de Bots (BOTS-KUSO-YARO)**: Un système de ressources stratégiques où les utilisateurs génèrent et consomment des "bots" pour des actions avancées (scans, attaques simulées).
-   **Extension OSINT Aggregator**: Un outil puissant pour mener des enquêtes en sources ouvertes, avec sélection de modules, export de rapports et analyse par l'IA.
-   **Chargeur d'Applications Universel (en développement)**: Une sandbox basée sur Docker pour exécuter des applications dans un environnement isolé.
-   **VPN Vénère Natif**: Un visualiseur de connexion VPN avec une intégration de proxy pour les requêtes externes.
-   **Éléments Narratifs**: Des secrets et des événements scriptés, comme le mot de passe "infect" qui déclenche une prise de contrôle simulée.
-   **Interface de Configuration "Palimpseste"**: Une interface de paramètres unique qui évolue visuellement en remontant le temps technologique.

## Roadmap / Plan d'Action

Le projet est très avancé. Les fonctionnalités majeures comme le système d'extensions, le Bunker interactif, le Chargeur d'Applications, l'authentification par rôles et le système de bots sont en place. Le développement se concentre sur :
-   La finalisation du **système de mise à jour in-app** (Phase 13).
-   L'amélioration continue de l'expérience utilisateur et la correction de bugs.

Pour une liste complète des fonctionnalités terminées, en cours et planifiées, avec les détails de chaque phase de développement, veuillez consulter notre **Roadmap détaillée**.

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
    -   **Chemin du Bunker** : Modifiez `user.user_folder_path` pour définir où les données utilisateur seront stockées.
    -   **Clé API OSINT** : Pour utiliser la recherche de fuites de données, obtenez une clé API sur haveibeenpwned.com/API et ajoutez-la dans `config.json` à l'emplacement `user.api_keys.hibp_api_key`.

## Lancement

Pour que le Chargeur d'Applications Universel fonctionne, assurez-vous que **Docker Desktop** est installé et en cours d'exécution sur votre machine.

Pour démarrer l'application, exécutez le script principal :

```bash
python conteneur_monde.py
```

## Structure du Projet

-   `conteneur_monde.py`: Script principal de l'application (backend Flask et logique pywebview).
-   `INTERFACES/`: Contient les ressources front-end.
-   `LOGIQUES/`: Contient la logique métier plus complexe.
-   `RESSOURCES/`: Fichiers divers utilisés par l'application.