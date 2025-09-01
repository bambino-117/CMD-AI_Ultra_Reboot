# 🪟 Guide Installation Windows 10 - CMD-AI Ultra Reboot

## 📋 Checklist complète

### 1️⃣ Préparation USB (Linux)
```bash
# Copier le projet sur USB
cp -r /home/boris/Bureau/CMD-AI_Ultra_Reboot /media/usb/
# Ou utiliser l'archive
cp /home/boris/Bureau/CMD-AI_Ultra_Reboot_Source.tar.gz /media/usb/
```

### 2️⃣ Installation Python (Windows 10)
1. **Télécharger Python 3.11+** : https://python.org/downloads/
2. **Installation** :
   - ✅ Cocher "Add Python to PATH"
   - ✅ Cocher "Install for all users"
   - Cliquer "Install Now"
3. **Vérifier** : Ouvrir CMD → `python --version`

### 3️⃣ Installation VSCode (Windows 10)
1. **Télécharger** : https://code.visualstudio.com/
2. **Installation** :
   - ✅ Cocher "Add to PATH"
   - ✅ Cocher "Create desktop icon"
   - ✅ Cocher "Register Code as editor"

### 4️⃣ Installation Amazon Q (VSCode)
1. **Ouvrir VSCode**
2. **Extensions** (Ctrl+Shift+X)
3. **Rechercher** : "Amazon Q"
4. **Installer** : Amazon Q Developer
5. **Se connecter** avec compte AWS (optionnel)

### 5️⃣ Préparation Projet
```cmd
# Copier depuis USB vers C:\
xcopy E:\CMD-AI_Ultra_Reboot C:\CMD-AI_Ultra_Reboot /E /I

# Ou extraire archive
# Utiliser 7-Zip ou WinRAR pour extraire .tar.gz

# Ouvrir dans VSCode
cd C:\CMD-AI_Ultra_Reboot
code .
```

### 6️⃣ Installation Dépendances
```cmd
# Dans le terminal VSCode (Ctrl+`)
pip install -r requirements.txt
pip install pyinstaller

# Vérifier installations
python -c "import tkinter, PIL, requests, psutil, pygments; print('✅ Dépendances OK')"
```

### 7️⃣ Test Application
```cmd
# Tester l'app
python main.py

# Si erreur tkinter sur Windows 10
pip install tk
```

### 8️⃣ Compilation .exe
```cmd
# Méthode 1 - Script automatique
python build_executable.py

# Méthode 2 - Manuel
pyinstaller --onefile --windowed --name CMD-AI_Ultra_Reboot --icon ressources/icons/CMD-AI_Ultra_main.ico --add-data "ressources;ressources" --add-data "extensions;extensions" main.py
```

### 9️⃣ Vérification
```cmd
# Tester l'exécutable
dist\CMD-AI_Ultra_Reboot.exe

# Vérifier taille (devrait être ~40-60MB)
dir dist\CMD-AI_Ultra_Reboot.exe
```

## 🔧 Dépannage Windows 10

### Erreur Python PATH
```cmd
# Ajouter manuellement au PATH
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311
```

### Erreur tkinter
```cmd
# Réinstaller Python avec tkinter
# Ou installer séparément
pip install tk
```

### Erreur PyInstaller
```cmd
# Mettre à jour
pip install --upgrade pyinstaller
pip install --upgrade setuptools
```

### Erreur permissions
```cmd
# Exécuter CMD en tant qu'administrateur
# Ou changer répertoire vers Documents
cd %USERPROFILE%\Documents
```

## 📦 Résultat Final

Après compilation réussie :
- **Exécutable** : `dist\CMD-AI_Ultra_Reboot.exe`
- **Taille** : ~40-60 MB
- **Fonctionnel** : Interface graphique + toutes fonctionnalités

## 🎯 Commandes Rapides

```cmd
# Installation complète en une fois
pip install -r requirements.txt pyinstaller
python build_executable.py
dist\CMD-AI_Ultra_Reboot.exe
```

## 📞 Support

Si problème :
1. **Vérifier Python** : `python --version`
2. **Vérifier pip** : `pip --version`
3. **Logs PyInstaller** : Regarder dans `build\CMD-AI_Ultra_Reboot\`
4. **Tester étape par étape** : `python main.py` d'abord

---
**Temps estimé** : 30-45 minutes selon connexion internet