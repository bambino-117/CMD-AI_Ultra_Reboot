# server.py

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import logging

# --- Configuration ---
# Désactiver les logs HTTP de Flask pour garder la console propre
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
# Autorise les connexions depuis n'importe quelle origine.
# Crucial pour que votre application pywebview puisse se connecter.
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- État du Serveur (en mémoire vive uniquement) ---
# Dictionnaire pour mapper les pseudos aux identifiants de session (sid)
# et inversement pour une recherche rapide.
# Exemple :
# connected_users = { 'pseudo1': 'sid_xyz', 'pseudo2': 'sid_abc' }
# sid_to_pseudo = { 'sid_xyz': 'pseudo1', 'sid_abc': 'pseudo2' }
connected_users = {}
sid_to_pseudo = {}

def get_user_list():
    """Retourne la liste des pseudos des utilisateurs connectés."""
    return list(connected_users.keys())

# --- Gestionnaires d'Événements Socket.IO ---

@socketio.on('connect')
def handle_connect():
    """Gère la connexion d'un nouvel utilisateur."""
    print(f"[CONNEXION] Client connecté : {request.sid}")

@socketio_on('register')
def handle_register(data):
    """
    Enregistre un utilisateur avec son pseudo. C'est la première action
    que le client doit faire après s'être connecté.
    """
    pseudo = data.get('pseudo')
    if not pseudo:
        return

    # Si le pseudo est déjà pris, on pourrait gérer le conflit ici.
    # Pour l'instant, on écrase l'ancienne connexion si elle existe.
    if pseudo in connected_users:
        old_sid = connected_users[pseudo]
        print(f"[AVERTISSEMENT] Pseudo '{pseudo}' déjà utilisé. Déconnexion de l'ancienne session {old_sid}.")
        # On pourrait notifier l'ancien client de sa déconnexion.
        socketio.emit('force_disconnect', {'message': 'Ce pseudo est maintenant utilisé par une autre session.'}, room=old_sid)
        socketio.close_room(old_sid)


    # Enregistrer le nouvel utilisateur
    connected_users[pseudo] = request.sid
    sid_to_pseudo[request.sid] = pseudo
    print(f"[REGISTER] '{pseudo}' enregistré avec le SID {request.sid}")

    # Diffuser la liste mise à jour des utilisateurs à tout le monde
    emit('update_user_list', {'users': get_user_list()}, broadcast=True)
    print(f"[BROADCAST] Liste des utilisateurs mise à jour envoyée. Total : {len(connected_users)}")

@socketio.on('private_message')
def handle_private_message(data):
    """
    Relaye un message privé d'un utilisateur à un autre.
    """
    recipient_pseudo = data.get('recipient_pseudo')
    message = data.get('message')
    sender_pseudo = sid_to_pseudo.get(request.sid)

    if not sender_pseudo:
        print(f"[ERREUR] Message reçu d'un SID non enregistré : {request.sid}")
        return

    recipient_sid = connected_users.get(recipient_pseudo)

    if recipient_sid:
        # Le destinataire est connecté, on lui envoie le message.
        print(f"[MSG PRIVÉ] De '{sender_pseudo}' à '{recipient_pseudo}'")
        emit('new_private_message', {
            'sender_pseudo': sender_pseudo,
            'message': message
        }, room=recipient_sid)
    else:
        # Le destinataire n'est pas trouvé.
        print(f"[ERREUR] Destinataire '{recipient_pseudo}' non trouvé pour un message de '{sender_pseudo}'.")
        # On pourrait notifier l'expéditeur que l'utilisateur est hors ligne.
        emit('user_not_found', {'pseudo': recipient_pseudo}, room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    """Gère la déconnexion d'un utilisateur."""
    pseudo = sid_to_pseudo.pop(request.sid, None)
    if pseudo:
        del connected_users[pseudo]
        print(f"[DECONNEXION] '{pseudo}' (SID: {request.sid}) déconnecté.")
        # Diffuser la liste mise à jour des utilisateurs à tout le monde
        emit('update_user_list', {'users': get_user_list()}, broadcast=True)
        print(f"[BROADCAST] Liste des utilisateurs mise à jour envoyée. Total : {len(connected_users)}")
    else:
        print(f"[DECONNEXION] SID inconnu {request.sid} déconnecté.")


if __name__ == '__main__':
    print("[INFO] Démarrage du serveur relais de chat...")
    # Utiliser eventlet est recommandé pour la production.
    # Pour le développement, le mode par défaut de Flask est suffisant.
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

