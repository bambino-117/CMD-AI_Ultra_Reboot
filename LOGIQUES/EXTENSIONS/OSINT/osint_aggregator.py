import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, parse_qs
from datetime import datetime
import os

from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
from LOGIQUES.EXTENSIONS.OSINT.deep_social import search_social_media
from LOGIQUES.EXTENSIONS.OSINT.database_search import search_leaked_databases
from LOGIQUES.utils import secure_path

class OsintExtension(BaseExtension):
    """
    Extension pour l'outil d'analyse OSINT (Centre d'Analyse).
    Contient toute la logique pour effectuer des recherches et sauvegarder des rapports.
    """
    NAME = "OSINT Aggregator"
    DESCRIPTION = "Lance des scans OSINT sur des cibles, consulte et sauvegarde les rapports."

    def execute(self, *args, **kwargs):
        """
        L'exécution de cette extension est principalement gérée par son template.
        Cette méthode pourrait être utilisée pour des vérifications ou des initialisations futures.
        """
        return {
            "status": "info",
            "message": "L'interface de l'extension OSINT est gérée par son point d'entrée. Aucune action directe à exécuter ici."
        }

    def execute_scan(self, target, modules, callback, config):
        """
        Orchestre le scan OSINT sur plusieurs sources, en fonction des modules sélectionnés.
        """
        if not target:
            callback({'status': 'error', 'message': 'Aucune cible spécifiée.'})
            return

        if not modules:
            callback({'status': 'log', 'message': '// Avertissement : Aucun module de scan sélectionné. Lancement du scan complet par défaut.'})
            modules = ['web', 'social', 'leaks'] # Par défaut, on lance tout

        callback({'status': 'log', 'message': f'// Initialisation du scan OSINT pour : {target}...'})
        callback({'status': 'log', 'message': f'// Modules activés : {", ".join(modules)}'})

        web_results = []
        social_results = []
        leak_results = []

        # 1. Lancer le scan web
        if 'web' in modules:
            web_results = self._search_duckduckgo(target, callback)

        # 2. Lancer le scan des réseaux sociaux
        if 'social' in modules:
            callback({'status': 'log', 'message': '// [SOCIAL] Lancement du scan des réseaux sociaux...'})
            social_results = search_social_media(target, callback) # La fonction gère son propre log de fin
        
        # 3. Lancer la recherche de fuites de données
        if 'leaks' in modules:
            callback({'status': 'log', 'message': '// [HIBP] Interrogation des bases de données de fuites...'})
            hibp_api_key = config.get('user', {}).get('api_keys', {}).get('hibp_api_key')
            leak_results = search_leaked_databases(target, hibp_api_key)
            # N'afficher le message de fin que si la recherche n'a pas retourné d'erreur
            if not isinstance(leak_results, dict) or 'error' not in leak_results:
                callback({'status': 'log', 'message': '// [HIBP] Recherche terminée.'})

        # 4. Agréger et envoyer les résultats finaux
        final_results = {
            "web": web_results,
            "social": social_results,
            "leaks": leak_results
        }
        callback({'status': 'success', 'results': final_results})

    def _search_duckduckgo(self, target, callback):
        """Effectue une recherche sur DuckDuckGo et retourne une liste de résultats."""
        try:
            callback({'status': 'log', 'message': '// [DDG] Envoi de la requête au réseau DuckDuckGo...'})
            
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(target)}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            callback({'status': 'log', 'message': f'// [DDG] Réponse reçue ({response.status_code}). Analyse du DOM...'})

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            result_items = soup.find_all('div', class_='result')
            callback({'status': 'log', 'message': f'// [DDG] {len(result_items)} résultats potentiels trouvés. Extraction...'})

            for item in result_items:
                title_tag, snippet_tag = item.find('a', class_='result__a'), item.find('a', class_='result__snippet')
                if title_tag and snippet_tag:
                    link = title_tag['href']
                    if link.startswith('/l/'):
                        qs = parse_qs(link.split('?')[1])
                        link = unquote(qs.get('uddg', [''])[0]) if 'uddg' in qs else link
                    results.append({'title': title_tag.get_text(strip=True), 'link': link, 'snippet': snippet_tag.get_text(strip=True)})
            return results

        except requests.exceptions.RequestException as e:
            callback({'status': 'error', 'message': f'[DDG] Erreur réseau lors du scan : {e}'})
            return []
        except Exception as e:
            callback({'status': 'error', 'message': f'[DDG] Erreur inattendue lors du scan : {e}'})
            return []

    def _secure_path(self, filename, config):
        """Utilise la fonction de chemin sécurisé partagée."""
        user_path = config.get('user', {}).get('user_folder_path')
        return secure_path(filename, user_path)

    def save_report(self, target, results, config):
        try:
            if not target or not isinstance(results, dict): return {'status': 'error', 'message': 'Données du rapport invalides.'}
            
            web_results = results.get('web', [])
            social_results = results.get('social', {})
            leak_results = results.get('leaks', [])
            ai_analysis = results.get('ai_analysis') # Récupère l'analyse IA
            
            report_content = f"# Rapport OSINT : {target}\n## Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if ai_analysis:
                report_content += f"## Analyse du Logicateur\n\n---\n\n{ai_analysis}\n\n"

            report_content += "## Données Brutes Collectées\n\n"
            report_content += "### Résultats de Scan Web\n\n---\n\n"
            if not web_results: report_content += "Aucun résultat trouvé sur le web.\n"
            else: report_content += "".join([f"#### {res.get('title', 'Sans titre')}\n**Lien:** [{res.get('link', '#')}]({res.get('link', '#')})\n\n**Extrait:**\n> {res.get('snippet', 'Aucun extrait.')}\n\n---\n\n" for res in web_results])

            report_content += "\n### Analyse des Réseaux Sociaux\n\n---\n\n"
            # social_results est maintenant une liste de dictionnaires
            if not social_results:
                report_content += "Aucune activité sociale significative détectée.\n"
            else:
                report_content += "**Profils trouvés via Sherlock:**\n\n"
                for profile in social_results:
                    report_content += f"- **{profile.get('site')}**: {profile.get('url')}\n"
            
            report_content += "\n### Analyse des Fuites de Données (Have I Been Pwned)\n\n---\n\n"
            if isinstance(leak_results, dict) and 'error' in leak_results:
                report_content += f"Erreur lors de la recherche : {leak_results['error']}\n"
            elif not leak_results:
                report_content += "Aucune fuite de données trouvée pour cette cible.\n"
            else:
                report_content += f"La cible a été trouvée dans **{len(leak_results)}** fuite(s) de données :\n\n"
                for leak in leak_results:
                    report_content += f"- **Site :** {leak.get('Name')}\n  - **Date de la fuite :** {leak.get('BreachDate')}\n  - **Données compromises :** {', '.join(leak.get('DataClasses', []))}\n\n"

            # Créer un nom de dossier sécurisé pour la cible
            safe_target_name = "".join(c for c in target if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
            folder_name = f"OSINT_{safe_target_name}"
            
            # Créer le dossier dans le Bunker s'il n'existe pas
            folder_path, error = self._secure_path(folder_name, config)
            if error: return {'status': 'error', 'message': error}
            os.makedirs(folder_path, exist_ok=True)

            # Créer le nom du fichier de rapport
            report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
            # Construire le chemin complet du fichier à l'intérieur du nouveau dossier
            full_report_path = os.path.join(folder_path, report_filename)

            with open(full_report_path, 'w', encoding='utf-8') as f: f.write(report_content)
            return {'status': 'success', 'message': f"Rapport '{report_filename}' sauvegardé dans le dossier '{folder_name}'."}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la sauvegarde du rapport : {e}"}