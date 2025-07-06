# Compatibilité CMD-AI Ultra Reboot

## Systèmes Supportés ✅

### Windows 10/11
- **Python**: 3.8+ (depuis python.org)
- **Lancement**: `launch.bat` ou `python main.py`
- **Icône**: .ico natif
- **Élévation**: UAC automatique

### macOS 10.15+
- **Python**: 3.8+ (Homebrew recommandé)
- **Lancement**: `launch.command` ou `python3 main.py`
- **Icône**: PNG via iconphoto
- **Élévation**: osascript

### Linux (Ubuntu/Debian/Kali)
- **Python**: 3.8+ avec python3-tk
- **Lancement**: `launch.sh` ou `python3 main.py`
- **Icône**: PNG via iconphoto
- **Élévation**: sudo

## Dépendances Requises

```bash
pip install -r requirements.txt
```

- **tkinter**: Interface graphique (built-in)
- **Pillow**: Gestion images
- **requests**: Requêtes HTTP

## Installation par Plateforme

### Windows
```cmd
git clone [repo]
cd CMD-AI_Ultra_Reboot
pip install -r requirements.txt
launch.bat
```

### macOS
```bash
git clone [repo]
cd CMD-AI_Ultra_Reboot
pip3 install -r requirements.txt
chmod +x launch.command
./launch.command
```

### Linux
```bash
git clone [repo]
cd CMD-AI_Ultra_Reboot
pip3 install -r requirements.txt
chmod +x launch.sh
./launch.sh
```

## Vérification

```bash
python check_compatibility.py
python fix_compatibility.py
```

## Problèmes Courants

### Tkinter manquant (Linux)
```bash
sudo apt install python3-tk
```

### Pillow manquant
```bash
pip install Pillow
```

### Permissions (macOS/Linux)
```bash
chmod +x launch.*
```

## Fonctionnalités par Plateforme

| Fonctionnalité | Windows | macOS | Linux |
|----------------|---------|-------|-------|
| Interface GUI | ✅ | ✅ | ✅ |
| Icône barre | ✅ | ✅ | ✅ |
| Élévation privilèges | ✅ | ✅ | ✅ |
| Ouverture dossiers | ✅ | ✅ | ✅ |
| Extensions IA | ✅ | ✅ | ✅ |
| Rapport système | ✅ | ✅ | ✅ |

## Support

- **Testé**: Linux Kali, Windows 10/11
- **Compatible**: macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.8 à 3.13