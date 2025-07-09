# 🏗️ Instructions de Compilation - CMD-AI Ultra Reboot

## Vue d'ensemble

CMD-AI Ultra Reboot peut être compilé pour Linux, Windows et macOS en utilisant PyInstaller. Voici les instructions détaillées pour chaque plateforme.

## 📋 Prérequis généraux

### Dépendances Python requises
```bash
pip install pyinstaller>=5.0
pip install pillow>=8.0.0
pip install requests>=2.25.0
pip install psutil>=5.8.0
```

### Dépendances optionnelles (pour toutes les fonctionnalités)
```bash
pip install -r requirements_optional.txt
```

## 🐧 Compilation Linux

### Méthode automatique
```bash
python build_simple.py
```

### Méthode manuelle
```bash
pyinstaller --onefile --windowed \
    --name CMD-AI_Ultra_Reboot \
    --add-data "core:core" \
    --add-data "ui:ui" \
    --add-data "extensions:extensions" \
    --add-data "language_models:language_models" \
    --add-data "plugins:plugins" \
    --add-data "ressources:ressources" \
    --add-data "user:user" \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import PIL \
    --hidden-import requests \
    --clean \
    main.py
```

### Résultats Linux
- **Exécutable** : `dist/CMD-AI_Ultra_Reboot`
- **Package portable** : `CMD-AI_Ultra_Reboot_v2.0.0_Portable.tar.gz`
- **Script d'installation** : `install.sh`

### Installation Linux
```bash
# Version portable
tar -xzf CMD-AI_Ultra_Reboot_v2.0.0_Portable.tar.gz
cd CMD-AI_Ultra_Reboot_v2.0.0_Portable
./lancer.sh

# Installation système
sudo ./install.sh
cmd-ai  # Lancer depuis n'importe où
```

## 🪟 Compilation Windows

### Prérequis Windows
- Python 3.8+ installé
- PyInstaller installé
- Exécuter depuis PowerShell ou CMD

### Méthode automatique
```powershell
python build_windows.py
```

### Méthode manuelle
```powershell
pyinstaller --onefile --windowed ^
    --name CMD-AI_Ultra_Reboot ^
    --icon ressources/icons/CMD-AI_Ultra_main.ico ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --add-data "extensions;extensions" ^
    --add-data "language_models;language_models" ^
    --add-data "plugins;plugins" ^
    --add-data "ressources;ressources" ^
    --add-data "user;user" ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import PIL ^
    --hidden-import requests ^
    --clean ^
    main.py
```

### Résultats Windows
- **Exécutable** : `dist/CMD-AI_Ultra_Reboot.exe`
- **Package portable** : `CMD-AI_Ultra_Reboot_v2.0.0_Windows_Portable.zip`
- **Script d'installation** : `Install_Windows.bat`

### Installation Windows
```batch
REM Version portable
# Extraire le ZIP et double-cliquer sur Lancer_CMD-AI.bat

REM Installation système (en tant qu'administrateur)
Install_Windows.bat
```

## 🍎 Compilation macOS

### Prérequis macOS
- Python 3.8+ installé (via Homebrew recommandé)
- PyInstaller installé
- Xcode Command Line Tools

### Installation des prérequis
```bash
# Homebrew (si pas installé)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python et dépendances
brew install python
pip3 install pyinstaller pillow requests psutil
```

### Méthode automatique
```bash
python3 build_macos.py
```

### Méthode manuelle
```bash
pyinstaller --onedir --windowed \
    --name "CMD-AI Ultra Reboot" \
    --icon ressources/icons/CMD-AI_Ultra_main.ico \
    --add-data "core:core" \
    --add-data "ui:ui" \
    --add-data "extensions:extensions" \
    --add-data "language_models:language_models" \
    --add-data "plugins:plugins" \
    --add-data "ressources:ressources" \
    --add-data "user:user" \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import PIL \
    --hidden-import requests \
    --clean \
    main.py
```

### Résultats macOS
- **Application** : `dist/CMD-AI Ultra Reboot.app`
- **Package** : `CMD-AI_Ultra_Reboot_v2.0.0_macOS.tar.gz`
- **Script d'installation** : `Install_macOS.sh`

### Installation macOS
```bash
# Package complet
tar -xzf CMD-AI_Ultra_Reboot_v2.0.0_macOS.tar.gz
cd CMD-AI_Ultra_Reboot_v2.0.0_macOS
./Installer.command

# Installation manuelle
./Install_macOS.sh
```

## 🔧 Compilation multi-plateforme

### Script universel (expérimental)
```bash
python build_multiplatform.py
```

Ce script tente de compiler pour toutes les plateformes, mais il est recommandé d'utiliser les scripts spécifiques à chaque OS.

## 📦 Structure des packages

### Package portable typique
```
CMD-AI_Ultra_Reboot_v2.0.0_Portable/
├── CMD-AI_Ultra_Reboot(.exe)    # Exécutable principal
├── lancer.sh / Lancer_CMD-AI.bat # Script de lancement
├── README.md                     # Documentation
├── CHANGELOG.md                  # Historique des versions
├── LICENSE                       # Licence
├── requirements.txt              # Dépendances
├── TOUR_COMPLET_APP.md          # Guide complet
└── TESTER_TRACEBACK_GUIDE.md    # Guide testeurs
```

### Installation système
- **Linux** : `/opt/cmd-ai-ultra-reboot/` + lien `/usr/local/bin/cmd-ai`
- **Windows** : `C:\Program Files\CMD-AI Ultra Reboot\` + raccourcis
- **macOS** : `/Applications/CMD-AI Ultra Reboot.app` + lien `/usr/local/bin/cmd-ai`

## 🐛 Résolution de problèmes

### Erreurs communes

#### "Module not found"
```bash
# Ajouter le module manquant
--hidden-import nom_du_module
```

#### "Permission denied" (Linux/macOS)
```bash
chmod +x dist/CMD-AI_Ultra_Reboot
```

#### "Application can't be opened" (macOS)
```bash
# Autoriser l'application
sudo xattr -rd com.apple.quarantine "CMD-AI Ultra Reboot.app"
```

#### Taille d'exécutable importante
- Normal pour une application complète (30-50 MB)
- Contient Python + toutes les dépendances
- Version `--onedir` plus rapide mais plus volumineuse

### Optimisations

#### Réduire la taille
```bash
# Utiliser UPX (si installé)
--upx-dir /path/to/upx

# Exclure des modules
--exclude-module module_name
```

#### Améliorer les performances
```bash
# Version répertoire (plus rapide au démarrage)
--onedir

# Optimisations
--optimize 2
```

## 🧪 Tests post-compilation

### Tests de base
```bash
# Linux/macOS
./dist/CMD-AI_Ultra_Reboot

# Windows
dist\CMD-AI_Ultra_Reboot.exe
```

### Tests des fonctionnalités
1. **Interface** : Vérifier que l'interface s'ouvre
2. **Extensions** : Tester `plugin list`
3. **IA** : Configurer un modèle et tester
4. **Marketplace** : Ouvrir le marketplace
5. **Thèmes** : Changer de thème

### Tests d'intégration
1. **Plugins éditeurs** : Installer et tester
2. **Traceback** : Vérifier la capture d'erreurs
3. **Sauvegarde** : Tester les conversations
4. **Export** : Générer des rapports

## 📋 Checklist de release

### Avant compilation
- [ ] Tests unitaires passent
- [ ] Documentation à jour
- [ ] Version incrémentée
- [ ] CHANGELOG.md mis à jour
- [ ] Dépendances vérifiées

### Après compilation
- [ ] Exécutables testés sur chaque OS
- [ ] Packages portables créés
- [ ] Scripts d'installation testés
- [ ] Taille des fichiers acceptable
- [ ] Fonctionnalités principales testées

### Distribution
- [ ] Archives créées et nommées correctement
- [ ] Checksums générés (optionnel)
- [ ] Documentation d'installation claire
- [ ] Release notes rédigées

## 🚀 Automatisation (CI/CD)

### GitHub Actions (exemple)
```yaml
name: Build Multi-Platform

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install pyinstaller pillow requests psutil
    
    - name: Build application
      run: |
        python build_simple.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: CMD-AI-${{ matrix.os }}
        path: dist/
```

---

**🏗️ Compilation réussie = Application prête pour distribution !** 🎉