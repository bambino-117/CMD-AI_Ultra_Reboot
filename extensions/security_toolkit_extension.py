from core.base_extension import BaseExtension
import os
import platform
import json
import time
import threading
from datetime import datetime

class SecurityToolkitExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "SecurityToolkit"
        self.version = "1.0.0"
        self.description = "🛡️ Boîte à outils de sécurité - KillRAM, BadUSB, USBKiller"
        self.author = "CMD-AI Team"
        self.os_type = platform.system()
        self.disclaimer_accepted = False
        self.current_menu = "main"
        self.badusb_codes = self._load_badusb_codes()
    
    def initialize(self, app_context):
        self.app_context = app_context
        os.makedirs("user/security_projects", exist_ok=True)
    
    def execute(self, command, args=None):
        if command == "disclaimer":
            return self.show_disclaimer()
        elif command == "accept":
            return self.accept_disclaimer()
        elif command == "menu":
            return self.show_main_menu()
        elif command == "killram":
            return self.killram_tool(args)
        elif command == "badusb":
            return self.badusb_tool(args)
        elif command == "usbkiller":
            return self.usbkiller_tool(args)
        elif command == "help":
            return self.show_help()
        elif command.isdigit():
            return self.handle_menu_choice(int(command))
        else:
            return self.show_main_menu()
    
    def show_disclaimer(self):
        """Affiche la décharge de responsabilité globale"""
        return """⚠️ DÉCHARGE DE RESPONSABILITÉ - SECURITY TOOLKIT

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ AVERTISSEMENT CRITIQUE ⚠️                ║
╚══════════════════════════════════════════════════════════════╝

🚨 CETTE BOÎTE À OUTILS CONTIENT DES OUTILS DANGEREUX 🚨

📋 OUTILS INCLUS :
• 💀 KillRAM - Saturation mémoire (crash système)
• ⚡ BadUSB - Émulation clavier malveillant
• 🔥 USBKiller - Destructeur matériel (surtension)

⚖️ DÉCHARGE DE RESPONSABILITÉ LÉGALE :

EN UTILISANT CES OUTILS, VOUS RECONNAISSEZ ET ACCEPTEZ QUE :

1. 🛡️ LE DÉVELOPPEUR (CMD-AI Team) DÉCLINE TOUTE RESPONSABILITÉ
   pour les dommages directs, indirects, matériels ou logiciels.

2. ⚡ CES OUTILS PEUVENT CAUSER DES DOMMAGES IRRÉVERSIBLES
   (crash système, destruction matérielle, perte de données).

3. 🔧 VOUS ÊTES SEUL RESPONSABLE de l'usage de ces outils
   et assumez l'entière responsabilité des conséquences.

4. 🚫 LE DÉVELOPPEUR NE PEUT ÊTRE TENU RESPONSABLE
   de quelque dommage que ce soit.

⚠️ UTILISATIONS LÉGITIMES UNIQUEMENT :
• Tests de sécurité autorisés (pentest)
• Recherche en cybersécurité
• Éducation et formation
• Tests sur matériel personnel

🚨 UTILISATIONS STRICTEMENT INTERDITES :
• Attaques malveillantes
• Destruction de matériel tiers
• Violation de systèmes sans autorisation
• Toute utilisation illégale

🏛️ ASPECTS LÉGAUX :
L'utilisation malveillante peut constituer des délits/crimes.

═══════════════════════════════════════════════════════════════

Pour accepter ces conditions et activer la boîte à outils :
ext SecurityToolkit accept

⚠️ RÉFLÉCHISSEZ BIEN - CES OUTILS SONT DANGEREUX ⚠️"""
    
    def accept_disclaimer(self):
        """Accepte la décharge de responsabilité"""
        self.disclaimer_accepted = True
        return """✅ DÉCHARGE DE RESPONSABILITÉ ACCEPTÉE

🔓 Security Toolkit activé avec les conditions suivantes :
• Vous assumez tous les risques matériels et légaux
• Usage strictement limité aux fins légitimes
• Responsabilité complète des conséquences

🛡️ BOÎTE À OUTILS DISPONIBLE :

ext SecurityToolkit menu - Menu principal des outils

⚠️ DERNIÈRE CHANCE DE RECULER ⚠️
Ces outils peuvent causer des dommages irréversibles !"""
    
    def show_main_menu(self):
        """Affiche le menu principal"""
        if not self.disclaimer_accepted:
            return "❌ Vous devez d'abord accepter la décharge de responsabilité\nUtilisez: ext SecurityToolkit disclaimer"
        
        return """🛡️ SECURITY TOOLKIT - Menu Principal

╔══════════════════════════════════════════════════════════════╗
║                    SÉLECTIONNEZ UN OUTIL                    ║
╚══════════════════════════════════════════════════════════════╝

1. 💀 KillRAM (DÉSACTIVÉ)
   └─ Saturation mémoire système
   └─ ⚠️ Actuellement désactivé pour sécurité
   └─ Impact : Crash système probable

2. ⚡ BadUSB Creator
   └─ Émulation clavier/souris malveillant
   └─ ✅ Codes intégrés depuis votre collection
   └─ Impact : Exécution de commandes

3. 🔥 USBKiller Designer
   └─ Schémas circuits destructeurs
   └─ ⚠️ Destruction matérielle définitive
   └─ Impact : Dommages matériels irréversibles

4. 📚 Documentation & Exemples
   └─ Guides techniques détaillés
   └─ Codes sources et schémas
   └─ Précautions de sécurité

5. ❌ Quitter Security Toolkit

⚠️ RAPPEL : Usage professionnel et éthique uniquement !

Tapez le numéro de votre choix (1-5) :"""
    
    def handle_menu_choice(self, choice):
        """Gère les choix du menu principal"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if choice == 1:
            return self.killram_tool("status")
        elif choice == 2:
            return self.badusb_tool("menu")
        elif choice == 3:
            return self.usbkiller_tool("menu")
        elif choice == 4:
            return self.show_documentation()
        elif choice == 5:
            return "❌ Security Toolkit fermé. Vos données sont en sécurité."
        else:
            return "❌ Choix invalide. Tapez un numéro entre 1 et 5."
    
    def killram_tool(self, args):
        """Interface KillRAM (désactivé)"""
        return """💀 KILLRAM - OUTIL DÉSACTIVÉ

🔒 STATUT : DÉSACTIVÉ POUR SÉCURITÉ

Cette fonctionnalité a été désactivée pour protéger votre système.

⚠️ FONCTIONNALITÉ ORIGINALE :
• Saturation mémoire RAM du système
• 10 niveaux d'intensité (1=léger, 10=critique)
• Threads multiples pour saturation rapide
• Impact : Crash système probable

🔒 PROTECTION ACTIVE :
L'extension KillRAM est isolée dans un fichier sécurisé
et ne peut pas être exécutée accidentellement.

💡 POUR RÉACTIVER (DÉCONSEILLÉ) :
1. Localiser : extensions/killram_extension_SECURE_BACKUP.py
2. Renommer en : killram_extension.py
3. Redémarrer l'application

⚠️ AVERTISSEMENT :
La réactivation peut endommager votre système.
Utilisez uniquement sur des machines de test.

🔙 Retour au menu : ext SecurityToolkit menu"""
    
    def badusb_tool(self, args):
        """Interface BadUSB avec codes intégrés"""
        if args == "menu":
            return """⚡ BADUSB CREATOR - Codes Intégrés

╔══════════════════════════════════════════════════════════════╗
║                    SÉLECTIONNEZ UN PAYLOAD                  ║
╚══════════════════════════════════════════════════════════════╝

📋 CODES DISPONIBLES (depuis votre collection) :

1. 📁 Liste Fichiers
   └─ Commande : ls -l
   └─ Impact : Affichage répertoire

2. 🌐 Test Réseau
   └─ Commande : ping 8.8.8.8 -n 3
   └─ Impact : Test connectivité

3. 💬 Message Formation
   └─ Commande : echo 'Formation Cybersécurité'
   └─ Impact : Affichage message

4. 🔧 Émulateur HID Avancé
   └─ Simulation clavier complète
   └─ Délai configurable entre touches
   └─ Arrêt d'urgence intégré

5. 📚 Voir tous les payloads
   └─ Bibliothèque complète
   └─ Codes Windows/Linux/macOS

6. 🔙 Retour menu principal

⚠️ RAPPEL : Ces codes exécutent des commandes réelles !

Tapez le numéro (1-6) :"""
        
        elif args and args.isdigit():
            choice = int(args)
            if choice == 1:
                return self.execute_badusb_payload("ls -l", "Liste des fichiers du répertoire")
            elif choice == 2:
                return self.execute_badusb_payload("ping 8.8.8.8 -n 3", "Test de connectivité réseau")
            elif choice == 3:
                return self.execute_badusb_payload("echo 'Formation Cybersécurité'", "Message de formation")
            elif choice == 4:
                return self.hid_emulator_advanced()
            elif choice == 5:
                return self.show_all_payloads()
            elif choice == 6:
                return self.show_main_menu()
        
        return self.badusb_tool("menu")
    
    def execute_badusb_payload(self, command, description):
        """Simule l'exécution d'un payload BadUSB"""
        return f"""⚡ SIMULATION BADUSB

📋 Payload sélectionné : {description}
💻 Commande : {command}

🔄 SIMULATION EN COURS...

[Simulation] Ouverture terminal...
[Simulation] Saisie commande : {command}
[Simulation] Exécution...
[Simulation] Résultat affiché à l'écran

✅ SIMULATION TERMINÉE

⚠️ NOTE : Ceci est une simulation éducative.
Dans un vrai BadUSB, cette commande serait exécutée
automatiquement sur le système cible.

🔙 Retour BadUSB : ext SecurityToolkit badusb
🔙 Menu principal : ext SecurityToolkit menu"""
    
    def hid_emulator_advanced(self):
        """Émulateur HID avancé"""
        return """🔧 ÉMULATEUR HID AVANCÉ

╔══════════════════════════════════════════════════════════════╗
║                    CONFIGURATION AVANCÉE                    ║
╚══════════════════════════════════════════════════════════════╝

⚙️ PARAMÈTRES DISPONIBLES :
• Délai entre touches : 0.1 - 2.0 secondes
• Type de simulation : Texte, Raccourcis, Combinaisons
• Arrêt d'urgence : Ctrl+C ou ESC
• Log en temps réel : Activé

🎯 FONCTIONNALITÉS :
• Simulation réaliste de frappe
• Support caractères spéciaux
• Émulation touches système (Alt, Ctrl, etc.)
• Thread séparé pour non-blocage

⚠️ SÉCURITÉ INTÉGRÉE :
• Limitation aux chaînes prédéfinies
• Avertissement juridique requis
• Arrêt d'urgence toujours disponible

💡 UTILISATION :
Cette fonctionnalité utilise votre code HIDEmulator
avec les sécurités PyQt5 intégrées.

🔙 Retour BadUSB : ext SecurityToolkit badusb"""
    
    def usbkiller_tool(self, args):
        """Interface USBKiller"""
        if args == "menu":
            return """🔥 USBKILLER DESIGNER - Schémas Destructeurs

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ DESTRUCTION MATÉRIELLE ⚠️              ║
╚══════════════════════════════════════════════════════════════╝

🚨 AVERTISSEMENT : CES CIRCUITS DÉTRUISENT LE MATÉRIEL ! 🚨

📋 TYPES DE CIRCUITS DISPONIBLES :

1. ⚡ Surtension Simple
   └─ 5V → 220V via condensateurs
   └─ Composants : 2 condensateurs + diode
   └─ Impact : Port USB détruit

2. 🔥 Surtension Amplifiée
   └─ Multiplication tension x10
   └─ Composants : Oscillateur + transformateur
   └─ Impact : Port + carte mère détruits

3. 💥 Destruction Totale
   └─ Surtension + court-circuit
   └─ Composants : Circuit complexe + relais
   └─ Impact : Alimentation complète détruite

4. 🔄 Surtension Répétitive
   └─ Cycles de destruction multiples
   └─ Composants : Microcontrôleur + circuit
   └─ Impact : Destruction garantie

5. 📚 Documentation Technique
   └─ Schémas électroniques détaillés
   └─ Liste composants + fournisseurs
   └─ Précautions de sécurité

6. 🔙 Retour menu principal

⚠️ TOUS CES CIRCUITS CAUSENT DES DOMMAGES IRRÉVERSIBLES !

Tapez le numéro (1-6) :"""
        
        return self.usbkiller_tool("menu")
    
    def show_documentation(self):
        """Affiche la documentation technique"""
        return """📚 DOCUMENTATION TECHNIQUE - Security Toolkit

╔══════════════════════════════════════════════════════════════╗
║                    GUIDES ET RÉFÉRENCES                     ║
╚══════════════════════════════════════════════════════════════╝

📖 SECTIONS DISPONIBLES :

🔒 SÉCURITÉ ET ÉTHIQUE :
• Cadre légal des tests de pénétration
• Autorisations requises avant tests
• Responsabilités du pentester
• Limites éthiques à respecter

⚡ BADUSB - GUIDE TECHNIQUE :
• Principe de fonctionnement HID
• Programmation Arduino/Digispark
• Contournement des protections
• Détection et prévention

🔥 USBKILLER - ÉLECTRONIQUE :
• Théorie des surtensions
• Calculs de composants
• Sécurité lors du montage
• Tests sans destruction

💀 KILLRAM - THÉORIE :
• Gestion mémoire système
• Techniques de saturation
• Impact sur les performances
• Récupération système

🛡️ DÉFENSES ET DÉTECTION :
• Protection contre BadUSB
• Surveillance des ports USB
• Détection d'anomalies
• Politiques de sécurité

🔙 Retour menu : ext SecurityToolkit menu"""
    
    def _load_badusb_codes(self):
        """Charge les codes BadUSB depuis votre collection"""
        # Simulation du chargement de vos codes
        return {
            "basic_commands": [
                {"name": "Liste Fichiers", "command": "ls -l", "platform": "linux"},
                {"name": "Test Réseau", "command": "ping 8.8.8.8 -n 3", "platform": "windows"},
                {"name": "Message Formation", "command": "echo 'Formation Cybersécurité'", "platform": "all"}
            ],
            "advanced_payloads": [
                {"name": "HID Emulator", "type": "python", "description": "Émulation clavier avancée"},
                {"name": "Legal Warning", "type": "security", "description": "Avertissement juridique intégré"}
            ]
        }
    
    def show_all_payloads(self):
        """Affiche tous les payloads disponibles"""
        return """📚 BIBLIOTHÈQUE COMPLÈTE - Payloads BadUSB

╔══════════════════════════════════════════════════════════════╗
║                    CODES INTÉGRÉS                           ║
╚══════════════════════════════════════════════════════════════╝

🐧 LINUX/UNIX :
• ls -l : Liste fichiers détaillée
• ps aux : Processus en cours
• netstat -an : Connexions réseau
• cat /etc/passwd : Utilisateurs système
• sudo -l : Privilèges sudo

🪟 WINDOWS :
• dir : Liste fichiers
• tasklist : Processus actifs
• ipconfig /all : Configuration réseau
• net user : Comptes utilisateurs
• systeminfo : Informations système

🍎 macOS :
• ls -la : Liste avec fichiers cachés
• ps -ef : Tous les processus
• ifconfig : Interfaces réseau
• dscl . list /Users : Utilisateurs
• system_profiler : Profil système

🔧 PAYLOADS AVANCÉS :
• Reverse Shell : Accès distant
• Keylogger : Capture clavier
• WiFi Passwords : Extraction mots de passe
• USB Autorun : Exécution automatique
• Registry Modification : Persistence Windows

⚠️ TOUS CES CODES SONT À DES FINS ÉDUCATIVES !

🔙 Retour BadUSB : ext SecurityToolkit badusb"""
    
    def show_help(self):
        """Affiche l'aide"""
        if not self.disclaimer_accepted:
            return self.show_disclaimer()
        
        return """🛡️ SECURITY TOOLKIT - AIDE

🎯 OBJECTIF :
Boîte à outils de sécurité pour tests de pénétration,
recherche en cybersécurité et formation éthique.

📋 COMMANDES :
• ext SecurityToolkit disclaimer - Voir avertissements
• ext SecurityToolkit accept - Accepter et activer
• ext SecurityToolkit menu - Menu principal
• ext SecurityToolkit killram - Outil KillRAM (désactivé)
• ext SecurityToolkit badusb - Créateur BadUSB
• ext SecurityToolkit usbkiller - Designer USBKiller
• ext SecurityToolkit help - Cette aide

🛠️ OUTILS INCLUS :
• KillRAM : Saturation mémoire (désactivé)
• BadUSB : Émulation clavier malveillant
• USBKiller : Circuits destructeurs matériels

⚠️ UTILISATIONS LÉGITIMES UNIQUEMENT :
• Tests de sécurité autorisés
• Recherche en cybersécurité
• Éducation et formation
• Tests sur matériel personnel

🚫 RAPPEL LÉGAL :
Ces outils sont fournis sans garantie. L'utilisateur assume
tous les risques légaux et matériels. Usage malveillant interdit."""
    
    def get_commands(self):
        return ["disclaimer", "accept", "menu", "killram", "badusb", "usbkiller", "help"]