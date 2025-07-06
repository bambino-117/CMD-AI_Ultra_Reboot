import re
import platform
from enum import Enum

class CommandType(Enum):
    SYSTEM_COMMAND = "system"
    AI_CHAT = "chat"
    HELP = "help"
    UNKNOWN = "unknown"

class TextInterpreter:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.command_prefixes = {
            'system': ['cmd:', 'exec:', '$', '>', 'run:'],
            'chat': ['chat:', 'ai:', '?', 'ask:'],
            'help': ['help', 'aide', '/?', '--help']
        }
    
    def interpret(self, text):
        """Interprète le texte et retourne le type de commande et le contenu traité"""
        text = text.strip()
        
        if not text:
            return CommandType.UNKNOWN, ""
        
        # Détection du type de commande
        command_type = self._detect_command_type(text)
        processed_text = self._process_text(text, command_type)
        
        return command_type, processed_text
    
    def _detect_command_type(self, text):
        """Détecte le type de commande basé sur les préfixes"""
        text_lower = text.lower()
        
        # Vérifier les préfixes système
        for prefix in self.command_prefixes['system']:
            if text_lower.startswith(prefix):
                return CommandType.SYSTEM_COMMAND
        
        # Vérifier les préfixes chat/IA
        for prefix in self.command_prefixes['chat']:
            if text_lower.startswith(prefix):
                return CommandType.AI_CHAT
        
        # Vérifier les commandes d'aide
        for prefix in self.command_prefixes['help']:
            if text_lower.startswith(prefix):
                return CommandType.HELP
        
        # Par défaut, considérer comme chat IA
        return CommandType.AI_CHAT
    
    def _process_text(self, text, command_type):
        """Traite le texte selon son type"""
        if command_type == CommandType.SYSTEM_COMMAND:
            return self._clean_system_command(text)
        elif command_type == CommandType.AI_CHAT:
            return self._clean_chat_text(text)
        elif command_type == CommandType.HELP:
            return self._clean_help_command(text)
        
        return text
    
    def _clean_system_command(self, text):
        """Nettoie les commandes système en retirant les préfixes"""
        for prefix in self.command_prefixes['system']:
            if text.lower().startswith(prefix):
                return text[len(prefix):].strip()
        return text
    
    def _clean_chat_text(self, text):
        """Nettoie le texte de chat en retirant les préfixes"""
        for prefix in self.command_prefixes['chat']:
            if text.lower().startswith(prefix):
                return text[len(prefix):].strip()
        return text
    
    def _clean_help_command(self, text):
        """Nettoie les commandes d'aide"""
        for prefix in self.command_prefixes['help']:
            if text.lower().startswith(prefix):
                return text[len(prefix):].strip()
        return text
    
    def get_os_type(self):
        """Retourne le type d'OS pour adapter les commandes"""
        return self.os_type
    
    def is_system_command(self, text):
        """Vérifie si le texte est une commande système"""
        command_type, _ = self.interpret(text)
        return command_type == CommandType.SYSTEM_COMMAND
    
    def is_chat_request(self, text):
        """Vérifie si le texte est une demande de chat IA"""
        command_type, _ = self.interpret(text)
        return command_type == CommandType.AI_CHAT