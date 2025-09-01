#!/bin/bash
echo "🔐 Configuration de l'authentification Git"

echo "Choisissez votre méthode d'authentification :"
echo "1) Token GitHub (recommandé)"
echo "2) SSH Key"
echo "3) Authentification manuelle"

read -p "Votre choix (1-3): " choice

case $choice in
    1)
        echo "📝 Pour créer un token GitHub :"
        echo "1. Allez sur https://github.com/settings/tokens"
        echo "2. Cliquez 'Generate new token (classic)'"
        echo "3. Cochez 'repo' et 'workflow'"
        echo "4. Copiez le token généré"
        echo ""
        read -p "Entrez votre token GitHub: " token
        git remote set-url origin https://$token@github.com/bambino-117/CMD-AI_Ultra_Reboot.git
        echo "✅ Token configuré"
        ;;
    2)
        echo "🔑 Configuration SSH :"
        if [ ! -f ~/.ssh/id_rsa ]; then
            echo "Génération d'une clé SSH..."
            ssh-keygen -t rsa -b 4096 -C "bambino117@example.com" -f ~/.ssh/id_rsa -N ""
        fi
        echo "📋 Copiez cette clé publique dans GitHub (Settings > SSH Keys) :"
        cat ~/.ssh/id_rsa.pub
        echo ""
        read -p "Appuyez sur Entrée après avoir ajouté la clé sur GitHub..."
        git remote set-url origin git@github.com:bambino-117/CMD-AI_Ultra_Reboot.git
        echo "✅ SSH configuré"
        ;;
    3)
        echo "🔓 Authentification manuelle - utilisez :"
        echo "git push https://bambino-117@github.com/bambino-117/CMD-AI_Ultra_Reboot.git main"
        ;;
esac

echo ""
echo "🚀 Test de la connexion :"
git push origin main