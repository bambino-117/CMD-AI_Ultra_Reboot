from flask import Flask, render_template
import webview
import threading

# --- Variable de Contrôle du Mode ---
DEBUG = False  # Mettre à False pour simuler le mode "production" (silencieux)
import json
import os
import importlib.util
import inspect
import platform
from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
from LOGIQUES.vpn_manager import VpnManager
from LOGIQUES.utils import secure_path
import shutil
from datetime import datetime

# --- NOUVEAU : Importation du module de mécanique ---
try:
    from LOGIQUES.mecannique import search_admin_data
except ImportError:
    search_admin_data = None
import requests
from bs4 import BeautifulSoup

# --- Configuration des Chemins ---
# Le script est à la racine du projet. Le dossier 'INTERFACES' contient les ressources.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
INTERFACES_FOLDER = os.path.join(PROJECT_ROOT, 'INTERFACES')
TEMPLATE_FOLDER = os.path.join(INTERFACES_FOLDER, 'templates')
STATIC_FOLDER = os.path.join(INTERFACES_FOLDER, 'static')
LOGIQUES_FOLDER = os.path.join(PROJECT_ROOT, 'LOGIQUES')
EXTENSIONS_FOLDER = os.path.join(LOGIQUES_FOLDER, 'EXTENSIONS')
CONTENEURS_FOLDER = os.path.join(LOGIQUES_FOLDER, 'CONTENEURS')
RESSOURCES_FOLDER = os.path.join(PROJECT_ROOT, 'RESSOURCES')
CONFIG_FILE_PATH = os.path.join(INTERFACES_FOLDER, 'config.json')

# --- DÉBOGAGE DE CHEMIN ---
print(f"[DEBUG] Chemin absolu du dossier des conteneurs attendu : {os.path.abspath(CONTENEURS_FOLDER)}")

# --- Stockage Global pour les Extensions ---
loaded_extensions = {}
# --- NOUVEAU : État global du VPN ---
vpn_global_state = {
    "is_connected": False,
    "proxy_address": None
}


# Initialise l'application Flask en spécifiant les dossiers
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

# --- CONFIGURATION DU CACHE ---
# Force la désactivation du cache pour les fichiers statiques (CSS, JS, images) en mode DEBUG.
# C'est la méthode la plus fiable pour s'assurer que les changements sont pris en compte.
if DEBUG:
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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
            with open(CONFIG_FILE_PATH, 'w') as f:
                json.dump(data, f, indent=2)
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

    def check_bunker_password(self, password_attempt):
        """Exposée au JS. Vérifie le mot de passe d'accès au Bunker."""
        # Mot de passe "master" codé en dur pour le concepteur
        developer_password = "openme"
        
        # Mot de passe défini par l'utilisateur dans la config
        user_password = self.config.get('user', {}).get('password', '')

        # Accès accordé si le mot de passe correspond à celui de l'utilisateur (s'il est défini)
        # OU s'il correspond au mot de passe concepteur.
        if (user_password and password_attempt == user_password) or (password_attempt == developer_password):
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Accès refusé'}

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
        """
        source_file_path = os.path.join(RESSOURCES_FOLDER, 'boutton Infect.md')
        target_filename = 'neural_ghost.py'

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
            dest_path, error = self._secure_path(target_filename)
            if error:
                return {'status': 'error', 'message': error}

            # 6. Écrire le fichier
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(full_code)

            # --- MISE À JOUR DE L'ÉTAT D'INFECTION (Étape 7) ---
            self.config['user']['neural_ghost_active'] = True
            self.save_settings(self.config)

            # 7. Retourner un succès
            return {'status': 'success', 'message': f'Fichier {target_filename} injecté dans le Bunker.'}
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
        if "OSINT Aggregator" in loaded_extensions:
            osint_ext = loaded_extensions["OSINT Aggregator"]
            # L'extension a besoin de la configuration pour le chemin du Bunker
            return osint_ext.save_report(target, results, self.config)
        else:
            return {'status': 'error', 'message': 'L\'extension OSINT n\'est pas chargée.'}

    def export_osint_report(self, target, results, export_format):
        """Exposée au JS. Exporte un rapport OSINT dans un format donné."""
        if "OSINT Aggregator" in loaded_extensions:
            osint_ext = loaded_extensions["OSINT Aggregator"]
            # L'extension a besoin de la config pour certains paramètres mais ici on peut l'omettre
            # car le chemin des téléchargements est standard.
            return osint_ext.export_report(target, results, export_format, self.config)
        else:
            return {'status': 'error', 'message': 'L\'extension OSINT n\'est pas chargée.'}

    def export_osint_to_bunker(self, target, results, export_format):
        """Exposée au JS. Exporte un rapport OSINT dans un nouveau dossier du Bunker."""
        if "OSINT Aggregator" in loaded_extensions:
            osint_ext = loaded_extensions["OSINT Aggregator"]
            # La méthode a besoin de la config pour le chemin du Bunker
            return osint_ext.export_report_to_bunker(target, results, export_format, self.config)
        else:
            return {'status': 'error', 'message': 'L\'extension OSINT n\'est pas chargée.'}

    def run_osint_scan(self, target, modules, callback):
        """Exposée au JS. Wrapper pour appeler la méthode de scan de l'extension OSINT."""
        if "OSINT Aggregator" in loaded_extensions:
            osint_ext = loaded_extensions["OSINT Aggregator"]
            # L'extension a besoin de la configuration pour les éventuelles clés API
            osint_ext.execute_scan(target, modules, callback, self.config)
        else:
            callback({'status': 'error', 'message': 'L\'extension OSINT n\'est pas chargée.'})

    def run_deep_social_scan(self, target, callback):
        """Exposée au JS. Appelle l'outil de recherche sociale et retourne les résultats."""
        from LOGIQUES.EXTENSIONS.OSINT.deep_social import search_social_media
        try:
            # La fonction search_social_media retourne les résultats,
            # nous devons les encapsuler dans un callback de succès pour le JS.
            results = search_social_media(target, callback)
            callback({'status': 'success', 'results': results})
        except Exception as e:
            callback({'status': 'error', 'message': str(e)})

    def open_file_dialog(self):
        """Exposée au JS. Ouvre une boîte de dialogue de sélection de fichier."""
        if not self.window:
            return None
        # Retourne une liste de chemins de fichiers sélectionnés
        return self.window.create_file_dialog(webview.OPEN_DIALOG)

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

    def upload_file_to_sandbox(self, host_file_path):
        """Exposée au JS. Téléverse un fichier dans la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].upload_file_to_sandbox(host_file_path)
        return {'status': 'error', 'message': 'Extension non chargée.'}

    def execute_in_sandbox(self, command):
        """Exposée au JS. Exécute une commande dans la sandbox."""
        ext_name = "Chargeur d'Applications Universel"
        if ext_name in loaded_extensions:
            return loaded_extensions[ext_name].execute_in_sandbox(command)
        return {'status': 'error', 'message': 'Extension non chargée.'}


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


@app.route('/')
def login_page():
    """
    Sert la page de "connexion" (aboutissement.html).
    Ce sera le point d'entrée de l'application.
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
    """
    return render_template('settings.html')

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
    return render_template('portail_conteneur.html')

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
        # Les templates d'extension sont dans un sous-dossier pour l'organisation.
        template_path = os.path.join('extensions', template_name)
        full_template_path = os.path.join(app.template_folder, template_path)

        if os.path.exists(full_template_path):
            return render_template(template_path, extension=ext_details)
        else:
            ext_details['error_message'] = f"Template '{template_name}' introuvable dans le dossier 'extensions'."

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

def run_server():
    """
    Lance le serveur Flask.
    En mode non-debug, on désactive le logging de Werkzeug pour ne pas polluer la console.
    """
    if not DEBUG:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    app.run(port=5000, debug=DEBUG, use_reloader=False) # Le reloader doit être False pour pywebview

def deep_update(d, u):
    """Met à jour récursivement un dictionnaire."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def load_config():
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
            'pseudo': 'Anonyme',
            'user_folder_path': os.path.join(os.path.expanduser('~'), 'Documents', 'Megastructure_Data'),
            'password': '', # Mot de passe par défaut pour le Bunker. L'utilisateur doit le définir.
            'neural_ghost_active': False, # Drapeau d'infection
            'installed_extensions': {}, # Stocke les extensions installées par l'utilisateur
            # Ajout pour la cohérence avec le README et les futures extensions
            'api_keys': {
                'hibp_api_key': 'YOUR_HIBP_API_KEY_HERE'
            }
        },
        'vpn': {
            'proxy_address': 'http://127.0.0.1:9050' # Adresse par défaut (ex: Tor)
        }
    }
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
                            instance = obj()
                            print(f"Extension chargée : {instance.NAME} depuis {filename}")
                            loaded_extensions[instance.NAME] = instance
                except Exception as e:
                    print(f"Erreur lors du chargement de l'extension {filename}: {e}")

# Variable globale pour stocker la configuration
app_config = {}

if __name__ == '__main__':
    # 1. Lancer le serveur Flask dans un thread séparé pour ne pas bloquer la fenêtre.
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Permet de fermer le thread quand l'app se ferme
    server_thread.start()

    # 1.5. Charger les extensions disponibles depuis le disque.
    load_extensions_from_disk()

    # 2. Charger la configuration initiale dans la variable globale.
    app_config = load_config()

    # 3. Créer une instance de l'API en lui passant la configuration.
    api = Api(config=app_config)

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