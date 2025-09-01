from core.base_extension import BaseExtension
import os
import shutil
import json
from datetime import datetime

class FileManagerExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "FileManager"
        self.version = "1.0.0"
        self.description = "Gestionnaire de fichiers avancé avec recherche et organisation"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "search":
            return self.search_files(args)
        elif command == "organize":
            return self.organize_files(args)
        elif command == "duplicate":
            return self.find_duplicates(args)
        elif command == "clean":
            return self.clean_temp_files()
        elif command == "help":
            return self.show_help()
        else:
            return "Commandes: search, organize, duplicate, clean, help"
    
    def search_files(self, pattern=None):
        """Recherche de fichiers par pattern"""
        if not pattern:
            pattern = "*"
        
        try:
            import glob
            current_dir = os.getcwd()
            
            # Recherche récursive
            files = glob.glob(f"**/*{pattern}*", recursive=True)
            
            if not files:
                return f"🔍 Aucun fichier trouvé pour '{pattern}'"
            
            result = f"🔍 RECHERCHE: '{pattern}' ({len(files)} résultats)\n\n"
            
            for file in files[:20]:  # Limiter à 20 résultats
                if os.path.isfile(file):
                    size = os.path.getsize(file)
                    size_str = self._format_size(size)
                    result += f"📄 {file} ({size_str})\n"
                elif os.path.isdir(file):
                    result += f"📁 {file}/\n"
            
            if len(files) > 20:
                result += f"\n... et {len(files) - 20} autres résultats"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur recherche: {e}"
    
    def organize_files(self, directory=None):
        """Organise les fichiers par type"""
        if not directory:
            directory = "."
        
        try:
            if not os.path.exists(directory):
                return f"❌ Dossier '{directory}' non trouvé"
            
            organized = {
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
                "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
                "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
            }
            
            moved_files = 0
            
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    ext = os.path.splitext(filename)[1].lower()
                    
                    for category, extensions in organized.items():
                        if ext in extensions:
                            category_dir = os.path.join(directory, category)
                            os.makedirs(category_dir, exist_ok=True)
                            
                            src = os.path.join(directory, filename)
                            dst = os.path.join(category_dir, filename)
                            
                            if not os.path.exists(dst):
                                shutil.move(src, dst)
                                moved_files += 1
                            break
            
            return f"✅ Organisation terminée: {moved_files} fichiers déplacés"
            
        except Exception as e:
            return f"❌ Erreur organisation: {e}"
    
    def find_duplicates(self, directory=None):
        """Trouve les fichiers dupliqués"""
        if not directory:
            directory = "."
        
        try:
            import hashlib
            
            file_hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        if file_hash in file_hashes:
                            duplicates.append((filepath, file_hashes[file_hash]))
                        else:
                            file_hashes[file_hash] = filepath
                    except:
                        continue
            
            if not duplicates:
                return "✅ Aucun doublon trouvé"
            
            result = f"🔍 DOUBLONS TROUVÉS ({len(duplicates)})\n\n"
            for dup, original in duplicates[:10]:
                result += f"📄 {dup}\n   ↳ Identique à: {original}\n\n"
            
            if len(duplicates) > 10:
                result += f"... et {len(duplicates) - 10} autres doublons"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur recherche doublons: {e}"
    
    def clean_temp_files(self):
        """Nettoie les fichiers temporaires"""
        try:
            temp_patterns = ["*.tmp", "*.temp", "*~", ".DS_Store", "Thumbs.db"]
            cleaned = 0
            
            import glob
            for pattern in temp_patterns:
                for file in glob.glob(f"**/{pattern}", recursive=True):
                    try:
                        os.remove(file)
                        cleaned += 1
                    except:
                        continue
            
            return f"🧹 Nettoyage terminé: {cleaned} fichiers temporaires supprimés"
            
        except Exception as e:
            return f"❌ Erreur nettoyage: {e}"
    
    def _format_size(self, size):
        """Formate la taille en unités lisibles"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def show_help(self):
        """Affiche l'aide"""
        return """📁 GESTIONNAIRE DE FICHIERS

📌 Commandes disponibles:
• ext FileManager search [pattern] - Rechercher fichiers
• ext FileManager organize [dossier] - Organiser par type
• ext FileManager duplicate [dossier] - Trouver doublons
• ext FileManager clean - Nettoyer fichiers temporaires
• ext FileManager help - Cette aide

💡 Exemples:
• ext FileManager search "*.pdf"
• ext FileManager organize ~/Downloads
• ext FileManager duplicate .
• ext FileManager clean

🔧 Fonctionnalités:
• Recherche récursive avec patterns
• Organisation automatique par type de fichier
• Détection de doublons par hash MD5
• Nettoyage des fichiers temporaires"""
    
    def get_commands(self):
        return ["search", "organize", "duplicate", "clean", "help"]