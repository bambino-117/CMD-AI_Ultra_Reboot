#!/usr/bin/env python3
"""
Script d'installation du système de traceback pour testeurs
Installe un gestionnaire temporaire dans terminal/PowerShell/CMD
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def create_windows_traceback_script():
    """Crée le script PowerShell pour Windows"""
    ps_script = '''
# Script de traceback temporaire pour CMD-AI Ultra Reboot
# Version testeurs - Capture automatique des erreurs

$ErrorActionPreference = "Continue"
$TracebackDir = "$env:TEMP\\cmdai_tracebacks"

# Créer le dossier de tracebacks
if (!(Test-Path $TracebackDir)) {
    New-Item -ItemType Directory -Path $TracebackDir -Force
}

# Fonction de capture d'erreur
function Capture-CMDAIError {
    param(
        [string]$ErrorMessage,
        [string]$ErrorType = "PowerShell",
        [string]$Context = "Manual"
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $ReportFile = "$TracebackDir\\traceback_$Timestamp.json"
    
    $Report = @{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        system = @{
            os = "Windows"
            version = [System.Environment]::OSVersion.VersionString
            powershell = $PSVersionTable.PSVersion.ToString()
            user = $env:USERNAME
        }
        error = @{
            type = $ErrorType
            message = $ErrorMessage
            context = $Context
            command_line = $MyInvocation.Line
        }
        environment = @{
            path = $env:PATH
            temp = $env:TEMP
            working_dir = (Get-Location).Path
        }
    }
    
    $Report | ConvertTo-Json -Depth 3 | Out-File -FilePath $ReportFile -Encoding UTF8
    
    Write-Host "🚨 ERREUR CAPTURÉE - Rapport sauvé: $ReportFile" -ForegroundColor Red
    Write-Host "📧 Envoyez ce fichier aux développeurs CMD-AI" -ForegroundColor Yellow
    
    return $ReportFile
}

# Fonction de test CMD-AI
function Test-CMDAI {
    param([string]$Command = "")
    
    try {
        if ($Command -eq "") {
            Write-Host "🤖 CMD-AI Ultra Reboot - Mode Test Traceback" -ForegroundColor Cyan
            Write-Host "Tapez 'help' pour l'aide ou une commande CMD-AI" -ForegroundColor Green
            return
        }
        
        # Simuler l'exécution de CMD-AI
        $CMDAIPath = Get-ChildItem -Path "." -Name "main.py" -Recurse | Select-Object -First 1
        
        if ($CMDAIPath) {
            Write-Host "🔄 Exécution: python $CMDAIPath" -ForegroundColor Yellow
            python $CMDAIPath
        } else {
            Write-Host "❌ main.py non trouvé dans le répertoire courant" -ForegroundColor Red
            Capture-CMDAIError -ErrorMessage "main.py non trouvé" -ErrorType "FileNotFound" -Context "Test-CMDAI"
        }
    }
    catch {
        $ErrorMsg = $_.Exception.Message
        Write-Host "❌ ERREUR: $ErrorMsg" -ForegroundColor Red
        Capture-CMDAIError -ErrorMessage $ErrorMsg -ErrorType "Exception" -Context "Test-CMDAI"
    }
}

# Fonction de rapport manuel
function Report-CMDAIIssue {
    param([string]$Description)
    
    if ($Description -eq "") {
        Write-Host "Usage: Report-CMDAIIssue 'Description du problème'" -ForegroundColor Yellow
        return
    }
    
    $ReportFile = Capture-CMDAIError -ErrorMessage $Description -ErrorType "ManualReport" -Context "UserReport"
    Write-Host "✅ Rapport créé: $ReportFile" -ForegroundColor Green
}

# Fonction de nettoyage
function Clear-CMDAITracebacks {
    if (Test-Path $TracebackDir) {
        Remove-Item "$TracebackDir\\*" -Force
        Write-Host "🧹 Tracebacks nettoyés" -ForegroundColor Green
    }
}

# Fonction d'envoi (simulation)
function Send-CMDAITracebacks {
    $Reports = Get-ChildItem -Path $TracebackDir -Filter "*.json"
    
    if ($Reports.Count -eq 0) {
        Write-Host "📋 Aucun rapport à envoyer" -ForegroundColor Yellow
        return
    }
    
    Write-Host "📤 Simulation envoi de $($Reports.Count) rapports..." -ForegroundColor Cyan
    Write-Host "✅ Rapports 'envoyés' (simulation)" -ForegroundColor Green
    Write-Host "📁 Rapports conservés dans: $TracebackDir" -ForegroundColor Blue
}

# Messages d'aide
function Show-CMDAIHelp {
    Write-Host @"
🤖 CMD-AI ULTRA REBOOT - TESTEUR TRACEBACK

COMMANDES DISPONIBLES:
• Test-CMDAI [commande]     - Tester CMD-AI avec capture d'erreur
• Report-CMDAIIssue "desc"  - Signaler un problème manuellement  
• Send-CMDAITracebacks      - Envoyer les rapports (simulation)
• Clear-CMDAITracebacks     - Nettoyer les anciens rapports
• Show-CMDAIHelp           - Afficher cette aide

EXEMPLES:
Test-CMDAI "ext Weather current Paris"
Report-CMDAIIssue "Interface se fige au démarrage"
Send-CMDAITracebacks

📁 RAPPORTS: $TracebackDir
"@ -ForegroundColor Cyan
}

# Initialisation
Write-Host "🚀 Système de traceback CMD-AI installé!" -ForegroundColor Green
Write-Host "Tapez 'Show-CMDAIHelp' pour voir les commandes disponibles" -ForegroundColor Yellow

# Aliases pour faciliter l'usage
Set-Alias -Name cmdai -Value Test-CMDAI
Set-Alias -Name cmdai-report -Value Report-CMDAIIssue
Set-Alias -Name cmdai-send -Value Send-CMDAITracebacks
Set-Alias -Name cmdai-help -Value Show-CMDAIHelp
'''
    
    return ps_script

def create_bash_traceback_script():
    """Crée le script Bash pour Linux/macOS"""
    bash_script = '''#!/bin/bash
# Script de traceback temporaire pour CMD-AI Ultra Reboot
# Version testeurs - Capture automatique des erreurs

TRACEBACK_DIR="$HOME/.cmdai_tracebacks"
mkdir -p "$TRACEBACK_DIR"

# Fonction de capture d'erreur
capture_cmdai_error() {
    local error_message="$1"
    local error_type="${2:-Bash}"
    local context="${3:-Manual}"
    
    local timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    local report_file="$TRACEBACK_DIR/traceback_$timestamp.json"
    
    cat > "$report_file" << EOF
{
    "timestamp": "$(date '+%Y-%m-%d %H:%M:%S')",
    "system": {
        "os": "$(uname -s)",
        "version": "$(uname -r)",
        "shell": "$SHELL",
        "user": "$USER"
    },
    "error": {
        "type": "$error_type",
        "message": "$error_message",
        "context": "$context",
        "command_line": "$0 $*"
    },
    "environment": {
        "path": "$PATH",
        "home": "$HOME",
        "working_dir": "$(pwd)"
    }
}
EOF
    
    echo "🚨 ERREUR CAPTURÉE - Rapport sauvé: $report_file"
    echo "📧 Envoyez ce fichier aux développeurs CMD-AI"
    
    echo "$report_file"
}

# Fonction de test CMD-AI
test_cmdai() {
    local command="$1"
    
    if [ -z "$command" ]; then
        echo "🤖 CMD-AI Ultra Reboot - Mode Test Traceback"
        echo "Usage: test_cmdai 'commande' ou cmdai 'commande'"
        return
    fi
    
    local main_py=$(find . -name "main.py" -type f | head -1)
    
    if [ -n "$main_py" ]; then
        echo "🔄 Exécution: python $main_py"
        python "$main_py" || {
            capture_cmdai_error "Erreur exécution main.py" "PythonError" "test_cmdai"
        }
    else
        echo "❌ main.py non trouvé dans le répertoire courant"
        capture_cmdai_error "main.py non trouvé" "FileNotFound" "test_cmdai"
    fi
}

# Fonction de rapport manuel
report_cmdai_issue() {
    local description="$1"
    
    if [ -z "$description" ]; then
        echo "Usage: report_cmdai_issue 'Description du problème'"
        return
    fi
    
    local report_file=$(capture_cmdai_error "$description" "ManualReport" "UserReport")
    echo "✅ Rapport créé: $report_file"
}

# Fonction de nettoyage
clear_cmdai_tracebacks() {
    rm -f "$TRACEBACK_DIR"/*.json 2>/dev/null
    echo "🧹 Tracebacks nettoyés"
}

# Fonction d'envoi (simulation)
send_cmdai_tracebacks() {
    local report_count=$(ls "$TRACEBACK_DIR"/*.json 2>/dev/null | wc -l)
    
    if [ "$report_count" -eq 0 ]; then
        echo "📋 Aucun rapport à envoyer"
        return
    fi
    
    echo "📤 Simulation envoi de $report_count rapports..."
    echo "✅ Rapports 'envoyés' (simulation)"
    echo "📁 Rapports conservés dans: $TRACEBACK_DIR"
}

# Fonction d'aide
show_cmdai_help() {
    cat << 'EOF'
🤖 CMD-AI ULTRA REBOOT - TESTEUR TRACEBACK

COMMANDES DISPONIBLES:
• test_cmdai "commande"        - Tester CMD-AI avec capture d'erreur
• cmdai "commande"             - Alias pour test_cmdai
• report_cmdai_issue "desc"    - Signaler un problème manuellement
• send_cmdai_tracebacks        - Envoyer les rapports (simulation)
• clear_cmdai_tracebacks       - Nettoyer les anciens rapports
• show_cmdai_help             - Afficher cette aide

EXEMPLES:
cmdai "ext Weather current Paris"
report_cmdai_issue "Interface se fige au démarrage"
send_cmdai_tracebacks

📁 RAPPORTS: ~/.cmdai_tracebacks
EOF
}

# Aliases
alias cmdai='test_cmdai'
alias cmdai-report='report_cmdai_issue'
alias cmdai-send='send_cmdai_tracebacks'
alias cmdai-help='show_cmdai_help'

echo "🚀 Système de traceback CMD-AI installé!"
echo "Tapez 'show_cmdai_help' pour voir les commandes disponibles"
'''
    
    return bash_script

def install_traceback_system():
    """Installe le système de traceback selon l'OS"""
    system = platform.system()
    
    print("🔧 Installation du système de traceback pour testeurs...")
    
    if system == "Windows":
        # Script PowerShell
        ps_script = create_windows_traceback_script()
        script_path = Path("cmdai_traceback_tester.ps1")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)
        
        print(f"✅ Script PowerShell créé: {script_path}")
        print("\n📋 INSTRUCTIONS WINDOWS:")
        print("1. Ouvrir PowerShell en tant qu'administrateur")
        print("2. Exécuter: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
        print(f"3. Exécuter: . .\\{script_path}")
        print("4. Taper: Show-CMDAIHelp")
        
    else:
        # Script Bash pour Linux/macOS
        bash_script = create_bash_traceback_script()
        script_path = Path("cmdai_traceback_tester.sh")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(bash_script)
        
        # Rendre exécutable
        os.chmod(script_path, 0o755)
        
        print(f"✅ Script Bash créé: {script_path}")
        print(f"\n📋 INSTRUCTIONS {system.upper()}:")
        print(f"1. Exécuter: source ./{script_path}")
        print("2. Taper: show_cmdai_help")
    
    # Créer le guide d'utilisation
    create_tester_guide()
    
    print("\n🎯 SYSTÈME INSTALLÉ!")
    print("Les testeurs peuvent maintenant capturer automatiquement les erreurs.")

def create_tester_guide():
    """Crée le guide pour les testeurs"""
    guide = """# 🧪 GUIDE TESTEUR - SYSTÈME DE TRACEBACK

## Installation

### Windows (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
. .\\cmdai_traceback_tester.ps1
Show-CMDAIHelp
```

### Linux/macOS (Bash)
```bash
source ./cmdai_traceback_tester.sh
show_cmdai_help
```

## Utilisation

### Tester CMD-AI avec capture automatique
```bash
# Windows
Test-CMDAI "ext Weather current Paris"
cmdai "plugin list"

# Linux/macOS  
cmdai "ext Weather current Paris"
cmdai "plugin list"
```

### Signaler un problème manuellement
```bash
# Windows
Report-CMDAIIssue "L'interface se fige au démarrage"

# Linux/macOS
report_cmdai_issue "L'interface se fige au démarrage"
```

### Envoyer les rapports
```bash
# Windows
Send-CMDAITracebacks

# Linux/macOS
send_cmdai_tracebacks
```

## Emplacements des rapports

- **Windows**: `%TEMP%\\cmdai_tracebacks\\`
- **Linux/macOS**: `~/.cmdai_tracebacks/`

## Contenu des rapports

Chaque rapport JSON contient :
- Informations système (OS, version, utilisateur)
- Détails de l'erreur (type, message, contexte)
- Environnement d'exécution (PATH, répertoire, etc.)
- Horodatage précis

## Pour les développeurs

Les rapports peuvent être analysés avec :
```bash
ext CrashReporter list
ext DataAnalyzer analyze logs
```

---
**Merci de votre contribution au développement de CMD-AI Ultra Reboot !** 🙏
"""
    
    with open("TESTER_TRACEBACK_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("📖 Guide testeur créé: TESTER_TRACEBACK_GUIDE.md")

def main():
    """Point d'entrée principal"""
    print("🤖 CMD-AI Ultra Reboot - Installateur Traceback Testeurs")
    print("=" * 60)
    
    install_traceback_system()
    
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION TERMINÉE!")
    print("Les testeurs peuvent maintenant utiliser le système de traceback.")

if __name__ == "__main__":
    main()