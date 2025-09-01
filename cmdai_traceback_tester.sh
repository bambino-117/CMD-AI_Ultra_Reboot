#!/bin/bash
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
