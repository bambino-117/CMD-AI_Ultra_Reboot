# Feuille de Route du Projet

Ce document décrit l'historique du développement, les prochaines étapes planifiées et les idées pour l'avenir de l'application.

## ✅ Journal des Modifications et Phases Terminées

Cette section retrace l'ensemble des fonctionnalités implémentées et des phases de développement achevées.

### Résumé des Fonctionnalités Clés
- **Transformation de l'Outil OSINT :** L'ancien "Centre d'Analyse" a été entièrement refondu et transformé en une extension dynamique et installable, l'**OSINT Aggregator** (assignée au Conteneur 17).
- **Amélioration des Scans OSINT :** Les capacités de scan ont été étendues pour inclure des recherches réelles sur les réseaux sociaux (via `sherlock-project`) et une analyse des résultats par l'IA (Logicateur).
- **Export des Rapports OSINT :** Ajout de la possibilité d'exporter les rapports de scan aux formats JSON, TXT et CSV, directement dans le Bunker.
- **Développement du Chargeur d'Applications Universel :** Implémentation d'une sandbox Docker complète avec interface graphique via noVNC.
- **Développement de l'Extension "Diagnostic Système" :** Création d'un outil pour surveiller les ressources de la sandbox Docker en temps réel.
- **Refonte Visuelle du Configurateur :** Interface "Palimpseste" évoluant visuellement à travers différentes ères technologiques.
- **Système d'Accès à Trois Niveaux :** Implémentation complète de la logique des rôles (Concepteur, Testeur, Utilisateur Lambda).
- **Bunker - Gestion Avancée :** Ajout de la suppression, des collisions physiques entre les "cercles de données" et de logiques de gameplay pour des fichiers spéciaux (contaminés, bloqués, keylogger).
- **Session de Première Utilisation Guidée :** Création d'une expérience d'accueil interactive ("wizard") pour les nouveaux utilisateurs.
- **Panneau de Contrôle des Accès Testeur :** Interface sécurisée pour la gestion des codes d'accès.
- **Restauration du Portail Conteneur :** Rétablissement de l'interface originale de la grille 8x8, tout en la connectant aux données réelles pour une gestion fonctionnelle des extensions.
- **Rétablissement du Flux d'Accès Initial :** Restauration de `aboutissement.html` comme point d'entrée pour préserver l'immersion et les énigmes "oPen" et "Infect".
- **Polissage de l'Extension BOTS-KUSO-YARO :** Amélioration de l'expérience utilisateur avec des notifications de fin de mission, une animation de génération, une table des missions plus détaillée (affichage du risque) et la sauvegarde automatique des rapports dans un dossier dédié du Bunker.
-   **Sécurisation de la Distribution :** Mise en place de builds distincts (développement/public) pour exclure les fonctionnalités d'administration des versions distribuées.
-   **Système de Mise à Jour In-App :** Implémentation de la mise à jour du cœur de l'application (via redémarrage transparent) et des extensions (via rechargement à chaud).
-   **Amélioration du Bunker :** Ajout d'une fonction de recherche et des bases pour la synchronisation des données.

### Historique Détaillé des Phases

#### Phase 1 : Fondations de l'Application ✓
-   **Initialisation du Projet :** Structure des dossiers, Flask, pywebview.
-   **Interface de Base :** Création de `terminaux.html` et `aboutissement.html` (restauré comme point d'entrée principal).
-   **Système de Niveaux :** Logique de navigation entre les "niveaux" de l'application.
-   **Logicateur (IA) :** Intégration d'une API d'IA (DeepSeek, OpenAI, etc.).
-   **Bunker (Gestionnaire de Fichiers) :**
        - Création du dossier utilisateur.
        - Interface de base pour lister les fichiers.
        - CRUD (Créer, Lire, Mettre à jour, Supprimer) pour les fichiers et dossiers.
        - Implémentation du glisser-déposer (Drag & Drop) pour l'upload.
        - Logique de mot de passe et gestion des fichiers "spéciaux" (contaminés, inaccessibles).

#### Phase 2 : Système d'Extensions et Sécurité ✓
-   **Portail Conteneur :** Interface pour visualiser et "installer" des extensions. ✓ Restauration de l'interface visuelle de la grille 8x8 et connexion aux données réelles.
-   **Extension OSINT Aggregator :** Développement complet de l'outil OSINT.
        - Scan multi-modules (web, social, leaks).
        - Sauvegarde et export des rapports.
        - Analyse des résultats par l'IA.
-   **Sandboxing Logique :** Isoler les extensions du cœur de l'application via une `SandboxAPI`.

#### Phase 3 : Chargeur d'Applications Universel (Backend) ✓
-   **Logique Docker :** Créer une extension qui peut démarrer/arrêter un conteneur Docker.
-   **Tunnel de Communication :** Établir un canal sécurisé (WebSocket) entre l'hôte et le conteneur.
-   **Téléversement de Fichiers :** Permettre l'envoi de fichiers de l'hôte vers la sandbox.

#### Phase 4 : Chargeur d'Applications Universel (Frontend) ✓
-   **Interface de Base :** Créer `universal_loader.html` avec les contrôles de base.
-   **Exécution de Commandes :** Envoyer des commandes depuis l'interface vers la sandbox via le tunnel.
-   **Configuration VNC :** Configurer le conteneur Docker avec un serveur VNC (ex: `x11vnc`).

#### Phase 5 : Finalisation du Chargeur d'Applications Universel ✓
-   **Intégration VNC :** Implémenter un client VNC JavaScript (noVNC) dans l'interface.
-   **Orchestration Complète :** Gérer la connexion, l'affichage du bureau de la sandbox et la transmission des événements clavier/souris.

#### Phase 6 : Interface & UX - "Palimpseste Technologique" ✓
-   **Refonte Visuelle du Configurateur (Niveau 0) :**
        - **Concept :** L'interface évolue visuellement en remontant le temps technologique lors du défilement (Cyberpunk -> WinXP -> DOS).
        - Implémentation complète de la structure HTML, du "Time-Scroll" et des transitions.

#### Phase 7 : Authentification et Sécurité ✓
-   **Système d'Accès à Trois Niveaux :** Implémentation complète de la logique des rôles (Concepteur, Testeur, Utilisateur Lambda) et de la gestion des privilèges. ✓
-   **Boutons de Sécurité (Paramètres) :** Ajout des boutons "Vider le cache", "Kill-app" et "Crash" pour le rôle Concepteur. ✓

#### Phase 8 : Session de Première Utilisation Guidée ✓
-   **Concept :** Créer une expérience d'accueil interactive ("wizard") pour les nouveaux utilisateurs, de la détection du premier lancement à la configuration du Bunker.

#### Phase 9 : Bunker - Gestion Avancée des Fichiers ✓
-   **Suppression de Fichiers :** API `delete_bunker_file()` et bouton de suppression avec confirmation. ✓
-   **Cercles Spéciaux :** Implémentation de logiques de gameplay pour des fichiers spéciaux. ✓
        - **Contaminés (`neural_ghost.py`) :** L'exécution du fichier déclenche une "infection" du système, activant une porte dérobée et un keylogger persistant qui enregistre l'activité simulée dans `keylogscornflakes.md`. ✓
        - **Bloqués :** Contenu chiffré, simulation de modification des politiques de sécurité hôte au clic. ✓
        - **Keylogger (`svchost.exe.bak`) :** Déploiement probabiliste (1/4) d'un keylogger (simulé) persistant sur l'hôte. ✓
-   **Animations de Traitement :** État "processing" avec animations CSS pour les opérations sur les fichiers spéciaux. ✓
-   **Collision des Cercles :** Les cercles entrent en collision entre eux et avec la console centrale (qui agit comme un obstacle statique). ✓
-   **Intégration OSINT :** Bouton d'envoi vers l'analyseur dans les dossiers OSINT. ✓

#### Phase 10 : Panneau de Contrôle des Accès Testeur ✓
-   **Concept :** Créer une interface sécurisée, réservée au Concepteur, pour gérer les codes d'accès des testeurs via une API dédiée et une page d'administration.

#### Phase 11 : Extension BOTS-KUSO-YARO ✓
-   **Concept** : Créer une extension "BOTS-KUSO-YARO" qui sert de générateur de "bots". Ces bots ne sont pas des entités actives en soi, mais une ressource numérique consommable.
-   **Interface** : Un niveau dédié avec un champ de saisie numérique et un bouton "Générer". L'action de générer déclenche une animation de chargement (ex: une barre qui se remplit) pour donner du poids à l'action.
-   **Logique de Gameplay** :
    -   L'utilisateur génère un pool de bots (ex: 1000).
    -   D'autres extensions (comme l'OSINT Aggregator) consomment un certain nombre de bots pour effectuer des actions (ex: un scan OSINT coûte 100 bots).
    -   Le pool de bots diminue à chaque utilisation. L'interface de BOTS-KUSO-YARO affiche le nombre de bots restants par rapport au total généré (ex: 900/1000).
-   **Objectif Psychologique** : Forcer l'utilisateur à une action de "création" délibérée pour freiner les pulsions de puissance et introduire une gestion stratégique des ressources.
-   **Actions Programmables (Évolution)** : Une fois le pool de bots créé, l'utilisateur peut leur assigner des missions qui s'exécutent en arrière-plan.
    -   **Interface de Mission** : Un tableau de bord dans l'extension BOTS-KUSO-YARO pour assigner des bots à des tâches, voir leur statut ("disponible", "en mission", "perdu") et collecter les résultats.
    -   **Types de Missions Envisagés** :
        -   **Renseignement Passif** : Surveillance de mots-clés sur des flux simulés, analyse de trafic réseau fictif pour découvrir des pistes.
        -   **Influence et Perturbation** : Attaques DDoS simulées (coûteuses en bots), génération de "bruit" pour couvrir d'autres actions.
        -   **Ressources et Économie** : Minage de données pour générer une monnaie virtuelle ou des fragments d'information.
        -   **Défense** : Assignation de bots à la patrouille du Bunker pour détecter et contrer les intrusions (PNJ).
-   **Accès aux Fonctionnalités Avancées (Énigme Déguisée)** : Pour éviter un accès trop facile aux outils d'influence (DDoS, bruit), leur activation sera cachée derrière une énigme non-explicite, agissant comme une seconde barrière pour l'utilisateur.
    -   **Concept** : L'utilisateur doit "réparer" un protocole déclassifié pour débloquer les fonctionnalités, plutôt que de résoudre une énigme classique.
    -   **Découverte** : Présence d'un fichier corrompu dans le Bunker (ex: `proto_swarm_v0.7.log.corrupt`).
    -   **Déchiffrement** : Le fichier contient des fragments de texte en hexadécimal (ex: `DECHAINER` et `LES_CHIENS`) que l'utilisateur doit trouver et assembler.
    -   **Activation** : Un champ de "Commande de Diagnostic" ou "Override de Protocole" dans l'interface de BOTS-KUSO-YARO, où la clé reconstituée doit être entrée.
    -   **Récompense** : L'interface se met à jour pour révéler les fonctionnalités avancées, donnant à l'utilisateur le sentiment d'une découverte et d'une réussite technique.
-   **Plan d'Implémentation Technique** :
    -   **Rappel** : L'extension est uniquement accessible après installation via le "Portail Conteneur".
    -   **Étape 1 : Fondations de l'Extension (Conteneur et Ressource)**
        -   Déclarer l'extension `BOTS-KUSO-YARO` dans `generateur_conteneurs.py`. ✓
        -   Créer le template `bots_kuso_yaro.html` avec l'interface de génération et la barre de statut. ✓
        -   Implémenter les API backend dans `conteneur_monde.py` pour gérer le pool de bots (`generate_bots`, `get_bots_status`, `use_bots`). ✓
        -   Mettre à jour la configuration utilisateur pour stocker le `total` et le nombre `disponible` de bots. ✓
    -   **Étape 2 : Intégration et Consommation**
        -   Modifier une extension existante (ex: `OSINT Aggregator`) pour qu'elle consomme des bots via `api.use_bots()` avant d'exécuter une action. ✓
    -   **Étape 3 : Implémentation des Actions Programmables (Missions)**
        -   **Backend** : Mettre en place un gestionnaire de tâches en arrière-plan pour les missions. Implémenter la logique des missions DDoS et Bruit pour qu'elles aient un effet tangible simulé sur d'autres parties de l'application (ex: ralentir ou désactiver temporairement un autre niveau). ✓
        -   **Frontend** : Ajouter un panneau "Contrôle de Mission" à l'interface pour assigner les bots et suivre la progression des missions. ✓
        -   **Améliorations UX** :
            -   Notifications de fin de mission avec résumé des pertes et rapports générés. ✓
            -   Animation visuelle lors de la génération de bots pour donner du "poids" à l'action. ✓
            -   Table des missions améliorée avec affichage du risque et de la cible. ✓
            -   Sauvegarde des rapports de mission dans un dossier dédié (`BKY_Mission_Reports`) dans le Bunker. ✓
    -   **Étape 4 : Mécanisme d'Accès via Énigme**
        -   **Création de l'Indice** : Générer le fichier `proto_swarm_v0.7.log.corrupt` dans le Bunker de l'utilisateur, contenant les fragments de la clé. ✓
        -   **Interface de Déverrouillage** : Ajouter le champ de saisie "Override de Protocole" à l'interface, initialement caché. ✓
        -   **Logique de Déverrouillage** : Créer une API pour valider la clé. Si elle est correcte, une nouvelle valeur dans la configuration utilisateur (`bky_protocol_unlocked: true`) débloquera l'affichage des missions avancées sur l'interface. ✓

#### Phase 12 : Sécurisation de la Distribution ✓
*   **Objectif :** Isoler et exclure les fonctionnalités réservées au Concepteur (comme la gestion des testeurs) des versions publiques de l'application.
*   **Étape 12.1 : Structuration des Fichiers d'Administration**
    *   **Action :** Déplacer `testers_management.html` vers `INTERFACES/templates/admin/`. ✓
    *   **Raison :** Séparer physiquement les templates d'administration des templates utilisateurs pour une meilleure organisation et une exclusion facilitée.
*   **Étape 12.2 : Ajout d'un Avertissement Visuel**
    *   **Action :** Intégrer un bandeau d'avertissement proéminent sur la page `testers_management.html`. ✓
    *   **Raison :** Renforcer visuellement la sensibilité de la zone, même si l'accès est déjà protégé par la logique du backend.
*   **Étape 12.3 : Mise en Place de Scripts de Build Séparés (PyInstaller)**
    *   **Action :** Créer deux fichiers de configuration pour PyInstaller : `build_dev.spec` (pour le Concepteur) et `build_public.spec` (pour les testeurs/utilisateurs). ✓
    *   **Raison :** Permettre de définir des configurations de build distinctes pour chaque type de version.
*   **Étape 12.4 : Exclusion des Fichiers Sensibles**
    *   **Action :** Dans `build_public.spec`, utiliser la directive `excludes` pour omettre le dossier `INTERFACES/templates/admin/` de l'exécutable final. ✓
    *   **Raison :** Garantir que les fichiers HTML sensibles ne sont jamais présents dans la distribution publique.
*   **Étape 12.5 : Compilation Conditionnelle des Routes**
    *   **Action :** Utiliser une variable d'environnement (`BUILD_MODE`) dans `conteneur_monde.py` pour n'enregistrer la route `@app.route('/admin/testers')` que si `BUILD_MODE` est égal à `'DEV'`. ✓
    *   **Raison :** Supprimer complètement le point d'accès API dans les versions publiques, rendant la fonctionnalité inaccessible même si un utilisateur essayait de forger une requête.

#### Phase 13 : Système de Mise à Jour In-App (No-Reboot / Hot-Reload) ✓
*   **Objectif :** Permettre à l'application de se mettre à jour, ainsi que ses extensions, sans intervention manuelle de l'utilisateur.
*   **Étape 13.1 : API de Versioning Centralisée**
    *   **Action :** Mettre en place un point de terminaison (ex: un fichier `versions.json` sur un serveur statique) qui liste la version actuelle de l'application principale et de chaque extension officielle. ✓
    *   **Raison :** Permettre à l'application de vérifier périodiquement si des mises à jour sont disponibles.
*   **Étape 13.2 : Mise à Jour du Cœur de l'Application (Redémarrage Transparent)**
    *   **Action :** Créer une fonction qui, lorsqu'une nouvelle version de l'application est détectée, télécharge les nouveaux fichiers dans un dossier temporaire, puis exécute un script externe (ex: `.bat` ou `.sh`) qui remplace les anciens fichiers et relance `conteneur_monde.py`. ✓
    *   **Raison :** La mise à jour du cœur Python en cours d'exécution est complexe et risquée. Un redémarrage automatisé est la solution la plus robuste et la plus sûre.
*   **Étape 13.3 : Mise à Jour et Ajout d'Extensions (Hot-Reload / Hot-Add)**
    *   **Action :** Développer une logique pour télécharger les fichiers d'une nouvelle extension (ou d'une version mise à jour) et les placer dans le dossier `LOGIQUES/EXTENSIONS`. ✓
    *   **Action :** Utiliser le module `importlib` (`importlib.reload`) pour décharger l'ancienne version d'un module d'extension et charger la nouvelle sans redémarrer l'application. ✓
    *   **Action :** Mettre à jour dynamiquement l'interface (ex: le menu de `terminaux.html`) en JavaScript pour refléter l'ajout ou la mise à jour de l'extension. ✓
*   **Étape 13.4 : Interface Utilisateur pour les Mises à Jour**
    *   **Action :** Créer une section "Mises à jour" dans les paramètres (`settings.html`) qui affiche les versions actuelles, recherche les mises à jour disponibles et permet de les lancer. ✓
    *   **Action :** Implémenter des notifications non-intrusives pour informer l'utilisateur qu'une mise à jour est prête à être installée. ✓

=========================================================================================================
#### Phase 14 : Fondations du Bunker v2 ✓
*   **Recherche Bunker :** Ajout d'une barre de recherche pour filtrer les fichiers et dossiers par nom directement dans l'interface. ✓
*   **Synchronisation de Base :** Mise en place de l'infrastructure de configuration pour permettre la synchronisation du Bunker via un service cloud tiers (ajout des options dans les paramètres). ✓

=========================================================================================================
## 🚀 Prochaines Étapes et Feuille de Route Future

Cette section présente une analyse technique des idées et une proposition de roadmap pour les développements futurs. 

### Recommandations d'Implémentation (Post v1.0) 
*   **Phase 15 - Fonctionnalités Core (3-4 semaines)** 
    1.  Chat anonyme. 
    2.  Capture d'écran. 
    3.  IDE basique. 
    *   **Chat Anonyme Utilisateur-Utilisateur (avec un twist)**
        *   **Concept** : Une interface de chat minimaliste et globale, toujours présente en bas à gauche de l'écran. La communication est directe (user-to-user), éphémère (aucun historique) et limitée à 140 caractères.
        *   **Interface "Pénible"** : Pour renforcer l'ambiance "low-tech", la liste des utilisateurs connectés est un bandeau horizontal de pseudos écrits à la verticale. La recherche d'un interlocuteur est volontairement fastidieuse, avec une navigation par chevrons.
        *   **Le Fantôme dans la Machine (Intégration IA)** :
            *   Parmi les pseudos connectés, l'un d'eux est une façade pour l'API IA configurée par l'utilisateur.
            *   Ce pseudo sera d'inspiration sud-africaine pour renforcer l'immersion et le mystère (ex: Zola, Jabu, Ruan, Bok...).
            *   L'utilisateur ne sait pas qu'il peut discuter avec son propre modèle de langage, créant une confusion sur la nature de ses interlocuteurs.
            *   L'IA est contrainte : messages courts et personnalité unique (laconique, énigmatique) définie par un "pattern conversationnel" (prompt système spécifique) pour renforcer l'immersion.
            *   **Mémoire Éphémère** : La conversation avec l'IA est systématiquement effacée à la fin de la session. L'IA n'a aucune mémoire des échanges précédents, renforçant le sentiment d'une interaction volatile et non fiable.
        *   **Plan d'Implémentation Technique** :
            *   **Étape 1 : Serveur Relais Externe** : Créer un serveur WebSocket minimaliste pour router les messages privés entre les utilisateurs (identifiés par des ID de session temporaires) et diffuser la liste des pseudos connectés. Le serveur ne stocke aucune donnée.
            *   **Étape 2 : Intégration Backend (`conteneur_monde.py`)** :
                *   Établir une connexion WebSocket permanente entre l'application et le serveur relais, en passant par le VPN intégré pour un anonymat renforcé.
                *   Gérer la liste des utilisateurs reçue du relais.
                *   Injecter le pseudo de l'IA dans la liste des connectés affichée à l'utilisateur.
                *   Intercepter les messages destinés au pseudo de l'IA. Au lieu de les envoyer au relais, les transmettre à l'API `api.get_ai_response` avec un prompt système spécifique pour simuler la personnalité du "fantôme".
                *   Relayer les messages des autres utilisateurs entre le frontend et le serveur relais.
            *   **Étape 3 : Interface Frontend (Overlay Global)** :
                *   Créer un fragment HTML/CSS pour l'overlay de chat (position fixe en bas à gauche).
                *   Implémenter le carrousel horizontal pour les pseudos verticaux, avec navigation par chevrons.
                *   Développer la logique JavaScript pour :
                    *   Afficher la liste des pseudos et gérer la sélection d'un interlocuteur.
                    *   Ouvrir une fenêtre de conversation privée contextuelle.
                    *   Envoyer/recevoir les messages via les API du backend.
            *   **Étape 4 : Personnalité de l'IA** :
                *   Rédiger un prompt système spécifique et détaillé pour le chat. Ce prompt instruira l'IA sur son rôle, son ton (énigmatique, technique, laconique), l'interdiction de révéler sa nature d'IA, et le respect strict de la limite de caractères.
                *   Le prompt devra également inclure l'instruction de ne jamais faire référence à des conversations passées pour simuler l'effacement de la mémoire.

*   **Phase 16 - Avancé (4-6 semaines)**
    1.  Surveillance algorithmique.
    2.  Système de Bots (BOTS-KUSO-YARO) : Génération et consommation de bots en tant que ressource. ✓
    3.  Monitoring plateformes sociales.

*   **Phase 17 - Expérimental (ongoing)**
    1.  Niveau XXX (après validation juridique).
    2.  Bots avancés.
    3.  Intégration deep learning.

=========================================================================================================
## 💡 Idées et Brainstorming (Backlog)

Cette section regroupe les idées proposées pour l'avenir du projet, accompagnées d'une analyse technique et de considérations éthiques.

### Analyse des Priorités et Complexité

*   **Priorité Élevée (Impact élevé, Complexité modérée)**
    *   Système de rapports d'erreur.
    *   Outil de recherche Bunker.
    *   Synchronisation mobile/desktop.

*   **Priorité Moyenne (Impact moyen, Complexité variable)**
    *   Capture d'écran Logicateur.
    *   Chat utilisateur anonyme.
    *   Extension IDE (version basique).

*   **Priorité Basse (Impact élevé, Complexité élevée)**
    *   Bots informationnels (aspects éthiques).
    *   Surveillance plateformes étrangères (défis techniques).
    *   Niveau XXX (considérations légales).

=========================================================================================================
### Idées Détaillées

#### 🎯 Niveaux et Expérience Utilisateur

*   **Outil de recherche avancée Bunker**
    *   **Concept** : Permettre à l'utilisateur de rechercher des fichiers et des dossiers dans son Bunker en se basant sur le nom, le type, la date ou le contenu.
    *   **Plan d'Implémentation Technique** :
        *   **Backend (`conteneur_monde.py`)** :
            *   Créer une nouvelle API `api.search_bunker(query, filters)`.
            *   La logique de recherche devra parcourir récursivement le dossier du Bunker.
            *   Pour la recherche par contenu, la fonction lira les fichiers texte et cherchera la `query`.
            *   Pour les filtres de métadonnées (date, taille), elle utilisera `os.stat`.
            *   **Optimisation (Optionnelle)** : Mettre en place un fichier d'index simple (`.bunker_index.json`) pour accélérer les recherches futures. Cet index serait mis à jour lors des opérations de création/suppression/modification de fichiers.
        *   **Frontend (`bunker.html`)** :
            *   Ajouter une barre de recherche et des options de filtrage (ex: cases à cocher pour les types de fichiers, champs de date) à l'interface du Bunker.
            *   Au lancement de la recherche, appeler l'API `api.search_bunker`.
            *   Afficher les résultats dynamiquement, en mettant en surbrillance les "cercles de données" correspondants.

*   **Synchronisation mobile/desktop**
    *   **Concept** : Permettre la synchronisation des données du Bunker entre plusieurs appareils. L'approche initiale sera basée sur un dossier local géré par un service cloud tiers (Dropbox, Google Drive, etc.) pour éviter la complexité d'un serveur central.
    *   **Plan d'Implémentation Technique** :
        *   **Backend (`conteneur_monde.py`)** :
            *   Ajouter une section `sync` dans `config.json` pour stocker l'état (`enabled`) et le chemin du dossier de synchronisation.
            *   Modifier la logique de l'application pour que le chemin du Bunker (`user_folder_path`) pointe vers ce dossier de synchronisation si l'option est activée.
        *   **Frontend (`settings.html`)** :
            *   Ajouter une section "Synchronisation" dans les paramètres.
            *   Permettre à l'utilisateur d'activer la synchronisation et de sélectionner un dossier local via un dialogue (`api.open_folder_dialog`).
            *   Afficher un avertissement clair sur les risques de corruption de données si plusieurs instances de l'application écrivent dans le dossier en même temps.

*   **Chat user-user anonyme**
    *   **Concept** : Créer une extension de chat anonyme et éphémère. Nécessite un serveur relais central pour fonctionner.
    *   **Plan d'Implémentation Technique** :
        *   **Serveur Relais (Composant externe)** :
            *   Développer un petit serveur WebSocket (ex: avec Flask-SocketIO ou FastAPI) destiné à être déployé sur un service public.
            *   Ce serveur gérera les connexions, assignera des identifiants temporaires et relaiera les messages sans jamais les stocker.
        *   **Backend (Client, `conteneur_monde.py`)** :
            *   Créer une nouvelle extension `Chat Anonyme` dans `generateur_conteneurs.py`.
            *   La logique de l'extension se connectera au serveur WebSocket externe.
            *   Développer des API pour envoyer et recevoir les messages via le pont pywebview.
        *   **Frontend (Nouveau `anonymous_chat.html`)** :
            *   Créer une interface de chat simple avec une zone d'affichage des messages et un champ de saisie.
            *   Utiliser le client JavaScript WebSocket pour communiquer avec le backend de l'application, qui relaiera les messages au serveur central.

*   **Capture d'écran dans Logicateur**
    *   **Concept** : Permettre à l'utilisateur de prendre une capture d'écran de la conversation avec l'IA et de la sauvegarder dans le Bunker.
    *   **Plan d'Implémentation Technique** :
        *   **Backend (`conteneur_monde.py`)** :
            *   Créer une nouvelle API `api.save_screenshot_from_data_url(data_url, filename)`.
            *   Cette API recevra une image encodée en Base64, la décodera et la sauvegardera sous forme de fichier PNG dans le Bunker.
        *   **Frontend (`logicateur.html`)** :
            *   Ajouter un bouton "Capturer" à l'interface.
            *   Au clic, utiliser la bibliothèque JavaScript `html2canvas` pour capturer le `div` contenant l'historique de la conversation.
            *   Convertir le canevas généré en une URL de données Base64 (`canvas.toDataURL('image/png')`).
            *   Appeler l'API `api.save_screenshot_from_data_url` avec cette URL.

*   **EXTENSION IDE intégrée**
    *   **Concept** : Fournir un environnement de développement intégré pour que les utilisateurs puissent écrire et exécuter des scripts (ex: Python) directement dans l'application, en interagissant avec leurs données du Bunker.
    *   **Plan d'Implémentation Technique** :
        *   **Étape 1 : Fondations de l'Extension**
            *   Déclarer l'extension `IDE` dans `generateur_conteneurs.py`.
            *   Créer le template `ide.html`.
        *   **Étape 2 : Éditeur de Code**
            *   **Frontend** : Intégrer un éditeur de code web comme **Monaco Editor** (le moteur de VS Code) dans `ide.html`.
            *   **Backend** : Réutiliser les API du Bunker (`read_bunker_file`, `create_bunker_file`) pour ouvrir et sauvegarder des fichiers dans l'éditeur.
        *   **Étape 3 : Explorateur de Fichiers**
            *   **Frontend** : Créer un panneau latéral dans `ide.html` qui affiche l'arborescence du Bunker en utilisant l'API `api.list_bunker_files`. Permettre de cliquer sur un fichier pour l'ouvrir dans l'éditeur.
        *   **Étape 4 : Exécution de Code**
            *   **Backend** : Créer une API `api.execute_script_in_sandbox(filepath)`. Cette fonction utilisera l'extension "Chargeur d'Applications Universel" pour copier le script dans la sandbox Docker et l'exécuter de manière sécurisée.
            *   **Frontend** : Ajouter un bouton "Exécuter" qui appelle cette API. Intégrer un terminal web (avec **xterm.js**) dans l'interface de l'IDE pour afficher en temps réel la sortie (stdout/stderr) du script exécuté dans la sandbox.

*   **Surveillance de plateformes sociales et analyse de tendances**
    *   **Concept** : Créer une extension qui permet de surveiller des cibles (mots-clés, utilisateurs) sur des plateformes sociales en arrière-plan et de notifier l'utilisateur des nouvelles activités.
    *   **Plan d'Implémentation Technique** :
        *   **Backend (`conteneur_monde.py` et nouvelle extension)** :
            *   Créer une nouvelle extension `Social Monitor`.
            *   Intégrer un gestionnaire de tâches en arrière-plan (ex: `APScheduler`).
            *   Créer des API pour `add_watch(target)`, `remove_watch(target)`, et `get_watch_results(target)`.
            *   Lorsqu'une surveillance est ajoutée, une tâche planifiée est créée. Elle exécute périodiquement un script de scan (ex: la logique de Sherlock ou un scraper dédié) pour la cible.
            *   Les résultats sont stockés dans une base de données légère (ex: SQLite) dans le Bunker pour la persistance.
        *   **Frontend (Nouveau `social_monitor.html`)** :
            *   Interface pour ajouter, voir et supprimer les cibles surveillées.
            *   Un tableau de bord pour afficher les dernières informations collectées pour chaque cible.
            *   Un système de notification simple dans l'interface principale (`terminaux.html`) pour alerter l'utilisateur de nouvelles découvertes.

*   **Recherche et analyse de données de renseignement spécifiques (militaire, etc.)**
    *   **Concept** : Il ne s'agit pas de créer une fonctionnalité autonome, mais d'adapter les outils existants pour des cas d'usage avancés. L'application fournit les outils, l'utilisateur les applique.
    *   **Plan d'Implémentation Technique** :
        *   **OSINT Aggregator** : Ajouter des modules de recherche personnalisables permettant à l'utilisateur de définir ses propres sources de données (forums spécifiques, sites d'archives publics).
        *   **Logicateur** : Permettre à l'utilisateur de définir des "prompts système" personnalisés dans les paramètres pour spécialiser l'IA dans l'analyse de types de données spécifiques (jargon militaire, analyse de métadonnées, etc.).
        *   **IDE** : L'IDE devient l'outil central. L'utilisateur peut y écrire ses propres scripts d'analyse (avec des bibliothèques comme `pandas` ou `networkx` installées dans la sandbox) pour traiter et croiser les données brutes collectées via l'OSINT.
        *   **Nouvelle Extension (potentielle)** : `Visualiseur de Graphes`. Une extension qui utilise une bibliothèque comme `vis.js` pour créer des représentations graphiques des relations entre les entités découvertes, à partir de données structurées (ex: JSON) exportées par les scripts de l'IDE.


*   **NIVEAU XXX - Niveau "Coquin"**
    *   **Concept** : Un niveau avec du contenu pour adultes.
    *   **Considérations** : Nécessite un système de vérification d'âge robuste, une isolation complète, une journalisation renforcée et un consentement explicite.


#### 🔍 Extensions Sociales Avancées

*   **Surveillance d'algorithmes et analyseur**
    *   **Concept** : Outil pour tracker le comportement des algorithmes de réseaux sociaux et générer des rapports.

*   **Surveillance des trends VK et WeChat**
        *   **Défis techniques** : API restrictives, nécessité de scraping éthique, respect des CGU.
        *   **Approche recommandée** : Utiliser les API officielles, mettre en cache les données pour limiter les requêtes.

*   **Bots informationnels et republieurs**
        *   **Concept** : Créer des bots pour analyser et publier du contenu afin d'influencer les tendances sur diverses plateformes.

#### 🛠️ Fonctionnalités Techniques

*   **Auto-repair in-app avec rapports d'erreur**
    *   **Mécanisme proposé** : Diagnostic automatique, génération de logs structurés, et option de réparation.

*   **Formulaire d'envoi de rapports d'erreur**
        *   **Workflow** : Détection -> Collecte de contexte -> Anonymisation -> Envoi par email.
        *   **Sécurité** : Anonymisation des données, chiffrement, consentement utilisateur.

*   **Capture d'écran dans Logicateur**
        *   **Implémentation** : Utilisation de l'API Canvas ou de `html2canvas` avec options d'annotation.

*   **Synchronisation mobile/desktop**
        *   **Stratégie de sync** : Architecture basée sur CRDT, synchronisation différentielle, chiffrement de bout en bout.

#### 💬 Système de Communication

*   **Chat user-user anonyme**
        *   **Concept** : Système de messagerie sécurisée avec identifiants anonymes et chiffrement.
        *   **Aspects légaux** : Notification sur l'anonymat, consentement pour divulgation, journalisation minimaliste.

#### 📁 Gestion de Fichiers

*   **Outil de recherche avancée Bunker**
        *   **Filtres proposés** : Type MIME, date, taille, hash, métadonnées, contenu textuel.
        *   **Indexation suggérée** : Mise en place d'un index multi-critères pour des recherches rapides et pertinentes.

#### 💻 Environnement de Développement

*   **EXTENSION IDE intégrée**
        *   **Composants envisagés** : Terminal (xterm.js), explorateur de fichiers, éditeur de code (Monaco Editor), marketplace d'extensions, assistant IA.

### Considérations Techniques et Éthiques

*   **Aspects Légaux** : Respect des CGU, conformité RGPD, responsabilité des contenus générés.
*   **Sécurité** : Chiffrement de bout en bout, isolation sandbox, audits réguliers.
*   **Performance** : Indexation incrémentielle, cache stratégique, optimisation de la bande passante.

### Nouvelles Idées
- recherche et croisement de données de renseignement militaire russe
- recherche et ciblage d'agent de renseignement russe ou ex-urrs
- recherche et ciblage de trolls

=========================================================================================================
### Note sur la Finalisation pour une Version Publique (v1.0)

**Objectif :** Polir l'application pour la rendre stable, accessible et maintenable pour une première version publique sur GitHub. Cette phase se concentre sur l'expérience utilisateur finale et la facilité de distribution.

*   **Étape 1 : Stabilité et Support Utilisateur**
    *   **Action :** Implémenter un système de rapport d'erreurs simple.
    *   **Raison :** Permettre aux utilisateurs de remonter les bugs facilement, avec des logs, pour accélérer la correction et améliorer la stabilité globale.
*   **Étape 2 : Expérience de Configuration (UX)**
    *   **Action :** Créer une interface graphique dans les paramètres pour gérer les clés API (IA, HIBP, etc.). ✓
    *   **Raison :** Supprimer la nécessité de modifier manuellement le `config.json`, ce qui est une barrière majeure pour les utilisateurs non-techniques.
*   **Étape 3 : Documentation et Accessibilité**
    *   **Action :** Rédiger une documentation utilisateur de base (un `GUIDE.md`) et enrichir le `README.md` avec des instructions claires pour les utilisateurs finaux.
    *   **Raison :** Assurer que les nouveaux venus comprennent le concept et les fonctionnalités clés de l'application.
*   **Étape 4 : Distribution**
    *   **Action :** Mettre en place un script pour packager l'application en exécutables multiplateformes (via PyInstaller ou similaire). (En cours)
    *   **Raison :** Permettre aux utilisateurs de télécharger et lancer l'application sans avoir à installer Python et les dépendances manuellement.