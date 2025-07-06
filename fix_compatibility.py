#!/usr/bin/env python3
"""Corrections automatiques compatibilité"""

import os
import platform
import sys

def create_missing_dirs():
    """Créer les dossiers manquants"""
    dirs = ['user', 'logs', 'ressources/logos']
    
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Créé: {dir_path}")

def fix_icon_compatibility():
    """Corriger compatibilité icône"""
    ico_path = "ressources/icons/CMD-AI_Ultra_main.ico"
    png_path = "ressources/logos/CMD-AI_Ultra_main.png"
    
    if os.path.exists(ico_path) and not os.path.exists(png_path):
        try:
            from PIL import Image
            img = Image.open(ico_path)
            img.save(png_path, 'PNG')
            print("✅ Icône PNG créée pour Linux/macOS")
        except Exception as e:
            print(f"❌ Erreur conversion icône: {e}")

def check_python_version():
    """Vérifier version Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} compatible")
        return True
    else:
        print(f"⚠️ Python {version.major}.{version.minor} - Recommandé: 3.8+")
        return False

def create_launcher_scripts():
    """Créer scripts de lancement par plateforme"""
    system = platform.system()
    
    if system == "Windows":
        # Script .bat pour Windows
        bat_content = '''@echo off
cd /d "%~dp0"
python main.py
pause'''
        with open('launch.bat', 'w') as f:
            f.write(bat_content)
        print("✅ Créé: launch.bat (Windows)")
        
    elif system == "Darwin":
        # Script .command pour macOS
        command_content = '''#!/bin/bash
cd "$(dirname "$0")"
python3 main.py'''
        with open('launch.command', 'w') as f:
            f.write(command_content)
        os.chmod('launch.command', 0o755)
        print("✅ Créé: launch.command (macOS)")
        
    else:
        # Script .sh pour Linux
        sh_content = '''#!/bin/bash
cd "$(dirname "$0")"
python3 main.py'''
        with open('launch.sh', 'w') as f:
            f.write(sh_content)
        os.chmod('launch.sh', 0o755)
        print("✅ Créé: launch.sh (Linux)")

def main():
    print("CMD-AI Ultra Reboot - Corrections Compatibilité")
    print("=" * 50)
    
    create_missing_dirs()
    fix_icon_compatibility()
    check_python_version()
    create_launcher_scripts()
    
    print("\n✅ Corrections terminées")
    print(f"Plateforme: {platform.system()}")

if __name__ == "__main__":
    main()