#!/usr/bin/env python3
"""
Script de déploiement complet CMD-AI Ultra Reboot v2.1.0
Inclut contournement sécurité et liaisons extensions
"""

import os
import shutil
import zipfile
from pathlib import Path
from core.security_bypass import SecurityBypass
from core.extension_bridge import ExtensionBridge, IntegrationExamples

class DeploymentManager:
    def __init__(self):
        self.version = "2.1.0"
        self.app_name = "CMD-AI_Ultra_Reboot"
        self.deploy_dir = Path(f"deployment/{self.app_name}_v{self.version}")
        
    def create_deployment_package(self):
        """Crée le package de déploiement complet"""
        print(f"📦 Création du package de déploiement v{self.version}...")
        
        # Nettoyer et créer le dossier de déploiement
        if self.deploy_dir.exists():
            shutil.rmtree(self.deploy_dir)
        self.deploy_dir.mkdir(parents=True)
        
        # 1. Copier l'application principale
        self.copy_application_files()
        
        # 2. Générer les outils de sécurité
        self.generate_security_tools()
        
        # 3. Configurer les liaisons extensions
        self.setup_extension_bridges()
        
        # 4. Créer la documentation
        self.create_deployment_docs()
        
        # 5. Créer les archives
        self.create_archives()
        
        print(f"✅ Package de déploiement créé dans: {self.deploy_dir}")
        
    def copy_application_files(self):
        """Copie les fichiers de l'application"""
        print("📁 Copie des fichiers application...")
        
        # Fichiers et dossiers essentiels
        essential_items = [
            "main.py",
            "core/",
            "extensions/",
            "language_models/",
            "ui/",
            "ressources/",
            "requirements.txt",
            "README.md",
            "CHANGELOG.md",
            "LICENSE"
        ]
        
        for item in essential_items:
            src = Path(item)
            if src.exists():
                dst = self.deploy_dir / item
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
        
        # Créer les dossiers utilisateur
        (self.deploy_dir / "user").mkdir(exist_ok=True)
        (self.deploy_dir / "logs").mkdir(exist_ok=True)
        
        # Copier les configurations par défaut
        if Path("user").exists():
            for config_file in Path("user").glob("*.json"):
                if not config_file.name.startswith("chat_history"):
                    shutil.copy2(config_file, self.deploy_dir / "user" / config_file.name)
    
    def generate_security_tools(self):
        """Génère les outils de contournement sécurité"""
        print("🛡️ Génération des outils de sécurité...")
        
        # Créer le dossier security
        security_dir = self.deploy_dir / "security"
        security_dir.mkdir(exist_ok=True)
        
        # Générer les outils avec SecurityBypass
        bypass = SecurityBypass()
        
        # Script PowerShell pour Windows Defender
        ps_script = bypass.create_defender_exclusion_script()
        shutil.move(ps_script, security_dir / ps_script.name)
        
        # Page de téléchargement sécurisé
        html_page = bypass.create_browser_bypass_page()
        shutil.move(html_page, security_dir / html_page.name)
        
        # Rapport de sécurité
        report = bypass.generate_security_report()
        shutil.move(report, security_dir / report.name)
        
        # Créer un script d'installation automatique
        install_script = self.create_auto_installer()
        with open(security_dir / "auto_install.bat", "w") as f:
            f.write(install_script)
    
    def create_auto_installer(self):
        """Crée un script d'installation automatique"""
        return f'''@echo off
echo 🚀 Installation automatique {self.app_name} v{self.version}
echo.

REM Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Privilèges administrateur détectés
    echo 🛡️ Configuration Windows Defender...
    powershell -ExecutionPolicy Bypass -File "defender_exclusion.ps1"
) else (
    echo ⚠️ Privilèges administrateur requis pour Windows Defender
    echo Relancez en tant qu'administrateur pour une installation complète
)

echo.
echo 📦 Installation des dépendances Python...
pip install -r requirements.txt

echo.
echo 🎉 Installation terminée !
echo Lancez l'application avec: python main.py
echo.
pause
'''
    
    def setup_extension_bridges(self):
        """Configure les liaisons entre extensions"""
        print("🔗 Configuration des liaisons extensions...")
        
        # Créer le pont d'extensions
        bridge = ExtensionBridge()
        examples = IntegrationExamples(bridge)
        
        # Créer les workflows
        examples.setup_security_workflow()
        examples.setup_file_analysis_workflow()
        
        # Copier les configurations dans le déploiement
        bridge_dir = self.deploy_dir / "integrations"
        bridge_dir.mkdir(exist_ok=True)
        
        # Copier les fichiers de configuration
        config_files = [
            "user/extension_integrations.json",
            "user/smart_workflows.json"
        ]
        
        for config_file in config_files:
            if Path(config_file).exists():
                shutil.copy2(config_file, bridge_dir / Path(config_file).name)
    
    def create_deployment_docs(self):
        """Crée la documentation de déploiement"""
        print("📚 Création de la documentation...")
        
        docs_dir = self.deploy_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Guide d'installation
        install_guide = f'''# 🚀 Guide d'Installation - {self.app_name} v{self.version}

## 📋 Prérequis
- Python 3.8+
- Windows 10/11, macOS, ou Linux
- Connexion Internet (pour les modèles IA)

## 🔧 Installation Rapide

### Windows
1. Téléchargez l'archive
2. Extrayez dans un dossier
3. **Exécutez `security/auto_install.bat` en tant qu'administrateur**
4. Lancez `python main.py`

### Linux/macOS
```bash
# Extraire l'archive
unzip {self.app_name}_v{self.version}.zip
cd {self.app_name}_v{self.version}

# Installer les dépendances
pip3 install -r requirements.txt

# Lancer l'application
python3 main.py
```

## 🛡️ Résolution des Problèmes de Sécurité

### Windows Defender
- Utilisez `security/defender_exclusion.ps1`
- Ou ajoutez manuellement le dossier aux exclusions

### Navigateurs
- Chrome: "Conserver" → "Conserver quand même"
- Firefox: "..." → "Conserver le fichier"
- Edge: "Conserver" → "Afficher plus" → "Conserver quand même"

### Antivirus Tiers
- Ajoutez le dossier d'installation aux exclusions
- Consultez `security/security_report.txt`

## 🔗 Nouvelles Fonctionnalités v{self.version}

### Extensions Sécurité
- **BadUSB Creator**: Création de payloads USB
- **OSINT Extension**: Recherche d'informations
- **Security Toolkit**: Outils de sécurité
- **USB Manager**: Gestion avancée USB

### Liaisons Intelligentes
- Intégration automatique entre extensions
- Workflows de sécurité prédéfinis
- Analyse collaborative IA + Sécurité

### Système de Réparation
- Détection automatique des erreurs
- Réparation en temps réel
- Notifications de maintenance

## 📞 Support
- GitHub: https://github.com/bambino-117/CMD-AI_Ultra_Reboot
- Issues: Signalez les problèmes sur GitHub
- Wiki: Documentation complète disponible
'''
        
        with open(docs_dir / "INSTALL_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(install_guide)
        
        # Guide des nouvelles fonctionnalités
        features_guide = f'''# ✨ Nouvelles Fonctionnalités v{self.version}

## 🔐 Extensions Sécurité

### BadUSB Creator
```
ext BadUSBCreator create payload_name
ext BadUSBCreator list
ext BadUSBCreator deploy usb_device
```

### OSINT Extension
```
ext OSINTExtension search "target"
ext OSINTExtension analyze ip_address
ext OSINTExtension report
```

### Security Toolkit
```
ext SecurityToolkit scan system
ext SecurityToolkit analyze file.exe
ext SecurityToolkit report
```

### USB Manager
```
ext USBManager list
ext USBManager monitor
ext USBManager secure device_id
```

## 🔗 Liaisons Intelligentes

### Workflows Automatiques
- **security_analysis**: Analyse complète du système
- **file_analysis**: Analyse de fichiers suspects
- **network_monitoring**: Surveillance réseau

### Utilisation
```
# Déclencher un workflow
workflow run security_analysis

# Lister les workflows
workflow list

# Créer un workflow personnalisé
workflow create mon_workflow
```

## 🔧 Système de Réparation

### Commandes
```
repair status          # État du système
repair history         # Historique des réparations
repair manual type     # Réparation manuelle
```

### Notifications Automatiques
- Détection d'erreurs en temps réel
- Suggestions de réparation
- Maintenance préventive
'''
        
        with open(docs_dir / "NEW_FEATURES.md", "w", encoding="utf-8") as f:
            f.write(features_guide)
    
    def create_archives(self):
        """Crée les archives de distribution"""
        print("📦 Création des archives...")
        
        # Archive ZIP principale
        zip_name = f"{self.app_name}_v{self.version}_Complete.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.deploy_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.deploy_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Archive créée: {zip_name}")
        
        # Archive sécurité uniquement
        security_zip = f"{self.app_name}_v{self.version}_Security_Tools.zip"
        with zipfile.ZipFile(security_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            security_dir = self.deploy_dir / "security"
            if security_dir.exists():
                for file in security_dir.glob("*"):
                    zipf.write(file, file.name)
        
        print(f"✅ Archive sécurité créée: {security_zip}")
        
        return zip_name, security_zip

def main():
    print(f"🚀 Déploiement CMD-AI Ultra Reboot v2.1.0")
    print("=" * 50)
    
    deployer = DeploymentManager()
    deployer.create_deployment_package()
    
    print("\n🎉 Déploiement terminé avec succès !")
    print("\n📋 Fichiers créés:")
    print("• Package complet avec outils de sécurité")
    print("• Liaisons intelligentes entre extensions")
    print("• Documentation d'installation")
    print("• Scripts de contournement antivirus")
    print("• Workflows automatisés")

if __name__ == "__main__":
    main()