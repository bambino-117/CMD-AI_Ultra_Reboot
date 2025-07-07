from core.base_extension import BaseExtension
import re
import json
import base64
import hashlib
from datetime import datetime

class TextToolsExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "TextTools"
        self.version = "1.0.0"
        self.description = "Outils de traitement de texte: regex, hash, encode, format"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "regex":
            return self.regex_tool(args)
        elif command == "hash":
            return self.hash_text(args)
        elif command == "encode":
            return self.encode_text(args)
        elif command == "decode":
            return self.decode_text(args)
        elif command == "format":
            return self.format_text(args)
        elif command == "count":
            return self.count_text(args)
        elif command == "help":
            return self.show_help()
        else:
            return "Commandes: regex, hash, encode, decode, format, count, help"
    
    def regex_tool(self, pattern_and_text=None):
        """Outil regex pour recherche et remplacement"""
        if not pattern_and_text:
            return """🔍 OUTIL REGEX

Usage: ext TextTools regex "pattern|texte"
Ou: ext TextTools regex "pattern|texte|remplacement"

Exemples:
• ext TextTools regex "\\d+|J'ai 25 ans et 3 chats"
• ext TextTools regex "\\d+|J'ai 25 ans|XX"
• ext TextTools regex "[a-z]+@[a-z]+\\.[a-z]+|Contact: john@example.com"

Patterns utiles:
• \\d+ : nombres
• [a-zA-Z]+ : mots
• \\w+@\\w+\\.\\w+ : emails basiques
• \\b\\w{4}\\b : mots de 4 lettres"""
        
        try:
            parts = pattern_and_text.split("|")
            if len(parts) < 2:
                return "❌ Format: pattern|texte ou pattern|texte|remplacement"
            
            pattern = parts[0]
            text = parts[1]
            replacement = parts[2] if len(parts) > 2 else None
            
            # Compilation du pattern
            try:
                regex = re.compile(pattern)
            except re.error as e:
                return f"❌ Pattern regex invalide: {e}"
            
            if replacement is not None:
                # Mode remplacement
                result_text = regex.sub(replacement, text)
                matches = regex.findall(text)
                
                response = f"🔄 REMPLACEMENT REGEX\n\n"
                response += f"Pattern: {pattern}\n"
                response += f"Remplacement: {replacement}\n"
                response += f"Correspondances: {len(matches)}\n\n"
                response += f"Texte original:\n{text}\n\n"
                response += f"Résultat:\n{result_text}"
                
                return response
            else:
                # Mode recherche
                matches = regex.findall(text)
                match_objects = list(regex.finditer(text))
                
                response = f"🔍 RECHERCHE REGEX\n\n"
                response += f"Pattern: {pattern}\n"
                response += f"Texte: {text}\n"
                response += f"Correspondances trouvées: {len(matches)}\n\n"
                
                if matches:
                    response += "📋 Résultats:\n"
                    for i, (match, match_obj) in enumerate(zip(matches, match_objects), 1):
                        start, end = match_obj.span()
                        response += f"{i}. '{match}' (position {start}-{end})\n"
                else:
                    response += "❌ Aucune correspondance trouvée"
                
                return response
                
        except Exception as e:
            return f"❌ Erreur regex: {e}"
    
    def hash_text(self, text_and_algo=None):
        """Génère des hash de texte"""
        if not text_and_algo:
            return """🔐 GÉNÉRATEUR DE HASH

Usage: ext TextTools hash "texte|algorithme"

Algorithmes supportés:
• md5, sha1, sha256, sha512

Exemples:
• ext TextTools hash "Hello World|md5"
• ext TextTools hash "mot de passe|sha256"
• ext TextTools hash "données sensibles|sha512" """
        
        try:
            parts = text_and_algo.split("|")
            if len(parts) != 2:
                return "❌ Format: texte|algorithme"
            
            text = parts[0]
            algo = parts[1].lower()
            
            # Encodage du texte
            text_bytes = text.encode('utf-8')
            
            # Génération du hash
            if algo == "md5":
                hash_obj = hashlib.md5(text_bytes)
            elif algo == "sha1":
                hash_obj = hashlib.sha1(text_bytes)
            elif algo == "sha256":
                hash_obj = hashlib.sha256(text_bytes)
            elif algo == "sha512":
                hash_obj = hashlib.sha512(text_bytes)
            else:
                return f"❌ Algorithme non supporté: {algo}"
            
            hash_hex = hash_obj.hexdigest()
            
            result = f"🔐 HASH {algo.upper()}\n\n"
            result += f"Texte: {text}\n"
            result += f"Algorithme: {algo.upper()}\n"
            result += f"Hash: {hash_hex}\n"
            result += f"Longueur: {len(hash_hex)} caractères"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur hash: {e}"
    
    def encode_text(self, text_and_encoding=None):
        """Encode du texte"""
        if not text_and_encoding:
            return """🔤 ENCODAGE TEXTE

Usage: ext TextTools encode "texte|format"

Formats supportés:
• base64, hex, url

Exemples:
• ext TextTools encode "Hello World|base64"
• ext TextTools encode "données|hex"
• ext TextTools encode "texte avec espaces|url" """
        
        try:
            parts = text_and_encoding.split("|")
            if len(parts) != 2:
                return "❌ Format: texte|format"
            
            text = parts[0]
            encoding = parts[1].lower()
            
            if encoding == "base64":
                encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            elif encoding == "hex":
                encoded = text.encode('utf-8').hex()
            elif encoding == "url":
                import urllib.parse
                encoded = urllib.parse.quote(text)
            else:
                return f"❌ Format non supporté: {encoding}"
            
            result = f"🔤 ENCODAGE {encoding.upper()}\n\n"
            result += f"Texte original: {text}\n"
            result += f"Format: {encoding.upper()}\n"
            result += f"Résultat: {encoded}"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur encodage: {e}"
    
    def decode_text(self, text_and_encoding=None):
        """Décode du texte"""
        if not text_and_encoding:
            return """🔓 DÉCODAGE TEXTE

Usage: ext TextTools decode "texte_encodé|format"

Formats supportés:
• base64, hex, url

Exemples:
• ext TextTools decode "SGVsbG8gV29ybGQ=|base64"
• ext TextTools decode "48656c6c6f20576f726c64|hex"
• ext TextTools decode "texte%20avec%20espaces|url" """
        
        try:
            parts = text_and_encoding.split("|")
            if len(parts) != 2:
                return "❌ Format: texte_encodé|format"
            
            encoded_text = parts[0]
            encoding = parts[1].lower()
            
            if encoding == "base64":
                decoded = base64.b64decode(encoded_text).decode('utf-8')
            elif encoding == "hex":
                decoded = bytes.fromhex(encoded_text).decode('utf-8')
            elif encoding == "url":
                import urllib.parse
                decoded = urllib.parse.unquote(encoded_text)
            else:
                return f"❌ Format non supporté: {encoding}"
            
            result = f"🔓 DÉCODAGE {encoding.upper()}\n\n"
            result += f"Texte encodé: {encoded_text}\n"
            result += f"Format: {encoding.upper()}\n"
            result += f"Résultat: {decoded}"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur décodage: {e}"
    
    def format_text(self, text_and_format=None):
        """Formate du texte"""
        if not text_and_format:
            return """📝 FORMATAGE TEXTE

Usage: ext TextTools format "texte|format"

Formats disponibles:
• upper, lower, title, reverse
• remove_spaces, remove_numbers, remove_special
• lines, words

Exemples:
• ext TextTools format "hello world|upper"
• ext TextTools format "HELLO WORLD|lower"
• ext TextTools format "hello world|title"
• ext TextTools format "text with spaces|remove_spaces" """
        
        try:
            parts = text_and_format.split("|")
            if len(parts) != 2:
                return "❌ Format: texte|format"
            
            text = parts[0]
            format_type = parts[1].lower()
            
            if format_type == "upper":
                formatted = text.upper()
            elif format_type == "lower":
                formatted = text.lower()
            elif format_type == "title":
                formatted = text.title()
            elif format_type == "reverse":
                formatted = text[::-1]
            elif format_type == "remove_spaces":
                formatted = re.sub(r'\s+', '', text)
            elif format_type == "remove_numbers":
                formatted = re.sub(r'\d+', '', text)
            elif format_type == "remove_special":
                formatted = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            elif format_type == "lines":
                lines = text.split('\n')
                formatted = f"Nombre de lignes: {len(lines)}"
            elif format_type == "words":
                words = text.split()
                formatted = f"Nombre de mots: {len(words)}"
            else:
                return f"❌ Format non supporté: {format_type}"
            
            result = f"📝 FORMATAGE {format_type.upper()}\n\n"
            result += f"Texte original: {text}\n"
            result += f"Format: {format_type.upper()}\n"
            result += f"Résultat: {formatted}"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur formatage: {e}"
    
    def count_text(self, text=None):
        """Compte les éléments dans un texte"""
        if not text:
            return """📊 COMPTEUR DE TEXTE

Usage: ext TextTools count "votre texte ici"

Compte automatiquement:
• Caractères (avec et sans espaces)
• Mots
• Lignes
• Paragraphes
• Caractères spéciaux

Exemple:
• ext TextTools count "Hello World! Comment allez-vous?" """
        
        try:
            # Comptages
            chars_total = len(text)
            chars_no_spaces = len(text.replace(' ', ''))
            words = len(text.split())
            lines = len(text.split('\n'))
            paragraphs = len([p for p in text.split('\n\n') if p.strip()])
            
            # Caractères spéciaux
            special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', text))
            numbers = len(re.findall(r'\d', text))
            
            result = f"📊 ANALYSE DE TEXTE\n\n"
            result += f"Texte: {text[:50]}{'...' if len(text) > 50 else ''}\n\n"
            result += f"📏 Caractères (total): {chars_total}\n"
            result += f"📏 Caractères (sans espaces): {chars_no_spaces}\n"
            result += f"📝 Mots: {words}\n"
            result += f"📄 Lignes: {lines}\n"
            result += f"📋 Paragraphes: {paragraphs}\n"
            result += f"🔢 Chiffres: {numbers}\n"
            result += f"🔣 Caractères spéciaux: {special_chars}"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur comptage: {e}"
    
    def show_help(self):
        """Affiche l'aide"""
        return """🔤 OUTILS DE TEXTE

📌 Commandes disponibles:
• ext TextTools regex "pattern|texte" - Recherche regex
• ext TextTools hash "texte|algo" - Génération de hash
• ext TextTools encode "texte|format" - Encodage
• ext TextTools decode "texte|format" - Décodage
• ext TextTools format "texte|format" - Formatage
• ext TextTools count "texte" - Comptage d'éléments
• ext TextTools help - Cette aide

💡 Exemples rapides:
• ext TextTools regex "\\d+|J'ai 25 ans"
• ext TextTools hash "password|sha256"
• ext TextTools encode "Hello|base64"
• ext TextTools format "hello|upper"
• ext TextTools count "Bonjour le monde!"

🔧 Fonctionnalités:
• Regex avec recherche et remplacement
• Hash MD5, SHA1, SHA256, SHA512
• Encodage/décodage Base64, Hex, URL
• Formatage de texte avancé
• Analyse et comptage de texte"""
    
    def get_commands(self):
        return ["regex", "hash", "encode", "decode", "format", "count", "help"]