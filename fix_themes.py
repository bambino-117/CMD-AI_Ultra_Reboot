#!/usr/bin/env python3
"""
Correctif pour forcer l'application des thèmes
"""

import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.theme_manager import ThemeManager

def fix_themes():
    """Corrige et teste les thèmes"""
    print("🔧 Correctif des Thèmes CMD-AI Ultra Reboot")
    print("=" * 50)
    
    # Initialiser le gestionnaire de thèmes
    theme_manager = ThemeManager()
    
    print("📋 Thèmes disponibles:")
    for theme_id, theme_data in theme_manager.themes.items():
        current = " (ACTUEL)" if theme_id == theme_manager.current_theme else ""
        print(f"  • {theme_id}: {theme_data['name']}{current}")
    
    print(f"\n🎨 Thème actuel: {theme_manager.current_theme}")
    
    # Forcer le thème par défaut à "light"
    if theme_manager.current_theme != "light":
        print("🔄 Réinitialisation au thème clair...")
        result = theme_manager.set_theme("light")
        print(result)
    
    # Test de changement de thème
    print("\n🧪 Test de changement de thème:")
    
    test_themes = ["dark", "neon", "light"]
    for theme in test_themes:
        print(f"\n  Changement vers '{theme}'...")
        result = theme_manager.set_theme(theme)
        print(f"  Résultat: {result}")
        
        # Vérifier que le thème a bien changé
        if theme_manager.current_theme == theme:
            print(f"  ✅ Thème '{theme}' activé")
        else:
            print(f"  ❌ Échec activation thème '{theme}'")
    
    print("\n💡 Pour tester visuellement:")
    print("  python3 test_themes.py")
    
    print("\n📝 Dans l'application principale:")
    print("  theme list    - Voir tous les thèmes")
    print("  theme set neon - Activer le thème néon")
    print("  theme toggle  - Basculer clair/sombre")

if __name__ == "__main__":
    fix_themes()