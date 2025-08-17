#!/usr/bin/env python3
import os
import shutil
import zipfile

def create_portable_exe():
    print("Création de l'exécutable portable...")
    
    # Créer le dossier dist
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Créer un fichier batch qui lance l'application
    launcher_content = '''@echo off
cd /d "%~dp0"
echo Demarrage de CMD-AI Ultra Reboot V3...
python server.py
'''
    
    with open('dist/CMD-AI_Ultra_Reboot_V3_Launcher.bat', 'w') as f:
        f.write(launcher_content)
    
    # Copier tous les fichiers nécessaires
    files_to_copy = [
        'Interface.html',
        'server.py',
        'search-engine.html',
        'extensions',
        'marketplace'
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                if os.path.exists(f'dist/{item}'):
                    shutil.rmtree(f'dist/{item}')
                shutil.copytree(item, f'dist/{item}')
            else:
                shutil.copy2(item, 'dist/')
    
    # Créer un README pour l'utilisateur
    readme_content = '''CMD-AI Ultra Reboot V3 - Version Portable

INSTALLATION:
1. Assurez-vous que Python est installé sur votre système
2. Double-cliquez sur "CMD-AI_Ultra_Reboot_V3_Launcher.bat"
3. L'application s'ouvrira dans votre navigateur

REQUIREMENTS:
- Python 3.x installé
- Navigateur web moderne

UTILISATION:
- L'application se lance sur http://localhost:8080
- Toutes les fonctionnalités sont disponibles
- Appuyez sur Ctrl+C dans la console pour arrêter
'''
    
    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Exécutable portable créé dans le dossier 'dist/'")
    print("📁 Fichiers créés:")
    print("   - CMD-AI_Ultra_Reboot_V3_Launcher.bat (lanceur)")
    print("   - Interface.html (application principale)")
    print("   - server.py (serveur web)")
    print("   - extensions/ (toutes les extensions)")
    print("   - README.txt (instructions)")

if __name__ == "__main__":
    create_portable_exe()