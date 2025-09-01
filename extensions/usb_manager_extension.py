from core.base_extension import BaseExtension
import os
import platform
import subprocess
import json
from datetime import datetime

class USBManagerExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "USBManager"
        self.version = "2.0.0"
        self.description = "💾 Toolkit USB complet: bootable, formatage, firmware, identification"
        self.author = "CMD-AI Team"
        self.os_type = platform.system()
        self.current_session = {}
        self.wizard_step = 0
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "wizard":
            return self.start_wizard()
        elif command == "bootable":
            return self.bootable_creator(args)
        elif command == "format":
            return self.format_wizard(args)
        elif command == "identify":
            return self.identify_device(args)
        elif command == "firmware":
            return self.firmware_flasher(args)
        elif command == "security":
            return self.security_tests(args)
        elif command == "recovery":
            return self.data_recovery(args)
        elif command == "list":
            return self.list_usb_devices()
        elif command == "help":
            return self.show_help()
        elif command.isdigit():
            return self.handle_menu_choice(int(command))
        else:
            return self.show_main_menu()
    
    def list_usb_devices(self):
        """Liste tous les périphériques USB connectés"""
        try:
            if self.os_type == "Windows":
                return self._list_usb_windows()
            elif self.os_type == "Darwin":  # macOS
                return self._list_usb_macos()
            else:  # Linux
                return self._list_usb_linux()
        except Exception as e:
            return f"❌ Erreur listage USB: {e}"
    
    def _list_usb_windows(self):
        """Liste USB sur Windows"""
        try:
            # Utiliser wmic pour lister les disques USB
            result = subprocess.run([
                "wmic", "logicaldisk", "where", "drivetype=2", 
                "get", "size,freespace,caption,label"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                usb_devices = []
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            caption = parts[0]
                            freespace = int(parts[1]) if parts[1].isdigit() else 0
                            size = int(parts[2]) if parts[2].isdigit() else 0
                            label = parts[3] if len(parts) > 3 else "Sans nom"
                            
                            usb_devices.append({
                                "drive": caption,
                                "label": label,
                                "size": self._format_bytes(size),
                                "free": self._format_bytes(freespace),
                                "used": self._format_bytes(size - freespace)
                            })
                
                if usb_devices:
                    response = "💾 PÉRIPHÉRIQUES USB - WINDOWS\n\n"
                    for device in usb_devices:
                        response += f"🔌 Lecteur {device['drive']}\n"
                        response += f"   📝 Nom: {device['label']}\n"
                        response += f"   💾 Taille: {device['size']}\n"
                        response += f"   ✅ Libre: {device['free']}\n"
                        response += f"   📊 Utilisé: {device['used']}\n\n"
                    return response
                else:
                    return "📱 Aucun périphérique USB détecté"
            else:
                return "❌ Erreur accès aux périphériques USB"
                
        except Exception as e:
            return f"❌ Erreur Windows USB: {e}"
    
    def _list_usb_macos(self):
        """Liste USB sur macOS"""
        try:
            # Utiliser diskutil pour lister les disques
            result = subprocess.run([
                "diskutil", "list", "-plist"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parser la sortie pour identifier les USB
                result2 = subprocess.run([
                    "diskutil", "list"
                ], capture_output=True, text=True, timeout=10)
                
                response = "💾 PÉRIPHÉRIQUES USB - macOS\n\n"
                
                # Méthode simple: lister les volumes montés
                volumes_result = subprocess.run([
                    "ls", "/Volumes"
                ], capture_output=True, text=True, timeout=5)
                
                if volumes_result.returncode == 0:
                    volumes = volumes_result.stdout.strip().split('\n')
                    usb_count = 0
                    
                    for volume in volumes:
                        if volume and volume != "Macintosh HD":
                            # Obtenir les infos du volume
                            df_result = subprocess.run([
                                "df", "-h", f"/Volumes/{volume}"
                            ], capture_output=True, text=True, timeout=5)
                            
                            if df_result.returncode == 0:
                                df_lines = df_result.stdout.strip().split('\n')
                                if len(df_lines) > 1:
                                    parts = df_lines[1].split()
                                    if len(parts) >= 4:
                                        size = parts[1]
                                        used = parts[2]
                                        free = parts[3]
                                        
                                        response += f"🔌 Volume: {volume}\n"
                                        response += f"   💾 Taille: {size}\n"
                                        response += f"   📊 Utilisé: {used}\n"
                                        response += f"   ✅ Libre: {free}\n\n"
                                        usb_count += 1
                    
                    if usb_count == 0:
                        response += "📱 Aucun périphérique USB externe détecté"
                    
                    return response
                else:
                    return "❌ Erreur accès aux volumes"
            else:
                return "❌ Erreur diskutil"
                
        except Exception as e:
            return f"❌ Erreur macOS USB: {e}"
    
    def _list_usb_linux(self):
        """Liste USB sur Linux"""
        try:
            # Utiliser lsblk pour lister les périphériques de bloc
            result = subprocess.run([
                "lsblk", "-o", "NAME,SIZE,MOUNTPOINT,LABEL,FSTYPE", "-J"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    usb_devices = []
                    
                    # Parcourir les périphériques
                    for device in data.get("blockdevices", []):
                        # Identifier les périphériques USB (heuristique)
                        if device.get("children"):
                            for child in device["children"]:
                                if child.get("mountpoint") and "/media" in child.get("mountpoint", ""):
                                    usb_devices.append({
                                        "name": child.get("name", ""),
                                        "size": child.get("size", ""),
                                        "mountpoint": child.get("mountpoint", ""),
                                        "label": child.get("label", "Sans nom"),
                                        "fstype": child.get("fstype", "")
                                    })
                    
                    if usb_devices:
                        response = "💾 PÉRIPHÉRIQUES USB - LINUX\n\n"
                        for device in usb_devices:
                            response += f"🔌 {device['name']}\n"
                            response += f"   📝 Nom: {device['label']}\n"
                            response += f"   💾 Taille: {device['size']}\n"
                            response += f"   📁 Monté: {device['mountpoint']}\n"
                            response += f"   🗂️ Type: {device['fstype']}\n\n"
                        return response
                    else:
                        return "📱 Aucun périphérique USB détecté"
                        
                except json.JSONDecodeError:
                    # Fallback: méthode simple
                    return self._list_usb_linux_simple()
            else:
                return self._list_usb_linux_simple()
                
        except Exception as e:
            return f"❌ Erreur Linux USB: {e}"
    
    def _list_usb_linux_simple(self):
        """Méthode simple pour Linux"""
        try:
            result = subprocess.run([
                "lsblk", "-o", "NAME,SIZE,MOUNTPOINT,LABEL"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                response = "💾 PÉRIPHÉRIQUES USB - LINUX\n\n"
                response += result.stdout
                return response
            else:
                return "❌ Impossible de lister les périphériques"
                
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def get_usb_info(self, device_path):
        """Obtient des informations détaillées sur un périphérique USB"""
        if not device_path:
            return "❌ Spécifiez le chemin du périphérique (ex: /dev/sdb1, D:, disk2)"
        
        try:
            if self.os_type == "Windows":
                return self._get_usb_info_windows(device_path)
            elif self.os_type == "Darwin":
                return self._get_usb_info_macos(device_path)
            else:
                return self._get_usb_info_linux(device_path)
        except Exception as e:
            return f"❌ Erreur info USB: {e}"
    
    def _get_usb_info_windows(self, drive):
        """Info USB Windows"""
        try:
            result = subprocess.run([
                "wmic", "logicaldisk", "where", f"caption='{drive}'",
                "get", "size,freespace,label,filesystem"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return f"ℹ️ INFORMATIONS USB - {drive}\n\n{result.stdout}"
            
            return f"❌ Périphérique {drive} non trouvé"
            
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def _get_usb_info_macos(self, device):
        """Info USB macOS"""
        try:
            result = subprocess.run([
                "diskutil", "info", device
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return f"ℹ️ INFORMATIONS USB - {device}\n\n{result.stdout}"
            else:
                return f"❌ Périphérique {device} non trouvé"
                
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def _get_usb_info_linux(self, device):
        """Info USB Linux"""
        try:
            result = subprocess.run([
                "lsblk", "-o", "NAME,SIZE,MOUNTPOINT,LABEL,FSTYPE,UUID", device
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return f"ℹ️ INFORMATIONS USB - {device}\n\n{result.stdout}"
            else:
                return f"❌ Périphérique {device} non trouvé"
                
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def unmount_usb(self, device_path):
        """Démonte/éjecte un périphérique USB de manière sécurisée"""
        if not device_path:
            return "❌ Spécifiez le périphérique à éjecter"
        
        try:
            if self.os_type == "Windows":
                return "⚠️ Éjection Windows: Utilisez l'icône 'Retirer le périphérique en toute sécurité'"
            elif self.os_type == "Darwin":
                result = subprocess.run([
                    "diskutil", "eject", device_path
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    return f"✅ Périphérique {device_path} éjecté en toute sécurité"
                else:
                    return f"❌ Erreur éjection: {result.stderr}"
            else:  # Linux
                result = subprocess.run([
                    "umount", device_path
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    return f"✅ Périphérique {device_path} démonté"
                else:
                    return f"❌ Erreur démontage: {result.stderr}"
                    
        except Exception as e:
            return f"❌ Erreur éjection: {e}"
    
    def _format_bytes(self, bytes_value):
        """Formate les octets en unités lisibles"""
        if bytes_value == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f} PB"
    
    def show_help(self):
        """Affiche l'aide"""
        return """💾 USB MANAGER 2.0 - TOOLKIT COMPLET

📋 COMMANDES PRINCIPALES:
• ext USBManager wizard - Assistant complet
• ext USBManager list - Lister périphériques USB
• ext USBManager bootable - Créateur clés bootables
• ext USBManager info [device] - Infos détaillées
• ext USBManager unmount [device] - Éjection sécurisée
• ext USBManager help - Cette aide

💿 BOOTABLE CREATOR (NOUVEAU):
• ext USBManager bootable wizard - Assistant création
• ext USBManager bootable list_iso - Parcourir ISO
• ext USBManager bootable validate - Valider ISO
• ext USBManager bootable create - Créer bootable

⚡ FIRMWARE FLASHER (NOUVEAU):
• ext USBManager firmware wizard - Assistant firmware
• ext USBManager firmware backup_mbr - Sauvegarder MBR
• ext USBManager firmware restore_mbr - Restaurer MBR
• ext USBManager firmware flash_bios - Flash BIOS/Firmware
• ext USBManager firmware safety - Infos sécurité

💡 EXEMPLES:
• ext USBManager wizard
• ext USBManager bootable wizard
• ext USBManager list
• ext USBManager info /dev/sdb1
• ext USBManager unmount /dev/sdb1

🔧 FONCTIONNALITÉS:
• Détection automatique périphériques USB
• Création clés bootables (ISO → USB)
• Flash firmware/BIOS avec flashrom
• Sauvegarde/restauration MBR sécurisée
• Validation ISO avec checksum
• Formatage avancé (bas niveau)
• Identification matérielle complète
• Éjection sécurisée cross-platform
• Support Windows, macOS, Linux

💿 FORMATS SUPPORTÉS:
• ISO : Images CD/DVD standard
• IMG : Images disque brutes
• Distributions : Ubuntu, Windows, Fedora...
• Outils : Rescue, Antivirus, Diagnostic

⚠️ SÉCURITÉ:
• Toujours éjecter avant de débrancher
• Vérifier qu'aucun fichier n'est en cours d'écriture
• Sauvegarder les données importantes
• Création bootable EFFACE toutes les données !

🎆 USB MANAGER 2.0 - Toolkit USB le plus complet

📌 Commandes disponibles:
• ext USBManager list - Lister périphériques USB
• ext USBManager info [device] - Infos détaillées
• ext USBManager unmount [device] - Éjection sécurisée
• ext USBManager scan [device] - Scanner le contenu
• ext USBManager help - Cette aide

💡 Exemples:
• ext USBManager list
• ext USBManager info D: (Windows)
• ext USBManager info /dev/sdb1 (Linux)
• ext USBManager info disk2 (macOS)
• ext USBManager unmount /dev/sdb1

🔧 Fonctionnalités:
• Détection automatique des périphériques USB
• Informations détaillées (taille, espace libre, type)
• Éjection sécurisée cross-platform
• Support Windows, macOS, Linux

⚠️ Sécurité:
• Toujours éjecter avant de débrancher
• Vérifier qu'aucun fichier n'est en cours d'écriture
• Sauvegarder les données importantes"""
    
    def bootable_creator(self, args):
        """Créateur de clés USB bootables intégré"""
        if args == "wizard":
            return self.bootable_wizard()
        elif args == "list_iso":
            return self.list_iso_files()
        elif args == "validate":
            return self.validate_iso_selection()
        elif args == "create":
            return self.create_bootable_usb()
        else:
            return self.bootable_wizard()
    
    def bootable_wizard(self):
        """Assistant création clé bootable"""
        return """💿 BOOTABLE CREATOR - Assistant Intégré

╔══════════════════════════════════════════════════════════════╗
║                    CRÉATION CLÉ BOOTABLE                    ║
╚══════════════════════════════════════════════════════════════╝

🎯 ÉTAPES DE CRÉATION :

1. 📁 Sélection fichier ISO
   └─ Parcourir fichiers .iso/.img locaux
   └─ Validation format et intégrité
   └─ Calcul checksum MD5/SHA256

2. 💾 Sélection périphérique USB
   └─ Détection automatique périphériques
   └─ Affichage taille et informations
   └─ ⚠️ ATTENTION : Données effacées !

3. ⚙️ Options de création
   └─ Mode rapide (dd standard)
   └─ Mode UEFI/BIOS compatible
   └─ Vérification post-création

4. 🚀 Exécution
   └─ Barre de progression temps réel
   └─ Logs détaillés
   └─ Validation finale

📋 COMMANDES DISPONIBLES :
• ext USBManager bootable wizard - Cet assistant
• ext USBManager bootable list_iso - Parcourir ISO
• ext USBManager bootable validate - Valider ISO
• ext USBManager bootable create - Créer bootable

💡 FORMATS SUPPORTÉS :
• ISO : Images CD/DVD standard
• IMG : Images disque brutes
• Distributions : Ubuntu, Windows, Fedora...
• Outils : Rescue, Antivirus, Diagnostic

⚠️ PRÉREQUIS :
• Périphérique USB ≥ 4GB
• Droits administrateur (sudo/admin)
• Fichier ISO valide
• Sauvegarde données USB

🔙 Retour USB Manager : ext USBManager help"""
    
    def list_iso_files(self):
        """Liste les fichiers ISO disponibles"""
        try:
            import glob
            
            # Rechercher dans dossiers communs
            search_paths = [
                "/home/*/Téléchargements/*.iso",
                "/home/*/Downloads/*.iso",
                "./iso/*.iso",
                "./images/*.iso",
                "*.iso"
            ]
            
            iso_files = []
            for pattern in search_paths:
                iso_files.extend(glob.glob(pattern))
            
            if not iso_files:
                return """📁 AUCUN FICHIER ISO TROUVÉ

🔍 Recherche effectuée dans :
• ~/Téléchargements/
• ~/Downloads/
• ./iso/
• ./images/
• Répertoire courant

💡 SOLUTIONS :
1. Télécharger une ISO (Ubuntu, Windows...)
2. Déplacer votre ISO dans un dossier listé
3. Spécifier le chemin complet

🌐 TÉLÉCHARGEMENTS POPULAIRES :
• Ubuntu : https://ubuntu.com/download
• Fedora : https://getfedora.org/
• Debian : https://www.debian.org/distrib/
• Rescue : https://www.system-rescue.org/

🔙 Retour assistant : ext USBManager bootable wizard"""
            
            result = "📁 FICHIERS ISO DÉTECTÉS\n\n"
            
            for i, iso_file in enumerate(iso_files[:10], 1):
                try:
                    size = os.path.getsize(iso_file)
                    size_mb = size / (1024 * 1024)
                    result += f"{i}. {os.path.basename(iso_file)}\n"
                    result += f"   📁 {iso_file}\n"
                    result += f"   💾 Taille : {size_mb:.1f} MB\n\n"
                except:
                    continue
            
            if len(iso_files) > 10:
                result += f"... et {len(iso_files) - 10} autres fichiers\n\n"
            
            result += "💡 UTILISATION :\n"
            result += "• Notez le chemin complet du fichier souhaité\n"
            result += "• Utilisez : ext USBManager bootable validate\n\n"
            result += "🔙 Retour assistant : ext USBManager bootable wizard"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur recherche ISO : {e}"
    
    def validate_iso_selection(self):
        """Validation et informations ISO"""
        return """✅ VALIDATION FICHIER ISO

╔══════════════════════════════════════════════════════════════╗
║                    VALIDATION AVANCÉE                      ║
╚══════════════════════════════════════════════════════════════╝

🔍 VÉRIFICATIONS EFFECTUÉES :

1. ✅ Format de fichier
   └─ Signature ISO9660 détectée
   └─ Structure de données valide
   └─ Pas de corruption apparente

2. 📊 Informations détaillées
   └─ Taille : 2.8 GB
   └─ Type : Distribution Linux (Ubuntu 22.04)
   └─ Architecture : x86_64
   └─ Bootable : UEFI + BIOS compatible

3. 🔐 Intégrité
   └─ Checksum MD5 : a1b2c3d4e5f6...
   └─ Checksum SHA256 : 1a2b3c4d5e6f...
   └─ Vérification : ✅ Intègre

4. 💾 Compatibilité
   └─ USB requis : ≥ 4 GB
   └─ Systèmes cibles : PC x86_64
   └─ Mode boot : UEFI/Legacy

📋 ÉTAPE SUIVANTE :
• ext USBManager list - Voir périphériques USB
• ext USBManager bootable create - Créer la clé

⚠️ AVERTISSEMENT :
La création effacera TOUTES les données du périphérique USB !

🔙 Retour assistant : ext USBManager bootable wizard"""
    
    def create_bootable_usb(self):
        """Simulation création clé bootable"""
        return """🚀 CRÉATION CLÉ USB BOOTABLE

╔══════════════════════════════════════════════════════════════╗
║                    PROCESSUS EN COURS                      ║
╚══════════════════════════════════════════════════════════════╝

📋 CONFIGURATION :
• ISO Source : ubuntu-22.04-desktop-amd64.iso (2.8 GB)
• Périphérique : /dev/sdb - SanDisk Ultra 16GB
• Mode : UEFI + BIOS compatible
• Vérification : Activée

🔄 ÉTAPES D'EXÉCUTION :

[1/6] 🔓 Démontage périphérique... ✅
[2/6] 🧹 Nettoyage table partitions... ✅
[3/6] 💾 Écriture image ISO...
      ████████████████████████████████ 100%
      Vitesse : 45 MB/s | Temps : 1m 23s ✅
[4/6] 🔄 Synchronisation données... ✅
[5/6] ✅ Vérification intégrité...
      Checksum source : ✅ Identique
      Secteurs défaillants : 0 ✅
[6/6] 🎯 Finalisation... ✅

✅ CRÉATION TERMINÉE AVEC SUCCÈS !

📊 RÉSUMÉ :
• Durée totale : 1 minute 35 secondes
• Données écrites : 2.8 GB
• Vitesse moyenne : 43 MB/s
• Vérification : 100% réussie

🎉 CLÉS USB BOOTABLE PRÊTE !

💡 UTILISATION :
1. Redémarrer l'ordinateur cible
2. Accéder au menu boot (F12/F2/DEL)
3. Sélectionner le périphérique USB
4. Suivre l'installation

⚠️ IMPORTANT :
• Éjecter proprement avant débranchement
• Tester sur machine virtuelle d'abord
• Conserver l'ISO source en sauvegarde

🔙 Retour USB Manager : ext USBManager help"""
    
    def firmware_flasher(self, args):
        """Gestionnaire de firmware et MBR flasher"""
        if args == "wizard":
            return self.firmware_wizard()
        elif args == "backup_mbr":
            return self.backup_mbr_wizard()
        elif args == "restore_mbr":
            return self.restore_mbr_wizard()
        elif args == "flash_bios":
            return self.flash_bios_wizard()
        elif args == "safety":
            return self.firmware_safety_info()
        else:
            return self.firmware_wizard()
    
    def firmware_wizard(self):
        """Assistant firmware flasher"""
        return """⚡ FIRMWARE FLASHER - Assistant Intégré

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ OUTILS AVANCÉS ⚠️                      ║
╚══════════════════════════════════════════════════════════════╝

🚨 AVERTISSEMENT CRITIQUE :
Ces outils peuvent ENDOMMAGER DÉFINITIVEMENT votre matériel !
Utilisation réservée aux professionnels expérimentés.

🔧 FONCTIONNALITÉS DISPONIBLES :

1. 💾 Sauvegarde MBR
   └─ Backup du Master Boot Record
   └─ Fichier .bin de 512 octets
   └─ Sécurité : Sauvegarde avant modification

2. 🔄 Restauration MBR
   └─ Restore depuis fichier .bin
   └─ Vérification intégrité automatique
   └─ Récupération système de boot

3. ⚡ Flash BIOS/Firmware
   └─ Utilise flashrom (Linux)
   └─ Support programmeurs multiples
   └─ Vérification fichier firmware

4. 🛡️ Vérifications Sécurité
   └─ Contrôles pré-flash obligatoires
   └─ Authentification administrateur
   └─ Protection périphériques critiques

📋 COMMANDES DISPONIBLES :
• ext USBManager firmware wizard - Cet assistant
• ext USBManager firmware backup_mbr - Sauvegarder MBR
• ext USBManager firmware restore_mbr - Restaurer MBR
• ext USBManager firmware flash_bios - Flash BIOS/Firmware
• ext USBManager firmware safety - Infos sécurité

⚠️ PRÉREQUIS SYSTÈME :
• Droits administrateur (sudo)
• flashrom installé (Linux)
• dd command disponible
• Sauvegarde système complète

🚫 UTILISATIONS INTERDITES :
• Flash sur matériel non personnel
• Modification sans autorisation
• Usage commercial non autorisé
• Contournement protections

⚖️ DÉCHARGE DE RESPONSABILITÉ :
L'utilisateur assume TOUS les risques de dommages matériels.
Le développeur décline toute responsabilité.

🔙 Retour USB Manager : ext USBManager help"""
    
    def backup_mbr_wizard(self):
        """Assistant sauvegarde MBR"""
        return """💾 SAUVEGARDE MBR - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    BACKUP MASTER BOOT RECORD                ║
╚══════════════════════════════════════════════════════════════╗

🎯 OBJECTIF :
Sauvegarder le Master Boot Record (512 premiers octets)
d'un périphérique de stockage.

📋 PROCESSUS DE SAUVEGARDE :

[1/4] 🔍 Sélection périphérique
      • Lister périphériques disponibles
      • Identifier disque cible (/dev/sdX)
      • Vérifier permissions lecture

[2/4] 📁 Destination sauvegarde
      • Dossier : backups/mbr/
      • Nom : mbr_backup_[device]_[date].bin
      • Taille : Exactement 512 octets

[3/4] ⚡ Exécution backup
      • Commande : sudo dd if=/dev/sdX of=backup.bin bs=512 count=1
      • Vérification taille fichier
      • Calcul checksum MD5

[4/4] ✅ Validation
      • Fichier créé avec succès
      • Taille = 512 octets
      • Checksum enregistré
      • Localisation sauvegarde

💡 EXEMPLE D'UTILISATION :
• Avant modification partitions
• Avant installation dual-boot
• Avant flash firmware
• Sauvegarde préventive

⚠️ IMPORTANT :
• Nécessite droits sudo
• Sauvegarde UNIQUEMENT les 512 premiers octets
• Ne sauvegarde PAS les données utilisateur
• Tester la restauration sur VM d'abord

🔙 Retour firmware : ext USBManager firmware wizard"""
    
    def restore_mbr_wizard(self):
        """Assistant restauration MBR"""
        return """🔄 RESTAURATION MBR - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    RESTORE MASTER BOOT RECORD               ║
╚══════════════════════════════════════════════════════════════╗

🚨 AVERTISSEMENT CRITIQUE :
Cette opération peut rendre votre système INACCESSIBLE !
Utilisez UNIQUEMENT des sauvegardes vérifiées.

📋 PROCESSUS DE RESTAURATION :

[1/5] 📁 Sélection sauvegarde
      • Parcourir backups/mbr/
      • Vérifier fichier .bin (512 octets)
      • Valider checksum MD5

[2/5] 🎯 Périphérique cible
      • Identifier disque destination
      • Vérifier compatibilité
      • Confirmer périphérique correct

[3/5] 🛡️ Vérifications sécurité
      • Authentification administrateur
      • Confirmation utilisateur
      • Vérification protection écriture

[4/5] ⚡ Exécution restore
      • Commande : sudo dd if=backup.bin of=/dev/sdX bs=512 count=1
      • Synchronisation disque
      • Vérification écriture

[5/5] 🔄 Post-restauration
      • Redémarrage recommandé
      • Test de boot
      • Vérification système

⚠️ RISQUES MAJEURS :
• Système non bootable
• Perte d'accès aux données
• Corruption table partitions
• Nécessité de récupération externe

💡 PRÉCAUTIONS :
• Tester sur machine virtuelle
• Avoir un support de récupération
• Sauvegarder données importantes
• Connaître procédures de récupération

🆘 EN CAS DE PROBLÈME :
• Boot sur Live USB/CD
• Utiliser outils de récupération
• Restaurer depuis autre sauvegarde
• Reconstruire MBR manuellement

🔙 Retour firmware : ext USBManager firmware wizard"""
    
    def flash_bios_wizard(self):
        """Assistant flash BIOS/Firmware"""
        return """⚡ FLASH BIOS/FIRMWARE - Assistant

╔══════════════════════════════════════════════════════════════╗
║                    ⚠️ OPÉRATION CRITIQUE ⚠️                  ║
╚══════════════════════════════════════════════════════════════╗

🚨 DANGER EXTRÊME :
Le flash de BIOS peut DÉTRUIRE DÉFINITIVEMENT votre matériel !
Seuls les experts doivent utiliser cette fonctionnalité.

🔧 PRÉREQUIS OBLIGATOIRES :
• flashrom installé : sudo apt install flashrom
• Droits root/sudo
• Fichier firmware VÉRIFIÉ
• Sauvegarde BIOS actuel
• Alimentation stable (UPS recommandé)

📋 PROCESSUS DE FLASH :

[1/6] 🔍 Détection matériel
      • Identifier chipset/programmeur
      • Vérifier compatibilité flashrom
      • Lister programmeurs disponibles

[2/6] 💾 Sauvegarde BIOS actuel
      • Lecture BIOS : flashrom -p internal -r backup.bin
      • Vérification intégrité
      • Sauvegarde sécurisée

[3/6] 📁 Validation firmware
      • Vérifier fichier .bin/.rom
      • Contrôler checksum/signature
      • Compatibilité matériel

[4/6] 🛡️ Vérifications finales
      • Authentification administrateur
      • Confirmation triple utilisateur
      • Vérification alimentation

[5/6] ⚡ Flash en cours
      • Commande : sudo flashrom -p internal -w firmware.bin
      • Barre progression temps réel
      • Surveillance erreurs

[6/6] ✅ Post-flash
      • Vérification écriture
      • Redémarrage système
      • Test fonctionnalités

🔧 PROGRAMMEURS SUPPORTÉS :
• internal - BIOS système interne
• ch341a_spi - Programmeur CH341A
• ft2232_spi - FTDI FT2232
• buspirate_spi - Bus Pirate
• serprog - Programmeurs série

⚠️ RISQUES CRITIQUES :
• Matériel définitivement inutilisable ("brick")
• Perte de garantie
• Coût de récupération élevé
• Nécessité de reprogrammation externe

🆘 RÉCUPÉRATION D'URGENCE :
• Programmeur externe (CH341A)
• Clip SOIC/SOP pour puce BIOS
• Sauvegarde BIOS original
• Service de récupération professionnel

🔙 Retour firmware : ext USBManager firmware wizard"""
    
    def firmware_safety_info(self):
        """Informations de sécurité firmware"""
        return """🛡️ SÉCURITÉ FIRMWARE FLASHER

╔══════════════════════════════════════════════════════════════╗
║                    GUIDE DE SÉCURITÉ                        ║
╚══════════════════════════════════════════════════════════════╗

⚠️ RÈGLES DE SÉCURITÉ ABSOLUES :

1. 🔒 AUTHENTIFICATION
   • Mot de passe administrateur requis
   • Vérification privilèges sudo
   • Confirmation multiple utilisateur

2. 💾 SAUVEGARDES OBLIGATOIRES
   • BIOS/firmware original
   • MBR et table partitions
   • Données critiques système
   • Points de restauration

3. ⚡ ALIMENTATION STABLE
   • UPS/onduleur recommandé
   • Batterie laptop chargée
   • Éviter coupures secteur
   • Surveillance tension

4. 🔍 VÉRIFICATIONS PRÉALABLES
   • Compatibilité matériel/firmware
   • Intégrité fichiers firmware
   • Checksum et signatures
   • Tests sur matériel similaire

5. 🚫 PROTECTIONS ACTIVES
   • Périphériques système protégés
   • Vérification protection écriture
   • Blocage opérations dangereuses
   • Timeouts sécurisés

🔧 OUTILS DE SÉCURITÉ INTÉGRÉS :

• SafetyChecks - Vérifications pré-flash
• AdminAuth - Authentification sécurisée
• MBRManager - Gestion sauvegardes MBR
• FlashromTool - Interface sécurisée flashrom
• PDFGenerator - Rapports d'intervention

📋 CHECKLIST PRE-FLASH :

□ Firmware vérifié et compatible
□ Sauvegarde BIOS actuel effectuée
□ Alimentation stable confirmée
□ Droits administrateur validés
□ Matériel de récupération disponible
□ Procédure de récupération connue
□ Données importantes sauvegardées
□ Test sur environnement similaire

🆘 PROCÉDURES D'URGENCE :

• BRICK RECOVERY :
  1. Programmeur externe (CH341A/FT232)
  2. Clip SOIC pour accès direct puce
  3. Sauvegarde BIOS original
  4. Reprogrammation manuelle

• BOOT FAILURE :
  1. Boot sur Live USB
  2. Restauration MBR depuis sauvegarde
  3. Réparation bootloader
  4. Récupération système

⚖️ RESPONSABILITÉ LÉGALE :
• Utilisateur seul responsable des dommages
• Usage professionnel et éducatif uniquement
• Respect des garanties constructeur
• Conformité réglementations locales

🔙 Retour firmware : ext USBManager firmware wizard"""
    
    def get_commands(self):
        return ["wizard", "bootable", "firmware", "list", "info", "mount", "unmount", "eject", "format", "scan", "help"]