import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, parse_qs
from datetime import datetime
import os

from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
from .deep_social import search_social_media

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

    def execute_scan(self, target, callback, config):
        """
        Orchestre le scan OSINT sur plusieurs sources.
        """
        if not target:
            callback({'status': 'error', 'message': 'Aucune cible spécifiée.'})
            return

        callback({'status': 'log', 'message': f'// Initialisation du scan OSINT complet pour : {target}...'})

        # 1. Lancer le scan web
        web_results = self._search_duckduckgo(target, callback)

        # 2. Lancer le scan des réseaux sociaux
        callback({'status': 'log', 'message': '// [SOCIAL] Lancement du scan des réseaux sociaux...'})
        social_results = search_social_media(target, callback) # La fonction gère son propre log de fin

        # 3. Agréger et envoyer les résultats finaux
        final_results = {
            "web": web_results,
            "social": social_results
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
        user_path = config.get('user', {}).get('user_folder_path')
        if not user_path: return None, "Le dossier utilisateur n'est pas configuré."
        clean_filename = os.path.basename(filename)
        full_path = os.path.normpath(os.path.join(user_path, clean_filename))
        if not full_path.startswith(os.path.normpath(user_path)): return None, "Accès refusé : tentative de sortie du répertoire autorisé."
        return full_path, None

    def save_report(self, target, results, config):
        try:
            if not target or not isinstance(results, dict): return {'status': 'error', 'message': 'Données du rapport invalides.'}
            
            web_results = results.get('web', [])
            social_results = results.get('social', {})
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
                    report_content += f"- **{profile.get('site')}**: {profile.get('url')}})\n"

            safe_target_name = "".join(c for c in target if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
            filename = f"osint_report_{safe_target_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            full_path, error = self._secure_path(filename, config)
            if error: return {'status': 'error', 'message': error}
            with open(full_path, 'w', encoding='utf-8') as f: f.write(report_content)
            return {'status': 'success', 'message': f"Rapport '{filename}' sauvegardé dans le Bunker."}
        except Exception as e:
            return {'status': 'error', 'message': f"Erreur lors de la sauvegarde du rapport : {e}"}