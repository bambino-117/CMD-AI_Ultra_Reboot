# Installation des outils de capture d'écran

## Linux (Ubuntu/Debian)
```bash
# Option 1: scrot (simple et léger)
sudo apt install scrot

# Option 2: gnome-screenshot (GNOME)
sudo apt install gnome-screenshot

# Option 3: ImageMagick (universel)
sudo apt install imagemagick

# Option 4: flameshot (moderne)
sudo apt install flameshot

# Option 5: spectacle (KDE)
sudo apt install kde-spectacle
```

## Linux (Fedora/CentOS)
```bash
# scrot
sudo dnf install scrot

# gnome-screenshot
sudo dnf install gnome-screenshot

# ImageMagick
sudo dnf install ImageMagick
```

## Linux (Arch)
```bash
# scrot
sudo pacman -S scrot

# gnome-screenshot
sudo pacman -S gnome-screenshot

# ImageMagick
sudo pacman -S imagemagick
```

## Test de l'extension
```bash
# Dans CMD-AI Ultra Reboot
ext Screenshot capture
ext Screenshot select
```

## Fallback Python
Si aucun outil n'est installé, l'extension utilise PIL + tkinter (capture plein écran uniquement).

## Recommandation
**scrot** est l'outil le plus simple et compatible :
```bash
sudo apt install scrot
```