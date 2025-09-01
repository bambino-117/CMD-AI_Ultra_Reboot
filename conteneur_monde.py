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
from datetime import datetime
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

    def list_bunker_files(self):
        """Exposée au JS. Liste les fichiers dans le dossier utilisateur ("Bunker")."""
        user_path = self.config.get('user', {}).get('user_folder_path')
        if not user_path or not os.path.isdir(user_path):
            return {'status': 'error', 'message': 'Bunker directory not found or not configured.'}
        try:
            files = os.listdir(user_path)
            return {'status': 'success', 'files': files}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _secure_path(self, filename):
        """
        Construit un chemin sécurisé à l'intérieur du dossier utilisateur.
        Empêche les attaques par traversée de répertoire (path traversal).
        Retourne (chemin_complet, None) en cas de succès, ou (None, message_erreur) en cas d'échec.
        """
        user_path = self.config.get('user', {}).get('user_folder_path')
        if not user_path:
            return None, "Le dossier utilisateur n'est pas configuré."

        # Nettoie le nom de fichier pour ne garder que le nom de base (ex: 'notes.txt')
        # Empêche les chemins comme '../secrets.txt'
        clean_filename = os.path.basename(filename)
        
        # Construit le chemin complet et le normalise
        full_path = os.path.normpath(os.path.join(user_path, clean_filename))
        
        # Vérification finale : s'assurer que le chemin résolu est bien DANS le dossier utilisateur.
        if not full_path.startswith(os.path.normpath(user_path)):
            return None, "Accès refusé : tentative de sortie du répertoire autorisé."
            
        return full_path, None

    def read_bunker_file(self, filename):
        """Exposée au JS. Lit le contenu d'un fichier dans le Bunker de manière sécurisée."""
        full_path, error = self._secure_path(filename)
        if error:
            return {'status': 'error', 'message': error}

        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return {'status': 'success', 'content': content}
        except FileNotFoundError:
            return {'status': 'error', 'message': f'Fichier non trouvé : {os.path.basename(filename)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de lire le fichier : {e}'}

    def check_bunker_password(self, password_attempt):
        """Exposée au JS. Vérifie le mot de passe d'accès au Bunker."""
        # Utilise 'admin' comme mot de passe par défaut s'il n'est pas défini
        correct_password = self.config.get('user', {}).get('password', 'admin')
        if password_attempt == correct_password:
            return {'status': 'success'}
        else:
            # Ne donnez pas trop d'informations en cas d'échec
            return {'status': 'error', 'message': 'Accès refusé'}

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
        response = requests.post(f'{base_url}/chat/completions', headers=headers, json=data, timeout=30)
        response.raise_for_status()
        ai_response = response.json()
        return ai_response['choices'][0]['message']['content']

    def _call_google_gemini_api(self, model, prompt, api_key):
        """Appelle l'API Google Gemini."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = { "contents": [{"parts": [{"text": prompt}]}] }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
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

            # 3. Trouver un niveau disponible (de 501 à 999)
            used_levels = {ext['level'] for ext in installed_extensions.values()}
            new_level = next((level for level in range(501, 1000) if level not in used_levels), -1)

            if new_level == -1:
                return {'status': 'error', 'message': 'Plus de niveaux disponibles pour les extensions.'}

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

    def get_conteneurs(self):
        """
        Exposée au JS. Scanne, lit et retourne les données de tous les conteneurs.
        """
        if not os.path.isdir(CONTENEURS_FOLDER):
            return {'status': 'error', 'message': f"Le répertoire des conteneurs est introuvable."}

        conteneurs_data = []
        try:
            # S'assure que les fichiers sont lus dans un ordre prévisible (00, 01, 02...)
            for filename in sorted(os.listdir(CONTENEURS_FOLDER)):
                if filename.startswith('conteneur_') and filename.endswith('.json'):
                    file_path = os.path.join(CONTENEURS_FOLDER, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        conteneurs_data.append(data)
            
            # Tri final par ID pour garantir l'ordre, au cas où les noms de fichiers seraient incohérents
            conteneurs_data.sort(key=lambda x: x.get('id', 0))

            return {'status': 'success', 'conteneurs': conteneurs_data}
        except json.JSONDecodeError as e:
            return {'status': 'error', 'message': f"Erreur de décodage JSON dans un fichier conteneur : {e}"}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur inattendue lors de la lecture des conteneurs : {e}"}

    def save_osint_report(self, target, results):
        """
        Exposée au JS. Formate les résultats d'un scan OSINT en Markdown
        et les sauvegarde dans un fichier dans le Bunker.
        """
        try:
            if not target or not isinstance(results, list):
                return {'status': 'error', 'message': 'Données du rapport invalides.'}

            # 1. Formater le contenu en Markdown
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_content = f"# Rapport OSINT : {target}\n"
            report_content += f"## Généré le {timestamp}\n\n"
            report_content += f"---\n\n"

            if not results:
                report_content += "Aucun résultat trouvé pour cette cible.\n"
            else:
                for i, res in enumerate(results):
                    report_content += f"### Résultat {i+1}: {res.get('title', 'Sans titre')}\n"
                    report_content += f"**Lien:** [{res.get('link', '#')}]({res.get('link', '#')})\n\n"
                    report_content += f"**Extrait:**\n"
                    report_content += f"> {res.get('snippet', 'Aucun extrait.')}\n\n"
                    report_content += f"---\n\n"

            # 2. Générer un nom de fichier sécurisé et unique
            safe_target_name = "".join(c for c in target if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
            report_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"osint_report_{safe_target_name}_{report_timestamp}.md"

            # 3. Utiliser _secure_path pour obtenir le chemin complet et sécurisé
            full_path, error = self._secure_path(filename)
            if error:
                return {'status': 'error', 'message': error}

            # 4. Écrire le fichier
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

            return {'status': 'success', 'message': f"Rapport '{filename}' sauvegardé dans le Bunker."}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la sauvegarde du rapport : {e}"}

    def run_osint_scan(self, target, callback):
        """
        Exposée au JS. Effectue une recherche web simple pour la cible
        et retourne les titres et liens des résultats via un callback.
        """
        if not target:
            callback({'status': 'error', 'message': 'Aucune cible spécifiée.'})
            return

        try:
            # Utilise DuckDuckGo pour éviter les blocages de Google
            # On utilise la version HTML pour un scraping plus simple et stable
            from urllib.parse import unquote, parse_qs
            
            callback({'status': 'log', 'message': f'// Initialisation du scan pour la cible : {target}...'})
            
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(target)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            callback({'status': 'log', 'message': '// Envoi de la requête au réseau DuckDuckGo...'})
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            callback({'status': 'log', 'message': f'// Réponse reçue ({response.status_code}). Analyse du DOM...'})

            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            result_items = soup.find_all('div', class_='result')
            callback({'status': 'log', 'message': f'// {len(result_items)} résultats potentiels trouvés. Extraction...'})

            for item in result_items:
                title_tag = item.find('a', class_='result__a')
                snippet_tag = item.find('a', class_='result__snippet')
                
                if title_tag and snippet_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    snippet = snippet_tag.get_text(strip=True)
                    
                    if link.startswith('/l/'):
                        qs = parse_qs(link.split('?')[1])
                        if 'uddg' in qs:
                            link = unquote(qs['uddg'][0])

                    results.append({'title': title, 'link': link, 'snippet': snippet})
            
            callback({'status': 'success', 'results': results})

        except requests.exceptions.RequestException as e:
            callback({'status': 'error', 'message': f'Erreur réseau lors du scan : {e}'})
        except Exception as e:
            callback({'status': 'error', 'message': f'Erreur inattendue lors du scan : {e}'})

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

@app.route('/centre_analyse')
def centre_analyse_page():
    """
    Sert la page du Centre d'Analyse (Niveau 500).
    """
    return render_template('centre_analyse.html')

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

    return render_template('extension_placeholder.html', extension=ext_details)

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
            'password': 'admin', # Mot de passe par défaut pour le Bunker
            'neural_ghost_active': False, # Drapeau d'infection
            'installed_extensions': {} # Stocke les extensions installées par l'utilisateur
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
    Scanne le dossier EXTENSIONS, importe dynamiquement les modules
    et instancie les classes qui héritent de BaseExtension.
    """
    if not os.path.isdir(EXTENSIONS_FOLDER):
        print(f"Avertissement : Le dossier des extensions '{EXTENSIONS_FOLDER}' n'a pas été trouvé.")
        return

    for filename in os.listdir(EXTENSIONS_FOLDER):
        # On ne charge que les fichiers python, en ignorant les fichiers de base/init
        if filename.endswith('.py') and filename not in ['__init__.py', 'base_extension.py']:
            module_name = filename[:-3]
            file_path = os.path.join(EXTENSIONS_FOLDER, filename)
            
            try:
                # Importation dynamique du module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # On cherche les classes dans le module qui sont des extensions valides
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseExtension) and obj is not BaseExtension:
                        instance = obj()
                        print(f"Extension chargée : {instance.NAME}")
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