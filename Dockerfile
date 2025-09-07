# Utiliser une image de base Debian stable
FROM debian:bullseye-slim

# Empêcher les installations interactives
ENV DEBIAN_FRONTEND=noninteractive

# Mettre à jour les paquets et installer les dépendances nécessaires
# - xvfb: Le serveur X virtuel (framebuffer)
# - fluxbox: Un gestionnaire de fenêtres très léger
# - x11vnc: Le serveur VNC qui va capturer le bureau virtuel
# - websockify: Le proxy WebSocket pour noVNC
# - wine: Pour exécuter des applications Windows (.exe)
# - wget, ca-certificates: Utilitaires de base
RUN apt-get update && apt-get install -y \
  xvfb \
  fluxbox \
  x11vnc \
  websockify \
  wine \
  wget \
  ca-certificates \
  --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail pour les applications
WORKDIR /app

# Copier le script de démarrage dans le conteneur
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Exposer les ports (VNC et WebSocket)
EXPOSE 5900
EXPOSE 6080

# Commande par défaut pour lancer le script de démarrage
CMD ["/start.sh"]