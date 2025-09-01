#!/bin/bash
# Script pour nettoyer le repository des fichiers inutiles

echo "🧹 Nettoyage du repository GitHub..."

# Supprimer du tracking Git (mais garder en local)
git rm --cached -r cmd_ai_ultra_reboot.egg-info/ 2>/dev/null
git rm --cached -r CMD-AI_Ultra_Reboot_v*/ 2>/dev/null
git rm --cached -r dist_linux/ 2>/dev/null
git rm --cached -r utils/ 2>/dev/null
git rm --cached *.tar.gz 2>/dev/null
git rm --cached *.spec 2>/dev/null
git rm --cached *.pdf 2>/dev/null
git rm --cached "plan de route.txt" 2>/dev/null
git rm --cached "tester_codes.txt" 2>/dev/null
git rm --cached "contenu USB tranfert de l'app pour compile windows" 2>/dev/null
git rm --cached build_*.py 2>/dev/null
git rm --cached build_*.bat 2>/dev/null
git rm --cached build_*.sh 2>/dev/null
git rm --cached CMD-AI_Ultra_Reboot 2>/dev/null
git rm --cached docker-compose.yml 2>/dev/null
git rm --cached Dockerfile.* 2>/dev/null
git rm --cached check_compatibility.py 2>/dev/null
git rm --cached compatibility_patch.py 2>/dev/null
git rm --cached validate_release.py 2>/dev/null
git rm --cached launch.py 2>/dev/null
git rm --cached launch.sh 2>/dev/null
git rm --cached setup.py 2>/dev/null

echo "✅ Fichiers supprimés du tracking Git"
echo "💡 Faites maintenant: git commit -m 'Clean: Remove build files and personal notes'"