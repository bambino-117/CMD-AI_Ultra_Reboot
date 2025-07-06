#!/usr/bin/env python3
"""Validation de la version stable"""

import os
import sys
import importlib.util

def validate_imports():
    """Valide que tous les modules s'importent correctement"""
    print("=== Validation des imports ===")
    
    modules_to_test = [
        'core.user_manager',
        'core.system_detector', 
        'language_models.llm_manager',
        'extensions.aichat_extension',
        'ui.setup_dialog',
        'ui.splash_screen'
    ]
    
    failed = []
    for module in modules_to_test:
        try:
            spec = importlib.util.spec_from_file_location(
                module, 
                module.replace('.', '/') + '.py'
            )
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                print(f"✓ {module}")
            else:
                failed.append(module)
                print(f"✗ {module} - Spec non trouvé")
        except Exception as e:
            failed.append(module)
            print(f"✗ {module} - {str(e)}")
    
    return len(failed) == 0

def validate_structure():
    """Valide la structure des fichiers"""
    print("\n=== Validation structure ===")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'INSTALL_OLLAMA.md',
        'core/__init__.py',
        'ui/__init__.py',
        'language_models/__init__.py',
        'extensions/__init__.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            missing.append(file)
            print(f"✗ {file}")
    
    return len(missing) == 0

def validate_functionality():
    """Test fonctionnel rapide"""
    print("\n=== Test fonctionnel ===")
    
    try:
        # Test LLM Manager
        from language_models.llm_manager import LLMManager
        llm = LLMManager()
        response = llm.get_response("test")
        print(f"✓ LLM Manager - Réponse: {response[:30]}...")
        
        # Test User Manager
        from core.user_manager import UserManager
        um = UserManager()
        print(f"✓ User Manager - Pseudo: {um.has_username()}")
        
        # Test System Detector
        from core.system_detector import SystemDetector
        sd = SystemDetector()
        info = sd.detect_system_info()
        print(f"✓ System Detector - OS: {info.get('system', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"✗ Test fonctionnel échoué: {e}")
        return False

def main():
    print("🔍 Validation version stable CMD-AI Ultra")
    print("=" * 50)
    
    # Tests
    imports_ok = validate_imports()
    structure_ok = validate_structure()
    function_ok = validate_functionality()
    
    # Résultat
    print("\n" + "=" * 50)
    if imports_ok and structure_ok and function_ok:
        print("✅ VALIDATION RÉUSSIE - Prêt pour compilation!")
        return 0
    else:
        print("❌ VALIDATION ÉCHOUÉE - Corrections nécessaires")
        return 1

if __name__ == "__main__":
    sys.exit(main())