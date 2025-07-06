#!/usr/bin/env python3
"""Script de compilation pour version stable"""

import os
import shutil
import zipfile
import datetime

def create_release():
    print("=== Création Version Stable CMD-AI Ultra ===")
    
    # Nettoyer les fichiers de test
    test_files = ['test_setup.py', 'user/settings.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Nettoyé: {file}")
    
    # Créer dossier de release
    release_dir = f"release_v1.0_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    # Copier les fichiers nécessaires
    files_to_copy = [
        'main.py',
        'requirements.txt',
        'README.md',
        'core/',
        'extensions/',
        'ui/',
        'ressources/',
        'utils/'
    ]
    
    os.makedirs(release_dir)
    os.makedirs(f"{release_dir}/user")  # Dossier user vide
    os.makedirs(f"{release_dir}/logs")  # Dossier logs vide
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, f"{release_dir}/{item}")
            else:
                shutil.copy2(item, release_dir)
            print(f"Copié: {item}")
    
    # Créer script de lancement
    launcher_script = """#!/bin/bash
echo "=== CMD-AI Ultra Reboot ==="
echo "Installation des dépendances..."
pip install -r requirements.txt
echo "Lancement de l'application..."
python main.py
"""
    
    with open(f"{release_dir}/launch.sh", 'w') as f:
        f.write(launcher_script)
    os.chmod(f"{release_dir}/launch.sh", 0o755)
    
    # Créer archive
    archive_name = f"{release_dir}.zip"
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n✅ Version stable créée: {archive_name}")
    print(f"📁 Dossier: {release_dir}")
    print("\n🚀 Prêt pour les testeurs!")
    
    return archive_name

if __name__ == "__main__":
    create_release()