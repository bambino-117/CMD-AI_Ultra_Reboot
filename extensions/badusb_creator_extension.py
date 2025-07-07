from core.base_extension import BaseExtension
import os
import platform
import json
from datetime import datetime

class BadUSBCreatorExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "BadUSBCreator"
        self.version = "1.0.0"
        self.description = "⚡ Créateur BadUSB & USBKiller - Assistant guidé"
        self.author = "CMD-AI Team"
        self.os_type = platform.system()
        self.disclaimer_accepted = False
        self.current_project = {}
        self.wizard_step = 0
    
    def initialize(self, app_context):
        self.app_context = app_context
        os.makedirs("user/badusb_projects", exist_ok=True)
    
    def execute(self, command, args=None):
        if command == "disclaimer":
            return self.show_disclaimer()
        elif command == "accept":
            return self.accept_disclaimer()
        elif command == "wizard":
            return self.start_wizard()
        elif command == "badusb":
            return self.badusb_creator(args)
        elif command == "usbkiller":
            return self.usbkiller_creator(args)
        elif command == "payloads":
            return self.show_payloads()
        elif command == "generate":
            return self.generate_code(args)
        elif command == "help":
            return self.show_help()
        elif command.isdigit():
            return self.handle_wizard_choice(int(command))
        else:
            return self.show_disclaimer()
    
    def show_disclaimer(self):
        """Affiche la décharge de responsabilité"""
        return """⚠️ DÉCHARGE DE RESPONSABILITÉ - BADUSB CREATOR

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ AVERTISSEMENT CRITIQUE ⚠️                ║
╚══════════════════════════════════════════════════════════════╝

🚨 CETTE EXTENSION CRÉE DES OUTILS POTENTIELLEMENT DANGEREUX 🚨

📋 QUE FAIT BADUSB CREATOR :
• Génère du code pour périphériques BadUSB
• Crée des payloads USBKiller (destructeurs matériels)
• Produit des scripts d'attaque automatisés
• Peut causer des dommages irréversibles au matériel

⚖️ DÉCHARGE DE RESPONSABILITÉ LÉGALE :

EN UTILISANT CETTE EXTENSION, VOUS RECONNAISSEZ ET ACCEPTEZ QUE :

1. 🛡️ LE DÉVELOPPEUR (CMD-AI Team) DÉCLINE TOUTE RESPONSABILITÉ
   pour les dommages directs, indirects, matériels ou logiciels
   résultant de l'utilisation de cette extension.

2. ⚡ LES USBKILLERS PEUVENT DÉTRUIRE DÉFINITIVEMENT LE MATÉRIEL
   (cartes mères, ports USB, composants électroniques).

3. 💻 LES BADUSB PEUVENT COMPROMETTRE LA SÉCURITÉ DES SYSTÈMES
   et causer des pertes de données ou violations de confidentialité.

4. 🔧 VOUS ÊTES SEUL RESPONSABLE de l'usage de ces outils
   et assumez l'entière responsabilité des conséquences.

5. 🚫 LE DÉVELOPPEUR NE PEUT ÊTRE TENU RESPONSABLE
   de la destruction matérielle, perte de données, ou dommages.

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
L'utilisation malveillante de ces outils peut constituer :
• Destruction de biens (délit/crime)
• Intrusion dans système informatique
• Violation de la loi informatique et libertés
• Actes de cyberterrorisme

═══════════════════════════════════════════════════════════════

Pour accepter ces conditions et activer l'extension :
ext BadUSBCreator accept

⚠️ RÉFLÉCHISSEZ BIEN - CES OUTILS SONT DANGEREUX ⚠️"""
    
    def accept_disclaimer(self):
        """Accepte la décharge de responsabilité"""
        self.disclaimer_accepted = True
        return """✅ DÉCHARGE DE RESPONSABILITÉ ACCEPTÉE

🔓 Extension BadUSB Creator activée avec les conditions suivantes :
• Vous assumez tous les risques matériels et légaux
• Usage strictement limité aux fins légitimes
• Responsabilité complète des conséquences

🎯 ASSISTANT DE CRÉATION DISPONIBLE :

1. ext BadUSBCreator wizard - Assistant guidé complet
2. ext BadUSBCreator badusb - Créateur BadUSB spécialisé
3. ext BadUSBCreator usbkiller - Créateur USBKiller
4. ext BadUSBCreator payloads - Bibliothèque de payloads
5. ext BadUSBCreator generate [type] - Génération directe

💡 RECOMMANDATION : Commencez par l'assistant guidé
ext BadUSBCreator wizard

⚠️ DERNIÈRE CHANCE DE RECULER ⚠️
Ces outils peuvent causer des dommages irréversibles !"""
    
    def start_wizard(self):
        """Démarre l'assistant de création guidé"""
        if not self.disclaimer_accepted:
            return "❌ Vous devez d'abord accepter la décharge de responsabilité\nUtilisez: ext BadUSBCreator disclaimer"
        
        self.wizard_step = 1
        return """🧙‍♂️ ASSISTANT BADUSB & USBKILLER

Bienvenue dans l'assistant de création guidé !

╔══════════════════════════════════════════════════════════════╗
║                    ÉTAPE 1/5 - TYPE D'OUTIL                 ║
╚══════════════════════════════════════════════════════════════╝

Que souhaitez-vous créer ?

1. 🖱️ BadUSB - Clavier/Souris malveillant
   • Exécute des commandes automatiquement
   • Simule la frappe clavier
   • Contourne les protections antivirus
   • Impact : Logiciel (récupérable)

2. ⚡ USBKiller - Destructeur matériel
   • Surtension électrique destructive
   • Détruit ports USB et composants
   • Dommages matériels irréversibles
   • Impact : Matériel (DÉFINITIF)

3. 🔄 Combo - BadUSB + USBKiller
   • Phase 1 : Extraction de données
   • Phase 2 : Destruction matérielle
   • Impact : Total (données + matériel)

4. 📚 Voir exemples et templates
   • Bibliothèque de payloads
   • Codes pré-faits
   • Documentation technique

5. ❌ Annuler et quitter

⚠️ RAPPEL : USBKiller détruit DÉFINITIVEMENT le matériel !

Tapez le numéro de votre choix (1-5) :"""
    
    def handle_wizard_choice(self, choice):
        """Gère les choix de l'assistant"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if self.wizard_step == 1:
            return self.wizard_step_1(choice)
        elif self.wizard_step == 2:
            return self.wizard_step_2(choice)
        elif self.wizard_step == 3:
            return self.wizard_step_3(choice)
        elif self.wizard_step == 4:
            return self.wizard_step_4(choice)
        elif self.wizard_step == 5:
            return self.wizard_step_5(choice)
        else:
            return self.start_wizard()
    
    def wizard_step_1(self, choice):
        """Étape 1 : Choix du type d'outil"""
        if choice == 1:
            self.current_project["type"] = "badusb"
            self.wizard_step = 2
            return """🖱️ BADUSB SÉLECTIONNÉ

╔══════════════════════════════════════════════════════════════╗
║                  ÉTAPE 2/5 - PLATEFORME CIBLE               ║
╚══════════════════════════════════════════════════════════════╝

Sur quel système la cible s'exécutera-t-elle ?

1. 🪟 Windows (toutes versions)
   • PowerShell, CMD, Registry
   • Contournement UAC
   • Téléchargement de payloads

2. 🐧 Linux (Ubuntu, Debian, etc.)
   • Bash, terminal
   • Élévation de privilèges
   • Backdoors système

3. 🍎 macOS (Intel/Apple Silicon)
   • Terminal, AppleScript
   • Contournement Gatekeeper
   • Persistence système

4. 🌐 Multi-plateforme
   • Détection automatique OS
   • Payloads adaptatifs
   • Compatibilité maximale

Tapez le numéro (1-4) :"""
        
        elif choice == 2:
            self.current_project["type"] = "usbkiller"
            self.wizard_step = 2
            return """⚡ USBKILLER SÉLECTIONNÉ

╔══════════════════════════════════════════════════════════════╗
║                 ÉTAPE 2/5 - TYPE DE DESTRUCTION             ║
╚══════════════════════════════════════════════════════════════╝

⚠️ ATTENTION : DESTRUCTION MATÉRIELLE IRRÉVERSIBLE ⚠️

Quel type de USBKiller voulez-vous créer ?

1. ⚡ Surtension simple
   • 5V → 220V via condensateurs
   • Détruit port USB uniquement
   • Composants : 2 condensateurs + diode

2. 🔥 Surtension amplifiée
   • Multiplication de tension x10
   • Détruit port + carte mère
   • Composants : Circuit oscillateur + transformateur

3. 💥 Destruction totale
   • Surtension + court-circuit
   • Détruit alimentation complète
   • Composants : Circuit complexe + relais

4. 🔄 Surtension répétitive
   • Cycles de destruction multiples
   • Assure destruction complète
   • Composants : Microcontrôleur + circuit

⚠️ TOUS CES CIRCUITS DÉTRUISENT DÉFINITIVEMENT LE MATÉRIEL !

Tapez le numéro (1-4) :"""
        
        elif choice == 3:
            self.current_project["type"] = "combo"
            return self.combo_wizard()
        
        elif choice == 4:
            return self.show_payloads()
        
        elif choice == 5:
            return "❌ Assistant annulé. Vos données sont en sécurité."
        
        else:
            return "❌ Choix invalide. Tapez un numéro entre 1 et 5."
    
    def wizard_step_2(self, choice):
        """Étape 2 : Configuration spécifique"""
        if self.current_project["type"] == "badusb":
            platforms = ["windows", "linux", "macos", "multiplatform"]
            if 1 <= choice <= 4:
                self.current_project["platform"] = platforms[choice-1]
                self.wizard_step = 3
                return f"""✅ Plateforme : {platforms[choice-1].upper()}

╔══════════════════════════════════════════════════════════════╗
║                   ÉTAPE 3/5 - TYPE D'ATTAQUE                ║
╚══════════════════════════════════════════════════════════════╝

Quel type d'attaque BadUSB voulez-vous implémenter ?

1. 📊 Extraction de données
   • Copie fichiers sensibles
   • Historique navigateur
   • Mots de passe sauvegardés
   • Envoi par email/FTP

2. 🚪 Backdoor/Accès distant
   • Shell reverse
   • VNC/RDP caché
   • Tunnel SSH
   • Contrôle permanent

3. 💻 Exécution de payload
   • Téléchargement + exécution
   • Malware personnalisé
   • Ransomware
   • Keylogger

4. 🔧 Modification système
   • Création utilisateur admin
   • Désactivation antivirus
   • Modification registre
   • Persistence boot

5. 🎭 Social engineering
   • Faux écran de connexion
   • Vol d'identifiants
   • Phishing local
   • Capture webcam/micro

Tapez le numéro (1-5) :"""
        
        elif self.current_project["type"] == "usbkiller":
            killer_types = ["simple", "amplified", "total", "repetitive"]
            if 1 <= choice <= 4:
                self.current_project["killer_type"] = killer_types[choice-1]
                self.wizard_step = 3
                return f"""⚡ Type USBKiller : {killer_types[choice-1].upper()}

╔══════════════════════════════════════════════════════════════╗
║                 ÉTAPE 3/5 - SCHÉMA ÉLECTRONIQUE             ║
╚══════════════════════════════════════════════════════════════╝

Voulez-vous générer le schéma électronique ?

1. 📋 Schéma complet avec composants
   • Liste des composants nécessaires
   • Schéma de câblage détaillé
   • Instructions de soudure
   • Précautions de sécurité

2. 🛠️ Instructions de montage uniquement
   • Étapes de construction
   • Outils nécessaires
   • Tests de fonctionnement
   • Dépannage

3. ⚠️ Avertissements de sécurité
   • Risques électriques
   • Protection personnelle
   • Précautions de manipulation
   • Premiers secours

4. 📦 Package complet
   • Schéma + Instructions + Sécurité
   • Fichiers exportables
   • Documentation PDF

Tapez le numéro (1-4) :"""
        
        return "❌ Choix invalide"
    
    def show_payloads(self):
        """Affiche la bibliothèque de payloads"""
        return """📚 BIBLIOTHÈQUE DE PAYLOADS

╔══════════════════════════════════════════════════════════════╗
║                      BADUSB PAYLOADS                        ║
╚══════════════════════════════════════════════════════════════╝

🪟 WINDOWS :
• Reverse Shell PowerShell
• UAC Bypass + Admin
• WiFi Password Extractor
• Browser Password Dump
• Disable Windows Defender
• Create Hidden Admin User
• Registry Persistence
• Download & Execute

🐧 LINUX :
• Bash Reverse Shell
• SSH Key Injection
• Sudo Password Bypass
• Crontab Persistence
• Network Scanner
• Log Cleaner
• Backdoor Service

🍎 macOS :
• AppleScript Payload
• Keychain Dump
• Gatekeeper Bypass
• LaunchAgent Persistence
• Terminal Command Injection

╔══════════════════════════════════════════════════════════════╗
║                    USBKILLER CIRCUITS                       ║
╚══════════════════════════════════════════════════════════════╝

⚡ CIRCUITS DISPONIBLES :
• Simple Capacitor Killer (5V→220V)
• Voltage Multiplier Circuit
• Oscillator-Based Killer
• Repetitive Pulse Generator
• Multi-Stage Amplifier

🔧 COMPOSANTS TYPES :
• Condensateurs haute tension
• Diodes de redressement
• Transformateurs élévateurs
• Circuits intégrés 555
• Relais de commutation

⚠️ TOUS CES CIRCUITS SONT DESTRUCTEURS !

Pour générer un payload spécifique :
ext BadUSBCreator generate [nom_payload]"""
    
    def show_help(self):
        """Affiche l'aide"""
        if not self.disclaimer_accepted:
            return self.show_disclaimer()
        
        return """⚡ BADUSB CREATOR - AIDE

🎯 OBJECTIF :
Créer des outils BadUSB et USBKiller pour tests de sécurité
et recherche en cybersécurité.

📋 COMMANDES :
• ext BadUSBCreator disclaimer - Voir avertissements
• ext BadUSBCreator accept - Accepter et activer
• ext BadUSBCreator wizard - Assistant guidé complet
• ext BadUSBCreator badusb [type] - Créateur BadUSB
• ext BadUSBCreator usbkiller [type] - Créateur USBKiller
• ext BadUSBCreator payloads - Bibliothèque de codes
• ext BadUSBCreator generate [payload] - Génération directe
• ext BadUSBCreator help - Cette aide

🛠️ TYPES BADUSB :
• Keyboard/Mouse simulation
• Command execution
• Data exfiltration
• System backdoors
• Social engineering

⚡ TYPES USBKILLER :
• Simple voltage surge
• Amplified destruction
• Total system kill
• Repetitive pulses

⚠️ UTILISATIONS LÉGITIMES UNIQUEMENT :
• Tests de sécurité autorisés
• Recherche en cybersécurité
• Éducation et formation
• Tests sur matériel personnel

🚫 RAPPEL LÉGAL :
Cet outil est fourni sans garantie. L'utilisateur assume
tous les risques légaux et matériels. Usage malveillant interdit."""
    
    def get_commands(self):
        return ["disclaimer", "accept", "wizard", "badusb", "usbkiller", "payloads", "generate", "help"]