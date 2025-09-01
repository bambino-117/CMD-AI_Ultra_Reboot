import tkinter as tk
from tkinter import ttk
import random
import colorsys

class MarketplaceTiles:
    def __init__(self, parent, dispatcher):
        self.parent = parent
        self.dispatcher = dispatcher
        self.tiles_window = None
        self.colors_used = set()
    
    def generate_imperial_color(self):
        """Génère des couleurs style Empire (gris, bleus foncés, rouges sombres)"""
        imperial_colors = [
            '#2C3E50', '#34495E', '#1B2631', '#17202A',  # Gris Empire
            '#1F2937', '#374151', '#4B5563', '#6B7280',  # Gris modernes
            '#7F1D1D', '#991B1B', '#B91C1C', '#DC2626',  # Rouges sombres
            '#1E3A8A', '#1E40AF', '#2563EB', '#3B82F6',  # Bleus impériaux
            '#581C87', '#6B21A8', '#7C2D12', '#92400E'   # Violets/oranges sombres
        ]
        
        available_colors = [c for c in imperial_colors if c not in self.colors_used]
        if not available_colors:
            self.colors_used.clear()
            available_colors = imperial_colors
        
        color = random.choice(available_colors)
        self.colors_used.add(color)
        return color
    
    def get_contrasting_color(self, bg_color):
        """Retourne une couleur contrastante"""
        hex_color = bg_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return '#FFFFFF' if luminance < 0.5 else '#000000'
    
    def show_marketplace_tiles(self):
        """Affiche le marketplace avec des tuiles cliquables"""
        if self.tiles_window:
            self.tiles_window.destroy()
        
        # Créer une nouvelle fenêtre
        self.tiles_window = tk.Toplevel(self.parent.root)
        self.tiles_window.title("🔌 Marketplace - Extensions")
        self.tiles_window.geometry("800x600")
        self.tiles_window.configure(bg='#0D1117')  # Fond sombre style Empire
        
        # Frame principal avec scrollbar (fond noir)
        main_frame = tk.Frame(self.tiles_window, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(main_frame, bg='#0D1117', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Espace en haut (sans titre)
        spacer = tk.Frame(scrollable_frame, bg='#0D1117', height=10)
        spacer.pack()
        
        # Récupérer les extensions
        marketplace = self.dispatcher.plugin_manager.get_marketplace()
        plugins = marketplace.get('plugins', [])
        installed_plugins = {p['id'] for p in self.dispatcher.plugin_manager.installed_plugins['plugins']}
        
        # Créer les tuiles en grille (fond noir)
        tiles_frame = tk.Frame(scrollable_frame, bg='#000000')
        tiles_frame.pack(fill='both', expand=True)
        
        for i, plugin in enumerate(plugins):
            row = i // 3
            col = i % 3
            
            self.create_imperial_tile(tiles_frame, plugin, installed_plugins, row, col)
        
        # Pack le canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bouton fermer
        close_btn = tk.Button(
            self.tiles_window,
            text="❌ FERMER",
            command=self.tiles_window.destroy,
            bg='#7F1D1D',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=3
        )
        close_btn.pack(side='bottom', pady=10)
    
    def create_imperial_tile(self, parent, plugin, installed_plugins, row, col):
        """Crée une tuile style caisse impériale"""
        is_installed = plugin['id'] in installed_plugins
        bg_color = self.generate_imperial_color()
        text_color = self.get_contrasting_color(bg_color)
        
        # Créer la tuile impériale personnalisée
        from ui.imperial_tile_widget import ImperialTile
        
        tile = ImperialTile(
            parent, 
            plugin, 
            is_installed, 
            bg_color, 
            text_color,
            self.show_extension_detail
        )
        
        tile.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configurer le grid
        parent.grid_columnconfigure(col, weight=1)
    
    def on_tile_hover(self, widget, entering):
        """Effet hover sur les tuiles"""
        if entering:
            widget.configure(cursor="hand2")
        else:
            widget.configure(cursor="")
    
    def show_extension_detail(self, plugin, is_installed):
        """Affiche les détails d'une extension dans une fenêtre dédiée"""
        from ui.extension_detail_window import ExtensionDetailWindow
        
        detail_window = ExtensionDetailWindow(self.parent, plugin, is_installed, self.dispatcher)
        detail_window.show_detail_window()
    
    def get_extension_readme(self, plugin_id):
        """Génère un README pour l'extension"""
        readmes = {
            'weather': """🌤️ EXTENSION MÉTÉO

FONCTIONNALITÉS:
• Météo actuelle par ville
• Prévisions 3 jours
• Géolocalisation automatique
• Données météo détaillées

COMMANDES:
• ext Weather current [ville] - Météo actuelle
• ext Weather forecast [ville] - Prévisions
• ext Weather help - Aide complète

EXEMPLES:
• ext Weather current Paris
• ext Weather forecast London
• ext Weather current (utilise Paris par défaut)""",

            'filemanager': """📁 GESTIONNAIRE DE FICHIERS

FONCTIONNALITÉS:
• Recherche de fichiers par pattern
• Organisation automatique par type
• Détection de fichiers dupliqués
• Nettoyage des fichiers temporaires

COMMANDES:
• ext FileManager search [pattern] - Rechercher
• ext FileManager organize [dossier] - Organiser
• ext FileManager duplicate [dossier] - Doublons
• ext FileManager clean - Nettoyer

EXEMPLES:
• ext FileManager search "*.pdf"
• ext FileManager organize ~/Downloads
• ext FileManager duplicate .""",

            'networktools': """🌐 OUTILS RÉSEAU

FONCTIONNALITÉS:
• Test de connectivité (ping)
• Scan de ports réseau
• Test de vitesse internet
• Géolocalisation d'adresses IP
• Scan des réseaux WiFi

COMMANDES:
• ext NetworkTools ping [host] - Tester connexion
• ext NetworkTools scan [ip] - Scanner ports
• ext NetworkTools speed - Test vitesse
• ext NetworkTools ip [adresse] - Info IP
• ext NetworkTools wifi - Scanner WiFi

EXEMPLES:
• ext NetworkTools ping google.com
• ext NetworkTools scan 192.168.1.1
• ext NetworkTools speed""",

            'systemmonitor': """🖥️ MONITORING SYSTÈME

FONCTIONNALITÉS:
• Statut système complet
• Top des processus consommateurs
• Usage des disques
• Statistiques réseau
• Températures système
• Monitoring temps réel

COMMANDES:
• ext SystemMonitor status - Statut général
• ext SystemMonitor processes - Top processus
• ext SystemMonitor disk - Usage disques
• ext SystemMonitor network - Stats réseau
• ext SystemMonitor temp - Températures
• ext SystemMonitor monitor - Temps réel

EXEMPLES:
• ext SystemMonitor status
• ext SystemMonitor processes""",

            'texttools': """🔤 OUTILS DE TEXTE

FONCTIONNALITÉS:
• Recherche et remplacement regex
• Génération de hash (MD5, SHA256, etc.)
• Encodage/décodage (Base64, Hex, URL)
• Formatage de texte avancé
• Analyse et comptage de texte

COMMANDES:
• ext TextTools regex "pattern|texte" - Regex
• ext TextTools hash "texte|algo" - Hash
• ext TextTools encode "texte|format" - Encoder
• ext TextTools decode "texte|format" - Décoder
• ext TextTools format "texte|format" - Formater
• ext TextTools count "texte" - Analyser

EXEMPLES:
• ext TextTools hash "password|sha256"
• ext TextTools regex "\\d+|J'ai 25 ans"
• ext TextTools encode "Hello|base64" """,

            'usbmanager': """💾 GESTIONNAIRE USB

FONCTIONNALITÉS:
• Détection automatique des périphériques USB
• Informations détaillées (taille, espace libre, type)
• Éjection sécurisée cross-platform
• Support Windows, macOS, Linux
• Scan du contenu des périphériques

COMMANDES:
• ext USBManager list - Lister périphériques USB
• ext USBManager info [device] - Infos détaillées
• ext USBManager unmount [device] - Éjection sécurisée
• ext USBManager scan [device] - Scanner le contenu
• ext USBManager help - Aide complète

EXEMPLES:
• ext USBManager list
• ext USBManager info D: (Windows)
• ext USBManager info /dev/sdb1 (Linux)
• ext USBManager unmount /dev/sdb1

⚠️ SÉCURITÉ:
• Toujours éjecter avant de débrancher
• Vérifier qu'aucun fichier n'est en cours d'écriture
• Sauvegarder les données importantes""",

            'scriptmoica': """🎨 SCRIPT MOI ÇA, CHIEN!

GÉNÉRATEUR D'INTERFACES AUTOMATIQUE
Analyse vos designs et génère du code Python !

FONCTIONNALITÉS:
• Plugins pour GIMP, Krita, Photoshop
• Analyse automatique d'images d'interface
• Détection intelligente : boutons, champs, labels
• Génération multi-format : Tkinter, PyQt5, HTML/CSS
• Renvoi automatique vers CMD-AI
• Interface intégrée dans les éditeurs

COMMANDES:
• ext UIPluginManager install - Installer plugins
• ext UIPluginManager status - Vérifier logiciels
• ext UIPluginManager uninstall - Désinstaller
• ext UIPluginManager help - Aide complète

WORKFLOW:
1. Installez les plugins avec 'install'
2. Ouvrez GIMP/Krita/Photoshop
3. Créez/ouvrez une image d'interface
4. Utilisez le plugin 'UI Generator'
5. Obtenez le code Python automatiquement
6. Code sauvé dans user/generated_interfaces/

LOGICIELS SUPPORTÉS:
• GIMP (toutes versions) - Plugin Python-Fu
• Krita (4.0+) - Docker PyQt5 intégré
• Photoshop (2022+) - Extension CEP

FORMATS DE SORTIE:
• Tkinter - Interface Python native
• PyQt5 - Interface moderne Qt
• HTML/CSS - Pages web responsives

DÉTECTION INTELLIGENTE:
• Rectangles → Boutons/Champs/Frames
• Texte → Labels et titres
• Formes → Widgets spécialisés
• Couleurs → Thèmes automatiques
• Positions → Placement précis

AVANTAGES:
• Plus besoin de coder l'interface manuellement
• Gain de temps considérable
• Code propre et optimisé
• Intégration directe dans les éditeurs pros
• Remplacement de l'ancien GIMP Clone Studio

EXEMPLES D'USAGE:
• Mockup → Code Tkinter en 30 secondes
• Design Figma → Interface PyQt5 fonctionnelle
• Wireframe → Page HTML responsive

🎯 RÉVOLUTIONNEZ VOTRE WORKFLOW DE DÉVELOPPEMENT!""",

            'securitytoolkit': """🛡️ SECURITY TOOLKIT - CONTENEUR D'OUTILS

⚠️ CONTENEUR D'OUTILS DE SÉCURITÉ :
Regroupe 3 outils puissants pour tests de sécurité.
Utilisation strictement limitée aux fins légitimes !

🔧 INTERFACE CONTENEUR :
Menu interactif avec accès séparé à chaque outil :

1️⃣ ⚠️💀⚠️ KILLRAM ⚠️💀⚠️
   • Saturation mémoire système
   • DÉSACTIVÉ PAR DÉFAUT
   • Entouré de symboles de danger
   • Avertissement machine critique
   
2️⃣ ⚡ BADUSB CREATOR
   • Émulation clavier malveillant
   • Payloads HID intégrés
   • Tests de sécurité USB
   
3️⃣ 🔥 USBKILLER DESIGNER
   • Schémas circuits destructeurs
   • Documentation électronique
   • Composants et précautions

FONCTIONNALITÉS :
• Menu interactif avec choix numérotés
• Décharge de responsabilité intégrée
• Codes BadUSB intégrés depuis collection
• Schémas USBKiller détaillés
• Documentation technique complète

COMMANDES :
• ext SecurityToolkit menu - Menu conteneur principal
• ext SecurityToolkit killram - ⚠️💀 KillRAM (DANGER)
• ext SecurityToolkit badusb - ⚡ BadUSB Creator
• ext SecurityToolkit usbkiller - 🔥 USBKiller Designer
• ext SecurityToolkit disclaimer - Avertissements
• ext SecurityToolkit help - Aide complète

EXEMPLES :
• ext SecurityToolkit disclaimer
• ext SecurityToolkit menu
• ext SecurityToolkit badusb

⚠️💀⚠️ KILLRAM - OUTIL CRITIQUE ⚠️💀⚠️
• Saturation mémoire RAM du système
• 10 niveaux d'intensité (1=léger, 10=critique)
• DÉSACTIVÉ PAR DÉFAUT pour sécurité
• Fichier isolé : killram_extension_SECURE_BACKUP.py
• AVERTISSEMENT MACHINE : Risque de crash total
• ACTIVATION MANUELLE REQUISE après téléchargement

🔓 ACTIVATION KILLRAM :
1. Localiser : extensions/killram_extension_SECURE_BACKUP.py
2. Renommer en : killram_extension.py
3. Redémarrer CMD-AI Ultra Reboot
4. Accepter décharge de responsabilité
5. ⚠️ UTILISER UNIQUEMENT SUR MACHINES DE TEST ⚠️

BADUSB CREATOR :
• Émulation clavier/souris malveillant
• Codes intégrés depuis votre collection
• Payloads Windows, Linux, macOS
• Émulateur HID avancé avec sécurités
• Simulation éducative sécurisée

USBKILLER DESIGNER :
• Schémas circuits destructeurs
• 4 types : Simple, Amplifié, Total, Répétitif
• Surtension 5V→220V+ (DESTRUCTEUR !)
• Liste composants + précautions
• Documentation électronique détaillée

🚫 UTILISATIONS INTERDITES :
• Attaques malveillantes
• Destruction de matériel tiers
• Violation de systèmes sans autorisation
• Toute utilisation illégale

⚖️ DÉCHARGE DE RESPONSABILITÉ :
Le développeur décline toute responsabilité pour les dommages
matériels, logiciels ou légaux. Utilisateur seul responsable.

🎯 UTILISATIONS LÉGITIMES :
• Tests de sécurité autorisés (pentest)
• Recherche en cybersécurité
• Éducation et formation
• Tests sur matériel personnel

🛡️ INTERFACE UNIFIÉE :
Menu interactif en zone de texte avec navigation
par choix numérotés et accès direct aux outils.""",

            'dataanalyzer': """🤖 DATA ANALYZER - ANALYSEUR IA

ANALYSE INTELLIGENTE DES DONNÉES
Interprétation automatique des résultats complexes !

FONCTIONNALITÉS :
• Analyse multi-sources (OSINT, réseau, système)
• Détection automatique d'anomalies
• Corrélation de données intelligente
• Génération de rapports IA
• Visualisations graphiques
• Recommandations contextuelles

COMMANDES :
• ext DataAnalyzer analyze [source] - Analyser données
• ext DataAnalyzer interpret [type] - Interpréter résultats
• ext DataAnalyzer visualize [type] - Créer graphiques
• ext DataAnalyzer report [type] - Rapports IA
• ext DataAnalyzer patterns [source] - Détecter patterns
• ext DataAnalyzer help - Aide complète

SOURCES SUPPORTÉES :
• OSINT - Résultats de recherche renseignement
• Network - Données réseau et connexions
• System - Monitoring système et performance
• Logs - Fichiers de logs et événements
• Custom - Fichiers de données personnalisés

ANALYSE IA AVANCÉE :
• Détection patterns temporels
• Identification anomalies comportementales
• Scoring automatique des risques
• Prédiction de tendances
• Corrélations cachées

VISUALISATIONS :
• Timelines interactives des événements
• Graphiques de corrélation
• Cartes de réseau et connexions
• Matrices de risques
• Tableaux de bord dynamiques

RAPPORTS GÉNÉRÉS :
• Rapport sécurité complet avec scoring
• Analyse performance avec recommandations
• Synthèse OSINT avec corrélations
• Résumé exécutif pour management

EXEMPLES D'USAGE :
• Analyser résultats scan OSINT complexe
• Interpréter données monitoring réseau
• Détecter patterns suspects dans logs
• Générer rapport sécurité automatique
• Visualiser évolution performance système

INTÉGRATION :
• Compatible avec toutes les extensions CMD-AI
• Import/export formats standards
• API pour intégration personnalisée
• Sauvegarde automatique des analyses

🤖 TRANSFORMEZ VOS DONNÉES EN INSIGHTS ACTIONABLES !""",

            'crashreporter': """📋 CRASH REPORTER - GESTIONNAIRE TESTEURS

SYSTÈME DE RAPPORT AUTOMATIQUE
Aide les développeurs à corriger les bugs rapidement !

FONCTIONNALITÉS :
• Capture automatique des erreurs
• Rapports manuels pour testeurs
• Envoi sécurisé aux développeurs
• Gestion locale des rapports
• Nettoyage automatique
• Anonymisation des données

COMMANDES :
• ext CrashReporter list - Lister rapports
• ext CrashReporter report "description" - Rapport manuel
• ext CrashReporter send - Envoyer rapports
• ext CrashReporter clean - Nettoyer anciens
• ext CrashReporter help - Aide complète

CAPTURE AUTOMATIQUE :
• Tracebacks Python complets
• Informations système contextuelles
• Logs récents inclus
• Horodatage précis
• Environnement d'exécution

RAPPORTS MANUELS :
• Problèmes de performance
• Comportements étranges
• Suggestions d'amélioration
• Bugs difficiles à reproduire
• Retours d'expérience

ENVOI SÉCURISÉ :
• Chiffrement des communications
• Anonymisation automatique
• Pas de données personnelles
• Envoi volontaire uniquement
• Confirmation utilisateur

CONFIDENTIALITÉ :
• Stockage local sécurisé
• Suppression automatique (30 jours)
• Aucune collecte de données privées
• Respect RGPD complet
• Transparence totale

POUR LES TESTEURS :
• Contribution précieuse au développement
• Correction rapide des bugs signalés
• Amélioration continue de l'app
• Reconnaissance de la communauté
• Accès aux versions bêta

EXEMPLES D'USAGE :
• Signaler crash au démarrage
• Rapporter lenteur interface
• Suggerer nouvelle fonctionnalité
• Documenter bug reproductible
• Partager retour d'expérience

INTÉGRATION POWERSHELL/CMD :
• Scripts d'envoi automatique Windows
• Commandes curl pour Linux/macOS
• Webhooks configurés
• Notifications de confirmation

📋 AIDEZ-NOUS À AMÉLIORER CMD-AI POUR TOUS !""",

            'killram_old': """🔒 KILLRAM - EXTENSION DÉSACTIVÉE

🔒 STATUT : DÉSACTIVÉE POUR SÉCURITÉ

Cette extension a été désactivée pour protéger votre système.

⚠️ RAISONS DE LA DÉSACTIVATION :
• Risque de crash système complet
• Perte de données possible
• Outil potentiellement destructif
• Non adapté aux machines de production

FONCTIONNALITÉS ORIGINALES :
• Saturation mémoire RAM du système
• Tests de stress mémoire extrêmes
• 10 niveaux d'intensité (1=léger, 10=critique)
• Threads multiples pour saturation rapide

COMMANDE ACTUELLE :
• ext KillRAM disabled - Message de désactivation

🔓 POUR RÉACTIVER (DÉCONSEILLÉ) :
1. Localiser : extensions/killram_extension_SECURE_BACKUP.py
2. Renommer en : killram_extension.py
3. Redémarrer l'application
4. Accepter la décharge de responsabilité

⚠️ AVERTISSEMENT :
La réactivation de cette extension peut endommager votre système.
Utilisez uniquement sur des machines de test ou virtuelles.

🔒 PROTECTION ACTIVE :
Votre système est protégé contre l'exécution accidentelle de cet outil

⚠️ AVERTISSEMENT CRITIQUE :
Cet outil peut ENDOMMAGER votre système et causer une PERTE DE DONNÉES.
Utilisation à vos propres risques uniquement !

FONCTIONNALITÉS :
• Saturation mémoire RAM du système
• Tests de stress mémoire
• Simulation de conditions dégradées
• 10 niveaux d'intensité (1=léger, 10=critique)
• Décharge de responsabilité intégrée

COMMANDES :
• ext KillRAM disclaimer - Voir avertissements
• ext KillRAM accept - Accepter les risques
• ext KillRAM start [1-10] - Démarrer attaque
• ext KillRAM stop - Arrêter (si possible)
• ext KillRAM status - Statut de l'attaque

EXEMPLES :
• ext KillRAM disclaimer
• ext KillRAM accept
• ext KillRAM start 3 (intensité légère)
• ext KillRAM start 8 CONFIRM (critique)

🚫 UTILISATIONS INTERDITES :
• Attaques malveillantes
• Sabotage de systèmes tiers
• Déni de service
• Toute utilisation illégale

⚖️ DÉCHARGE DE RESPONSABILITÉ :
Le développeur (CMD-AI Team) décline toute responsabilité
pour les dommages causés par cet outil. Utilisateur seul responsable.

🎯 UTILISATIONS LÉGITIMES :
• Tests de robustesse d'applications
• Recherche en sécurité informatique
• Tests de stress mémoire
• Simulation de conditions de faible mémoire"""
        }
        
        return readmes.get(plugin_id, f"""📖 README - {plugin_id.upper()}

Cette extension fait partie du marketplace CMD-AI Ultra Reboot.

Pour plus d'informations, utilisez:
ext {plugin_id} help

Consultez la documentation complète après installation.""")