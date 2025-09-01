# 🧪 GUIDE TESTEUR - SYSTÈME DE TRACEBACK

## Installation

### Windows (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
. .\cmdai_traceback_tester.ps1
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

- **Windows**: `%TEMP%\cmdai_tracebacks\`
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
