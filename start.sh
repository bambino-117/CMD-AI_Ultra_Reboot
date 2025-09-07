#!/bin/bash

# Définir la variable d'environnement DISPLAY pour le serveur X virtuel
export DISPLAY=:1

# Lancer le serveur X virtuel en arrière-plan sur l'écran :1
# -screen 0 1024x768x24: Crée un écran de 1024x768 avec une profondeur de couleur de 24 bits
echo "Démarrage du serveur X virtuel (Xvfb)..."
Xvfb :1 -screen 0 1024x768x24 &

# Lancer le gestionnaire de fenêtres léger en arrière-plan
echo "Démarrage du gestionnaire de fenêtres (Fluxbox)..."
fluxbox &

# Lancer le proxy WebSocket pour noVNC
# Il écoutera sur le port 6080 et redirigera le trafic vers le serveur VNC sur le port 5900
echo "Démarrage du proxy WebSocket (websockify)..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# Lancer le serveur VNC et le lier à l'écran virtuel
# -display :1: Se connecte à l'écran créé par Xvfb
# -forever: Continue de fonctionner même après la déconnexion du premier client
# -usepw: Utilise un mot de passe (ici, vide par défaut pour la simplicité)
echo "Démarrage du serveur VNC (x11vnc)..."
x11vnc -display :1 -forever -usepw