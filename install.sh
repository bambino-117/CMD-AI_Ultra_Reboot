#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║              CMD-AI ULTRA REBOOT v2.0.0                 ║"
echo "║                    INSTALLATION                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo

echo "📦 Installation de CMD-AI Ultra Reboot..."

# Répertoire d'installation
INSTALL_DIR="/opt/cmd-ai-ultra-reboot"
BIN_DIR="/usr/local/bin"

echo "📁 Création du répertoire: $INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"

echo "📋 Copie des fichiers..."
sudo cp CMD-AI_Ultra_Reboot "$INSTALL_DIR/"
sudo cp *.md "$INSTALL_DIR/" 2>/dev/null || true
sudo cp *.txt "$INSTALL_DIR/" 2>/dev/null || true

echo "🔧 Configuration des permissions..."
sudo chmod +x "$INSTALL_DIR/CMD-AI_Ultra_Reboot"

echo "🔗 Création du lien symbolique..."
sudo ln -sf "$INSTALL_DIR/CMD-AI_Ultra_Reboot" "$BIN_DIR/cmd-ai"

echo "🖥️ Création du raccourci bureau..."
DESKTOP_FILE="$HOME/.local/share/applications/cmd-ai-ultra-reboot.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=CMD-AI Ultra Reboot
Comment=Application de chat/terminal IA modulaire
Exec=$INSTALL_DIR/CMD-AI_Ultra_Reboot
Terminal=false
Type=Application
Categories=Development;Utility;
StartupNotify=true
EOF

echo
echo "🎉 INSTALLATION TERMINÉE !"
echo
echo "Vous pouvez lancer l'application avec:"
echo "• cmd-ai (depuis le terminal)"
echo "• Ou depuis le menu des applications"
echo
