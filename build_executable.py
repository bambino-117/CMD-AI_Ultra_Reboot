#!/usr/bin/env python3
"""
Script de compilation en exécutable pour CMD-AI Ultra Reboot
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("✅ PyInstaller déjà installé")
        return True
    except ImportError:
        print("📦 Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur installation PyInstaller")
            return False

def clean_build():
    """Nettoie les dossiers de build"""
    print("🧹 Nettoyage des anciens builds...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Supprimé: {dir_name}/")
    
    # Nettoyer les .pyc
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))

def create_spec_file():
    """Crée le fichier .spec pour PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ressources', 'ressources'),
        ('extensions', 'extensions'),
        ('language_models', 'language_models'),
        ('ui', 'ui'),
        ('core', 'core'),
        ('utils', 'utils'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'json',
        'sqlite3',
        'threading',
        'queue',
        'datetime',
        'os',
        'sys',
        'platform',
        'subprocess',
        'webbrowser',
        'tempfile',
        'shutil',
        'glob',
        'hashlib',
        'base64',
        'urllib.parse',
        'urllib.request',
        'psutil',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CMD-AI_Ultra_Reboot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ressources/icons/CMD-AI_Ultra_main.ico' if os.path.exists('ressources/icons/CMD-AI_Ultra_main.ico') else None,
)
'''
    
    with open("CMD-AI_Ultra_Reboot.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec créé")

def build_executable():
    """Compile l'exécutable"""
    print("🔨 Compilation en cours...")
    print("⏳ Cela peut prendre plusieurs minutes...")
    
    try:
        # Utiliser le fichier .spec
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "CMD-AI_Ultra_Reboot.spec"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilation réussie !")
            return True
        else:
            print("❌ Erreur de compilation:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_installer():
    """Crée un installateur simple"""
    print("📦 Création de l'installateur...")
    
    # Créer le dossier de distribution
    dist_dir = "CMD-AI_Ultra_Reboot_v2.0.0"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir)
    
    # Copier l'exécutable
    exe_name = "CMD-AI_Ultra_Reboot.exe" if sys.platform == "win32" else "CMD-AI_Ultra_Reboot"
    exe_path = os.path.join("dist", exe_name)
    
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, dist_dir)
        print(f"   Copié: {exe_name}")
    
    # Copier les fichiers essentiels
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "LICENSE" if os.path.exists("LICENSE") else None
    ]
    
    for file in files_to_copy:
        if file and os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"   Copié: {file}")
    
    # Créer un script d'installation
    install_script = f"""#!/bin/bash
# Installateur CMD-AI Ultra Reboot v2.0.0

echo "🤖 CMD-AI Ultra Reboot - Installation"
echo "===================================="

# Créer le dossier d'installation
INSTALL_DIR="$HOME/CMD-AI_Ultra_Reboot"
mkdir -p "$INSTALL_DIR"

# Copier l'exécutable
cp "{exe_name}" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/{exe_name}"

# Créer un lien symbolique
sudo ln -sf "$INSTALL_DIR/{exe_name}" "/usr/local/bin/cmd-ai" 2>/dev/null || true

echo "✅ Installation terminée !"
echo "💡 Lancez avec: cmd-ai ou $INSTALL_DIR/{exe_name}"
"""
    
    with open(os.path.join(dist_dir, "install.sh"), "w") as f:
        f.write(install_script)
    
    os.chmod(os.path.join(dist_dir, "install.sh"), 0o755)
    
    # Créer une archive
    archive_name = f"{dist_dir}.tar.gz"
    shutil.make_archive(dist_dir, 'gztar', '.', dist_dir)
    
    print(f"✅ Archive créée: {archive_name}")
    
    return True

def main():
    """Fonction principale"""
    print("🚀 BUILD CMD-AI ULTRA REBOOT")
    print("=" * 40)
    
    # Vérifications préliminaires
    if not os.path.exists("main.py"):
        print("❌ Fichier main.py non trouvé")
        return False
    
    # Étapes de build
    steps = [
        ("Installation PyInstaller", install_pyinstaller),
        ("Nettoyage", clean_build),
        ("Création fichier .spec", create_spec_file),
        ("Compilation", build_executable),
        ("Création installateur", create_installer),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Échec: {step_name}")
            return False
    
    print("\n🎉 BUILD TERMINÉ AVEC SUCCÈS !")
    print("=" * 40)
    print("📁 Fichiers générés:")
    print("   • dist/CMD-AI_Ultra_Reboot(.exe)")
    print("   • CMD-AI_Ultra_Reboot_v2.0.0.tar.gz")
    print("\n💡 Pour distribuer:")
    print("   1. Testez l'exécutable dans dist/")
    print("   2. Distribuez l'archive .tar.gz")
    print("   3. Les utilisateurs peuvent utiliser install.sh")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)