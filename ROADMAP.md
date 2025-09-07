# Roadmap du Projet

Cette section liste les fonctionnalités terminées, en cours et planifiées pour le projet.

## Fonctionnalités Terminées

-   **Transformation de l'Outil OSINT :** L'ancien "Centre d'Analyse" a été entièrement refondu et transformé en une extension dynamique et installable, l'**OSINT Aggregator** (assignée au Conteneur 17).
-   **Amélioration des Scans OSINT :** Les capacités de scan ont été étendues pour inclure des recherches réelles sur les réseaux sociaux (via `sherlock-project`) et une analyse des résultats par l'IA (Logicateur).
-   **Refactoring et Nettoyage :** Le code a été nettoyé, les modules renommés pour plus de clarté, et les anciens templates (`centre_analyse.html`, etc.) ont été supprimés après leur intégration dans le nouveau système d'extensions.
-   **Export des Rapports OSINT :** Ajout de la possibilité d'exporter les rapports de scan aux formats JSON, TXT et CSV.
-   **Filtrage et Tri des Résultats OSINT :** Ajout de contrôles pour filtrer par mot-clé et trier les résultats de scan.
-   **Export OSINT vers Bunker :** Ajout de la possibilité d'exporter les rapports OSINT directement dans un nouveau dossier au sein du Bunker.
-   **Sélection des Modules de Scan OSINT :** Ajout de cases à cocher pour permettre des recherches ciblées (Web, Social, Fuites).
-   **Développement du Chargeur d'Applications Universel (Phases 1-3) :**
    -   **Socle de la Sandbox :** Implémentation du contrôle de conteneur Docker (démarrage, arrêt, statut) et de la vérification de la disponibilité de Docker.
    -   **Gestion du Système de Fichiers :** Mise en place d'un volume partagé persistant pour la sandbox, avec des API pour téléverser et lister des fichiers.
    -   **Préparation à l'Exécution Graphique :** Création d'une image Docker personnalisée avec les dépendances pour une interface graphique (Wine, Xvfb, VNC) et une API pour exécuter des commandes à l'intérieur.
    -   **Interface Utilisateur :** Développement de l'interface de base pour le contrôle de la sandbox, la gestion des fichiers et l'affichage des logs.
-   **Développement de l'Extension "Diagnostic Système" (Conteneur 42) :** Création d'un outil pour surveiller les ressources (CPU, RAM, Réseau) de la sandbox Docker en temps réel. L'extension est installable et fournit une interface de visualisation avec des jauges et des indicateurs qui se rafraîchissent automatiquement.
-   **Finalisation du Chargeur d'Applications Universel (Phase 5) :**
    -   **Intégration VNC :** Implémentation d'un client noVNC dans l'interface (`universal_loader.html`) pour afficher et interagir avec le bureau distant de la sandbox.
    -   **Orchestration Complète :** Le backend (`universal_loader.py`) gère le cycle de vie complet du conteneur, y compris l'exposition des ports VNC et la communication avec le frontend.

### Historique des Phases Terminées

#### Phase 1 : Fondations de l'Application ✓
-   **Initialisation du Projet :** Structure des dossiers, Flask, pywebview.
-   **Interface de Base :** Création de `terminaux.html` et `aboutissement.html`.
-   **Système de Niveaux :** Logique de navigation entre les "niveaux" de l'application.
-   **Logicateur (IA) :** Intégration d'une API d'IA (DeepSeek, OpenAI, etc.).
-   **Bunker (Gestionnaire de Fichiers) :**
    -   Création du dossier utilisateur.
    -   Interface de base pour lister les fichiers.
    -   CRUD (Créer, Lire, Mettre à jour, Supprimer) pour les fichiers et dossiers.
    -   Implémentation du glisser-déposer (Drag & Drop) pour l'upload.
    -   Logique de mot de passe et gestion des fichiers "spéciaux" (contaminés, inaccessibles).

#### Phase 2 : Système d'Extensions et Sécurité ✓
-   **Portail Conteneur :** Interface pour visualiser et "installer" des extensions.
-   **Extension OSINT Aggregator :** Développement complet de l'outil OSINT.
    -   Scan multi-modules (web, social, leaks).
    -   Sauvegarde et export des rapports.
    -   Analyse des résultats par l'IA.
-   **Sandboxing Logique :** Isoler les extensions du cœur de l'application via une `SandboxAPI`.

#### Phase 3 : Chargeur d'Applications Universel (Backend) ✓
-   **Logique Docker :** Créer une extension qui peut démarrer/arrêter un conteneur Docker.
-   **Tunnel de Communication :** Établir un canal sécurisé (WebSocket) entre l'hôte et le conteneur.
-   **Téléversement de Fichiers :** Permettre l'envoi de fichiers de l'hôte vers la sandbox.

#### Phase 4 : Chargeur d'Applications Universel (Frontend) ✓
-   **Interface de Base :** Créer `universal_loader.html` avec les contrôles de base.
-   **Exécution de Commandes :** Envoyer des commandes depuis l'interface vers la sandbox via le tunnel.
-   **Configuration VNC :** Configurer le conteneur Docker avec un serveur VNC (ex: `x11vnc`).
-   **Phase 5 : Finalisation Chargeur d'Applications Universel ✓**
    -   Intégrer un client VNC JavaScript (noVNC) dans l'interface.
    -   Gérer la connexion et l'affichage du bureau de la sandbox.
    -   Configurer noVNC pour capturer les événements clavier/souris et les transmettre au serveur VNC.

## Fonctionnalités en Cours et à Venir
 
### Phase 6 : Interface & UX - "Palimpseste Technologique" (Terminée ✓)
-   **Refonte Visuelle du Configurateur (Niveau 0) :**
    -   **Concept :** L'interface évolue visuellement en remontant le temps technologique lors du défilement vers le bas (Cyberpunk -> WinXP -> DOS).
    -   **Étape 6.1 : Conception des "Ères Technologiques".** ✓
    -   **Étape 6.2 : Structure HTML unifiée.** ✓
    -   **Étape 6.3 : Implémentation du "Time-Scroll".** ✓
    -   **Étape 6.4 : Transitions et finitions.** ✓
 
### Phase 7 : Authentification et Sécurité (En cours ▶)
-   **Système d'Accès à Trois Niveaux :**
    -   **Étape 7.1 : Définition des Rôles.** ✓
        -   **Concepteur :** Accès total via un mot de passe maître non modifiable. Privilèges maximums.
        -   **Testeur :** Accès étendu via un code spécial à usage unique ou multiple, saisi dans le champ pseudo. Débloque toutes les extensions.
        -   **Utilisateur Lambda :** Accès standard via la création d'un compte (pseudo + mot de passe). Accès à un sous-ensemble d'extensions par défaut.
    -   **Étape 7.2 : Implémentation de la Logique d'Authentification.** ✓
        -   Mettre à jour la fonction `check_bunker_password` (ou créer une nouvelle fonction de login) pour gérer les trois cas de figure.
        -   Créer la logique pour lire une liste de codes "Testeur" depuis un fichier externe (qui sera défini par le Concepteur).
    -   **Étape 7.3 : Adaptation de l'Interface de Connexion.** ✓
        -   La page `aboutissement.html` servira de portail de connexion. Le champ "pseudo" acceptera soit un pseudo pour la création de compte, soit un code testeur.
    -   **Étape 7.4 : Gestion des Privilèges par Rôle.** ✓
        -   Modifier la logique de chargement des extensions (`get_installed_extensions`, menu dynamique) pour qu'elle filtre les extensions affichées en fonction du rôle de l'utilisateur connecté.
-   **Boutons de Sécurité (Paramètres) :** (À faire)
    -   **"Vider le cache" :** Archive le Bunker (`cmd-ai-after-cache-kill.zip`) et remet l'app à l'état post-install.
    -   **"Kill-app" :** Désinstallation complète avec privilèges admin et effacement des traces.
    -   **"Crash" :** Cumul précédent + attaque killram pour redémarrage forcé et vidage RAM.

### Phase 8 : Session de Première Utilisation Guidée (À faire)
-   **Concept :** Créer une expérience d'accueil interactive ("wizard") pour les nouveaux utilisateurs, les guidant à travers la création de leur identité et la configuration initiale de l'application avec un ton immersif.
-   **Étape 8.1 : Détection du Premier Lancement.** Implémenter une logique qui vérifie l'absence de mot de passe dans `config.json` pour déclencher la session guidée.
-   **Étape 8.2 : Conception de l'Interface du "Guide".** Créer `wizard.html` comme interface en plusieurs étapes pour l'accueil.
-   **Étape 8.3 : Création de l'Identité Cryptée.** Étape dédiée à la saisie du pseudonyme et du mot de passe, qui seront sauvegardés pour créer le premier compte utilisateur.
-   **Étape 8.4 : Configuration du Bunker.** Permettre à l'utilisateur de confirmer ou de choisir l'emplacement de son dossier Bunker.
-   **Étape 8.5 : Orchestration Backend.** Créer les routes et fonctions API (`complete_first_run_setup`) pour gérer la séquence de configuration et la redirection finale vers l'interface principale.
 
### Phase 9 : Bunker - Gestion Avancée des Fichiers (Terminée ✓)
-   **Suppression de Fichiers :** API `delete_bunker_file()` et bouton de suppression avec confirmation. ✓
-   **Cercles Spéciaux :** Implémentation de logiques de gameplay pour des fichiers spéciaux. ✓
    -   **Contaminés (`neural_ghost.py`) :** L'exécution du fichier déclenche une "infection" du système, activant une porte dérobée et un keylogger persistant qui enregistre l'activité simulée dans `keylogscornflakes.md`. ✓
    -   **Bloqués :** Contenu chiffré, simulation de modification des politiques de sécurité hôte au clic. ✓
    -   **Keylogger (`svchost.exe.bak`) :** Déploiement probabiliste (1/4) d'un keylogger (simulé) persistant sur l'hôte. ✓
-   **Animations de Traitement :** État "processing" avec animations CSS pour les opérations sur les fichiers spéciaux. ✓
-   **Collision des Cercles :** Les cercles entrent en collision entre eux et avec la console centrale (qui agit comme un obstacle statique). ✓
-   **Intégration OSINT :** Bouton d'envoi vers l'analyseur dans les dossiers OSINT. ✓

## Feuille de Route Future et Analyse Détaillée

Cette section présente une analyse technique des idées et une proposition de roadmap pour les développements futurs.

### Idées Proposées et Analyse Technique

#### 🎯 Niveaux et Expérience Utilisateur

*   **NIVEAU XXX - Niveau "Coquin"**
    *   **Concept** : Un niveau avec du contenu pour adultes.
    *   **Considérations** : Nécessite un système de vérification d'âge robuste, une isolation complète, une journalisation renforcée et un consentement explicite.

*   **NIVEAU MEDIAS - Flux Vidéos**
    *   **Proposition** : Intégration de streaming vidéo.
    *   **Architecture suggérée** : Player HTML5 personnalisé, cache local, support multi-format (MP4, WebM, HLS).

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

### Considérations Techniques et Éthiques

*   **Aspects Légaux** : Respect des CGU, conformité RGPD, responsabilité des contenus générés.
*   **Sécurité** : Chiffrement de bout en bout, isolation sandbox, audits réguliers.
*   **Performance** : Indexation incrémentielle, cache stratégique, optimisation de la bande passante.

### Recommandations d'Implémentation (Nouvelles Phases)

*   **Phase 10 - Fondations (2-3 semaines)**
    1.  Système de rapports d'erreur.
    2.  Recherche avancée Bunker.
    3.  Synchronisation de base.

*   **Phase 11 - Fonctionnalités Core (3-4 semaines)**
    1.  Chat anonyme.
    2.  Capture d'écran.
    3.  IDE basique.

*   **Phase 12 - Avancé (4-6 semaines)**
    1.  Surveillance algorithmique.
    2.  Bots informationnels (version limitée).
    3.  Monitoring plateformes sociales.

*   **Phase 13 - Expérimental (ongoing)**
    1.  Niveau XXX (après validation juridique).
    2.  Bots avancés.
    3.  Intégration deep learning.