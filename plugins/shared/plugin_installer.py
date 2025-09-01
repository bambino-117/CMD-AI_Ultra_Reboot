#!/usr/bin/env python3
"""
Installateur automatique des plugins
Détecte les logiciels et installe les plugins appropriés
"""

import os
import sys
import shutil
import platform
from pathlib import Path

class PluginInstaller:
    def __init__(self):
        self.system = platform.system()
        self.plugins_dir = Path(__file__).parent.parent
        
    def detect_software(self):
        """Détecter les logiciels installés"""
        detected = {}
        
        # GIMP
        gimp_paths = self._get_gimp_paths()
        if any(Path(p).exists() for p in gimp_paths):
            detected['gimp'] = self._find_existing_path(gimp_paths)
        
        # Krita
        krita_paths = self._get_krita_paths()
        if any(Path(p).exists() for p in krita_paths):
            detected['krita'] = self._find_existing_path(krita_paths)
        
        # Photoshop
        ps_paths = self._get_photoshop_paths()
        if any(Path(p).exists() for p in ps_paths):
            detected['photoshop'] = self._find_existing_path(ps_paths)
        
        return detected
    
    def _get_gimp_paths(self):
        """Obtenir les chemins possibles de GIMP"""
        if self.system == "Windows":
            return [
                "C:/Program Files/GIMP 2/lib/gimp/2.0/plug-ins",
                "C:/Program Files (x86)/GIMP 2/lib/gimp/2.0/plug-ins"
            ]
        elif self.system == "Darwin":  # macOS
            return [
                "/Applications/GIMP-2.10.app/Contents/Resources/lib/gimp/2.0/plug-ins",
                os.path.expanduser("~/Library/Application Support/GIMP/2.10/plug-ins")
            ]
        else:  # Linux
            return [
                os.path.expanduser("~/.config/GIMP/2.10/plug-ins"),
                "/usr/lib/gimp/2.0/plug-ins"
            ]
    
    def _get_krita_paths(self):
        """Obtenir les chemins possibles de Krita"""
        if self.system == "Windows":
            return [
                os.path.expanduser("~/AppData/Roaming/krita/pykrita"),
                "C:/Program Files/Krita (x64)/share/krita/pykrita"
            ]
        elif self.system == "Darwin":  # macOS
            return [
                os.path.expanduser("~/Library/Application Support/krita/pykrita"),
                "/Applications/krita.app/Contents/Resources/pykrita"
            ]
        else:  # Linux
            return [
                os.path.expanduser("~/.local/share/krita/pykrita"),
                "/usr/share/krita/pykrita"
            ]
    
    def _get_photoshop_paths(self):
        """Obtenir les chemins possibles de Photoshop"""
        if self.system == "Windows":
            return [
                "C:/Program Files/Adobe/Adobe Photoshop 2024/Plug-ins",
                "C:/Program Files/Adobe/Adobe Photoshop 2023/Plug-ins"
            ]
        elif self.system == "Darwin":  # macOS
            return [
                "/Applications/Adobe Photoshop 2024/Plug-ins",
                "/Applications/Adobe Photoshop 2023/Plug-ins"
            ]
        else:
            return []  # Photoshop pas disponible sur Linux
    
    def _find_existing_path(self, paths):
        """Trouver le premier chemin existant"""
        for path in paths:
            if Path(path).exists():
                return path
        return None
    
    def install_gimp_plugin(self, target_path):
        """Installer le plugin GIMP"""
        try:
            source = self.plugins_dir / "gimp" / "ui_generator.py"
            target = Path(target_path) / "ui_generator.py"
            
            # Créer le dossier si nécessaire
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Copier le plugin
            shutil.copy2(source, target)
            
            # Rendre exécutable sur Unix
            if self.system != "Windows":
                os.chmod(target, 0o755)
            
            return True
        except Exception as e:
            print(f"Erreur installation GIMP: {e}")
            return False
    
    def install_krita_plugin(self, target_path):
        """Installer le plugin Krita"""
        try:
            source_dir = self.plugins_dir / "krita"
            target_dir = Path(target_path) / "ui_generator"
            
            # Créer le dossier
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copier les fichiers
            for file in source_dir.glob("*.py"):
                shutil.copy2(file, target_dir / file.name)
            
            # Créer __init__.py
            init_file = target_dir / "__init__.py"
            init_file.write_text("from .ui_generator_krita import *\n")
            
            return True
        except Exception as e:
            print(f"Erreur installation Krita: {e}")
            return False
    
    def install_all(self):
        """Installer tous les plugins détectés"""
        detected = self.detect_software()
        results = {}
        
        print("🔍 Logiciels détectés:")
        for software, path in detected.items():
            print(f"  ✅ {software.upper()}: {path}")
        
        print("\n📦 Installation des plugins:")
        
        # GIMP
        if 'gimp' in detected:
            success = self.install_gimp_plugin(detected['gimp'])
            results['gimp'] = success
            status = "✅" if success else "❌"
            print(f"  {status} GIMP Plugin")
        
        # Krita
        if 'krita' in detected:
            success = self.install_krita_plugin(detected['krita'])
            results['krita'] = success
            status = "✅" if success else "❌"
            print(f"  {status} Krita Plugin")
        
        # Photoshop (TODO)
        if 'photoshop' in detected:
            print("  ⏳ Photoshop Plugin (en développement)")
        
        return results
    
    def uninstall_all(self):
        """Désinstaller tous les plugins"""
        detected = self.detect_software()
        
        print("🗑️ Désinstallation des plugins:")
        
        # GIMP
        if 'gimp' in detected:
            plugin_path = Path(detected['gimp']) / "ui_generator.py"
            if plugin_path.exists():
                plugin_path.unlink()
                print("  ✅ GIMP Plugin supprimé")
        
        # Krita
        if 'krita' in detected:
            plugin_dir = Path(detected['krita']) / "ui_generator"
            if plugin_dir.exists():
                shutil.rmtree(plugin_dir)
                print("  ✅ Krita Plugin supprimé")

def main():
    """Point d'entrée principal"""
    installer = PluginInstaller()
    
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        installer.uninstall_all()
    else:
        results = installer.install_all()
        
        if any(results.values()):
            print("\n🎉 Installation terminée!")
            print("Redémarrez vos logiciels pour voir les plugins.")
        else:
            print("\n⚠️ Aucun plugin installé.")
            print("Vérifiez que GIMP/Krita sont installés.")

if __name__ == "__main__":
    main()