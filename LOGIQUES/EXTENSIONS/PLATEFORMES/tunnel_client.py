import socketio
import time
import subprocess
import os

# --- Configuration ---
# 'host.docker.internal' est un nom DNS spécial que Docker fournit
# pour que les conteneurs puissent se connecter aux services de l'hôte.
HOST_URL = 'http://host.docker.internal:5000'
NAMESPACE = '/sandbox'

# --- Initialisation du client Socket.IO ---
sio = socketio.Client(reconnection_delay_max=5)

@sio.event(namespace=NAMESPACE)
def connect():
    print('[TUNNEL_CLIENT] Connexion établie avec le serveur hôte.')
    sio.emit('sandbox_response', {'output': '[SYSTEM] Tunnel de communication initialisé.\n'}, namespace=NAMESPACE)

@sio.event(namespace=NAMESPACE)
def connect_error(data):
    print(f"[TUNNEL_CLIENT] Erreur de connexion : {data}")

@sio.event(namespace=NAMESPACE)
def disconnect():
    print('[TUNNEL_CLIENT] Déconnecté du serveur hôte.')

@sio.on('host_command', namespace=NAMESPACE)
def on_host_command(data):
    """Reçoit et exécute une commande de l'hôte."""
    command = data.get('command')
    if not command:
        return

    print(f"[TUNNEL_CLIENT] Commande reçue : {command}")
    try:
        # Exécute la commande dans le shell du conteneur
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="/sandbox_files")
        output = result.stdout + result.stderr
    except Exception as e:
        output = f"Erreur d'exécution : {e}\n"
    
    # Renvoie la sortie à l'hôte
    sio.emit('sandbox_response', {'output': output}, namespace=NAMESPACE)

if __name__ == '__main__':
    while True:
        try:
            print("[TUNNEL_CLIENT] Tentative de connexion à l'hôte...")
            sio.connect(HOST_URL, namespaces=[NAMESPACE])
            sio.wait()
        except socketio.exceptions.ConnectionError:
            print("[TUNNEL_CLIENT] Échec de la connexion, nouvelle tentative dans 5 secondes...")
            time.sleep(5)