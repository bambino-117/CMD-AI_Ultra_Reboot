#!/usr/bin/env python3
"""Patch de compatibilité 32-bit"""

import platform
import sys
import warnings

def is_32bit():
    """Détecte si on est en 32-bit"""
    return platform.machine().lower() in ['i386', 'i686', 'x86'] or sys.maxsize <= 2**32

def apply_32bit_patch():
    """Applique les corrections 32-bit"""
    if not is_32bit():
        return False
    
    print("🔧 Patch 32-bit activé")
    
    # 1. Pillow fallback
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("⚠️ Pillow manquant - Mode dégradé")
        # Créer des classes fallback
        class FakeImage:
            @staticmethod
            def open(path): return None
            @staticmethod
            def resize(size, method=None): return None
        
        class FakeImageTk:
            @staticmethod
            def PhotoImage(img): return None
        
        sys.modules['PIL.Image'] = FakeImage
        sys.modules['PIL.ImageTk'] = FakeImageTk
    
    # 2. Réduire utilisation mémoire
    import gc
    gc.set_threshold(100, 10, 10)  # GC plus agressif
    
    # 3. Désactiver logs verbeux
    import logging
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    
    return True

def patch_ui_for_32bit():
    """Adaptations UI pour 32-bit"""
    if not is_32bit():
        return
    
    # Icône simplifiée
    def simple_set_icon(self):
        try:
            self.root.title("🤖 CMD-AI Ultra")  # Emoji au lieu d'icône
        except:
            self.root.title("CMD-AI Ultra")
    
    # Remplacer la méthode set_icon
    from ui.interface import AppUI
    AppUI.set_icon = simple_set_icon

def patch_system_report():
    """Rapport système adapté 32-bit"""
    if not is_32bit():
        return
    
    original_generate = None
    
    def generate_32bit_report(self):
        report = original_generate(self) if original_generate else ""
        return report + "\n⚠️ Version 32-bit - Fonctionnalités limitées"
    
    try:
        from core.system_report import SystemReport
        original_generate = SystemReport.generate_report
        SystemReport.generate_report = generate_32bit_report
    except:
        pass

# Auto-application du patch
if __name__ != "__main__":
    if is_32bit():
        apply_32bit_patch()
        patch_ui_for_32bit()
        patch_system_report()