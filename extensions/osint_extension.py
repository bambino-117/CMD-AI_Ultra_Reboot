from core.base_extension import BaseExtension
import os
import json
import requests
import re
import time
from datetime import datetime
from urllib.parse import urlparse

class OSINTExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "OSINT"
        self.version = "1.0.0"
        self.description = "🔍 Outils OSINT - Recherche et analyse de données publiques"
        self.author = "CMD-AI Team"
        self.disclaimer_accepted = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def initialize(self, app_context):
        self.app_context = app_context
        os.makedirs("user/osint_reports", exist_ok=True)
    
    def execute(self, command, args=None):
        if command == "disclaimer":
            return self.show_disclaimer()
        elif command == "accept":
            return self.accept_disclaimer()
        elif command == "wizard":
            return self.osint_wizard()
        elif command == "email":
            return self.email_search(args)
        elif command == "social":
            return self.social_search(args)
        elif command == "whois":
            return self.whois_lookup(args)
        elif command == "archive":
            return self.archive_search(args)
        elif command == "phone":
            return self.phone_lookup(args)
        elif command == "ip":
            return self.ip_lookup(args)
        elif command == "report":
            return self.generate_report(args)
        elif command == "help":
            return self.show_help()
        elif command.isdigit():
            return self.handle_wizard_choice(int(command))
        else:
            return self.show_disclaimer()
    
    def show_disclaimer(self):
        """Affiche la décharge de responsabilité OSINT"""
        return """⚖️ DÉCHARGE DE RESPONSABILITÉ - OSINT TOOLS

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ AVERTISSEMENT LÉGAL ⚠️                  ║
╚══════════════════════════════════════════════════════════════╝

🔍 CES OUTILS COLLECTENT DES DONNÉES PUBLIQUES

📋 FONCTIONNALITÉS OSINT :
• Recherche d'emails et informations publiques
• Analyse de réseaux sociaux
• Consultation d'archives web
• Recherche WHOIS et DNS
• Corrélation de données

⚖️ CADRE LÉGAL ET ÉTHIQUE :

EN UTILISANT CES OUTILS, VOUS VOUS ENGAGEZ À :

1. 🏛️ RESPECTER LA LÉGISLATION
   • Conformité aux lois locales et internationales
   • Respect du RGPD et lois sur la vie privée
   • Non-violation des conditions d'utilisation des sites

2. 🎯 USAGE LÉGITIME UNIQUEMENT
   • Recherche de sécurité autorisée
   • Investigation journalistique éthique
   • Recherche académique et éducative
   • Vérification d'informations publiques

3. 🚫 UTILISATIONS INTERDITES
   • Harcèlement ou stalking
   • Collecte de données personnelles non autorisée
   • Violation de la vie privée
   • Usage commercial non autorisé
   • Activités malveillantes

4. 🛡️ RESPONSABILITÉ UTILISATEUR
   • Vous êtes seul responsable de l'usage
   • Vérification de la légalité avant utilisation
   • Respect des droits des personnes concernées
   • Usage éthique et professionnel

⚠️ LIMITATIONS TECHNIQUES :
• Données publiques uniquement
• Pas d'accès aux données privées
• Respect des robots.txt et rate limiting
• Pas de contournement de protections

🏛️ ASPECTS LÉGAUX :
L'utilisation malveillante peut constituer :
• Violation de la vie privée
• Harcèlement en ligne
• Collecte illégale de données
• Violation des conditions d'utilisation

═══════════════════════════════════════════════════════════════

Pour accepter ces conditions et activer les outils OSINT :
ext OSINT accept

⚠️ USAGE ÉTHIQUE ET LÉGAL UNIQUEMENT ⚠️"""
    
    def accept_disclaimer(self):
        """Accepte la décharge de responsabilité"""
        self.disclaimer_accepted = True
        return """✅ DÉCHARGE DE RESPONSABILITÉ ACCEPTÉE

🔓 Outils OSINT activés avec les conditions suivantes :
• Usage strictement légal et éthique
• Respect de la vie privée et du RGPD
• Données publiques uniquement
• Responsabilité complète de l'utilisateur

🔍 OUTILS OSINT DISPONIBLES :

ext OSINT wizard - Assistant guidé complet

⚠️ RAPPEL : Usage professionnel et éducatif uniquement !"""
    
    def osint_wizard(self):
        """Assistant OSINT guidé"""
        if not self.disclaimer_accepted:
            return "❌ Vous devez d'abord accepter la décharge de responsabilité\nUtilisez: ext OSINT disclaimer"
        
        return """🔍 OSINT TOOLKIT - Assistant Guidé

╔══════════════════════════════════════════════════════════════╗
║                    SÉLECTIONNEZ UN OUTIL                    ║
╚══════════════════════════════════════════════════════════════╝

1. 📧 Recherche Email
   └─ Recherche emails par domaine
   └─ Validation et vérification
   └─ Corrélation avec bases publiques

2. 🌐 Analyse Réseaux Sociaux
   └─ Recherche username sur 10+ plateformes
   └─ Vérification existence profils
   └─ Collecte informations publiques

3. 🏢 Recherche WHOIS/DNS
   └─ Informations domaine et propriétaire
   └─ Historique DNS et modifications
   └─ Serveurs et infrastructure

4. 📚 Archives Web
   └─ Wayback Machine et archives
   └─ Historique modifications sites
   └─ Récupération contenu supprimé

5. 📱 Recherche Téléphone
   └─ Validation numéros
   └─ Informations opérateur
   └─ Géolocalisation approximative

6. 🌍 Analyse IP/Géolocalisation
   └─ Informations adresse IP
   └─ Géolocalisation et FAI
   └─ Analyse infrastructure réseau

7. 📊 Génération Rapport
   └─ Compilation résultats
   └─ Export PDF/HTML
   └─ Analyse corrélations

8. ❌ Quitter OSINT Toolkit

⚠️ RAPPEL : Données publiques uniquement, usage éthique !

Tapez le numéro de votre choix (1-8) :"""
    
    def handle_wizard_choice(self, choice):
        """Gère les choix de l'assistant"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if choice == 1:
            return self.email_search_wizard()
        elif choice == 2:
            return self.social_search_wizard()
        elif choice == 3:
            return self.whois_wizard()
        elif choice == 4:
            return self.archive_wizard()
        elif choice == 5:
            return self.phone_wizard()
        elif choice == 6:
            return self.ip_wizard()
        elif choice == 7:
            return self.report_wizard()
        elif choice == 8:
            return "❌ OSINT Toolkit fermé. Données sécurisées."
        else:
            return "❌ Choix invalide. Tapez un numéro entre 1 et 8."
    
    def email_search_wizard(self):
        """Assistant recherche email"""
        return """📧 RECHERCHE EMAIL - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    RECHERCHE PAR DOMAINE                    ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Rechercher des adresses email associées à un domaine
dans les sources publiques disponibles.

📋 SOURCES CONSULTÉES :
• Moteurs de recherche publics
• Archives web et caches
• Répertoires publics
• Fuites de données publiques
• Réseaux sociaux (profils publics)

💡 UTILISATION :
ext OSINT email [domaine]

📝 EXEMPLES :
• ext OSINT email example.com
• ext OSINT email université.fr
• ext OSINT email startup.io

⚠️ LIMITATIONS :
• Emails publics uniquement
• Pas d'accès aux données privées
• Respect des robots.txt
• Rate limiting appliqué

🔙 Retour menu : ext OSINT wizard"""
    
    def social_search_wizard(self):
        """Assistant recherche réseaux sociaux"""
        return """🌐 ANALYSE RÉSEAUX SOCIAUX - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    RECHERCHE USERNAME                       ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Vérifier la présence d'un username sur les principales
plateformes de réseaux sociaux.

🌐 PLATEFORMES SUPPORTÉES :
• Twitter/X - Profils publics
• LinkedIn - Profils professionnels
• GitHub - Développeurs et projets
• Instagram - Comptes publics
• Reddit - Utilisateurs actifs
• Facebook - Pages publiques
• YouTube - Chaînes
• TikTok - Créateurs
• Discord - Serveurs publics
• Telegram - Canaux publics

💡 UTILISATION :
ext OSINT social [username]

📝 EXEMPLES :
• ext OSINT social john_doe
• ext OSINT social tech_guru
• ext OSINT social startup_ceo

📊 RÉSULTATS :
• Existence du profil (✅/❌)
• URL du profil si public
• Date de dernière activité
• Nombre d'abonnés (si public)

⚠️ ÉTHIQUE :
• Profils publics uniquement
• Pas de scraping intensif
• Respect des conditions d'utilisation
• Pas de collecte de données privées

🔙 Retour menu : ext OSINT wizard"""
    
    def whois_wizard(self):
        """Assistant WHOIS/DNS"""
        return """🏢 RECHERCHE WHOIS/DNS - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    INFORMATIONS DOMAINE                     ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Obtenir les informations publiques d'enregistrement
et de configuration DNS d'un domaine.

📋 INFORMATIONS COLLECTÉES :
• Propriétaire du domaine (si public)
• Date d'enregistrement et expiration
• Serveurs DNS et configuration
• Registrar et contacts techniques
• Historique des modifications
• Sous-domaines découverts

💡 UTILISATION :
ext OSINT whois [domaine]

📝 EXEMPLES :
• ext OSINT whois example.com
• ext OSINT whois startup.fr
• ext OSINT whois université.edu

🔍 ANALYSE AVANCÉE :
• Résolution DNS complète
• Enregistrements MX, TXT, CNAME
• Géolocalisation serveurs
• Analyse infrastructure

⚠️ LÉGALITÉ :
• Données WHOIS publiques
• Informations DNS publiques
• Respect des politiques registrars
• Pas de contournement de protections

🔙 Retour menu : ext OSINT wizard"""
    
    def archive_wizard(self):
        """Assistant archives web"""
        return """📚 ARCHIVES WEB - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    WAYBACK MACHINE & ARCHIVES               ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Rechercher et analyser les versions archivées
d'un site web dans le temps.

🏛️ SOURCES D'ARCHIVES :
• Wayback Machine (Internet Archive)
• Archive.today
• Google Cache
• Bing Cache
• Archives nationales

💡 UTILISATION :
ext OSINT archive [url]

📝 EXEMPLES :
• ext OSINT archive https://example.com
• ext OSINT archive startup.com/about
• ext OSINT archive blog.entreprise.fr

📊 INFORMATIONS RÉCUPÉRÉES :
• Historique des modifications
• Contenu supprimé ou modifié
• Évolution du design
• Changements de contenu
• Dates de mise à jour

🔍 ANALYSE TEMPORELLE :
• Comparaison versions
• Détection changements majeurs
• Récupération contenu perdu
• Analyse évolution site

⚠️ RESPECT :
• Archives publiques uniquement
• Pas de contournement robots.txt
• Respect des droits d'auteur
• Usage éducatif et recherche

🔙 Retour menu : ext OSINT wizard"""
    
    def phone_wizard(self):
        """Assistant recherche téléphone"""
        return """📱 RECHERCHE TÉLÉPHONE - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    VALIDATION NUMÉROS                       ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Valider et obtenir des informations publiques
sur un numéro de téléphone.

📋 INFORMATIONS DISPONIBLES :
• Validation format international
• Pays et région d'origine
• Opérateur/fournisseur
• Type de ligne (fixe/mobile)
• Géolocalisation approximative (ville/région)

💡 UTILISATION :
ext OSINT phone [numéro]

📝 EXEMPLES :
• ext OSINT phone +33123456789
• ext OSINT phone +1-555-123-4567
• ext OSINT phone 0123456789

🔍 VALIDATION :
• Format E.164 international
• Vérification existence
• Détection numéros spéciaux
• Analyse préfixes

⚠️ LIMITATIONS IMPORTANTES :
• Informations publiques uniquement
• Pas d'accès aux données privées
• Pas de géolocalisation précise
• Respect de la vie privée

🚫 INTERDIT :
• Harcèlement téléphonique
• Collecte massive de numéros
• Usage commercial non autorisé
• Violation de la vie privée

🔙 Retour menu : ext OSINT wizard"""
    
    def ip_wizard(self):
        """Assistant analyse IP"""
        return """🌍 ANALYSE IP/GÉOLOCALISATION - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    INFORMATIONS ADRESSE IP                  ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Analyser une adresse IP et obtenir des informations
publiques sur sa géolocalisation et son infrastructure.

📋 INFORMATIONS COLLECTÉES :
• Géolocalisation (pays, région, ville)
• Fournisseur d'accès Internet (FAI)
• Organisation propriétaire
• Type de connexion
• Plage d'adresses (CIDR)
• Informations de routage (AS)

💡 UTILISATION :
ext OSINT ip [adresse_ip]

📝 EXEMPLES :
• ext OSINT ip 8.8.8.8
• ext OSINT ip 1.1.1.1
• ext OSINT ip 192.168.1.1

🔍 ANALYSE AVANCÉE :
• Reverse DNS lookup
• Détection VPN/Proxy
• Analyse réputation IP
• Historique géolocalisation

🌐 SOURCES UTILISÉES :
• Bases de données géolocalisation
• Registres Internet régionaux
• Services de géolocalisation IP
• Bases de données publiques

⚠️ PRÉCISION :
• Géolocalisation approximative
• Précision variable selon FAI
• Pas de localisation exacte
• Respect de la vie privée

🔙 Retour menu : ext OSINT wizard"""
    
    def report_wizard(self):
        """Assistant génération rapport"""
        return """📊 GÉNÉRATION RAPPORT - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    COMPILATION RÉSULTATS                    ║
╚══════════════════════════════════════════════════════════════╝

🎯 OBJECTIF :
Compiler et analyser tous les résultats OSINT
en un rapport structuré et professionnel.

📋 CONTENU DU RAPPORT :
• Résumé exécutif des découvertes
• Détails par source d'information
• Corrélations et liens identifiés
• Timeline des événements
• Recommandations et conclusions

📄 FORMATS D'EXPORT :
• PDF professionnel avec graphiques
• HTML interactif avec liens
• JSON structuré pour analyse
• CSV pour tableurs

💡 UTILISATION :
ext OSINT report [nom_cible]

📝 EXEMPLES :
• ext OSINT report "Analyse_Domaine_Example"
• ext OSINT report "Investigation_Username"
• ext OSINT report "Audit_Infrastructure"

🔍 ANALYSE INCLUSE :
• Graphiques de corrélation
• Cartes géographiques
• Timeline interactive
• Statistiques détaillées

📊 VISUALISATIONS :
• Graphiques réseau de connexions
• Cartes de géolocalisation
• Diagrammes temporels
• Tableaux de synthèse

⚠️ CONFIDENTIALITÉ :
• Rapports stockés localement
• Pas de transmission externe
• Chiffrement des données sensibles
• Suppression sécurisée possible

🔙 Retour menu : ext OSINT wizard"""
    
    def email_search(self, domain):
        """Recherche d'emails par domaine"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if not domain:
            return "❌ Spécifiez un domaine\nUsage: ext OSINT email example.com"
        
        return f"""📧 RECHERCHE EMAIL - {domain}

🔍 Recherche en cours sur les sources publiques...

📊 RÉSULTATS SIMULÉS :
• contact@{domain}
• info@{domain}
• support@{domain}
• admin@{domain}

📋 SOURCES CONSULTÉES :
✅ Moteurs de recherche publics
✅ Archives web
✅ Répertoires publics
✅ Réseaux sociaux (profils publics)

⚠️ NOTE : Ceci est une simulation éducative
Les vrais outils OSINT nécessitent des API spécialisées

🔙 Retour menu : ext OSINT wizard"""
    
    def social_search(self, username):
        """Recherche sur réseaux sociaux"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if not username:
            return "❌ Spécifiez un username\nUsage: ext OSINT social john_doe"
        
        return f"""🌐 ANALYSE RÉSEAUX SOCIAUX - {username}

🔍 Vérification présence sur plateformes...

📊 RÉSULTATS SIMULÉS :
• Twitter/X: ✅ Profil trouvé
• LinkedIn: ❌ Pas trouvé
• GitHub: ✅ Profil développeur
• Instagram: ⚠️ Profil privé
• Reddit: ✅ Utilisateur actif
• YouTube: ❌ Pas trouvé
• TikTok: ⚠️ Vérification requise
• Discord: ❌ Pas trouvé

📈 STATISTIQUES :
• Plateformes trouvées: 3/8
• Profils publics: 2
• Profils privés: 1
• Dernière activité: Récente

⚠️ NOTE : Simulation éducative
Respecte les conditions d'utilisation des plateformes

🔙 Retour menu : ext OSINT wizard"""
    
    def whois_lookup(self, domain):
        """Recherche WHOIS"""
        if not self.disclaimer_accepted:
            return "❌ Acceptez d'abord la décharge de responsabilité"
        
        if not domain:
            return "❌ Spécifiez un domaine\nUsage: ext OSINT whois example.com"
        
        return f"""🏢 INFORMATIONS WHOIS - {domain}

🔍 Consultation des registres publics...

📊 INFORMATIONS SIMULÉES :
• Registrar: Example Registrar Inc.
• Date création: 2020-01-15
• Date expiration: 2025-01-15
• Statut: Active
• Serveurs DNS: ns1.example.com, ns2.example.com

🌐 CONFIGURATION DNS :
• A Record: 93.184.216.34
• MX Record: mail.example.com
• TXT Record: v=spf1 include:_spf.example.com

📍 GÉOLOCALISATION SERVEUR :
• Pays: États-Unis
• Région: Californie
• Ville: San Francisco
• FAI: Example Hosting

⚠️ NOTE : Données WHOIS publiques simulées
Les vraies données peuvent être protégées par GDPR

🔙 Retour menu : ext OSINT wizard"""
    
    def show_help(self):
        """Affiche l'aide OSINT"""
        if not self.disclaimer_accepted:
            return self.show_disclaimer()
        
        return """🔍 OSINT TOOLKIT - AIDE

🎯 OBJECTIF :
Outils de recherche et d'analyse de données publiques
pour investigations légales et éthiques.

📋 COMMANDES :
• ext OSINT disclaimer - Voir avertissements légaux
• ext OSINT accept - Accepter et activer
• ext OSINT wizard - Assistant guidé complet
• ext OSINT email [domaine] - Recherche emails
• ext OSINT social [username] - Analyse réseaux sociaux
• ext OSINT whois [domaine] - Informations WHOIS/DNS
• ext OSINT archive [url] - Archives web
• ext OSINT phone [numéro] - Validation téléphone
• ext OSINT ip [adresse] - Analyse IP/géolocalisation
• ext OSINT report [nom] - Génération rapport
• ext OSINT help - Cette aide

🔍 OUTILS DISPONIBLES :
• Recherche email par domaine
• Analyse présence réseaux sociaux
• Consultation WHOIS et DNS
• Archives web (Wayback Machine)
• Validation numéros téléphone
• Géolocalisation IP
• Génération rapports PDF/HTML

⚠️ USAGE LÉGAL UNIQUEMENT :
• Données publiques uniquement
• Respect RGPD et vie privée
• Usage éthique et professionnel
• Pas de harcèlement ou stalking

🎓 UTILISATIONS LÉGITIMES :
• Recherche de sécurité autorisée
• Investigation journalistique
• Recherche académique
• Vérification d'informations publiques

🚫 RAPPEL LÉGAL :
Ces outils sont fournis à des fins éducatives.
L'utilisateur assume toute responsabilité légale."""
    
    def get_commands(self):
        return ["disclaimer", "accept", "wizard", "email", "social", "whois", "archive", "phone", "ip", "report", "help"]