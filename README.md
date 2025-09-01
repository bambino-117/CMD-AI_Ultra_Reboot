# Mégastructure // CMD-AI Ultra Reboot

Une interface de bureau cyberpunk immersive construite avec Python, Flask et pywebview.

## Concept

Ce projet est une application de bureau qui simule une interface informatique d'un univers cyberpunk. Elle combine une interface utilisateur riche et thématique avec des fonctionnalités backend, y compris une connexion à diverses API d'IA, la gestion de fichiers locaux et un système d'extensions.

## Fonctionnalités

-   **Interface Immersive**: Une UI inspirée du cyberpunk avec des animations, des effets sonores et une typographie stylisée.
-   **Logicateur (IA)**: Intégration avec plusieurs fournisseurs d'IA (DeepSeek, OpenAI, Google, Groq, Ollama) pour une assistance conversationnelle.
-   **Bunker Sécurisé**: Un espace utilisateur local pour stocker des fichiers, protégé par un mot de passe.
-   **Système de Niveaux**: Navigation entre différents "niveaux" de l'application, chacun avec sa propre fonction.
-   **Configurateur**: Une page de paramètres pour personnaliser l'expérience (mode d'affichage, clés API, etc.).
-   **Éléments Narratifs**: Des secrets et des événements scriptés pour enrichir l'univers.

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