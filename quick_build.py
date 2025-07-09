#!/usr/bin/env python3
"""Build rapide sans PyInstaller - Crée un script exécutable"""

import os
import shutil
import zipfile
from pathlib import Path

def create_portable_version():
    print("🏗️ Création de CMD-AI Ultra Reboot v2.1.0 Portable")
    
    # Créer le dossier de distribution
    dist_dir = Path("dist/CMD-AI_Ultra_Reboot_v2.1.0_Portable")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers essentiels
    files_to_copy = [
        "main.py",
        "core/",
        "extensions/",
        "language_models/",
        "ui/",
        "ressources/",
        "requirements.txt",
        "README.md",
        "CHANGELOG.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dist_dir / item, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dist_dir / item)
    
    # Créer les dossiers utilisateur
    (dist_dir / "user").mkdir(exist_ok=True)
    (dist_dir / "logs").mkdir(exist_ok=True)
    
    # Créer un script de lancement
    launcher_content = '''#!/usr/bin/env python3
"""CMD-AI Ultra Reboot v2.1.0 - Launcher"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from main import main
if __name__ == "__main__":
    main()
'''
    
    with open(dist_dir / "CMD-AI_Ultra_Reboot.py", "w") as f:
        f.write(launcher_content)
    
    # Créer un script batch pour Windows
    batch_content = '''@echo off
python CMD-AI_Ultra_Reboot.py
pause
'''
    with open(dist_dir / "CMD-AI_Ultra_Reboot.bat", "w") as f:
        f.write(batch_content)
    
    # Créer un script shell pour Linux
    shell_content = '''#!/bin/bash
python3 CMD-AI_Ultra_Reboot.py
'''
    with open(dist_dir / "CMD-AI_Ultra_Reboot.sh", "w") as f:
        f.write(shell_content)
    
    os.chmod(dist_dir / "CMD-AI_Ultra_Reboot.sh", 0o755)
    
    print(f"✅ Version portable créée dans: {dist_dir}")
    
    # Créer une archive
    archive_name = "CMD-AI_Ultra_Reboot_v2.1.0_Portable.zip"
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"📦 Archive créée: {archive_name}")
    return archive_name

if __name__ == "__main__":
    create_portable_version()