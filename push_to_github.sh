#!/bin/bash
echo "🚀 Publication sur GitHub"

echo "Vous devez créer un token GitHub :"
echo "1. Allez sur : https://github.com/settings/tokens"
echo "2. Cliquez 'Generate new token (classic)'"
echo "3. Nom : CMD-AI-Token"
echo "4. Cochez : repo, workflow, write:packages"
echo "5. Cliquez 'Generate token'"
echo "6. COPIEZ le token (il ne sera plus visible)"
echo ""

read -p "Collez votre token GitHub ici : " token

if [ -z "$token" ]; then
    echo "❌ Token vide, annulation"
    exit 1
fi

echo "🔐 Configuration du token..."
git remote set-url origin https://$token@github.com/bambino-117/CMD-AI_Ultra_Reboot.git

echo "📤 Push vers GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Version 2.1.0 publiée avec succès !"
    echo "🌐 Voir sur : https://github.com/bambino-117/CMD-AI_Ultra_Reboot"
else
    echo "❌ Erreur lors du push"
    echo "💡 Vérifiez votre token et réessayez"
fi