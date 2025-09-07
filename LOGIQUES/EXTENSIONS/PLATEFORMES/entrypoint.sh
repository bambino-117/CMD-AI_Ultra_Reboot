#!/bin/bash

# Sécurise le script : arrête en cas d'erreur
set -e

# Définir la variable d'environnement DISPLAY pour le serveur X virtuel
export DISPLAY=:1

# Créer un fichier de mot de passe pour VNC (correspond à celui dans le HTML)
VNC_PASS_FILE="/root/.vnc/passwd"
mkdir -p /root/.vnc
x11vnc -storepasswd "megastructure" "${VNC_PASS_FILE}"

# Lancer le serveur X virtuel en arrière-plan sur l'écran :1
echo "[ENTRYPOINT] Démarrage du serveur X virtuel (Xvfb)..."
Xvfb ${DISPLAY} -screen 0 1024x768x24 &

# Attendre un court instant que Xvfb soit prêt
sleep 2

# Lancer le gestionnaire de fenêtres léger en arrière-plan
echo "[ENTRYPOINT] Démarrage du gestionnaire de fenêtres (Fluxbox)..."
fluxbox -display ${DISPLAY} &

# Lancer le proxy WebSocket pour noVNC en arrière-plan
# Il sert les fichiers de noVNC et redirige le trafic WebSocket (port 6080) vers le VNC (port 5900)
echo "[ENTRYPOINT] Démarrage du proxy WebSocket (websockify)..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# Lancer le serveur VNC et le lier à l'écran virtuel
echo "[ENTRYPOINT] Démarrage du serveur VNC (x11vnc)..."
# -forever: Continue de fonctionner même après la déconnexion du premier client
# -shared: Permet plusieurs connexions
x11vnc -display ${DISPLAY} -forever -shared -rfbport 5900 -passwdfile "${VNC_PASS_FILE}"