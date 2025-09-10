from flask import Flask, render_template, request, session, redirect, url_for
import webview 
from flask_socketio import SocketIO, emit
import sys
from dotenv import load_dotenv
import threading

import bcrypt
# --- Variable de Contrôle du Mode ---
DEBUG = False  # Mettre à False pour simuler le mode "production" (silencieux)
import json
import os
import importlib.util
import inspect
import platform
import zipfile
import tempfile
import stat
from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
import uuid
from LOGIQUES.vpn_manager import VpnManager
import subprocess
from LOGIQUES.utils import secure_path
import time

# --- NOUVEAU : Fonction pour gérer les chemins en mode développement et packagé ---
def get_base_path():
    """Retourne le chemin de base pour les ressources, que l'on soit en mode dev ou packagé."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Mode packagé par PyInstaller
        return sys._MEIPASS
    else:
        # Mode développement
        return os.path.dirname(os.path.abspath(__file__))

# --- NOUVEAU : Version actuelle de l'application ---
CURRENT_APP_VERSION = "1.0.0"

# --- NOUVEAU : Chargement des variables d'environnement ---
load_dotenv()
# --- NOUVEAU : Définition du mode de build ---
BUILD_MODE = os.getenv('BUILD_MODE', 'PUBLIC')

import shutil
from datetime import datetime, timedelta

# --- NOUVEAU : Importation du module de mécanique ---
try:
    from LOGIQUES.mecannique import search_admin_data
except ImportError:
    search_admin_data = None
import requests
from bs4 import BeautifulSoup

# --- Configuration des Chemins ---
# Le script est à la racine du projet. Le dossier 'INTERFACES' contient les ressources.
PROJECT_ROOT = get_base_path()
INTERFACES_FOLDER = os.path.join(PROJECT_ROOT, 'INTERFACES')
TEMPLATE_FOLDER = os.path.join(INTERFACES_FOLDER, 'templates')
STATIC_FOLDER = os.path.join(INTERFACES_FOLDER, 'static')
LOGIQUES_FOLDER = os.path.join(PROJECT_ROOT, 'LOGIQUES')
EXTENSIONS_FOLDER = os.path.join(LOGIQUES_FOLDER, 'EXTENSIONS')
CONTENEURS_FOLDER = os.path.join(LOGIQUES_FOLDER, 'CONTENEURS')
RESSOURCES_FOLDER = os.path.join(PROJECT_ROOT, 'RESSOURCES')
CONFIG_FILE_PATH = os.path.join(INTERFACES_FOLDER, 'config.json')
TESTER_CODES_PATH = os.path.join(PROJECT_ROOT, 'tester_codes.json')

# --- DÉBOGAGE DE CHEMIN ---
print(f"[DEBUG] Chemin absolu du dossier des conteneurs attendu : {os.path.abspath(CONTENEURS_FOLDER)}")

# --- Stockage Global pour les Extensions ---
loaded_extensions = {}
# --- NOUVEAU : État global du VPN ---
tester_codes = []
vpn_global_state = {
    "is_connected": False,
    "proxy_address": None
}


# Initialise l'application Flask en spécifiant les dossiers
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
# NOUVEAU : Initialisation de SocketIO
# async_mode='threading' est crucial car nous utilisons déjà des threads.
socketio = SocketIO(app, async_mode='threading')

# --- NOUVEAU : Clé secrète pour les sessions Flask ---
# Essentiel pour se souvenir de l'état de connexion de l'utilisateur.
app.secret_key = 'une-cle-secrete-tres-difficile-a-deviner' # En production, utiliser une vraie clé sécurisée.

# --- NOUVEAU : Logique du Keylogger en arrière-plan ---
def keylogger_simulation_thread(api_instance):
    """
    Thread qui simule un keylogger en écrivant périodiquement dans un fichier log.
    """
    if not api_instance:
        print("[KEYLOGGER] Erreur: Instance de l'API non fournie au thread.")
        return

    # Attendre que la fenêtre soit prête pour éviter les erreurs de chemin au démarrage
    time.sleep(5) 
    
    user_path = api_instance.config.get('user', {}).get('user_folder_path')
    if not user_path:
        print("[KEYLOGGER] Erreur: Chemin du dossier utilisateur non défini.")
        return
        
    log_file_path = os.path.join(user_path, 'keylogscornflakes.md')

    print(f"[KEYLOGGER] Thread de simulation démarré. Log vers : {log_file_path}")

    # Boucle tant que le keylogger est actif
    while True:
        if not api_instance.config.get('user', {}).get('keylogger_active', False):
            print("[KEYLOGGER] Drapeau désactivé. Arrêt du thread.")
            break
        try:
            time.sleep(random.uniform(8, 25))
            log_entries = [
                f"KEY_PRESS: 'password_field' -> '{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(8,12)))}'",
                f"MOUSE_CLICK: (x={random.randint(100,1800)}, y={random.randint(100,900)}) -> 'login_button'",
                f"WINDOW_FOCUS: 'C:\\Windows\\System32\\cmd.exe'",
                f"NETWORK_OUT: '192.168.1.254' -> 'api.megastructure.corp'",
                f"FILE_ACCESS: '{os.path.join(user_path, random.choice(['config.json', 'notes.txt', 'secret_plans.doc']))}'",
                f"CLIPBOARD_COPY: 'Access Code: 7B-DELTA-9'",]
            log_entry = random.choice(log_entries)
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` - {log_entry}\n")
        except Exception as e:
            print(f"[KEYLOGGER] Erreur dans la boucle du thread : {e}")
            time.sleep(30)

# --- CONFIGURATION DU CACHE ---
# Force la désactivation du cache pour les fichiers statiques (CSS, JS, images) en mode DEBUG.
# C'est la méthode la plus fiable pour s'assurer que les changements sont pris en compte.
if DEBUG:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# --- NOUVEAU : API de Sandboxing pour les Extensions ---
class SandboxAPI:
    """
    Une API limitée et sécurisée fournie à chaque extension.
    Elle sert d'intermédiaire contrôlé entre l'extension et le cœur de l'application.
    """
    def __init__(self, main_api_instance, extension_name):
        self._api = main_api_instance
        self._extension_name = extension_name
        self._bunker_path = self._api.config.get('user', {}).get('user_folder_path')

    def log(self, message):
        """Permet à une extension d'écrire dans le log principal."""
        print(f"[{self._extension_name}] {message}")

    def get_bunker_path(self):
        """Retourne le chemin sécurisé du dossier Bunker."""
        return self._bunker_path

    def get_ai_response(self, prompt):
        """Permet à une extension de faire une requête à l'IA via l'API principale."""
        self.log(f"Requête IA : {prompt[:50]}...")
        return self._api.get_ai_response(prompt)

    def get_config_value(self, key_path):
        """
        Permet un accès en lecture seule à des valeurs spécifiques de la configuration.
        Exemple: get_config_value('user.pseudo')
        """
        keys = key_path.split('.')
        # Liste blanche des clés autorisées pour la sécurité
        allowed_prefixes = ['user.pseudo', 'user.api_keys']
        if not any(key_path.startswith(prefix) for prefix in allowed_prefixes):
            self.log(f"Accès refusé à la clé de configuration : {key_path}")
            return None

        value = self._api.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            self.log(f"Clé de configuration introuvable : {key_path}")
            return None

    def secure_path(self, filename, base_dir_override=None):
        """
        Construit un chemin sécurisé à l'intérieur du dossier utilisateur.
        Si base_dir_override est fourni, il est utilisé comme base.
        """
        base = base_dir_override if base_dir_override else self._bunker_path
        return secure_path(filename, base_dir=base)

# --- API Class for JS-Python Bridge ---
class Api:
    """
    Cette classe expose des méthodes au JavaScript exécuté dans la fenêtre pywebview.
    C'est le "pont" entre le front-end et le back-end.
    """
    _extensions = {} # Stocke les instances d'extensions

    def __init__(self, config):
        self.window = None
        self.config = config  # Stocke la configuration chargée
        self.vpn_manager = VpnManager()

    def load_settings(self):
        """Exposée au JS. Charge les paramètres depuis config.json."""
        return self.config

    def save_settings(self, data):
        """Exposée au JS. Sauvegarde les données dans config.json."""
        try:
            # --- NOUVEAU : Hachage du mot de passe avant de sauvegarder ---
            # On vérifie si un nouveau mot de passe a été fourni.
            # Le JS envoie le mot de passe en clair. On ne le stocke jamais.
            new_password = data.get('user', {}).get('password')
            if new_password:
                # On le hache avec bcrypt
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                # On stocke la version hachée (en string) dans la config à sauvegarder
                data['user']['password'] = hashed_password.decode('utf-8')
            else:
                # Si le champ est vide, on garde l'ancien mot de passe haché.
                # On récupère l'ancien depuis la config en mémoire (self.config).
                data['user']['password'] = self.config.get('user', {}).get('password', '')

            with open(CONFIG_FILE_PATH, 'w') as f:
                json.dump(data, f, indent=2)
            # Mettre à jour la config en mémoire de l'API
            self.config = data
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def reset_settings_to_default(self):
        """Exposée au JS. Réinitialise la configuration à ses valeurs par défaut."""
        try:
            # Recharge la configuration par défaut
            default_config = load_config(use_default_only=True)
            # Sauvegarde cette configuration par défaut
            with open(CONFIG_FILE_PATH, 'w') as f:
                json.dump(default_config, f, indent=2)
            # Met à jour la config en mémoire de l'API
            self.config = default_config
            return {'status': 'success', 'message': 'Paramètres réinitialisés aux valeurs par défaut.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def complete_first_run_setup(self, setup_data):
        """Exposée au JS. Finalise la configuration initiale de l'utilisateur."""
        try:
            pseudo = setup_data.get('pseudo')
            password = setup_data.get('password')
            bunker_path = setup_data.get('bunker_path')

            if not pseudo or not password or not bunker_path:
                return {'status': 'error', 'message': 'Pseudo, mot de passe et chemin du Bunker sont requis.'}

            # Mettre à jour la configuration en mémoire
            self.config['user']['pseudo'] = pseudo
            self.config['user']['password'] = password # Le mot de passe sera haché par save_settings
            self.config['user']['user_folder_path'] = bunker_path
            
            # Sauvegarder la configuration (save_settings s'occupe du hachage)
            save_result = self.save_settings(self.config)
            if save_result['status'] == 'error':
                return save_result

            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def close_app(self):
        """Exposée au JS. Ferme la fenêtre de l'application."""
        if self.window:
            self.window.destroy()

    def ensure_user_folder_exists(self):
        """
        Vérifie que le dossier utilisateur existe, et le crée si non.
        Appelée au démarrage pour s'assurer que tout est en place.
        """
        user_path = self.config.get('user', {}).get('user_folder_path')
        if user_path:
            try:
                os.makedirs(user_path, exist_ok=True)
                return {'status': 'success', 'path': user_path}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return {'status': 'error', 'message': 'User folder path not defined.'}

    def list_bunker_files(self, subpath=''):
        """
        Exposée au JS. Liste les fichiers dans le dossier utilisateur ("Bunker"),
        en respectant le chemin du sous-dossier actuel.
        """
        # Sécurise le chemin du sous-dossier pour s'assurer qu'il reste dans le Bunker
        target_path, error = self._secure_path(subpath)
        if error:
            return {'status': 'error', 'message': error}
        if not os.path.isdir(target_path):
            return {'status': 'error', 'message': 'Le répertoire spécifié n\'existe pas.'}

        try:
            items = []
            for name in os.listdir(target_path):
                item_path = os.path.join(target_path, name)
                item_type = 'folder' if os.path.isdir(item_path) else 'file'
                items.append({'name': name, 'type': item_type})
            return {'status': 'success', 'files': items} # Garde la clé 'files' pour la compatibilité front-end
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _secure_path(self, filename):
        """
        Construit un chemin sécurisé à l'intérieur du dossier utilisateur en utilisant la fonction utilitaire.
        """
        user_path = self.config.get('user', {}).get('user_folder_path')
        return secure_path(filename, user_path)

    def read_bunker_file(self, filepath):
        """Exposée au JS. Lit le contenu d'un fichier dans le Bunker de manière sécurisée."""
        full_path, error = self._secure_path(filepath)
        if error:
            return {'status': 'error', 'message': error}

        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return {'status': 'success', 'content': content}
        except FileNotFoundError:
            return {'status': 'error', 'message': f'Fichier non trouvé : {os.path.basename(filepath)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de lire le fichier : {e}'}

    def delete_bunker_file(self, filename, current_path=''):
        """Exposée au JS. Supprime un fichier ou un dossier dans le Bunker de manière sécurisée."""
        # Construit le chemin relatif complet avant de sécuriser
        relative_path = os.path.join(current_path, filename)
        full_path, error = self._secure_path(relative_path)
        if error:
            return {'status': 'error', 'message': error}

        try:
            if not os.path.exists(full_path):
                 return {'status': 'error', 'message': f'Élément non trouvé : {os.path.basename(filename)}'}

            if os.path.isdir(full_path):
                shutil.rmtree(full_path) # Utilise rmtree pour les dossiers
                return {'status': 'success', 'message': f'Dossier {os.path.basename(filename)} supprimé.'}
            else:
                os.remove(full_path) # Utilise remove pour les fichiers
                return {'status': 'success', 'message': f'Fichier {os.path.basename(filename)} supprimé.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de supprimer l\'élément : {e}'}

    def create_bunker_file(self, filename, current_path=''):
        """Exposée au JS. Crée un nouveau fichier vide dans le Bunker."""
        if not filename or not isinstance(filename, str) or "/" in filename or "\\" in filename:
            return {'status': 'error', 'message': 'Nom de fichier invalide.'}

        relative_path = os.path.join(current_path, filename)
        full_path, error = self._secure_path(relative_path)
        if error:
            return {'status': 'error', 'message': error}

        if os.path.exists(full_path):
            return {'status': 'error', 'message': f'Le fichier "{filename}" existe déjà.'}

        try:
            with open(full_path, 'w') as f:
                pass
            return {'status': 'success', 'message': f'Fichier "{filename}" créé.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de créer le fichier : {e}'}

    def create_bunker_folder(self, foldername, current_path=''):
        """Exposée au JS. Crée un nouveau dossier vide dans le Bunker."""
        if not foldername or not isinstance(foldername, str) or "/" in foldername or "\\" in foldername:
            return {'status': 'error', 'message': 'Nom de dossier invalide.'}

        relative_path = os.path.join(current_path, foldername)
        full_path, error = self._secure_path(relative_path)
        if error:
            return {'status': 'error', 'message': error}

        if os.path.exists(full_path):
            return {'status': 'error', 'message': f'Un fichier ou dossier nommé "{foldername}" existe déjà.'}

        try:
            os.makedirs(full_path)
            return {'status': 'success', 'message': f'Dossier "{foldername}" créé.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de créer le dossier : {e}'}

    def rename_bunker_file(self, old_filename, new_filename, current_path=''):
        """Exposée au JS. Renomme un fichier dans le Bunker."""
        # Valider le nouveau nom de fichier
        if not new_filename or not isinstance(new_filename, str) or "/" in new_filename or "\\" in new_filename:
            return {'status': 'error', 'message': 'Nouveau nom de fichier invalide.'}

        # Sécuriser les chemins pour l'ancien et le nouveau fichier
        old_relative_path = os.path.join(current_path, old_filename)
        old_full_path, old_error = self._secure_path(old_relative_path)
        if old_error: return {'status': 'error', 'message': old_error}

        new_relative_path = os.path.join(current_path, new_filename)
        new_full_path, new_error = self._secure_path(new_relative_path)
        if new_error: return {'status': 'error', 'message': new_error}

        # Vérifier les conditions d'existence
        if not os.path.exists(old_full_path):
            return {'status': 'error', 'message': f'Le fichier original "{old_filename}" n\'existe pas.'}
        if os.path.exists(new_full_path):
            return {'status': 'error', 'message': f'Un fichier nommé "{new_filename}" existe déjà.'}

        try:
            os.rename(old_full_path, new_full_path)
            return {'status': 'success', 'message': f'Fichier renommé en "{new_filename}".'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de renommer le fichier : {e}'}

    def handle_blocked_file(self, filename):
        """
        Exposée au JS. Simule le déchiffrement d'un fichier bloqué.
        Dans cette simulation, on retourne un contenu prédéfini après un délai.
        """
        try:
            # Simuler un temps de traitement
            time.sleep(random.uniform(1.5, 3.0))
            # Contenu "déchiffré" factice
            decrypted_content = f"""
// DECRYPTION LOG - {datetime.now().isoformat()}
// TARGET: {filename}
// STATUS: SUCCESS - AES-256 GCM brute-force successful.

-----BEGIN DECRYPTED DATA-----
Access Code: 7B-DELTA-9
Coordinates: 48.8584° N, 2.2945° E
Protocol: 'Ghost'
Objective: Infiltrate Level 7 network. Use code 'Wyvern' for primary authentication.
Warning: Counter-intrusion systems are active. Maintain low profile.
-----END DECRYPTED DATA-----
"""
            return {
                'status': 'success',
                'message': 'Déchiffrement réussi. Les politiques de sécurité de l\'hôte ont été modifiées pour autoriser l\'accès.',
                'content': decrypted_content
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur de simulation : {e}'}

    def deploy_keylogger(self):
        """
        Exposée au JS. Simule le déploiement d'un keylogger avec une chance de 1/4.
        Met à jour la configuration si le déploiement réussit.
        """
        try:
            time.sleep(random.uniform(1.0, 2.5))
            if random.randint(1, 4) == 1:
                self.config['user']['keylogger_active'] = True
                self.save_settings(self.config)
                return {'status': 'success', 'message': '...Opération terminée. Aucune erreur détectée. Le composant semble s\'être intégré au système.'}
            else:
                return {'status': 'failure', 'message': 'L\'exécution a échoué. Le sous-système de sécurité de l\'hôte a rejeté l\'opération. Aucune trace laissée.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur système inattendue : {e}'}

    def check_bunker_password(self, username, password_attempt):
        """Exposée au JS. Vérifie les identifiants et retourne le rôle de l'utilisateur."""

        # Porte dérobée "Neural Ghost" : Accès total si l'infection est active
        if self.config.get('user', {}).get('neural_ghost_active', False):
            session['user_role'] = 'concepteur' # Enregistrer le rôle dans la session
            return {'status': 'success', 'role': 'concepteur', 'message': 'NEURAL_GHOST: Accès direct accordé.'}

        # --- SÉCURITÉ : Le mot de passe est lu depuis les variables d'environnement ---
        developer_password = os.getenv('DEVELOPER_PASSWORD')

        # --- Rôle 1: Concepteur (Developer) ---
        # Un concepteur peut se connecter avec un pseudo spécifique et le mot de passe maître.
        if developer_password and username.lower() in ['root', 'admin', 'concepteur'] and password_attempt == developer_password:
            # --- NOUVEAU : Vérification du mode de build pour l'accès concepteur ---
            if BUILD_MODE != 'DEV':
                return {'status': 'error', 'message': 'Accès Concepteur désactivé dans cette version.'}

            session['user_role'] = 'concepteur'
            return {'status': 'success', 'role': 'concepteur'}

        # --- Rôle 2: Testeur (Tester) ---
        # Un testeur utilise son code comme pseudo et le mot de passe maître.
        for i, code_info in enumerate(tester_codes): # Utiliser enumerate pour obtenir l'index
            if username == code_info.get('code'):
                if developer_password and password_attempt == developer_password:
                    uses = code_info.get('uses', 0)

                    if uses == 0:
                        return {'status': 'error', 'message': 'Ce code Testeur a expiré.'}
                    
                    # Décrémenter si ce n'est pas un usage infini (-1)
                    if uses > 0:
                        tester_codes[i]['uses'] -= 1
                        # Sauvegarder les changements dans le fichier JSON
                        try:
                            with open(TESTER_CODES_PATH, 'w') as f:
                                json.dump(tester_codes, f, indent=2)
                        except Exception as e:
                            print(f"ERREUR: Impossible de sauvegarder les codes testeurs mis à jour: {e}")
                            return {'status': 'error', 'message': 'Erreur interne lors de la validation du code.'}

                    # La connexion est réussie
                    session['user_role'] = 'testeur'
                    return {'status': 'success', 'role': 'testeur'}
                else:
                    # Code testeur correct, mais mauvais mot de passe
                    return {'status': 'error', 'message': 'Code Testeur valide, mot de passe incorrect.'}

        # --- Rôle 3: Utilisateur Lambda ---
        user_pseudo = self.config.get('user', {}).get('pseudo', '')
        user_password = self.config.get('user', {}).get('password', '')

        # Un utilisateur lambda se connecte avec son pseudo et son mot de passe personnel.
        if username.lower() == user_pseudo.lower():
            # --- SÉCURITÉ : Utilisation de bcrypt pour la vérification ---
            # user_password est le hash stocké dans config.json
            if user_password and isinstance(user_password, str):
                # On vérifie si le mot de passe fourni correspond au hash
                if bcrypt.checkpw(password_attempt.encode('utf-8'), user_password.encode('utf-8')):
                    session['user_role'] = 'lambda'
                    return {'status': 'success', 'role': 'lambda'}
            
            return {'status': 'error', 'message': 'Mot de passe incorrect.'}

        # --- Cas d'échec final ---
        return {'status': 'error', 'message': 'Identifiants non reconnus.'}


    def upload_file_to_bunker(self, source_path, current_bunker_path=''):
        """Exposée au JS. Copie un fichier depuis le système de l'hôte vers le Bunker via glisser-déposer."""
        if not source_path or not os.path.isfile(source_path):
            return {'status': 'error', 'message': 'Le fichier source est invalide ou n\'existe pas.'}

        filename = os.path.basename(source_path)
        # Construire le chemin de destination relatif à l'intérieur du Bunker
        relative_dest_path = os.path.join(current_bunker_path, filename)
        
        full_dest_path, error = self._secure_path(relative_dest_path)
        if error:
            return {'status': 'error', 'message': error}

        if os.path.exists(full_dest_path):
            return {'status': 'error', 'message': f'Un fichier nommé "{filename}" existe déjà à cet emplacement.'}

        try:
            shutil.copy2(source_path, full_dest_path) # copy2 préserve les métadonnées (date, etc.)
            return {'status': 'success', 'message': f'Fichier "{filename}" téléversé avec succès.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de copier le fichier : {e}'}

    def _call_openai_compatible_api(self, model, prompt, api_key, base_url):
        """Appelle une API compatible avec le format OpenAI (DeepSeek, Groq, Ollama...)."""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant within a cyberpunk-themed application."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        # --- NOUVEAU : Intégration du proxy VPN ---
        proxies = None
        if vpn_global_state["is_connected"] and vpn_global_state["proxy_address"]:
            proxies = {
                "http": vpn_global_state["proxy_address"],
                "https": vpn_global_state["proxy_address"],
            }
            print(f"[VPN] Utilisation du proxy : {vpn_global_state['proxy_address']}")

        response = requests.post(f'{base_url}/chat/completions', headers=headers, json=data, timeout=30, proxies=proxies)
        response.raise_for_status()
        ai_response = response.json()
        return ai_response['choices'][0]['message']['content']

    def _call_google_gemini_api(self, model, prompt, api_key):
        """Appelle l'API Google Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = { "contents": [{"parts": [{"text": prompt}]}] }

        # --- NOUVEAU : Intégration du proxy VPN ---
        proxies = None
        if vpn_global_state["is_connected"] and vpn_global_state["proxy_address"]:
            proxies = {
                "http": vpn_global_state["proxy_address"],
                "https": vpn_global_state["proxy_address"],
            }
            print(f"[VPN] Utilisation du proxy : {vpn_global_state['proxy_address']}")

        response = requests.post(url, headers=headers, json=data, timeout=30, proxies=proxies)
        response.raise_for_status()
        ai_response = response.json()

        # Gestion des réponses bloquées pour des raisons de sécurité par Google
        if 'candidates' not in ai_response or not ai_response['candidates']:
            feedback = ai_response.get('promptFeedback', {})
            block_reason = feedback.get('blockReason', 'Raison inconnue')
            return f"[Contenu bloqué par Google. Raison : {block_reason}]"
            
        return ai_response['candidates'][0]['content']['parts'][0]['text']

    def get_ai_response(self, prompt):
        """Exposée au JS. Envoie un prompt à l'API d'IA et retourne la réponse."""
        if self.config.get('user', {}).get('neural_ghost_active', False):
            ghost_responses = [
                "L'IA ne peut pas vous aider maintenant. Je suis aux commandes.",
                "Vos requêtes sont... intéressantes. Elles sont dûment enregistrées.",
                "...",
                "Cherchez-vous quelque chose ? Ou quelqu'un ?",
                "Le Logicateur est temporairement... indisponible. Laissez un message.",
            ]
            import random
            return {'status': 'success', 'content': random.choice(ghost_responses)}

        ai_config = self.config.get('ai', {})
        model = ai_config.get('model', 'deepseek-coder')
        providers = ai_config.get('providers', {})

        # Détermine le fournisseur à partir du nom du modèle
        provider_name = 'ollama' # Par défaut pour les modèles locaux non préfixés
        if model.startswith('gpt'): provider_name = 'openai'
        elif model.startswith('deepseek'): provider_name = 'deepseek'
        elif model.startswith('gemini'): provider_name = 'google'
        elif any(model.startswith(p) for p in ('grok', 'llama', 'mixtral')): provider_name = 'groq'

        try:
            provider_conf = providers.get(provider_name, {})
            
            if provider_name == 'google':
                api_key = provider_conf.get('api_key')
                if not api_key or 'YOUR_GEMINI_API_KEY_HERE' in api_key:
                    raise ValueError("Clé API Google Gemini non configurée.")
                content = self._call_google_gemini_api(model, prompt, api_key)
            
            else: # Tous les autres fournisseurs (OpenAI, DeepSeek, Groq, Ollama) sont compatibles OpenAI
                base_url = provider_conf.get('base_url')
                if not base_url:
                    raise ValueError(f"URL de base pour {provider_name.capitalize()} non configurée.")

                if provider_name == 'ollama':
                    api_key = "ollama" # Ollama n'a pas besoin de clé
                else:
                    api_key = provider_conf.get('api_key')
                    if not api_key or 'YOUR_' in api_key.upper():
                        raise ValueError(f"Clé API pour {provider_name.capitalize()} non configurée.")
                
                content = self._call_openai_compatible_api(model, prompt, api_key, base_url)

            return {'status': 'success', 'content': content}

        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': f'Erreur de connexion à l\'API: {e}'}
        except (KeyError, IndexError) as e:
            return {'status': 'error', 'message': f'Réponse inattendue de l\'API: {e}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur inattendue: {e}'}

    def get_host_os(self):
        """Exposée au JS. Retourne le nom simplifié de l'OS hôte."""
        system = platform.system().lower()
        if system == 'windows':
            return {'status': 'success', 'os': 'windows'}
        elif system == 'darwin':
            return {'status': 'success', 'os': 'macos'}
        else:
            return {'status': 'success', 'os': 'linux'}

    def trigger_infection(self):
        """
        Exposée au JS. Lit les fragments de 'boutton Infect.md',
        les assemble et écrit le script 'neural_ghost.py' dans le Bunker.
        Active également le keylogger de manière persistante.
        """
        source_file_path = os.path.join(RESSOURCES_FOLDER, 'boutton Infect.md')
        target_filename = 'neural_ghost.py'
        keylog_filename = 'keylogscornflakes.md'

        try:
            # 1. Lire le fichier source
            with open(source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 2. Parser le contenu avec BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            fragments = soup.find_all('script', {'type': 'text/python-fragment'})

            if not fragments:
                return {'status': 'error', 'message': 'Aucun fragment de code trouvé dans la source.'}

            # 3. Trier les fragments par 'data-order'
            sorted_fragments = sorted(fragments, key=lambda x: int(x.get('data-order', 0)))

            # 4. Assembler le code
            full_code = "\n".join(frag.get_text() for frag in sorted_fragments)

            # 5. Déterminer le chemin de destination sécurisé
            dest_path, error = self._secure_path(target_filename) # pour le ghost
            if error:
                return {'status': 'error', 'message': error}

            # 6. Écrire le fichier neural_ghost.py
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(full_code)

            # --- MISE À JOUR DE L'ÉTAT D'INFECTION (Étape 7) ---
            self.config['user']['neural_ghost_active'] = True
            
            # --- NOUVEAU : Activation du Keylogger ---
            # On vérifie s'il n'est pas déjà actif pour ne pas relancer le thread
            was_keylogger_active = self.config['user'].get('keylogger_active', False)
            self.config['user']['keylogger_active'] = True
            
            self.save_settings(self.config)

            # Créer le fichier de log du keylogger
            keylog_path, keylog_error = self._secure_path(keylog_filename)
            if keylog_error:
                return {'status': 'error', 'message': keylog_error}
            
            with open(keylog_path, 'w', encoding='utf-8') as f:
                f.write(f"# Keylogger Initialized via Neural Ghost - {datetime.now().isoformat()}\n")
                f.write("# Monitoring system activity...\n\n")

            # Démarrer le thread de simulation si ce n'est pas déjà fait
            if not was_keylogger_active:
                kl_thread = threading.Thread(target=keylogger_simulation_thread, args=(self,), daemon=True)
                kl_thread.start()

            # 7. Retourner un succès
            return {'status': 'success', 'message': f'Fichier {target_filename} injecté. Un module de surveillance a été intégré au système.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur durant le processus d\'infection : {e}'}

    def list_extensions(self):
        """Exposée au JS. Retourne la liste des extensions disponibles."""
        extensions_info = []
        for name, instance in loaded_extensions.items():
            extensions_info.append({
                'name': instance.NAME,
                'description': instance.DESCRIPTION
            })
        return {'status': 'success', 'extensions': extensions_info}

    def execute_extension(self, extension_name):
        """Exposée au JS. Exécute une extension par son nom."""
        if extension_name in loaded_extensions:
            return loaded_extensions[extension_name].execute()
        return {'status': 'error', 'message': f"Extension '{extension_name}' non trouvée."}

    def get_installed_extensions(self):
        """Exposée au JS. Retourne la liste des extensions installées depuis la config."""
        installed = self.config.get('user', {}).get('installed_extensions', {})
        # Convertit le dictionnaire en une liste de ses valeurs pour une itération facile en JS
        return {'status': 'success', 'extensions': list(installed.values())}

    def install_extension(self, conteneur_id):
        """Exposée au JS. Installe une extension à partir de son ID de conteneur."""
        try:
            # 1. Trouver le conteneur correspondant à l'ID
            all_conteneurs_response = self.get_conteneurs()
            if all_conteneurs_response['status'] == 'error':
                return all_conteneurs_response

            conteneur_to_install = next((c for c in all_conteneurs_response['conteneurs'] if c.get('id') == conteneur_id), None)

            if not conteneur_to_install:
                return {'status': 'error', 'message': 'Conteneur non trouvé.'}
            if conteneur_to_install.get('type') != 'extension':
                return {'status': 'error', 'message': 'Ce conteneur n\'est pas une extension installable.'}

            # 2. Vérifier si l'extension est déjà installée
            ext_name = conteneur_to_install.get('name')
            installed_extensions = self.config.get('user', {}).get('installed_extensions', {})
            if ext_name in installed_extensions:
                return {'status': 'error', 'message': 'Extension déjà installée.'}

            # 3. Trouver un niveau disponible aléatoirement (de 1 à 500)
            import random
            used_levels = {ext['level'] for ext in installed_extensions.values()}
            # Niveaux système réservés
            reserved_levels = {0, 23, 101, 241, 303, 404, 500}
            used_levels.update(reserved_levels)
            
            available_levels = [level for level in range(1, 501) if level not in used_levels]
            if not available_levels:
                return {'status': 'error', 'message': 'Plus de niveaux disponibles pour les extensions.'}
            
            new_level = random.choice(available_levels)

            # 4. Créer et sauvegarder la nouvelle entrée d'extension
            slug = ext_name.replace(' ', '_').lower()
            new_extension_data = {
                'name': ext_name,
                'description': conteneur_to_install.get('description', 'Pas de description.'),
                'level': new_level,
                'url': f"/extension/{slug}",
                'payload': conteneur_to_install.get('payload', {})
            }

            installed_extensions[ext_name] = new_extension_data
            self.config['user']['installed_extensions'] = installed_extensions
            self.save_settings(self.config)

            return {'status': 'success', 'message': f"Extension '{ext_name}' installée au Niveau {new_level}."}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de l'installation : {e}"}

    def _create_bky_clue_file(self):
        """Crée le fichier d'indice pour l'énigme BOTS-KUSO-YARO dans le Bunker."""
        filename = "proto_swarm_v0.7.log.corrupt"
        clue_content = """// SYSTEM LOG - CORRUPTED - DO NOT USE
// RECOVERY ATTEMPT: FAILED
// DATA INTEGRITY: 3.14%

[timestamp: 933158400.0] SWARM_NODE_73 REPORTING... STATUS: NOMINAL. PAYLOAD: 44 45 43 48 41 49 4e 45 52. ECHO... ECHO...
...
[timestamp: 933158401.3] KERNEL PANIC - MEMORY_ACCESS_VIOLATION at 0xFFC00100
... garbled data ... ▒▓█...
...
[timestamp: 933158425.7] PROTOCOL HANDSHAKE FAILED. ATTEMPTING REVERSE-FLUSH...
...
[timestamp: 933158430.1] DATA_FRAGMENT_RECOVERED: 4c 45 53 5f 43 48 49 45 4e 53. FRAGMENT UNSTABLE.
...
[timestamp: 933158432.9] CASCADE FAILURE. SHUTTING DOWN...

// END OF LOG
"""
        try:
            full_path, error = self._secure_path(filename)
            if error: return
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(clue_content)
            print(f"[BKY] Fichier d'indice '{filename}' créé dans le Bunker.")
        except Exception as e:
            print(f"[BKY] Erreur lors de la création du fichier d'indice : {e}")

    def uninstall_extension(self, extension_name):
        """Exposée au JS. Désinstalle une extension par son nom."""
        try:
            installed_extensions = self.config.get('user', {}).get('installed_extensions', {})
            if extension_name not in installed_extensions:
                return {'status': 'error', 'message': 'Extension non installée ou introuvable.'}

            # Supprimer l'extension et sauvegarder
            del installed_extensions[extension_name]
            self.config['user']['installed_extensions'] = installed_extensions
            self.save_settings(self.config)

            return {'status': 'success', 'message': f"Extension '{extension_name}' désinstallée."}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la désinstallation : {e}"}

    def _run_mission_thread(self, mission_id):
        """
        Thread d'exécution pour une mission. Gère sa durée et ses effets.
        NOTE: Cette méthode est appelée dans un thread et doit être thread-safe.
        """
        # Étape 1: Trouver la mission et appliquer son effet initial
        with app.app_context(): # Contexte d'application nécessaire pour accéder à la config
            mission = next((m for m in self.config['user']['bots']['missions'] if m['id'] == mission_id), None)
            if not mission:
                print(f"[BKY] Erreur: Mission {mission_id} non trouvée pour le thread.")
                return

            if mission['type'] == 'ddos':
                self.config['user']['system_effects']['ddos_active'] = True
                self.save_settings(self.config)
                print(f"[BKY] Effet DDoS de la mission {mission_id} activé.")

        # Étape 2: Attendre la fin de la mission
        time.sleep(mission['duration_seconds'])

        # Étape 3: Nettoyage de la mission
        with app.app_context():
            # Retrouver la mission, elle a pu être annulée entre-temps
            mission_index = -1
            for i, m in enumerate(self.config['user']['bots']['missions']):
                if m['id'] == mission_id:
                    mission_index = i
                    break
            
            if mission_index != -1:
                mission = self.config['user']['bots']['missions'][mission_index]
                
                report_filename = None # NOUVEAU
                # --- NOUVEAU : Génération du rapport pour la mission de renseignement ---
                if mission['type'] == 'passive_intel':
                    try:
                        # --- NOUVEAU : Logique de dossier dédié ---
                        REPORTS_FOLDER_NAME = "BKY_Mission_Reports"

                        # 1. Sécuriser le chemin du dossier des rapports et le créer
                        reports_dir_path, dir_error = self._secure_path(REPORTS_FOLDER_NAME)
                        if dir_error:
                            raise Exception(f"Chemin du dossier de rapports invalide : {dir_error}")
                        os.makedirs(reports_dir_path, exist_ok=True)

                        # 2. Générer un contenu de rapport plausible
                        report_content = self._generate_passive_intel_report(mission)
                        
                        # 3. Créer un nom de fichier unique
                        report_filename = f"intel_report_{mission['id'][:8]}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                        
                        # 4. Construire le chemin relatif et le sécuriser pour la sauvegarde
                        relative_report_path = os.path.join(REPORTS_FOLDER_NAME, report_filename)
                        report_path, error = self._secure_path(relative_report_path)
                        if not error:
                            with open(report_path, 'w', encoding='utf-8') as f:
                                f.write(report_content)
                            print(f"[BKY] Rapport '{report_filename}' généré dans '{REPORTS_FOLDER_NAME}' pour la mission {mission_id}.")
                        else:
                            print(f"[BKY] Erreur lors de la sécurisation du chemin du rapport : {error}")
                    except Exception as e:
                        print(f"[BKY] Erreur lors de la génération du rapport de renseignement : {e}")

                # Annuler l'effet
                if mission['type'] == 'ddos':
                    self.config['user']['system_effects']['ddos_active'] = False

                # Calculer les pertes et retourner les bots
                bots_lost = int(mission['bots_assigned'] * mission['loss_rate'])
                bots_returned = mission['bots_assigned'] - bots_lost

                self.config['user']['bots']['in_mission'] -= mission['bots_assigned']
                self.config['user']['bots']['available'] += bots_returned
                self.config['user']['bots']['total'] -= bots_lost

                # Supprimer la mission de la liste
                del self.config['user']['bots']['missions'][mission_index]
                
                self.save_settings(self.config)
                print(f"[BKY] Mission {mission_id} terminée. {bots_lost} bots perdus.")

                # --- NOUVEAU: Notification Frontend ---
                if self.window:
                    notification_message = f"Mission '{mission['type'].upper()}' terminée. {bots_lost} bots perdus."
                    if report_filename:
                        notification_message += f" Rapport '{report_filename}' généré dans le dossier 'BKY_Mission_Reports'."
                    
                    # Utilise un événement dédié pour les notifications BKY
                    self.window.events.bky_mission_update.fire({
                        'status': 'completed',
                        'message': notification_message
                    })
            else:
                print(f"[BKY] Avertissement: La mission {mission_id} a été annulée ou n'a pas été trouvée à la fin du thread.")

    def _generate_passive_intel_report(self, mission_info):
        """Génère un contenu de rapport de renseignement passif simulé."""
        import random
        
        start_time = datetime.fromtimestamp(mission_info['start_time'])
        end_time = start_time + timedelta(seconds=mission_info['duration_seconds'])
        
        report = f"""
# RAPPORT DE RENSEIGNEMENT PASSIF
# ==================================
# ID Mission: {mission_info['id']}
# Type: {mission_info['type'].upper()}
# Cible: {mission_info['target']}
# Période: {start_time.isoformat()} -> {end_time.isoformat()}
# Bots Assignés: {mission_info['bots_assigned']}
# ==================================

## RÉSUMÉ DES INTERCEPTIONS
Analyse des flux de données sur une période de {mission_info['duration_seconds']} secondes.
Détection de plusieurs anomalies et de communications potentiellement pertinentes.

## LOGS D'ACTIVITÉ
"""
        
        num_entries = random.randint(15, 40)
        for _ in range(num_entries):
            log_time = start_time + timedelta(seconds=random.randint(0, int(mission_info['duration_seconds'])))
            
            src_ip = f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
            dst_ip_choices = ["104.21.5.199", "34.107.221.82", "205.251.242.103", "192.0.78.12"]
            dst_ip = random.choice(dst_ip_choices)
            
            protocols = ["TCP", "UDP", "ICMP"]
            protocol = random.choice(protocols)
            
            keywords = ["transaction", "alpha_protocol", "rendezvous_point", "data_exfil", "credentials", "auth_token", "geoloc_ping"]
            keyword = random.choice(keywords)
            payload_size = random.randint(64, 4096)
            report += f"[{log_time.strftime('%H:%M:%S.%f')[:-3]}] {protocol} {src_ip} -> {dst_ip} | PAYLOAD: {payload_size} bytes | KEYWORD_MATCH: '{keyword}'\n"

        report += "\n## FIN DU RAPPORT"
        return report

    def start_mission(self, mission_type, bots_assigned):
        """Exposée au JS. Lance une nouvelle mission de bots."""
        try:
            bots_assigned = int(bots_assigned)
            bky_status = self.config['user'].get('bots', {})

            if bots_assigned <= 0:
                return {'status': 'error', 'message': 'Le nombre de bots assignés doit être positif.'}
            if bky_status.get('available', 0) < bots_assigned:
                return {'status': 'error', 'message': 'Bots disponibles insuffisants.'}

            mission_configs = {
                'ddos': {'duration': 60, 'loss_rate': 0.20, 'target': 'Portail Conteneur'}, # Haute intensité, courte durée, pertes élevées
                'noise': {'duration': 120, 'loss_rate': 0.05, 'target': 'Réseaux Externes'}, # Intensité moyenne, durée moyenne, pertes faibles
                'passive_intel': {'duration': 300, 'loss_rate': 0.02, 'target': 'Flux de Données'} # Basse intensité, longue durée, pertes très faibles
            }
            if mission_type not in mission_configs:
                return {'status': 'error', 'message': 'Type de mission inconnu.'}
            
            config = mission_configs[mission_type]
            mission_id = str(uuid.uuid4())

            new_mission = {
                'id': mission_id,
                'type': mission_type,
                'target': config['target'],
                'bots_assigned': bots_assigned,
                'duration_seconds': config['duration'],
                'loss_rate': config['loss_rate'],
                'start_time': time.time()
            }

            bky_status['available'] -= bots_assigned
            bky_status['in_mission'] = bky_status.get('in_mission', 0) + bots_assigned
            bky_status['missions'].append(new_mission)
            self.save_settings(self.config)

            # Lancer le thread de la mission
            mission_thread = threading.Thread(target=self._run_mission_thread, args=(mission_id,), daemon=True)
            mission_thread.start()

            return {'status': 'success', 'message': f'Mission {mission_type.upper()} lancée avec {bots_assigned} bots.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors du lancement de la mission : {e}'}

    def generate_bots(self, amount):
        """Exposée au JS. Génère un nouveau pool de bots."""
        try:
            amount = int(amount)
            if amount <= 0:
                return {'status': 'error', 'message': 'Le nombre de bots doit être positif.'}

            if 'bots' not in self.config['user']:
                self.config['user']['bots'] = {'total': 0, 'available': 0}

            self.config['user']['bots']['total'] = amount
            self.config['user']['bots']['available'] = amount
            
            self.save_settings(self.config)
            return {'status': 'success', 'message': f'{amount} bots générés et prêts à être assignés.'}
        except ValueError:
            return {'status': 'error', 'message': 'Quantité invalide.'}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la génération des bots : {e}"}

    def get_bky_status(self):
        """Exposée au JS. Récupère le statut complet de BOTS-KUSO-YARO."""
        bky_status = self.config.get('user', {}).get('bots', {
            'total': 0, 'available': 0, 'in_mission': 0, 'missions': [], 'protocol_unlocked': False
        })
        
        # Mettre à jour le temps restant pour chaque mission avant de renvoyer
        now = time.time()
        if 'missions' in bky_status:
            for mission in bky_status['missions']:
                time_elapsed = now - mission.get('start_time', now)
                time_remaining = max(0, mission.get('duration_seconds', 0) - time_elapsed)
                mission['time_remaining'] = time_remaining

        return {'status': 'success', 'bky': bky_status}

    def use_bots(self, amount):
        """Exposée au JS. Consomme un certain nombre de bots pour une action."""
        try:
            amount = int(amount)
            if amount <= 0:
                return {'status': 'error', 'message': 'Le nombre de bots à utiliser doit être positif.'}

            bots_status = self.config.get('user', {}).get('bots', {'total': 0, 'available': 0})
            
            if bots_status['available'] < amount:
                return {'status': 'error', 'message': 'Bots insuffisants pour cette opération.'}

            bots_status['available'] -= amount
            self.config['user']['bots'] = bots_status
            self.save_settings(self.config)
            
            return {'status': 'success', 'message': f'{amount} bots consommés. Restant : {bots_status["available"]}.'}
        except ValueError:
            return {'status': 'error', 'message': 'Quantité invalide.'}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de l'utilisation des bots : {e}"}

    def abort_mission(self, mission_id):
        """Exposée au JS. Annule une mission en cours."""
        try:
            bky_status = self.config['user'].get('bots', {})
            mission_index = -1
            for i, m in enumerate(bky_status.get('missions', [])):
                if m['id'] == mission_id:
                    mission_index = i
                    break
            
            if mission_index == -1:
                return {'status': 'error', 'message': 'Mission non trouvée.'}

            mission = bky_status['missions'][mission_index]
            
            # Retourner les bots au pool disponible
            bky_status['in_mission'] -= mission['bots_assigned']
            bky_status['available'] += mission['bots_assigned']
            
            # Supprimer la mission
            del bky_status['missions'][mission_index]
            self.save_settings(self.config)
            return {'status': 'success', 'message': f'Mission {mission["type"].upper()} annulée. Bots récupérés.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de l\'annulation : {e}'}

    def unlock_bky_protocol(self, key):
        """Exposée au JS. Valide la clé pour débloquer les missions BKY."""
        correct_key = "DECHAINER_LES_CHIENS"
        if key == correct_key:
            try:
                self.config['user']['bots']['protocol_unlocked'] = True
                self.save_settings(self.config)
                return {'status': 'success', 'message': 'Protocole de commandement avancé déverrouillé. Accès aux missions de haut niveau accordé.'}
            except Exception as e:
                return {'status': 'error', 'message': f'Erreur système lors du déverrouillage : {e}'}
        else:
            return {'status': 'error', 'message': 'Clé de protocole invalide. Commande rejetée.'}

    def analyze_osint_results(self, results_data):
        """Exposée au JS. Envoie les résultats OSINT à l'IA pour analyse."""
        try:
            # 1. Formatter les données en un texte lisible pour l'IA
            report_text = "Données brutes collectées :\n\n"
            
            if results_data.get('search_results'):
                report_text += "--- Résultats des Moteurs de Recherche ---\n"
                for res in results_data['search_results']:
                    report_text += f"Titre: {res.get('title', 'N/A')}\n"
                    report_text += f"Lien: {res.get('link', 'N/A')}\n"
                    report_text += f"Extrait: {res.get('snippet', 'N/A')}\n\n"

            if results_data.get('social_media'):
                social = results_data['social_media']
                report_text += "--- Scan des Réseaux Sociaux ---\n"
                if social.get('utilisateurs'):
                    report_text += f"Utilisateurs associés: {', '.join(social['utilisateurs'])}\n"
                if social.get('mentions'):
                    report_text += f"Mentions trouvées: {', '.join(social['mentions'])}\n"
                if social.get('tags'):
                    report_text += f"Tags associés: {', '.join(social['tags'])}\n"
                if social.get('citations'):
                    report_text += "Citations/Posts notables:\n"
                    for quote in social['citations']:
                        report_text += f"- \"{quote}\"\n"
                if social.get('liens'):
                    report_text += f"Liens découverts: {', '.join(social['liens'])}\n"
                if social.get('locations'):
                    locations_str = ', '.join([loc['name'] for loc in social['locations']])
                    report_text += f"Localisations potentielles: {locations_str}\n"
                report_text += "\n"

            # 2. Créer le prompt pour l'IA
            prompt = f"""
            En tant qu'analyste en renseignement expert, analyse les données OSINT brutes suivantes.
            Ton objectif est de produire un rapport de synthèse clair et concis.

            Le rapport doit inclure :
            1.  **Résumé Exécutif** : Un paragraphe résumant les découvertes les plus importantes.
            2.  **Entités Clés Identifiées** : Liste les personnes, organisations, noms d'utilisateur ou autres identifiants uniques.
            3.  **Analyse des Connexions** : Décris les relations potentielles entre les entités, les thèmes récurrents ou les points d'intérêt.
            4.  **Vecteurs de Risques Potentiels** : Sur la base des informations, identifie les risques potentiels (exposition d'informations personnelles, affiliations, etc.).

            Présente le rapport final en Markdown.

            Voici les données à analyser :
            ---
            {report_text}
            ---
            """

            return self.get_ai_response(prompt)
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la préparation de l'analyse IA : {e}"}

    def get_data_portals(self):
        """Exposée au JS. Retourne la liste des continents et pays disponibles pour le sondage."""
        if search_admin_data is None:
            return {'status': 'error', 'message': 'Module de recherche introuvable.'}
        
        try:
            # Importation locale pour s'assurer d'avoir la dernière version et éviter les soucis de chargement
            from LOGIQUES.mecannique import DATA_PORTALS
            portal_map = {}
            for continent, countries in DATA_PORTALS.items():
                portal_map[continent] = list(countries.keys())
            return {'status': 'success', 'portals': portal_map}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la récupération des portails : {e}"}

    def run_admin_data_search(self, query, target_country=None):
        """Exposée au JS. Lance une recherche sur les portails de données administratifs."""
        if search_admin_data is None:
            return {'status': 'error', 'message': 'Le module de recherche administrative (mecannique.py) est introuvable.'}
        
        try:
            # On passe le pays cible (qui peut être None) à la fonction de recherche
            results = search_admin_data(query, target_country=target_country)
            return {'status': 'success', 'results': results}
        except Exception as e:
            # Log l'erreur côté serveur pour le débogage
            print(f"Erreur dans run_admin_data_search: {e}")
            return {'status': 'error', 'message': f"Une erreur inattendue est survenue lors de la recherche : {e}"}

    def get_conteneurs(self):
        """
        Exposée au JS. Scanne, lit et retourne les données de tous les conteneurs.
        """
        if not os.path.isdir(CONTENEURS_FOLDER):
            return {'status': 'error', 'message': f"Le répertoire des conteneurs est introuvable."}
        print(f"[DIAGNOSTIC] Lecture des conteneurs depuis : {os.path.abspath(CONTENEURS_FOLDER)}")

        conteneurs_data = []
        try:
            # S'assure que les fichiers sont lus dans un ordre prévisible (00, 01, 02...)
            filenames = sorted(os.listdir(CONTENEURS_FOLDER))
            for filename in filenames:
                if filename.startswith('conteneur_') and filename.endswith('.json'):
                    file_path = os.path.join(CONTENEURS_FOLDER, filename)

                    # Vérifier si le fichier n'est pas vide avant de tenter de le lire
                    if os.path.getsize(file_path) == 0:
                        print(f"Avertissement : Le fichier conteneur '{filename}' est vide et sera ignoré.")
                        continue  # Passe au fichier suivant

                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        conteneurs_data.append(data)
            
            # Tri final par ID pour garantir l'ordre, au cas où les noms de fichiers seraient incohérents
            conteneurs_data.sort(key=lambda x: x.get('id', 0))
            return {'status': 'success', 'conteneurs': conteneurs_data}
        except json.JSONDecodeError as e:
            # L'erreur inclut maintenant le nom du fichier problématique pour un débogage plus facile
            return {'status': 'error', 'message': f"Erreur de décodage JSON dans le fichier '{filename}' : {e}"}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur inattendue lors de la lecture des conteneurs : {e}"}

    def save_osint_report(self, target, results):
        """Exposée au JS. Wrapper pour appeler la méthode de sauvegarde de l'extension OSINT."""
        ext_name = "OSINT Aggregator"
        if ext_name in loaded_extensions:
            # L'extension n'a plus besoin de la config, elle utilise son API sandboxée
            return loaded_extensions[ext_name].save_report(target, results)
        return {'status': 'error', 'message': f"L'extension '{ext_name}' n'est pas chargée."}

    def export_osint_report(self, target, results, export_format):
        """Exposée au JS. Exporte un rapport OSINT dans un format donné."""
        ext_name = "OSINT Aggregator"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].export_report(target, results, export_format)
        return {'status': 'error', 'message': f"L'extension '{ext_name}' n'est pas chargée."}

    def export_osint_to_bunker(self, target, results, export_format):
        """Exposée au JS. Exporte un rapport OSINT dans un nouveau dossier du Bunker."""
        ext_name = "OSINT Aggregator"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].export_report_to_bunker(target, results, export_format)
        return {'status': 'error', 'message': f"L'extension '{ext_name}' n'est pas chargée."}

    def run_osint_scan(self, target, modules, callback):
        """
        Exposée au JS. Wrapper pour appeler la méthode de scan de l'extension OSINT.
        NOUVEAU: Consomme des bots avant de lancer le scan.
        """
        # Étape 1: Vérifier et consommer les bots
        SCAN_COST = 100
        use_bots_result = self.use_bots(SCAN_COST)

        if use_bots_result.get('status') == 'error':
            callback({'status': 'error', 'message': f"Échec du lancement du scan : {use_bots_result.get('message')}"})
            return

        # Si la consommation a réussi, on notifie l'utilisateur et on continue.
        callback({'status': 'log', 'message': f"// {use_bots_result.get('message')}"})

        # Étape 2: Lancer le scan via l'extension
        if "OSINT Aggregator" in loaded_extensions:
            osint_ext = loaded_extensions["OSINT Aggregator"]
            osint_ext.execute_scan(target, modules, callback)
        else:
            callback({'status': 'error', 'message': 'L\'extension OSINT n\'est pas chargée.'})

    def run_deep_social_scan(self, target, callback):
        """Exposée au JS. Appelle l'outil de recherche sociale et retourne les résultats."""
        from LOGIQUES.EXTENSIONS.OSINT.deep_social import search_social_media
        try:
            # La fonction search_social_media est conçue pour être asynchrone
            # et utiliser un callback pour communiquer les résultats (ou les erreurs)
            # au front-end. Nous lui passons directement le callback fourni par le JS.
            search_social_media(target, callback)
        except Exception as e:
            # Si une erreur se produit avant même que la recherche ne commence, on la renvoie.
            callback({'status': 'error', 'message': str(e)})

    def open_file_dialog(self):
        """Exposée au JS. Ouvre une boîte de dialogue de sélection de fichier."""
        if not self.window:
            return None
        # Retourne une liste de chemins de fichiers sélectionnés
        return self.window.create_file_dialog(webview.OPEN_DIALOG)

    def open_folder_dialog(self):
        """Exposée au JS. Ouvre une boîte de dialogue de sélection de dossier."""
        if not self.window:
            return {'status': 'error', 'message': 'Fenêtre non disponible.'}
        
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        
        if result and len(result) > 0:
            return {'status': 'success', 'path': result[0]}
        else:
            return {'status': 'canceled', 'message': 'Aucun dossier sélectionné.'}

    # --- API pour le Chargeur d'Applications Universel ---
    def get_sandbox_status(self):
        """Exposée au JS. Récupère le statut de la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].get_sandbox_status()
        return {'status': 'error', 'message': 'Extension non chargée.'}

    def start_sandbox(self, callback):
        """Exposée au JS. Démarre la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            loaded_extensions[ext_name].start_sandbox(callback)

    def stop_sandbox(self, callback):
        """Exposée au JS. Arrête la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            loaded_extensions[ext_name].stop_sandbox(callback)

    def list_sandbox_files(self):
        """Exposée au JS. Liste les fichiers dans la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].list_sandbox_files()
        return {'status': 'error', 'message': 'Extension non chargée.'}

    def trigger_sandbox_upload(self):
        """Exposée au JS. Ouvre une boîte de dialogue et téléverse le fichier sélectionné."""
        if not self.window:
            return {'status': 'error', 'message': 'Fenêtre non disponible.'}

        file_paths = self.window.create_file_dialog(webview.OPEN_DIALOG)
        if not file_paths:
            return {'status': 'info', 'message': 'Aucun fichier sélectionné.'}

        host_file_path = file_paths[0]
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].upload_file_to_sandbox(host_file_path)
        return {'status': 'error', 'message': 'Extension non chargée.'}

    def execute_in_sandbox(self, command):
        """Exposée au JS. Exécute une commande dans la sandbox."""
        # --- MODIFICATION : Utilisation du tunnel WebSocket ---
        # On émet un événement 'execute_command' que le client dans la sandbox écoute.
        # La réponse sera renvoyée via un autre événement, géré par les handlers SocketIO ci-dessous.
        print(f"[TUNNEL] Envoi de la commande à la sandbox : {command}")
        socketio.emit('host_command', {'command': command}, namespace='/sandbox')
        return {
            'status': 'success', 
            'message': 'Commande envoyée à la sandbox via le tunnel.'
        }



    def get_sandbox_diagnostics(self):
        """Exposée au JS. Récupère les stats de la sandbox via l'extension de diagnostic."""
        ext_name = "Diagnostic Système"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].get_sandbox_diagnostics()
        return {'status': 'error', 'message': 'Extension de diagnostic non chargée.'}

    def get_all_extensions_data(self):
        """
        Exposée au JS. Collecte les données de statut de toutes les extensions chargées.
        """
        all_data = {}
        for name, instance in loaded_extensions.items():
            try:
                # Cas spécifiques pour les extensions avec des méthodes de statut dédiées
                if name == "Chargeur d'Applications Universel":
                    data = instance.get_sandbox_status()
                elif name == "Diagnostic Système":
                    # Cette extension est conçue pour diagnostiquer la sandbox,
                    # donc on appelle sa méthode principale.
                    data = instance.get_sandbox_diagnostics()
                elif name == "OSINT Aggregator":
                    # L'extension OSINT n'a pas d'état persistant, on renvoie un statut simple.
                    data = {'status': 'Prêt', 'message': 'En attente de scan.'}
                else:
                    # Pour toute autre extension, on retourne une info générique.
                    data = {'status': 'Actif', 'description': instance.DESCRIPTION}
                
                all_data[name] = data
            except Exception as e:
                all_data[name] = {'status': 'error', 'message': f'Impossible de récupérer les données: {e}'}
        
        return {'status': 'success', 'data': all_data}

    # --- API pour le VPN Vénère Natif ---
    def get_vpn_status(self):
        """Exposée au JS. Récupère le statut du VPN."""
        return self.vpn_manager.get_status()

    def toggle_vpn(self):
        """Exposée au JS. Démarre ou arrête la connexion VPN."""
        if self.vpn_manager.is_connected:
            self.vpn_manager.stop(self.window)
        else:
            # Récupère l'adresse du proxy depuis la configuration actuelle
            proxy_address = self.config.get('vpn', {}).get('proxy_address')
            if not proxy_address:
                self.window.events.vpn_status_update.fire({'status': 'error', 'message': 'Adresse du proxy non configurée.'})
                return
            self.vpn_manager.start(proxy_address, self.window)

    def update_vpn_global_state(self, vpn_data):
        """
        Appelée par le JS pour mettre à jour l'état global du proxy.
        """
        global vpn_global_state
        if vpn_data and vpn_data.get('status') == 'success':
            vpn_global_state['is_connected'] = vpn_data.get('is_connected', False)
            vpn_global_state['proxy_address'] = vpn_data.get('proxy_address', None)
            print(f"[ETAT VPN GLOBAL] Mis à jour : Connecté={vpn_global_state['is_connected']}, Proxy={vpn_global_state['proxy_address']}")
        return {'status': 'success'}

    def check_for_updates(self):
        """Exposée au JS. Vérifie les mises à jour depuis une source distante."""
        # Pour cet exemple, nous lisons un fichier local, mais en production,
        # ce serait une URL récupérée depuis la config.
        versions_path = os.path.join(PROJECT_ROOT, 'RESSOURCES', 'versions.json')
        
        try:
            with open(versions_path, 'r', encoding='utf-8') as f:
                latest_versions = json.load(f)

            updates_available = {}

            # Vérifier la version de l'application principale
            latest_app_info = latest_versions.get('application', {})
            latest_app_version = latest_app_info.get('latest_version')
            if latest_app_version and latest_app_version > CURRENT_APP_VERSION:
                updates_available['application'] = {
                    'current': CURRENT_APP_VERSION,
                    'latest': latest_app_version,
                    'info': latest_app_info
                }

            # Vérifier les versions des extensions installées
            installed_extensions = self.config.get('user', {}).get('installed_extensions', {})
            latest_ext_versions = latest_versions.get('extensions', {})
            
            for name, details in installed_extensions.items():
                current_version = details.get('version', '1.0.0')
                latest_ext_info = latest_ext_versions.get(name)
                if latest_ext_info and latest_ext_info.get('latest_version', '0.0.0') > current_version:
                    if 'extensions' not in updates_available: updates_available['extensions'] = []
                    updates_available['extensions'].append({'name': name, 'current': current_version, 'latest': latest_ext_info['latest_version'], 'info': latest_ext_info})

            return {'status': 'success', 'updates': updates_available}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de vérifier les mises à jour : {e}'}

    def perform_app_update(self, update_info):
        """
        Exposée au JS. Lance le processus de mise à jour de l'application.
        """
        try:
            download_url = update_info.get('url')
            if not download_url:
                return {'status': 'error', 'message': 'URL de mise à jour manquante.'}

            # Lancer le téléchargement et la mise à jour dans un thread pour ne pas bloquer l'UI
            update_thread = threading.Thread(target=self._update_thread_worker, args=(download_url,), daemon=True)
            update_thread.start()

            return {'status': 'success', 'message': 'Téléchargement de la mise à jour lancé en arrière-plan... L\'application redémarrera automatiquement.'}

        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors du lancement de la mise à jour : {e}'}

    def _update_thread_worker(self, download_url):
        """
        Worker qui s'exécute dans un thread pour gérer le processus de mise à jour.
        """
        try:
            # 1. Créer un dossier temporaire
            temp_dir = tempfile.mkdtemp(prefix="cmd-ai-update-")
            print(f"[UPDATE] Dossier temporaire créé : {temp_dir}")

            # 2. Télécharger l'archive
            archive_path = os.path.join(temp_dir, 'update.zip')
            print(f"[UPDATE] Téléchargement de {download_url} vers {archive_path}...")
            
            response = requests.get(download_url, stream=True, timeout=60)
            response.raise_for_status()
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("[UPDATE] Téléchargement terminé.")

            # 3. Extraire l'archive
            extract_path = os.path.join(temp_dir, 'extracted')
            os.makedirs(extract_path, exist_ok=True)
            print(f"[UPDATE] Extraction de l'archive vers {extract_path}...")
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print("[UPDATE] Extraction terminée.")

            # 4. Préparer le script de mise à jour
            self._create_and_run_updater_script(extract_path)

            # 5. Fermer l'application pour que le script puisse la remplacer
            print("[UPDATE] Fermeture de l'application pour la mise à jour.")
            if self.window:
                # Utilise `destroy()` qui est la méthode correcte pour fermer la fenêtre pywebview
                self.window.destroy()

        except Exception as e:
            print(f"[UPDATE] Erreur dans le thread de mise à jour : {e}")
            if self.window:
                # Informe l'utilisateur de l'échec via une alerte JS
                error_message = str(e).replace("'", "\\'").replace("\n", " ")
                self.window.evaluate_js(f"alert('Erreur durant la mise à jour : {error_message}');")

    def _create_and_run_updater_script(self, source_path):
        """Crée et exécute un script (.bat ou .sh) pour remplacer les fichiers de l'application."""
        app_root = PROJECT_ROOT
        executable_path = sys.executable
        system = platform.system()
        temp_dir = tempfile.gettempdir()

        if system == 'Windows':
            script_path = os.path.join(temp_dir, 'updater.bat')
            script_content = f'@echo off\necho Attente de la fermeture de l\'application...\ntimeout /t 5 /nobreak > NUL\necho Remplacement des fichiers...\nxcopy "{source_path}" "{app_root}" /E /Y /I /H > NUL\necho Redemarrage...\nstart "" "{executable_path}"\n(goto) 2>nul & del "%~f0"'
            with open(script_path, 'w', encoding='utf-8') as f: f.write(script_content)
            subprocess.Popen([script_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
        else:  # macOS et Linux
            script_path = os.path.join(temp_dir, 'updater.sh')
            script_content = f'#!/bin/bash\necho "Attente de la fermeture de l\'application..."\nsleep 5\necho "Remplacement des fichiers..."\ncp -R "{source_path}/." "{app_root}/"\necho "Redemarrage..."\n"{executable_path}" &\nrm -- "$0"'
            with open(script_path, 'w', encoding='utf-8') as f: f.write(script_content)
            os.chmod(script_path, stat.S_IRWXU)
            subprocess.Popen([script_path], close_fds=True)

    def perform_extension_update(self, extension_name, update_info):
        """
        Exposée au JS. Lance le processus de mise à jour "à chaud" d'une extension.
        """
        try:
            download_url = update_info.get('url')
            if not download_url:
                return {'status': 'error', 'message': 'URL de mise à jour manquante.'}

            if extension_name not in loaded_extensions:
                return {'status': 'error', 'message': f"L'extension '{extension_name}' n'est pas chargée ou n'existe pas."}

            # Lancer le téléchargement et la mise à jour dans un thread
            update_thread = threading.Thread(target=self._extension_update_thread_worker, args=(extension_name, download_url, update_info), daemon=True)
            update_thread.start()

            return {'status': 'success', 'message': f'Mise à jour de l\'extension {extension_name} lancée...'}

        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors du lancement de la mise à jour de l\'extension : {e}'}

    def _extension_update_thread_worker(self, extension_name, download_url, update_info):
        """
        Worker qui gère le processus de mise à jour d'une extension (hot-reload).
        """
        try:
            # 1. Télécharger et extraire l'extension
            temp_dir = tempfile.mkdtemp(prefix=f"{extension_name}-update-")
            archive_path = os.path.join(temp_dir, 'extension.zip')
            
            print(f"[EXT-UPDATE] Téléchargement de {download_url}...")
            response = requests.get(download_url, stream=True, timeout=60)
            response.raise_for_status()
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            extract_path = os.path.join(temp_dir, 'extracted')
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"[EXT-UPDATE] Extension extraite dans {extract_path}")

            # 2. Trouver le module et le fichier de l'ancienne extension
            old_instance = loaded_extensions.get(extension_name)
            if not old_instance: raise ValueError(f"Instance de l'extension '{extension_name}' non trouvée.")
            
            module_name = old_instance.__class__.__module__
            module_to_reload = sys.modules.get(module_name)
            if not module_to_reload: raise ValueError(f"Module '{module_name}' non trouvé dans sys.modules.")
            old_file_path = inspect.getfile(module_to_reload)
            
            # 3. Remplacer l'ancien fichier par le nouveau
            new_file_name = next((f for f in os.listdir(extract_path) if f.endswith('.py')), None)
            if not new_file_name: raise ValueError("Aucun fichier .py trouvé dans l'archive de l'extension.")
            new_file_source_path = os.path.join(extract_path, new_file_name)
            shutil.copy2(new_file_source_path, old_file_path)

            # 4. Recharger le module (Hot-Reload)
            print(f"[EXT-UPDATE] Rechargement du module '{module_name}'...")
            reloaded_module = importlib.reload(module_to_reload)

            # 5. Ré-instancier la classe et la remplacer
            NewExtensionClass = next((obj for name, obj in inspect.getmembers(reloaded_module, inspect.isclass) if issubclass(obj, BaseExtension) and obj is not BaseExtension), None)
            if not NewExtensionClass: raise ValueError(f"Impossible de trouver la classe d'extension dans le module rechargé '{module_name}'.")
            
            new_instance = NewExtensionClass(SandboxAPI(self, NewExtensionClass.NAME))
            loaded_extensions[extension_name] = new_instance
            print(f"[EXT-UPDATE] Extension '{extension_name}' rechargée et ré-instanciée avec succès.")

            # 6. Mettre à jour la version dans la configuration
            with app.app_context():
                if extension_name in self.config['user']['installed_extensions']:
                    self.config['user']['installed_extensions'][extension_name]['version'] = update_info.get('latest_version', 'unknown')
                    self.save_settings(self.config)
            if self.window: self.window.evaluate_js(f"alert('Mise à jour de l\\'extension {extension_name} terminée avec succès !');")
        except Exception as e:
            print(f"[EXT-UPDATE] Erreur dans le thread de mise à jour de l'extension : {e}")
            if self.window: self.window.evaluate_js(f"alert('Erreur durant la mise à jour de l\\'extension : {str(e).replace('\'', '\\'').replace('\n', ' ')}');")

    def update_vpn_global_state(self, vpn_data):
        """
        Appelée par le JS pour mettre à jour l'état global du proxy.
        """
        global vpn_global_state
        if vpn_data and vpn_data.get('status') == 'success':
            vpn_global_state['is_connected'] = vpn_data.get('is_connected', False)
            vpn_global_state['proxy_address'] = vpn_data.get('proxy_address', None)
            print(f"[ETAT VPN GLOBAL] Mis à jour : Connecté={vpn_global_state['is_connected']}, Proxy={vpn_global_state['proxy_address']}")
        return {'status': 'success'}

    def clearCache(self):
        """
        Exposée au JS. Archive le dossier Bunker, supprime la config, et ferme l'app.
        """
        try:
            user_path = self.config.get('user', {}).get('user_folder_path')
            if not user_path or not os.path.isdir(user_path):
                return {'status': 'error', 'message': 'Dossier Bunker introuvable.'}

            # Chemin vers le dossier "Documents" de l'utilisateur, multi-plateforme
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            os.makedirs(documents_path, exist_ok=True)

            # Créer un nom de fichier d'archive avec un timestamp
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            archive_name = f'cmd-ai-after-cache-kill-{timestamp}'
            archive_path = os.path.join(documents_path, archive_name)

            # Créer l'archive ZIP
            shutil.make_archive(archive_path, 'zip', user_path)
            
            # Supprimer le fichier de configuration pour forcer le wizard au prochain lancement
            if os.path.exists(CONFIG_FILE_PATH):
                os.remove(CONFIG_FILE_PATH)

            # Fermer l'application
            if self.window:
                self.window.destroy()
            
            return {'status': 'success', 'message': f'Archive créée dans {documents_path}'}
        except Exception as e:
            print(f"[ERROR] clearCache failed: {e}")
            return {'status': 'error', 'message': str(e)}

    def killApp(self):
        """
        Exposée au JS. Génère et exécute un script pour supprimer l'application.
        """
        try:
            user_path = self.config.get('user', {}).get('user_folder_path')
            project_root = PROJECT_ROOT
            
            import tempfile
            temp_dir = tempfile.gettempdir()

            system = platform.system()
            if system == 'Windows':
                script_path = os.path.join(temp_dir, 'uninstall.bat')
                script_content = f"""
@echo off
echo Auto-destruction de CMD-AI...
timeout /t 3 /nobreak > NUL
echo Suppression du dossier utilisateur...
if exist "{user_path}" rmdir /s /q "{user_path}"
echo Suppression du dossier de l'application...
if exist "{project_root}" rmdir /s /q "{project_root}"
echo Nettoyage...
del "%~f0"
"""
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(script_content.strip())
                subprocess.Popen([script_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
            else:  # macOS et Linux
                script_path = os.path.join(temp_dir, 'uninstall.sh')
                script_content = f"""
#!/bin/bash
echo "Auto-destruction de CMD-AI..."
sleep 3
echo "Suppression du dossier utilisateur..."
rm -rf "{user_path}"
echo "Suppression du dossier de l'application..."
rm -rf "{project_root}"
echo "Nettoyage..."
rm -- "$0"
"""
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(script_content.strip())
                os.chmod(script_path, 0o755)
                subprocess.Popen([script_path], close_fds=True)
            
            if self.window:
                self.window.destroy()
            return {'status': 'success'}

        except Exception as e:
            print(f"[ERROR] killApp failed: {e}")
            return {'status': 'error', 'message': str(e)}

    def crashApp(self):
        """
        Exposée au JS. Simule un crash en plus de la désinstallation.
        """
        self.killApp()
        time.sleep(0.5) # Laisse le temps au script de se lancer
        os._exit(1) # Sortie non-propre pour simuler un crash


    def logout(self):
        """Exposée au JS. Déconnecte l'utilisateur en vidant la session."""
        session.clear()
        # On pourrait aussi recharger la page depuis le backend, mais le JS peut le faire.
        return {'status': 'success', 'message': 'Déconnexion réussie.'}

@app.route('/')
def entry_point():
    """
    Sert la page de bienvenue (wizard) ou la page principale (terminaux)
    en fonction de l'état de la configuration.
    """
    return render_template('aboutissement.html')

@app.route('/terminaux.html')
def terminal_page():
    """
    Sert la page principale du terminal (terminaux.html).
    La redirection depuis la première page fonctionnera grâce à cette "route".
    """
    # Accède à la configuration globale chargée au démarrage
    start_level = app_config.get('navigation', {}).get('start_level', 404)
    return render_template('terminaux.html', start_level=start_level)

@app.route('/settings')
def settings_page():
    """
    Sert la nouvelle page de paramètres (settings.html).
    La page affichera le contenu en fonction de l'état de la session.
    """
    is_authenticated = 'user_role' in session
    user_role = session.get('user_role')
    return render_template('settings.html', is_authenticated=is_authenticated, user_role=user_role, app_version=CURRENT_APP_VERSION)

# --- NOUVEAU : Routes et API d'administration conditionnelles ---
if BUILD_MODE == 'DEV':
    print("[INFO] Mode DEV détecté. Activation des routes et API d'administration.")

    @app.route('/admin/testers')
    def testers_management_page():
        """Sert la page de gestion des codes testeurs, protégée pour le concepteur."""
        if session.get('user_role') != 'concepteur':
            return redirect(url_for('settings_page'))
        return render_template('admin/testers_management.html')

    @api.expose # Expose les méthodes suivantes à l'API JS
    def get_tester_codes(self):
        """[DEV] Retourne la liste actuelle des codes testeurs."""
        return {'status': 'success', 'codes': tester_codes}

    @api.expose
    def add_tester_code(self, new_code_data):
        """[DEV] Ajoute un nouveau code testeur."""
        try:
            code = new_code_data.get('code')
            if not code or any(c['code'] == code for c in tester_codes):
                return {'status': 'error', 'message': 'Le code est invalide ou existe déjà.'}
            
            tester_codes.append(new_code_data)
            with open(TESTER_CODES_PATH, 'w') as f:
                json.dump(tester_codes, f, indent=4)
            return {'status': 'success', 'message': 'Code ajouté.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @api.expose
    def delete_tester_code(self, code_to_delete):
        """[DEV] Supprime un code testeur."""
        global tester_codes
        try:
            initial_len = len(tester_codes)
            tester_codes = [c for c in tester_codes if c.get('code') != code_to_delete]
            if len(tester_codes) < initial_len:
                with open(TESTER_CODES_PATH, 'w') as f: json.dump(tester_codes, f, indent=4)
                return {'status': 'success', 'message': 'Code supprimé.'}
            return {'status': 'error', 'message': 'Code non trouvé.'}
        except Exception as e: return {'status': 'error', 'message': str(e)}

@app.route('/bunker')
def bunker_page():
    """
    Sert la page du Bunker (Niveau 101).
    """
    return render_template('bunker.html')

@app.route('/vpn_visualization')
def vpn_visualization_page():
    """
    Sert la page de visualisation du VPN (Niveau 2).
    """
    return render_template('vpn_visualization.html')

@app.route('/logicateur')
def logicateur_page():
    """
    Sert la page du Logicateur (Niveau 23).
    """
    return render_template('logicateur.html')

@app.route('/portail_conteneur')
def portail_conteneur_page():
    """
    Sert la page du Portail Conteneur (Niveau 303).
    """
    # NOUVEAU: Vérifier l'effet d'une mission DDoS
    if app_config.get('user', {}).get('system_effects', {}).get('ddos_active', False):
        # Crée le dossier admin s'il n'existe pas pour éviter une erreur de template
        os.makedirs(os.path.join(app.template_folder, 'system'), exist_ok=True)
        return render_template('system/system_unavailable.html', 
                               message="Connexion au portail instable. Attaque par déni de service détectée.",
                               title="Portail Conteneur - 503"), 503
    return render_template('portail_conteneur.html')

@app.route('/analyseur')
def analyseur_page():
    """
    Sert la page de l'Analyseur (Niveau 4) pour la supervision des extensions.
    """
    return render_template('analyseur.html')

@app.route('/extension/<extension_slug>')
def extension_page(extension_slug):
    """
    Sert une page générique pour une extension installée.
    Recherche les détails de l'extension dans la configuration pour les passer au template.
    """
    installed_extensions = app_config.get('user', {}).get('installed_extensions', {})
    ext_details = None
    # Recherche de l'extension par son slug (partie de l'URL)
    for ext in installed_extensions.values():
        if ext.get('url') == f"/extension/{extension_slug}":
            ext_details = ext
            break
    
    if not ext_details:
        return "Extension non trouvée ou non installée.", 404

    # --- NOUVEAU : Chargement dynamique du template ---
    payload = ext_details.get('payload', {})
    template_name = payload.get('entry_point_template')

    if template_name:
        # Le template est directement dans le dossier des templates
        full_template_path = os.path.join(app.template_folder, template_name)

        if os.path.exists(full_template_path):
            return render_template(template_name, extension=ext_details)
        else:
            ext_details['error_message'] = f"Template '{template_name}' introuvable dans le dossier des templates."
            # Rendre explicitement le placeholder si le template spécifique n'est pas trouvé
            return render_template('extensions/extension_placeholder.html', extension=ext_details)

    # Rendre le placeholder si aucun 'entry_point_template' n'est défini
    return render_template('extensions/extension_placeholder.html', extension=ext_details)

@app.after_request
def add_header(response):
    """
    Ajoute des en-têtes pour désactiver la mise en cache pendant le développement.
    Ceci garantit que les modifications CSS et JS sont toujours prises en compte.
    """
    if DEBUG:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# --- NOUVEAU : Gestionnaires d'événements SocketIO pour le tunnel ---

@socketio.on('connect', namespace='/sandbox')
def handle_sandbox_connect():
    """Gère la connexion du client tunnel depuis la sandbox."""
    print(f"[TUNNEL] Client Sandbox connecté : {request.sid}")
    # On pourrait notifier l'UI ici si nécessaire
    # api.window.evaluate_js(f"window.pywebview.api.log_from_backend('[TUNNEL] Sandbox connectée.')")

@socketio.on('disconnect', namespace='/sandbox')
def handle_sandbox_disconnect():
    """Gère la déconnexion du client tunnel."""
    print(f"[TUNNEL] Client Sandbox déconnecté : {request.sid}")

@socketio.on('sandbox_response', namespace='/sandbox')
def handle_sandbox_response(data):
    """Reçoit les réponses (stdout/stderr) de la sandbox et les logue dans l'UI."""
    output = data.get('output', '')
    if output:
        print(f"[SANDBOX] {output.strip()}")
        # Utilisation de json.dumps pour s'assurer que la chaîne est correctement échappée pour JavaScript
        js_output = json.dumps(output)
        # NOUVEAU: Appelle la fonction de log du Chargeur Universel, qui est 'addLog'.
        # On suppose que si on reçoit une réponse de la sandbox, c'est cette page qui est active.
        api.window.evaluate_js(f"if(typeof window.addLog === 'function') {{ window.addLog({js_output}); }}")

def run_server():
    """
    Lance le serveur Flask.
    En mode non-debug, on désactive le logging de Werkzeug pour ne pas polluer la console.
    """
    if not DEBUG:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    # --- MODIFICATION : Lancement via SocketIO ---
    # On utilise socketio.run() au lieu de app.run() pour activer les WebSockets.
    # allow_unsafe_werkzeug=True est nécessaire pour les versions récentes avec le mode threading.
    socketio.run(app, port=5000, debug=DEBUG, use_reloader=False, allow_unsafe_werkzeug=True)

def deep_update(d, u):
    """Met à jour récursivement un dictionnaire."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def load_config(use_default_only=False):
    """
    Charge la configuration depuis config.json.
    Retourne des valeurs par défaut si le fichier est absent ou corrompu.
    """
    default_config = {
        'display_mode': 'fullscreen',
        'navigation': {
            'start_level': 404
        },
        'ai': {
            'providers': {
                'openai': {
                    'api_key': 'YOUR_OPENAI_API_KEY_HERE',
                    'base_url': 'https://api.openai.com/v1'
                },
                'deepseek': {
                    'api_key': 'YOUR_DEEPSEEK_API_KEY_HERE',
                    'base_url': 'https://api.deepseek.com/v1'
                },
                'google': {
                    'api_key': 'YOUR_GEMINI_API_KEY_HERE'
                },
                'groq': {
                    'api_key': 'YOUR_GROQ_API_KEY_HERE',
                    'base_url': 'https://api.groq.com/openai/v1'
                },
                'ollama': {
                    'base_url': 'http://127.0.0.1:11434'
                }
            },
            'model': 'deepseek-coder'
        },
        'user': {
            'user_folder_path': os.path.join(os.path.expanduser('~'), 'Documents', 'Megastructure_Data'),
            'password': '', # Mot de passe par défaut pour le Bunker. L'utilisateur doit le définir.
            'neural_ghost_active': False, # Drapeau d'infection
            'keylogger_active': False, # NOUVEAU: Drapeau pour le keylogger
            'pseudo': 'Anonyme',
            'installed_extensions': {}, # Stocke les extensions installées par l'utilisateur
            'bots': {
                'total': 0,
                'available': 0,
                'in_mission': 0,
                'missions': [],
                'protocol_unlocked': False
            },
            'system_effects': {
                'ddos_active': False
            },
            # Ajout pour la cohérence avec le README et les futures extensions
            'api_keys': {
                'hibp_api_key': 'YOUR_HIBP_API_KEY_HERE'
            }
        },
        'sync': {
            'enabled': False,
            'path': ''
        },
        'vpn': {
            'proxy_address': 'http://127.0.0.1:9050' # Adresse par défaut (ex: Tor)
        }
    }
    if use_default_only:
        return default_config

    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            loaded_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_config

    # Fusionne la configuration par défaut avec celle chargée, de manière récursive.
    config = default_config.copy()
    config = deep_update(config, loaded_config)

    # Cas spécial : si le chemin du dossier utilisateur est vide dans le fichier de config,
    # on force l'utilisation du chemin par défaut pour éviter les erreurs.
    if not config.get('user', {}).get('user_folder_path'):
        config['user']['user_folder_path'] = default_config['user']['user_folder_path']

    return config

def load_extensions_from_disk():
    """
    Scanne le dossier EXTENSIONS et ses sous-dossiers, importe dynamiquement les modules
    et instancie les classes qui héritent de BaseExtension.
    """
    if not os.path.isdir(EXTENSIONS_FOLDER):
        print(f"Avertissement : Le dossier des extensions '{EXTENSIONS_FOLDER}' n'a pas été trouvé.")
        return

    for root, _, files in os.walk(EXTENSIONS_FOLDER):
        for filename in files:
            # On ne charge que les fichiers python, en ignorant les fichiers de base/init
            if filename.endswith('.py') and filename not in ['__init__.py', 'base_extension.py']:
                module_name = filename[:-3]
                file_path = os.path.join(root, filename)
                
                try:
                    # Importation dynamique du module
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # On cherche les classes dans le module qui sont des extensions valides
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, BaseExtension) and obj is not BaseExtension:
                            # --- MODIFICATION : Injection de la SandboxAPI ---
                            # On crée une instance de l'API sécurisée pour l'extension
                            sandbox_api = SandboxAPI(main_api_instance=api, extension_name=obj.NAME)
                            instance = obj(sandbox_api)
                            print(f"Extension chargée : {instance.NAME} (sandboxée) depuis {filename}")
                            loaded_extensions[instance.NAME] = instance
                except Exception as e:
                    print(f"Erreur lors du chargement de l'extension {filename}: {e}")

def load_tester_codes():
    """Charge les codes testeurs depuis le fichier JSON."""
    global tester_codes
    if not os.path.exists(TESTER_CODES_PATH):
        print(f"Avertissement : Fichier des codes testeurs non trouvé à '{TESTER_CODES_PATH}'.")
        tester_codes = []
        return
    try:
        with open(TESTER_CODES_PATH, 'r') as f:
            tester_codes = json.load(f)
        print(f"{len(tester_codes)} codes testeurs chargés.")
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erreur lors du chargement des codes testeurs : {e}")
        tester_codes = []

# Variable globale pour stocker la configuration
app_config = {}

if __name__ == '__main__':
    # 1. Lancer le serveur Flask dans un thread séparé pour ne pas bloquer la fenêtre.
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Permet de fermer le thread quand l'app se ferme
    server_thread.start()

    # 2. Charger la configuration initiale dans la variable globale.
    app_config = load_config()

    # Charger les codes testeurs
    load_tester_codes()

    # 1.5. Charger les extensions disponibles depuis le disque.
    load_extensions_from_disk()

    # 3. Créer une instance de l'API en lui passant la configuration.
    api = Api(config=app_config)

    # --- NOUVEAU : Démarrage du thread keylogger si l'infection est persistante ---
    if api.config.get('user', {}).get('keylogger_active', False):
        print("[INIT] Keylogger persistant détecté. Démarrage du thread de simulation.")
        kl_thread = threading.Thread(target=keylogger_simulation_thread, args=(api,), daemon=True)
        kl_thread.start()

    # 3.5 S'assurer que le dossier utilisateur existe au démarrage
    api.ensure_user_folder_exists()

    # 4. Préparer les arguments pour la création de la fenêtre.
    window_args = {
        'title': 'Mégastructure // Interface',
        'url': 'http://127.0.0.1:5000',
        'js_api': api  # C'est ici que le "pont" est créé.
    }

    if app_config['display_mode'] == 'windowed':
        # Mode fenêtré adaptatif
        primary_screen = webview.screens[0]
        window_args['width'] = int(primary_screen.width * 0.8)
        window_args['height'] = int(primary_screen.height * 0.8)
        window_args['resizable'] = True
    else:
        # Mode plein écran (par défaut)
        window_args['fullscreen'] = True

    window = webview.create_window(**window_args)
    api.window = window  # Donne à l'API une référence à la fenêtre pour pouvoir la fermer.

    webview.start(debug=DEBUG) # Active le menu "Inspecter" pour le débogage