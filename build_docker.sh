#!/bin/bash

echo "🐳 Compilation Docker multi-plateforme"
echo "======================================"

# Fonction de compilation Windows
build_windows() {
    echo "🪟 Compilation Windows (.exe)..."
    
    # Construire l'image Docker
    docker build -f Dockerfile.windows -t cmd-ai-windows-builder .
    
    # Compiler l'exécutable
    docker run --rm -v $(pwd)/dist_docker:/app/dist cmd-ai-windows-builder
    
    if [ -f "dist_docker/CMD-AI_Ultra_Reboot.exe" ]; then
        echo "✅ Exécutable Windows créé !"
        
        # Créer le package
        mkdir -p dist_windows
        cp dist_docker/CMD-AI_Ultra_Reboot.exe dist_windows/
        cp *.md dist_windows/
        cp requirements.txt dist_windows/
        
        # Créer l'installateur
        cat > dist_windows/install.bat << 'EOF'
@echo off
echo 🚀 Installation CMD-AI Ultra Reboot
echo.
echo Copie des fichiers...
if not exist "%USERPROFILE%\CMD-AI_Ultra_Reboot" mkdir "%USERPROFILE%\CMD-AI_Ultra_Reboot"
copy /Y CMD-AI_Ultra_Reboot.exe "%USERPROFILE%\CMD-AI_Ultra_Reboot\"
copy /Y *.md "%USERPROFILE%\CMD-AI_Ultra_Reboot\" 2>nul
echo.
echo ✅ Installation terminée !
echo 📍 Emplacement: %USERPROFILE%\CMD-AI_Ultra_Reboot
echo.
pause
EOF
        
        # Créer l'archive
        zip -r CMD-AI_Ultra_Reboot_Windows_v1.1.0.zip dist_windows/
        echo "📦 Package Windows créé : CMD-AI_Ultra_Reboot_Windows_v1.1.0.zip"
    else
        echo "❌ Échec compilation Windows"
    fi
}

# Fonction de compilation macOS (simulation)
build_macos() {
    echo "🍎 Simulation macOS (.app)..."
    echo "⚠️  Compilation macOS nécessite un Mac réel"
    echo "💡 Utilisez GitHub Actions ou un Mac physique"
    
    # Créer un package de sources pour macOS
    mkdir -p dist_macos_source
    cp -r . dist_macos_source/
    rm -rf dist_macos_source/.git dist_macos_source/dist* dist_macos_source/build
    
    cat > dist_macos_source/build_macos.sh << 'EOF'
#!/bin/bash
# Script à exécuter sur macOS
echo "🍎 Compilation macOS"
pip3 install -r requirements.txt
pip3 install pyinstaller
pyinstaller --onefile --windowed --name CMD-AI_Ultra_Reboot --icon ressources/logos/CMD-AI_Ultra_main.png --add-data "ressources:ressources" --add-data "extensions:extensions" main.py
echo "✅ Compilation terminée - Vérifiez le dossier dist/"
EOF
    chmod +x dist_macos_source/build_macos.sh
    
    tar -czf CMD-AI_Ultra_Reboot_macOS_Source_v1.1.0.tar.gz -C dist_macos_source .
    echo "📦 Sources macOS créées : CMD-AI_Ultra_Reboot_macOS_Source_v1.1.0.tar.gz"
}

# Menu principal
case "$1" in
    "windows")
        build_windows
        ;;
    "macos")
        build_macos
        ;;
    "all")
        build_windows
        build_macos
        echo ""
        echo "🎉 Compilation terminée !"
        echo "📦 Fichiers créés :"
        ls -lh *.zip *.tar.gz 2>/dev/null || echo "Aucun package créé"
        ;;
    *)
        echo "Usage: $0 {windows|macos|all}"
        echo ""
        echo "Exemples :"
        echo "  $0 windows  # Compile .exe Windows"
        echo "  $0 macos    # Prépare sources macOS"
        echo "  $0 all      # Compile tout"
        exit 1
        ;;
esac