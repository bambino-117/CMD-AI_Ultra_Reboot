#!/bin/bash
# Installateur CMD-AI Ultra Reboot v2.0.0

echo "🤖 CMD-AI Ultra Reboot v2.0.0 - Installation"
echo "============================================="

# Vérifications
if [ ! -f "CMD-AI_Ultra_Reboot" ]; then
    echo "❌ Fichier exécutable non trouvé"
    exit 1
fi

# Créer le dossier d'installation
INSTALL_DIR="$HOME/CMD-AI_Ultra_Reboot"
echo "📁 Création du dossier: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copier l'exécutable
echo "📦 Installation de l'exécutable..."
cp "CMD-AI_Ultra_Reboot" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/CMD-AI_Ultra_Reboot"

# Copier la documentation
cp README.md CHANGELOG.md LICENSE requirements.txt "$INSTALL_DIR/" 2>/dev/null || true

# Créer un lien symbolique (optionnel)
echo "🔗 Création du lien symbolique..."
if command -v sudo >/dev/null 2>&1; then
    sudo ln -sf "$INSTALL_DIR/CMD-AI_Ultra_Reboot" "/usr/local/bin/cmd-ai" 2>/dev/null || {
        echo "⚠️ Impossible de créer le lien système (permissions)"
        echo "💡 Vous pouvez lancer avec: $INSTALL_DIR/CMD-AI_Ultra_Reboot"
    }
else
    echo "⚠️ sudo non disponible, pas de lien système créé"
fi

# Créer un raccourci bureau (optionnel)
if [ -d "$HOME/Desktop" ] || [ -d "$HOME/Bureau" ]; then
    DESKTOP_DIR="$HOME/Desktop"
    [ -d "$HOME/Bureau" ] && DESKTOP_DIR="$HOME/Bureau"
    
    cat > "$DESKTOP_DIR/CMD-AI_Ultra_Reboot.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=CMD-AI Ultra Reboot
Comment=Application de chat/terminal IA modulaire
Exec=$INSTALL_DIR/CMD-AI_Ultra_Reboot
Icon=applications-development
Terminal=false
Categories=Development;Utility;
EOF
    
    chmod +x "$DESKTOP_DIR/CMD-AI_Ultra_Reboot.desktop"
    echo "🖥️ Raccourci bureau créé"
fi

echo ""
echo "✅ Installation terminée avec succès !"
echo "==========================================="
echo "🚀 Lancement:"
echo "   • Commande: cmd-ai (si lien créé)"
echo "   • Direct: $INSTALL_DIR/CMD-AI_Ultra_Reboot"
echo "   • Bureau: Double-clic sur l'icône"
echo ""
echo "📖 Documentation:"
echo "   • README: $INSTALL_DIR/README.md"
echo "   • Changelog: $INSTALL_DIR/CHANGELOG.md"
echo ""
echo "🔌 Fonctionnalités:"
echo "   • 6 modèles IA supportés"
echo "   • 9 extensions dans le marketplace"
echo "   • Interface avec thèmes"
echo "   • Intégration système complète"
echo ""
echo "💡 Premier lancement:"
echo "   1. Choisir un modèle IA (1-6)"
echo "   2. Ajouter clé API si nécessaire"
echo "   3. Explorer le marketplace 🔌"
echo ""
echo "🎉 Profitez de CMD-AI Ultra Reboot !"