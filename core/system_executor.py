import subprocess
import platform
import os
from core.logger import app_logger

class SystemExecutor:
    """Exécuteur de commandes système avec gestion des privilèges"""
    
    @staticmethod
    def execute_command(command, elevated=False):
        """Exécute une commande système"""
        system = platform.system()
        
        try:
            if system == "Windows":
                return SystemExecutor._execute_windows(command, elevated)
            elif system == "Darwin":  # macOS
                return SystemExecutor._execute_macos(command, elevated)
            else:  # Linux
                return SystemExecutor._execute_linux(command, elevated)
        except Exception as e:
            app_logger.error(f"Erreur exécution commande: {e}", "SYSTEM_EXECUTOR")
            return f"Erreur: {str(e)}"
    
    @staticmethod
    def _execute_windows(command, elevated):
        """Exécution Windows avec UAC si nécessaire"""
        if elevated:
            # Commande avec élévation UAC
            cmd = f'powershell -Command "Start-Process cmd -ArgumentList \'/c {command}\' -Verb RunAs -Wait"'
        else:
            cmd = command
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Erreur Windows: {result.stderr}"
    
    @staticmethod
    def _execute_macos(command, elevated):
        """Exécution macOS avec sudo si nécessaire"""
        if elevated:
            cmd = f"osascript -e 'do shell script \"{command}\" with administrator privileges'"
        else:
            cmd = command
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Erreur macOS: {result.stderr}"
    
    @staticmethod
    def _execute_linux(command, elevated):
        """Exécution Linux avec sudo si nécessaire"""
        if elevated:
            # Vérifier si sudo est disponible
            if os.system("which sudo > /dev/null 2>&1") == 0:
                cmd = f"sudo {command}"
            else:
                return "Erreur: sudo non disponible"
        else:
            cmd = command
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Erreur Linux: {result.stderr}"
    
    @staticmethod
    def needs_elevation(command):
        """Détermine si une commande nécessite des privilèges élevés"""
        elevated_commands = [
            # Windows
            'net user', 'net localgroup', 'sc ', 'reg add', 'reg delete',
            'diskpart', 'format', 'chkdsk', 'sfc',
            # Linux/macOS
            'sudo', 'su ', 'mount', 'umount', 'fdisk', 'parted',
            'systemctl', 'service', 'iptables', 'ufw',
            # Communs
            'install', 'uninstall', 'chmod 777', 'chown root'
        ]
        
        command_lower = command.lower()
        return any(elevated_cmd in command_lower for elevated_cmd in elevated_commands)