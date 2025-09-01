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
        """Détecte le type de commande basé sur les préfixes et reconnaissance native"""
        text_lower = text.lower()
        
        # Vérifier les préfixes explicites système
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
        
        # NOUVELLE LOGIQUE: Reconnaissance native des commandes
        first_word = text.split()[0].lower() if text.split() else ""
        if self._is_native_system_command(first_word, text):
            return CommandType.SYSTEM_COMMAND
        
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
    
    def _is_native_system_command(self, first_word, full_text):
        """Vérifie si c'est une vraie commande système native"""
        if not first_word:
            return False
        
        # Commandes communes cross-platform
        common_commands = {
            'ls', 'dir', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'del',
            'cp', 'copy', 'mv', 'move', 'cat', 'type', 'grep', 'find',
            'ps', 'tasklist', 'kill', 'taskkill', 'top', 'ping',
            'curl', 'wget', 'git', 'npm', 'pip', 'python', 'node',
            'sudo', 'chmod', 'chown', 'tar', 'zip', 'unzip'
        }
        
        # Commandes spécifiques par OS
        if self.os_type == 'windows':
            windows_commands = {
                'systeminfo', 'ipconfig', 'netstat', 'nslookup',
                'tracert', 'ren', 'tree', 'attrib', 'fc', 'xcopy',
                'robocopy', 'sfc', 'dism', 'powershell', 'cmd'
            }
            common_commands.update(windows_commands)
        
        elif self.os_type == 'darwin':  # macOS
            mac_commands = {
                'brew', 'say', 'open', 'screencapture', 'pbcopy',
                'pbpaste', 'launchctl', 'sw_vers', 'system_profiler',
                'diskutil', 'hdiutil', 'ditto', 'plutil'
            }
            common_commands.update(mac_commands)
        
        else:  # Linux
            linux_commands = {
                'apt', 'yum', 'dnf', 'pacman', 'systemctl', 'service',
                'mount', 'umount', 'df', 'du', 'free', 'uname',
                'lsof', 'netstat', 'ss', 'iptables', 'crontab'
            }
            common_commands.update(linux_commands)
        
        # Vérifier si le premier mot est une commande reconnue
        if first_word in common_commands:
            # Vérifications additionnelles pour éviter les faux positifs
            return self._validate_command_context(full_text)
        
        return False
    
    def _validate_command_context(self, text):
        """Valide le contexte pour éviter les faux positifs"""
        # Éviter les questions qui contiennent des mots de commandes
        question_indicators = [
            'comment', 'pourquoi', 'qu\'est-ce', 'que fait', 'how to',
            'what is', 'why does', 'can you', 'peux-tu', 'pouvez-vous',
            '?', 'help me', 'aide-moi'
        ]
        
        text_lower = text.lower()
        for indicator in question_indicators:
            if indicator in text_lower:
                return False
        
        # Si le texte est très long (>50 chars), probablement une conversation
        if len(text) > 50 and not any(char in text for char in ['|', '>', '<', '&']):
            return False
        
        return True