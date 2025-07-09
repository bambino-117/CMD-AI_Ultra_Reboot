#!/usr/bin/env python3
"""
Système d'enregistrement et d'envoi automatique des tracebacks
Pour les testeurs avec PowerShell/CMD
"""

import os
import sys
import traceback
import json
import platform
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

class TracebackReporter:
    def __init__(self):
        self.reports_dir = Path("user/crash_reports")
        self.reports_dir.mkdir(exist_ok=True)
        self.system_info = self._get_system_info()
        
    def _get_system_info(self):
        """Collecte les informations système"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": sys.version,
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "timestamp": datetime.now().isoformat()
        }
    
    def capture_traceback(self, exc_type, exc_value, exc_traceback):
        """Capture et sauvegarde un traceback"""
        try:
            # Générer le rapport
            report = {
                "system_info": self.system_info,
                "error": {
                    "type": exc_type.__name__,
                    "message": str(exc_value),
                    "traceback": traceback.format_exception(exc_type, exc_value, exc_traceback)
                },
                "context": self._get_context_info()
            }
            
            # Sauvegarder localement
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = self.reports_dir / f"crash_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Tenter l'envoi automatique
            self._attempt_auto_send(report_file, report)
            
            return report_file
            
        except Exception as e:
            print(f"Erreur lors de la capture du traceback: {e}")
            return None
    
    def _get_context_info(self):
        """Collecte les informations de contexte"""
        context = {
            "working_directory": os.getcwd(),
            "command_line": sys.argv,
            "environment": {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
                "USER": os.environ.get("USER", os.environ.get("USERNAME", ""))
            }
        }
        
        # Ajouter les logs récents si disponibles
        try:
            log_file = Path("logs/app.log")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    context["recent_logs"] = lines[-20:]  # 20 dernières lignes
        except:
            pass
            
        return context
    
    def _attempt_auto_send(self, report_file, report_data):
        """Tente l'envoi automatique du rapport"""
        try:
            # Méthode 1: PowerShell (Windows)
            if platform.system() == "Windows":
                self._send_via_powershell(report_file, report_data)
            
            # Méthode 2: curl (Linux/macOS)
            else:
                self._send_via_curl(report_file, report_data)
                
        except Exception as e:
            print(f"Envoi automatique échoué: {e}")
    
    def _send_via_powershell(self, report_file, report_data):
        """Envoi via PowerShell (Windows)"""
        ps_script = f'''
$reportData = @{{
    system = "{report_data['system_info']['os']}"
    error_type = "{report_data['error']['type']}"
    error_message = "{report_data['error']['message']}"
    timestamp = "{report_data['system_info']['timestamp']}"
    report_file = "{report_file}"
}}

# Simuler l'envoi (remplacer par vraie URL)
$webhook = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
$body = $reportData | ConvertTo-Json

try {{
    # Invoke-RestMethod -Uri $webhook -Method Post -Body $body -ContentType "application/json"
    Write-Host "Rapport sauvegardé: {report_file}"
}} catch {{
    Write-Host "Envoi échoué, rapport local disponible"
}}
'''
        
        # Exécuter le script PowerShell
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
            f.write(ps_script)
            ps_file = f.name
        
        try:
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], 
                         capture_output=True, text=True, timeout=10)
        finally:
            os.unlink(ps_file)
    
    def _send_via_curl(self, report_file, report_data):
        """Envoi via curl (Linux/macOS)"""
        # Préparer les données pour curl
        curl_data = {
            "system": report_data['system_info']['os'],
            "error_type": report_data['error']['type'],
            "error_message": report_data['error']['message'],
            "timestamp": report_data['system_info']['timestamp'],
            "report_file": str(report_file)
        }
        
        # Commande curl (remplacer par vraie URL)
        curl_cmd = [
            "curl", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(curl_data),
            "https://your-webhook-url.com/crash-reports"
        ]
        
        try:
            subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            print("Timeout lors de l'envoi du rapport")
    
    def generate_user_report(self, report_file):
        """Génère un rapport lisible pour l'utilisateur"""
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            user_report = f"""
🚨 RAPPORT DE CRASH - CMD-AI Ultra Reboot

📅 Date: {report['system_info']['timestamp']}
💻 Système: {report['system_info']['os']} {report['system_info']['os_version']}
🐍 Python: {report['system_info']['python_version'].split()[0]}

❌ ERREUR:
Type: {report['error']['type']}
Message: {report['error']['message']}

📁 Rapport complet sauvegardé: {report_file}

🔧 ACTIONS RECOMMANDÉES:
1. Redémarrer l'application
2. Vérifier les logs dans logs/app.log
3. Signaler le problème si récurrent

📧 SUPPORT:
- GitHub Issues: https://github.com/bambino-117/CMD-AI_Ultra_Reboot/issues
- Email: support@cmd-ai.com

Ce rapport a été automatiquement généré et peut être envoyé
aux développeurs pour améliorer l'application.
"""
            
            # Sauvegarder le rapport utilisateur
            user_report_file = report_file.with_suffix('.txt')
            with open(user_report_file, 'w', encoding='utf-8') as f:
                f.write(user_report)
            
            return user_report, user_report_file
            
        except Exception as e:
            return f"Erreur génération rapport utilisateur: {e}", None
    
    def list_crash_reports(self):
        """Liste tous les rapports de crash"""
        reports = []
        for report_file in self.reports_dir.glob("crash_*.json"):
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                
                reports.append({
                    "file": report_file,
                    "timestamp": report['system_info']['timestamp'],
                    "error_type": report['error']['type'],
                    "error_message": report['error']['message'][:100] + "..."
                })
            except:
                continue
        
        return sorted(reports, key=lambda x: x['timestamp'], reverse=True)
    
    def cleanup_old_reports(self, days=30):
        """Nettoie les anciens rapports"""
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        
        for report_file in self.reports_dir.glob("crash_*"):
            if report_file.stat().st_mtime < cutoff:
                report_file.unlink()

# Instance globale
traceback_reporter = TracebackReporter()

def install_traceback_handler():
    """Installe le gestionnaire de traceback global"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        # Afficher l'erreur normalement
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        
        # Capturer et sauvegarder
        report_file = traceback_reporter.capture_traceback(exc_type, exc_value, exc_traceback)
        
        if report_file:
            user_report, user_file = traceback_reporter.generate_user_report(report_file)
            print(f"\n{'='*60}")
            print("🚨 CRASH DÉTECTÉ - RAPPORT AUTOMATIQUE GÉNÉRÉ")
            print(f"{'='*60}")
            print(user_report)
            print(f"{'='*60}")
    
    sys.excepthook = handle_exception

def manual_report_crash(error_description):
    """Permet de signaler manuellement un problème"""
    try:
        report = {
            "system_info": traceback_reporter.system_info,
            "error": {
                "type": "ManualReport",
                "message": error_description,
                "traceback": ["Rapport manuel utilisateur"]
            },
            "context": traceback_reporter._get_context_info()
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = traceback_reporter.reports_dir / f"manual_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return f"✅ Rapport manuel sauvegardé: {report_file}"
        
    except Exception as e:
        return f"❌ Erreur création rapport: {e}"