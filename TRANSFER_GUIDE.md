# 📁 Guide de transfert vers Windows

## 🚀 Méthode 1 - GitHub (Recommandée)

### Sur Linux (VSCode)
```bash
git push origin main
```

### Sur Windows
```bash
git clone https://github.com/bambino-117/CMD-AI_Ultra_Reboot.git
cd CMD-AI_Ultra_Reboot
pip install -r requirements.txt
pip install pyinstaller
python build_executable.py
```

## 📦 Méthode 2 - Archive ZIP

### Télécharger
- Archive créée : `CMD-AI_Ultra_Reboot_Source.tar.gz` (99MB)
- Extraire sur Windows avec 7-Zip ou WinRAR

### Compiler sur Windows
```bash
cd CMD-AI_Ultra_Reboot
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name CMD-AI_Ultra_Reboot --icon ressources/icons/CMD-AI_Ultra_main.ico --add-data "ressources;ressources" --add-data "extensions;extensions" main.py
```

## 🔗 Méthode 3 - VSCode Remote

Si tu utilises Remote-SSH :
1. **Clic droit** sur le dossier CMD-AI_Ultra_Reboot
2. **Download Folder**
3. Choisir destination sur Windows

## ☁️ Méthode 4 - Cloud

### Google Drive / OneDrive
```bash
# Copier vers dossier synchronisé
cp -r CMD-AI_Ultra_Reboot ~/GoogleDrive/
```

### WeTransfer / Dropbox
- Uploader l'archive tar.gz
- Télécharger sur Windows

## 🎯 Recommandation

**GitHub** est la meilleure option :
- ✅ Synchronisation automatique
- ✅ Historique des versions
- ✅ Pas de limite de taille
- ✅ Accessible partout

## 🔧 Compilation Windows

Une fois le code sur Windows :

```bash
# Installer Python 3.11+ depuis python.org
# Ouvrir PowerShell/CMD dans le dossier

pip install -r requirements.txt
pip install pyinstaller
python build_executable.py
```

Le .exe sera dans `dist_windows/`