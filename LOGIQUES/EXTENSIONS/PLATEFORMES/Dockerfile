# Utiliser une image de base Debian stable avec une interface graphique minimale
FROM debian:bullseye-slim

# NOUVEAU : Installer python3 et pip
RUN apt-get update && apt-get install -y python3 python3-pip --no-install-recommends

# Définir des arguments pour éviter les questions interactives lors de l'installation
ARG DEBIAN_FRONTEND=noninteractive

# Mettre à jour les paquets et installer les dépendances nécessaires
# - x11vnc: Le serveur VNC
# - xvfb: Le framebuffer virtuel (écran virtuel)
# - fluxbox: Un gestionnaire de fenêtres très léger
# - xterm: Un terminal basique pour les tests
# - procps: Pour `pgrep` utilisé dans le script
# - net-tools: Pour des outils réseau si besoin
# - novnc: Le client web VNC (HTML/JS)
# - websockify: Le proxy WebSocket pour noVNC
RUN apt-get update && apt-get install -y \
  x11vnc \
  xvfb \
  fluxbox \
  xterm \
  firefox-esr \
  firefox-esr-l10n-fr \
  pcmanfm \
  procps \
  net-tools \
  novnc \
  websockify \
  --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Créer un répertoire pour le script d'entrée
WORKDIR /usr/src/app

# NOUVEAU : Installer les dépendances Python pour le tunnel
RUN pip3 install --no-cache-dir "python-socketio[client]"

# Copier les scripts dans le conteneur
COPY entrypoint.sh .
COPY tunnel_client.py .

# NOUVEAU : Créer un dossier pour les fichiers téléversés
RUN mkdir /sandbox_files

# Rendre le script d'entrée exécutable
RUN chmod +x entrypoint.sh

# Exposer le port VNC
EXPOSE 5900

# NOUVEAU : Modifier le point d'entrée pour lancer le client tunnel en arrière-plan
# L'esperluette (&) est cruciale pour le lancer en tâche de fond.
# On utilise un script shell pour pouvoir lancer plusieurs commandes.
CMD ["/bin/bash", "-c", "python3 /usr/src/app/tunnel_client.py & /usr/src/app/entrypoint.sh"]