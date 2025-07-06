# 🐧 Installation CMD-AI Ultra Reboot - Linux

## 📦 Installation rapide

### 1. Télécharger
```bash
# Téléchargez le package depuis GitHub Releases
wget https://github.com/bambino-117/CMD-AI_Ultra_Reboot/releases/latest/download/CMD-AI_Ultra_Reboot_Linux.tar.gz
tar -xzf CMD-AI_Ultra_Reboot_Linux.tar.gz
cd CMD-AI_Ultra_Reboot_Linux/
```

### 2. Installer les dépendances
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-tk python3-pil python3-requests python3-psutil python3-pygments

# Optionnel: Outils de capture d'écran
sudo apt install scrot

# Fedora/CentOS
sudo dnf install python3-tkinter python3-pillow python3-requests python3-psutil python3-pygments scrot

# Arch Linux
sudo pacman -S tk python-pillow python-requests python-psutil python-pygments scrot
```

### 3. Lancer l'application
```bash
# Rendre exécutable
chmod +x CMD-AI_Ultra_Reboot

# Lancer
./CMD-AI_Ultra_Reboot
```

## 🔧 Installation système (optionnel)

```bash
# Copier vers /usr/local/bin
sudo cp CMD-AI_Ultra_Reboot /usr/local/bin/
sudo chmod +x /usr/local/bin/CMD-AI_Ultra_Reboot

# Créer un raccourci bureau
cat > ~/.local/share/applications/cmd-ai-ultra-reboot.desktop << EOF
[Desktop Entry]
Name=CMD-AI Ultra Reboot
Comment=Multi-platform AI chat application
Exec=/usr/local/bin/CMD-AI_Ultra_Reboot
Icon=applications-development
Terminal=false
Type=Application
Categories=Development;Utility;
EOF
```

## 🧪 Mode testeur

Si vous avez un code testeur (format: 001Z), saisissez-le dans le champ "Pseudo" pour activer le mode testeur.

## 🆘 Dépannage

### L'application ne démarre pas
```bash
# Vérifier les dépendances
python3 -c "import tkinter, PIL, requests, psutil; print('✅ Dépendances OK')"

# Lancer en mode debug
./CMD-AI_Ultra_Reboot --debug
```

### Erreur de capture d'écran
```bash
# Installer scrot (recommandé)
sudo apt install scrot

# Ou alternatives
sudo apt install gnome-screenshot imagemagick flameshot
```

### Problème de permissions
```bash
# Rendre exécutable
chmod +x CMD-AI_Ultra_Reboot

# Vérifier les permissions
ls -la CMD-AI_Ultra_Reboot
```

## 📞 Support

- **GitHub Issues** : https://github.com/bambino-117/CMD-AI_Ultra_Reboot/issues
- **Documentation** : Voir les fichiers .md inclus
- **Guide testeur** : TESTER_GUIDE.md

---
**CMD-AI Ultra Reboot v1.1.0** - Développé avec ❤️ pour la communauté