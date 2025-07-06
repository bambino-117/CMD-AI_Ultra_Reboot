#!/usr/bin/env python3
"""
Script de compilation pour CMD-AI Ultra Reboot
Génère des exécutables pour Windows (.exe) et macOS (.app)
"""

import os
import sys
import platform
import subprocess
import shutil

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("✅ PyInstaller déjà installé")
    except ImportError:
        print("📦 Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Compile l'application en exécutable"""
    system = platform.system()
    
    # Paramètres communs
    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "CMD-AI_Ultra_Reboot",
        "--icon", "ressources/icons/CMD-AI_Ultra_main.ico" if system == "Windows" else "ressources/logos/CMD-AI_Ultra_main.png",
        "--add-data", "ressources;ressources" if system == "Windows" else "ressources:ressources",
        "--add-data", "extensions;extensions" if system == "Windows" else "extensions:extensions",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "pygments.lexers",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "main.py"
    ]
    
    print(f"🔨 Compilation pour {system}...")
    
    try:
        subprocess.check_call(base_cmd)
        print(f"✅ Compilation {system} réussie !")
        
        # Créer le dossier de distribution
        dist_folder = f"dist_{system.lower()}"
        os.makedirs(dist_folder, exist_ok=True)
        
        # Copier l'exécutable
        if system == "Windows":
            shutil.copy("dist/CMD-AI_Ultra_Reboot.exe", f"{dist_folder}/")
        elif system == "Darwin":  # macOS
            shutil.copytree("dist/CMD-AI_Ultra_Reboot.app", f"{dist_folder}/CMD-AI_Ultra_Reboot.app")
        else:  # Linux
            shutil.copy("dist/CMD-AI_Ultra_Reboot", f"{dist_folder}/")
        
        # Copier les fichiers nécessaires
        files_to_copy = [
            "README.md",
            "CHANGELOG.md",
            "TESTER_GUIDE.md",
            "INSTALL_SCREENSHOT_TOOLS.md",
            "requirements.txt"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy(file, f"{dist_folder}/")
        
        print(f"📦 Package créé dans {dist_folder}/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur de compilation: {e}")
        return False
    
    return True

def create_installer_script():
    """Crée un script d'installation"""
    system = platform.system()
    
    if system == "Windows":
        installer_content = """@echo off
echo 🚀 Installation CMD-AI Ultra Reboot
echo.
echo Copie des fichiers...
if not exist "%USERPROFILE%\\CMD-AI_Ultra_Reboot" mkdir "%USERPROFILE%\\CMD-AI_Ultra_Reboot"
copy /Y CMD-AI_Ultra_Reboot.exe "%USERPROFILE%\\CMD-AI_Ultra_Reboot\\"
copy /Y *.md "%USERPROFILE%\\CMD-AI_Ultra_Reboot\\" 2>nul
echo.
echo ✅ Installation terminée !
echo 📍 Emplacement: %USERPROFILE%\\CMD-AI_Ultra_Reboot
echo.
pause"""
        
        with open("dist_windows/install.bat", "w") as f:
            f.write(installer_content)
    
    elif system == "Darwin":  # macOS
        installer_content = """#!/bin/bash
echo "🚀 Installation CMD-AI Ultra Reboot"
echo
echo "Copie vers Applications..."
cp -R CMD-AI_Ultra_Reboot.app /Applications/
echo
echo "✅ Installation terminée !"
echo "📍 L'application est maintenant dans Applications"
echo
read -p "Appuyez sur Entrée pour continuer..."
"""
        
        with open("dist_darwin/install.sh", "w") as f:
            f.write(installer_content)
        os.chmod("dist_darwin/install.sh", 0o755)

def main():
    print("🏗️  CMD-AI Ultra Reboot - Générateur d'exécutable")
    print("=" * 50)
    
    # Vérifier les prérequis
    if not os.path.exists("main.py"):
        print("❌ main.py non trouvé !")
        return
    
    # Installer PyInstaller
    install_pyinstaller()
    
    # Compiler
    if build_executable():
        create_installer_script()
        print("\n🎉 Build terminé avec succès !")
        print(f"📦 Fichiers dans dist_{platform.system().lower()}/")
    else:
        print("\n❌ Échec du build")

if __name__ == "__main__":
    main()