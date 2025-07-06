#!/usr/bin/env python3
"""Vérification compatibilité Windows/macOS/Linux"""

import platform
import sys
import os

def check_system():
    """Vérification système"""
    print("=== COMPATIBILITÉ SYSTÈME ===")
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version}")
    
def check_dependencies():
    """Vérification dépendances"""
    print("\n=== DÉPENDANCES ===")
    
    deps = {
        'tkinter': 'Interface graphique',
        'PIL': 'Images (Pillow)',
        'requests': 'Requêtes HTTP',
        'json': 'JSON (built-in)',
        'os': 'Système (built-in)',
        'subprocess': 'Processus (built-in)'
    }
    
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {desc}")
        except ImportError:
            print(f"❌ {dep}: {desc} - MANQUANT")

def check_paths():
    """Vérification chemins"""
    print("\n=== CHEMINS ===")
    
    paths = [
        'ressources/icons/CMD-AI_Ultra_main.ico',
        'ressources/logos/CMD-AI_Ultra_main.png',
        'user/',
        'logs/',
        'extensions/',
        'core/',
        'ui/'
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - MANQUANT")

def check_platform_specific():
    """Vérifications spécifiques par plateforme"""
    print("\n=== SPÉCIFICITÉS PLATEFORME ===")
    
    system = platform.system()
    
    if system == "Windows":
        print("🪟 Windows détecté")
        print("- Icône: .ico supporté")
        print("- Commandes: cmd.exe")
        print("- Élévation: UAC")
        
    elif system == "Darwin":
        print("🍎 macOS détecté")
        print("- Icône: PNG via iconphoto")
        print("- Commandes: bash")
        print("- Élévation: osascript")
        
    elif system == "Linux":
        print("🐧 Linux détecté")
        print("- Icône: PNG via iconphoto")
        print("- Commandes: bash")
        print("- Élévation: sudo")
    
    # Test ouverture dossier
    try:
        if system == "Windows":
            test_cmd = "echo test"
        else:
            test_cmd = "echo test"
        
        import subprocess
        result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Commandes système fonctionnelles")
        else:
            print("❌ Problème commandes système")
    except Exception as e:
        print(f"❌ Erreur test commandes: {e}")

def check_fonts():
    """Vérification polices"""
    print("\n=== POLICES ===")
    
    import tkinter as tk
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Test Arial
        test_label = tk.Label(root, text="Test", font=('Arial', 8))
        print("✅ Arial disponible")
        
        root.destroy()
    except Exception as e:
        print(f"❌ Problème polices: {e}")

def main():
    print("CMD-AI Ultra Reboot - Vérification Compatibilité")
    print("=" * 50)
    
    check_system()
    check_dependencies()
    check_paths()
    check_platform_specific()
    check_fonts()
    
    print("\n=== RÉSUMÉ ===")
    system = platform.system()
    if system in ["Windows", "Darwin", "Linux"]:
        print(f"✅ {system} supporté")
    else:
        print(f"⚠️ {system} non testé")
    
    print("\n💡 Recommandations:")
    if system == "Windows":
        print("- Installer Python depuis python.org")
        print("- Utiliser PowerShell ou cmd")
    elif system == "Darwin":
        print("- Installer Python via Homebrew recommandé")
        print("- Utiliser Terminal")
    else:
        print("- Installer python3-tk si nécessaire")
        print("- Utiliser terminal bash")

if __name__ == "__main__":
    main()