#!/usr/bin/env python3
"""
Script de publication GitHub pour CMD-AI Ultra Reboot v2.0.0
Prépare et pousse la nouvelle version
"""

import os
import subprocess
import json
from pathlib import Path

def prepare_release():
    """Prépare les fichiers pour la release"""
    print("🚀 CMD-AI Ultra Reboot v2.0.0 - Préparation GitHub Release")
    print("=" * 60)
    
    # Vérifier Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"✅ Git détecté: {result.stdout.strip()}")
    except:
        print("❌ Git non installé")
        return False
    
    # Vérifier le repo
    if not Path('.git').exists():
        print("❌ Pas un repository Git")
        return False
    
    print("✅ Repository Git détecté")
    
    # Nettoyer les fichiers temporaires
    cleanup_temp_files()
    
    # Créer le tag de version
    create_version_tag()
    
    # Préparer les assets de release
    prepare_release_assets()
    
    return True

def cleanup_temp_files():
    """Nettoie les fichiers temporaires"""
    print("\n🧹 Nettoyage des fichiers temporaires...")
    
    temp_patterns = [
        "*.pyc", "__pycache__", "*.pyo", "*.pyd",
        "build/", "*.egg-info/", ".pytest_cache/",
        "*.spec", ".DS_Store", "Thumbs.db"
    ]
    
    for pattern in temp_patterns:
        try:
            if pattern.endswith('/'):
                # Dossiers
                for path in Path('.').rglob(pattern[:-1]):
                    if path.is_dir():
                        import shutil
                        shutil.rmtree(path)
                        print(f"  🗑️ Supprimé: {path}")
            else:
                # Fichiers
                for path in Path('.').rglob(pattern):
                    if path.is_file():
                        path.unlink()
                        print(f"  🗑️ Supprimé: {path}")
        except:
            pass
    
    print("✅ Nettoyage terminé")

def create_version_tag():
    """Crée le tag de version"""
    print("\n🏷️ Création du tag de version...")
    
    version = "v2.0.0"
    
    try:
        # Vérifier si le tag existe déjà
        result = subprocess.run(['git', 'tag', '-l', version], capture_output=True, text=True)
        if result.stdout.strip():
            print(f"⚠️ Tag {version} existe déjà")
            # Supprimer l'ancien tag
            subprocess.run(['git', 'tag', '-d', version], capture_output=True)
            print(f"🗑️ Ancien tag {version} supprimé")
        
        # Créer le nouveau tag
        tag_message = f"CMD-AI Ultra Reboot {version} - Release complète avec 12 extensions, plugins éditeurs d'images, et compilation multi-plateforme"
        
        subprocess.run(['git', 'tag', '-a', version, '-m', tag_message], check=True)
        print(f"✅ Tag {version} créé")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur création tag: {e}")
        return False

def prepare_release_assets():
    """Prépare les assets de release"""
    print("\n📦 Préparation des assets de release...")
    
    # Vérifier les fichiers de release
    release_files = [
        "dist/CMD-AI_Ultra_Reboot",
        "CMD-AI_Ultra_Reboot_v2.0.0_Portable.tar.gz",
        "install.sh",
        "cmdai_traceback_tester.sh",
        "TOUR_COMPLET_APP.md",
        "BUILD_INSTRUCTIONS.md"
    ]
    
    available_files = []
    for file in release_files:
        if Path(file).exists():
            size = Path(file).stat().st_size / (1024 * 1024)
            print(f"  ✅ {file} ({size:.1f} MB)")
            available_files.append(file)
        else:
            print(f"  ⚠️ {file} (manquant)")
    
    print(f"\n📊 {len(available_files)}/{len(release_files)} fichiers disponibles")
    return available_files

def create_release_notes():
    """Crée les notes de release"""
    print("\n📝 Génération des notes de release...")
    
    release_notes = """# 🚀 CMD-AI Ultra Reboot v2.0.0 - Release Majeure

## 🎉 Nouveautés principales

### 🤖 **12 Extensions complètes**
- **AIchat** - Chat IA principal avec 6 modèles supportés
- **FileManager** - Gestion fichiers avancée avec organisation automatique
- **NetworkTools** - Outils réseau complets (ping, scan, vitesse, IP)
- **SystemMonitor** - Monitoring système temps réel
- **TextTools** - Traitement de texte avec regex, hash, encodage
- **Weather** - Météo et prévisions avec géolocalisation
- **USBManager** - Toolkit USB complet avec éjection sécurisée
- **SecurityToolkit** - Conteneur d'outils sécurité (KillRAM/BadUSB/USBKiller)
- **OSINT** - Recherche renseignement sources ouvertes
- **Screenshot** - Capture d'écran intégrée
- **Script moi ça, Chien!** - Générateur d'interfaces automatique
- **DataAnalyzer** - Analyseur de données avec IA

### 🎨 **Plugins éditeurs d'images**
- **GIMP Plugin** - Fenêtre flottante Python-Fu
- **Krita Plugin** - Docker PyQt5 intégré
- **Photoshop Plugin** - Extension CEP moderne
- **Génération automatique** - Code Tkinter/PyQt5/HTML depuis images

### 🔧 **Améliorations techniques**
- **Système de traceback** automatique pour testeurs
- **Interface moderne** avec 4 thèmes personnalisables
- **Marketplace style Empire** avec tuiles cliquables
- **Mode hors-ligne** intelligent avec cache
- **Intégration système** complète (notifications, raccourcis)

### 📦 **Compilation multi-plateforme**
- **Linux** - Exécutable + package portable + installateur
- **Windows** - .exe + ZIP portable + installateur .bat
- **macOS** - .app + DMG + installateur .sh

## 📥 Téléchargements

### Linux
- **Exécutable** : `CMD-AI_Ultra_Reboot` (36.8 MB)
- **Portable** : `CMD-AI_Ultra_Reboot_v2.0.0_Portable.tar.gz`
- **Installation** : `sudo ./install.sh`

### Windows
- Compilez avec : `python build_windows.py`
- Génère : .exe + package portable + installateur

### macOS  
- Compilez avec : `python3 build_macos.py`
- Génère : .app + DMG + installateur

## 🚀 Installation rapide

```bash
# Linux - Version portable
tar -xzf CMD-AI_Ultra_Reboot_v2.0.0_Portable.tar.gz
cd CMD-AI_Ultra_Reboot_v2.0.0_Portable
./lancer.sh

# Linux - Installation système
sudo ./install.sh
cmd-ai
```

## 🧪 Pour les testeurs

```bash
# Activer le système de traceback
source ./cmdai_traceback_tester.sh

# Tester avec capture automatique
cmdai "ext Weather current Paris"

# Signaler un problème
report_cmdai_issue "Description du problème"
```

## 📚 Documentation

- **Guide complet** : `TOUR_COMPLET_APP.md`
- **Compilation** : `BUILD_INSTRUCTIONS.md`
- **Testeurs** : `TESTER_TRACEBACK_GUIDE.md`
- **OSINT** : `OSINT_GUIDE.md`

## 🔒 Sécurité

- Extensions dangereuses désactivées par défaut
- Décharges de responsabilité intégrées
- Chiffrement des clés API
- Système de traceback anonymisé

## 🙏 Remerciements

Merci à tous les testeurs et contributeurs qui ont rendu cette version possible !

---

**🚀 CMD-AI Ultra Reboot v2.0.0 - L'IA modulaire et extensible !**
"""
    
    with open("RELEASE_NOTES_v2.0.0.md", 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print("✅ Notes de release créées: RELEASE_NOTES_v2.0.0.md")
    return release_notes

def git_operations():
    """Effectue les opérations Git"""
    print("\n📤 Opérations Git...")
    
    try:
        # Ajouter tous les fichiers
        print("📁 Ajout des fichiers...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        commit_message = "🚀 Release v2.0.0 - Version complète avec 12 extensions, plugins éditeurs, compilation multi-plateforme"
        print("💾 Commit...")
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push
        print("📤 Push vers GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        # Push tags
        print("🏷️ Push des tags...")
        subprocess.run(['git', 'push', 'origin', '--tags'], check=True)
        
        print("✅ Push terminé avec succès!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")
        return False

def main():
    """Point d'entrée principal"""
    if not prepare_release():
        print("❌ Échec de la préparation")
        return
    
    # Créer les notes de release
    create_release_notes()
    
    # Demander confirmation
    print("\n" + "="*60)
    print("🎯 PRÊT POUR LA PUBLICATION")
    print("="*60)
    print("✅ Fichiers nettoyés")
    print("✅ Tag v2.0.0 créé")
    print("✅ Assets préparés")
    print("✅ Notes de release générées")
    print("\n📤 Prêt à pousser vers GitHub...")
    
    response = input("\n🚀 Publier maintenant ? (o/N): ").lower().strip()
    
    if response in ['o', 'oui', 'y', 'yes']:
        if git_operations():
            print("\n🎉 PUBLICATION RÉUSSIE!")
            print("\n📋 PROCHAINES ÉTAPES:")
            print("1. Aller sur GitHub.com")
            print("2. Créer une nouvelle Release depuis le tag v2.0.0")
            print("3. Uploader les assets de release")
            print("4. Publier les notes de release")
            print("\n🔗 URL: https://github.com/bambino-117/CMD-AI_Ultra_Reboot/releases")
        else:
            print("\n❌ Échec de la publication")
    else:
        print("\n⏸️ Publication annulée")
        print("Vous pouvez relancer ce script quand vous êtes prêt")

if __name__ == "__main__":
    main()