#!/usr/bin/env python3
"""
Système UX intelligent avec guidage et menus contextuels
"""

import re
from typing import Dict, List, Tuple, Optional

class SmartUX:
    def __init__(self):
        self.intent_patterns = self._create_intent_patterns()
        self.guided_workflows = {}
        self.current_workflow = None
        self.workflow_step = 0
        
    def _create_intent_patterns(self) -> Dict[str, List[Tuple[str, str]]]:
        """Crée les patterns de reconnaissance d'intention"""
        return {
            "security_scan": [
                (r"(scan|analyser|vérifier).*(système|pc|ordinateur)", "system_scan"),
                (r"(scan|analyser).*(fichier|file)", "file_scan"),
                (r"(sécurité|security|malware|virus)", "security_check")
            ],
            "usb_tools": [
                (r"(créer|faire|générer).*(usb|clé)", "create_usb"),
                (r"(badusb|payload|usb.*attack)", "badusb_create"),
                (r"(gérer|manager).*(usb|périphérique)", "usb_manage")
            ],
            "network_analysis": [
                (r"(analyser|scan).*(réseau|network|ip)", "network_scan"),
                (r"(ping|test.*connexion)", "network_test"),
                (r"(vitesse|speed.*test)", "speed_test")
            ],
            "osint_research": [
                (r"(rechercher|chercher|enquête).*(info|information)", "osint_search"),
                (r"(analyser|investigate).*(ip|domain|email)", "osint_analyze"),
                (r"(osint|renseignement)", "osint_general")
            ],
            "file_management": [
                (r"(organiser|ranger).*(fichier|dossier)", "organize_files"),
                (r"(chercher|trouver).*(fichier)", "search_files"),
                (r"(nettoyer|clean)", "cleanup_files")
            ]
        }
    
    def detect_intent(self, user_input: str) -> Optional[Tuple[str, str]]:
        """Détecte l'intention de l'utilisateur"""
        user_input = user_input.lower()
        
        for category, patterns in self.intent_patterns.items():
            for pattern, action in patterns:
                if re.search(pattern, user_input):
                    return category, action
        
        return None
    
    def create_contextual_menu(self, category: str) -> str:
        """Crée un menu contextuel basé sur la catégorie"""
        menus = {
            "security_scan": """
🛡️ **ANALYSE SÉCURITÉ**

Que souhaitez-vous analyser ?
[1] 🖥️ Scanner tout le système
[2] 📁 Analyser un fichier spécifique  
[3] 🌐 Vérifier les connexions réseau
[4] 🔍 Analyse complète (système + réseau + fichiers)

Tapez le numéro de votre choix ou 'annuler'
""",
            
            "usb_tools": """
🔌 **OUTILS USB**

Que voulez-vous faire ?
[1] ⚡ Créer un payload BadUSB
[2] 📋 Gérer les périphériques USB
[3] 🔒 Sécuriser une clé USB
[4] 📊 Analyser un périphérique USB

Tapez le numéro de votre choix ou 'annuler'
""",
            
            "network_analysis": """
🌐 **ANALYSE RÉSEAU**

Choisissez votre action :
[1] 🔍 Scanner le réseau local
[2] 📡 Tester une connexion (ping)
[3] ⚡ Test de vitesse Internet
[4] 🕵️ Analyser une adresse IP

Tapez le numéro de votre choix ou 'annuler'
""",
            
            "osint_research": """
🕵️ **RECHERCHE OSINT**

Que voulez-vous investiguer ?
[1] 🌐 Rechercher des informations générales
[2] 📧 Analyser une adresse email
[3] 🌍 Analyser une adresse IP
[4] 🏢 Rechercher sur un domaine

Tapez le numéro de votre choix ou 'annuler'
""",
            
            "file_management": """
📁 **GESTION FICHIERS**

Que souhaitez-vous faire ?
[1] 🗂️ Organiser automatiquement
[2] 🔍 Rechercher des fichiers
[3] 🧹 Nettoyer les fichiers temporaires
[4] 📊 Analyser l'espace disque

Tapez le numéro de votre choix ou 'annuler'
"""
        }
        
        return menus.get(category, "Menu non disponible")
    
    def start_guided_workflow(self, category: str, choice: str) -> str:
        """Démarre un workflow guidé"""
        workflows = {
            ("security_scan", "1"): self._workflow_system_scan,
            ("security_scan", "2"): self._workflow_file_scan,
            ("security_scan", "3"): self._workflow_network_security_scan,
            ("security_scan", "4"): self._workflow_complete_scan,
            
            ("usb_tools", "1"): self._workflow_badusb_create,
            ("usb_tools", "2"): self._workflow_usb_manage,
            ("usb_tools", "3"): self._workflow_usb_secure,
            ("usb_tools", "4"): self._workflow_usb_analyze,
            
            ("network_analysis", "1"): self._workflow_network_local_scan,
            ("network_analysis", "2"): self._workflow_ping_test,
            ("network_analysis", "3"): self._workflow_speed_test,
            ("network_analysis", "4"): self._workflow_ip_analyze,
            
            ("osint_research", "1"): self._workflow_osint_general,
            ("osint_research", "2"): self._workflow_osint_email,
            ("osint_research", "3"): self._workflow_osint_ip,
            ("osint_research", "4"): self._workflow_osint_domain,
            
            ("file_management", "1"): self._workflow_organize_files,
            ("file_management", "2"): self._workflow_search_files,
            ("file_management", "3"): self._workflow_cleanup_files,
            ("file_management", "4"): self._workflow_disk_analyze
        }
        
        workflow_key = (category, choice)
        if workflow_key in workflows:
            self.current_workflow = workflow_key
            self.workflow_step = 0
            return workflows[workflow_key]()
        
        return "❌ Choix non reconnu. Tapez 'menu' pour revenir au menu."
    
    def continue_workflow(self, user_input: str) -> str:
        """Continue le workflow en cours"""
        if not self.current_workflow:
            return "Aucun workflow en cours."
        
        # Logique de continuation basée sur le workflow actuel
        # Ici on simule, dans la vraie implémentation on appellerait les extensions
        
        if self.workflow_step == 0:
            self.workflow_step = 1
            return self._execute_workflow_step(user_input)
        
        return "Workflow terminé. Tapez 'menu' pour un nouveau workflow."
    
    def _execute_workflow_step(self, user_input: str) -> str:
        """Exécute une étape du workflow"""
        category, choice = self.current_workflow
        
        if category == "security_scan" and choice == "1":
            return """
🔄 **SCAN SYSTÈME EN COURS...**

✅ Étape 1/4: Analyse des processus
✅ Étape 2/4: Vérification des fichiers système  
🔄 Étape 3/4: Scan des connexions réseau...
⏳ Étape 4/4: Génération du rapport IA

📊 **RÉSULTATS PRÉLIMINAIRES:**
• 156 processus analysés
• 3 connexions suspectes détectées
• 0 malware trouvé

Voulez-vous un rapport détaillé ? (oui/non)
"""
        
        return "Étape du workflow exécutée."
    
    # Workflows spécifiques
    def _workflow_system_scan(self) -> str:
        return """
🛡️ **SCAN SYSTÈME COMPLET**

Je vais analyser votre système en 4 étapes :
1. 🔍 Processus et services
2. 📁 Fichiers système critiques
3. 🌐 Connexions réseau actives
4. 🤖 Analyse IA des résultats

⏱️ Durée estimée : 2-3 minutes

Appuyez sur Entrée pour commencer ou tapez 'annuler'
"""
    
    def _workflow_file_scan(self) -> str:
        return """
📁 **ANALYSE DE FICHIER**

Pour analyser un fichier, j'ai besoin de :
1. 📂 Le chemin du fichier
2. 🔍 Type d'analyse (rapide/complète)

Glissez-déposez votre fichier ici ou tapez le chemin :
"""
    
    def _workflow_network_security_scan(self) -> str:
        return """
🌐 **SCAN SÉCURITÉ RÉSEAU**

Analyse des connexions réseau actives :
1. 🔍 Ports ouverts
2. 🔗 Connexions établies
3. ⚠️ Connexions suspectes
4. 🛡️ Recommandations sécurité

⏱️ Durée estimée : 1-2 minutes

Appuyez sur Entrée pour commencer ou tapez 'annuler'
"""
    
    def _workflow_complete_scan(self) -> str:
        return """
🔍 **ANALYSE COMPLÈTE**

Scan complet de sécurité en 3 phases :
1. 💻 Analyse système (processus, fichiers)
2. 🌐 Scan réseau (ports, connexions)
3. 📁 Vérification fichiers (malware, vulnérabilités)

⏱️ Durée estimée : 5-8 minutes
🤖 Analyse IA des résultats incluse

Appuyez sur Entrée pour démarrer l'analyse complète
"""
    
    def _workflow_badusb_create(self) -> str:
        return """
⚡ **CRÉATION PAYLOAD BADUSB**

⚠️ **ATTENTION**: Outil à des fins éducatives uniquement

Étapes de création :
1. 🎯 Choisir le type de payload
2. ⚙️ Configurer les paramètres
3. 🔧 Générer le code
4. 💾 Sauvegarder sur USB

Types disponibles :
[A] 📝 Récupération d'informations
[B] 🔓 Bypass sécurité
[C] 📊 Collecte de données
[D] 🎭 Payload personnalisé

Tapez la lettre de votre choix :
"""
    
    def _workflow_osint_general(self) -> str:
        return """
🕵️ **RECHERCHE OSINT**

Que souhaitez-vous rechercher ?

📝 Tapez votre requête (nom, entreprise, etc.) :
💡 Exemple : "John Doe Paris" ou "Entreprise XYZ"

🔍 Sources qui seront consultées :
• Réseaux sociaux publics
• Bases de données ouvertes  
• Moteurs de recherche spécialisés
• Archives web

⚠️ Recherche légale uniquement sur données publiques
"""
    
    def _workflow_usb_manage(self) -> str:
        """Workflow pour la gestion USB"""
        return """
💾 **GESTION USB AVANCÉE**

Gestion complète de vos périphériques USB :

Options disponibles :
[A] 📋 Lister tous les périphériques USB
[B] 🔍 Analyser un périphérique spécifique
[C] 🔒 Bloquer/Débloquer un périphérique
[D] 🧹 Nettoyer les traces USB
[E] 📊 Historique des connexions

Tapez la lettre de votre choix :
"""
    
    def _workflow_usb_secure(self) -> str:
        """Workflow pour la sécurisation USB"""
        return """
🔒 **SÉCURISATION USB**

Sécurisez vos périphériques USB :

Options disponibles :
[A] 🔐 Chiffrer un périphérique USB
[B] 🛡️ Créer une partition sécurisée
[C] 🔍 Scanner les menaces USB
[D] 📝 Configurer les règles de sécurité
[E] 🚫 Bloquer les USB non autorisés

Tapez la lettre de votre choix :
"""
    
    def _workflow_usb_analyze(self) -> str:
        """Workflow pour l'analyse USB"""
        return """
🔬 **ANALYSE USB**

Analysez vos périphériques USB :

Options disponibles :
[A] 📊 Analyse complète du périphérique
[B] 🦠 Détection de malware
[C] 📁 Analyse des fichiers
[D] 🔍 Récupération de données
[E] 📈 Rapport d'analyse

Tapez la lettre de votre choix :
"""
    
    def _workflow_network_local_scan(self) -> str:
        """Workflow pour le scan réseau local"""
        return """
🌐 **SCAN RÉSEAU LOCAL**

Analysez votre réseau local :

Options disponibles :
[A] 📡 Scan des périphériques connectés
[B] 🔍 Analyse des ports ouverts
[C] 🛡️ Détection d'intrusion
[D] 📊 Carte du réseau
[E] 🔒 Test de sécurité

Tapez la lettre de votre choix :
"""
    
    def _workflow_ping_test(self) -> str:
        """Workflow pour les tests ping"""
        return """
🏓 **TEST DE CONNECTIVITÉ**

Testez votre connectivité réseau :

Options disponibles :
[A] 🎯 Ping vers une adresse spécifique
[B] 📊 Test de latence avancé
[C] 🌍 Test de connectivité Internet
[D] 🔄 Test de stabilité
[E] 📈 Rapport de connectivité

Tapez la lettre de votre choix :
"""
    
    def _workflow_speed_test(self) -> str:
        """Workflow pour les tests de vitesse"""
        return """
⚡ **TEST DE DÉBIT**

Testez la vitesse de votre connexion :

Options disponibles :
[A] 📊 Test de débit complet
[B] 📥 Test de téléchargement
[C] 📤 Test d'upload
[D] 🔄 Test de latence
[E] 📈 Historique des tests

Tapez la lettre de votre choix :
"""
    
    def _workflow_ip_analyze(self) -> str:
        """Workflow pour l'analyse IP"""
        return """
🔍 **ANALYSE IP**

Analysez une adresse IP :

Options disponibles :
[A] 🌍 Géolocalisation IP
[B] 🏢 Informations sur l'ISP
[C] 🛡️ Réputation de l'IP
[D] 📊 Historique de l'IP
[E] 🔒 Test de sécurité

Tapez la lettre de votre choix :
"""
    
    def _workflow_osint_email(self) -> str:
        """Workflow pour l'analyse d'email"""
        return """
📧 **ANALYSE EMAIL**

Analysez une adresse email :

Options disponibles :
[A] 🔍 Vérification de l'existence
[B] 📊 Recherche dans les bases de données
[C] 🌐 Recherche sur les réseaux sociaux
[D] 📈 Historique des fuites de données
[E] 🔒 Test de sécurité

Tapez la lettre de votre choix :
"""
    
    def _workflow_osint_ip(self) -> str:
        """Workflow pour l'analyse IP OSINT"""
        return """
🌐 **ANALYSE IP OSINT**

Analysez une adresse IP :

Options disponibles :
[A] 🌍 Géolocalisation détaillée
[B] 🏢 Informations sur l'organisation
[C] 🛡️ Réputation et blacklists
[D] 📊 Historique et activité
[E] 🔒 Analyse de sécurité

Tapez la lettre de votre choix :
"""
    
    def _workflow_osint_domain(self) -> str:
        """Workflow pour l'analyse de domaine"""
        return """
🌐 **ANALYSE DOMAINE**

Analysez un nom de domaine :

Options disponibles :
[A] 🔍 Informations WHOIS
[B] 📊 Sous-domaines et DNS
[C] 🌐 Historique du domaine
[D] 🔒 Certificats SSL
[E] 📈 Réputation et sécurité

Tapez la lettre de votre choix :
"""
    
    def _workflow_organize_files(self) -> str:
        """Workflow pour organiser les fichiers"""
        return """
🗂️ **ORGANISATION FICHIERS**

Organisez automatiquement vos fichiers :

Options disponibles :
[A] 📁 Trier par type de fichier
[B] 📅 Organiser par date
[C] 📊 Trier par taille
[D] 🏷️ Organiser par tags
[E] 🤖 Organisation intelligente

Tapez la lettre de votre choix :
"""
    
    def _workflow_search_files(self) -> str:
        """Workflow pour rechercher des fichiers"""
        return """
🔍 **RECHERCHE FICHIERS**

Recherchez des fichiers sur votre système :

Options disponibles :
[A] 📝 Recherche par nom
[B] 📊 Recherche par taille
[C] 📅 Recherche par date
[D] 🔍 Recherche par contenu
[E] 🤖 Recherche intelligente

Tapez la lettre de votre choix :
"""
    
    def _workflow_cleanup_files(self) -> str:
        """Workflow pour nettoyer les fichiers"""
        return """
🧹 **NETTOYAGE FICHIERS**

Nettoyez votre système :

Options disponibles :
[A] 🗑️ Fichiers temporaires
[B] 📦 Cache des applications
[C] 🔄 Fichiers dupliqués
[D] 📊 Gros fichiers inutiles
[E] 🧹 Nettoyage complet

Tapez la lettre de votre choix :
"""
    
    def _workflow_disk_analyze(self) -> str:
        """Workflow pour analyser l'espace disque"""
        return """
📊 **ANALYSE DISQUE**

Analysez l'utilisation de votre disque :

Options disponibles :
[A] 📈 Utilisation par dossier
[B] 📊 Répartition par type
[C] 🔍 Gros fichiers
[D] 📅 Évolution dans le temps
[E] 💾 Recommandations d'optimisation

Tapez la lettre de votre choix :
"""
    
    def get_smart_suggestions(self, user_input: str) -> List[str]:
        """Génère des suggestions intelligentes"""
        suggestions = []
        
        # Suggestions basées sur l'historique et le contexte
        common_tasks = [
            "🛡️ Scanner mon système",
            "📁 Analyser un fichier",
            "🌐 Tester ma connexion",
            "🔌 Créer un payload USB",
            "🕵️ Rechercher des informations"
        ]
        
        # Filtrer selon l'input utilisateur
        for task in common_tasks:
            if any(word in user_input.lower() for word in task.lower().split()):
                suggestions.append(task)
        
        return suggestions[:3]  # Max 3 suggestions
    
    def format_response_with_actions(self, response: str, actions: List[str] = None) -> str:
        """Formate une réponse avec des actions suggérées"""
        if not actions:
            actions = ["💬 Poser une question", "🔧 Ouvrir le menu", "❓ Aide"]
        
        formatted = f"{response}\n\n"
        formatted += "**Actions rapides :**\n"
        for i, action in enumerate(actions, 1):
            formatted += f"[{i}] {action}\n"
        
        return formatted

def create_smart_dispatcher_integration():
    """Intègre SmartUX dans le dispatcher existant"""
    integration_code = '''
# Ajout dans dispatcher.py
from core.smart_ux import SmartUX

class Dispatcher:
    def __init__(self):
        # ... code existant ...
        self.smart_ux = SmartUX()
        self.awaiting_menu_choice = False
        self.current_menu_category = None
    
    def process_message(self, message):
        # Vérifier si on attend un choix de menu
        if self.awaiting_menu_choice:
            if message.lower() == 'annuler':
                self.awaiting_menu_choice = False
                self.current_menu_category = None
                return "❌ Opération annulée. Que puis-je faire pour vous ?"
            
            response = self.smart_ux.start_guided_workflow(self.current_menu_category, message)
            self.awaiting_menu_choice = False
            return response
        
        # Détecter l'intention utilisateur
        intent = self.smart_ux.detect_intent(message)
        if intent:
            category, action = intent
            menu = self.smart_ux.create_contextual_menu(category)
            self.awaiting_menu_choice = True
            self.current_menu_category = category
            return menu
        
        # Traitement normal si pas d'intention détectée
        return self._process_normal_message(message)
'''
    
    return integration_code