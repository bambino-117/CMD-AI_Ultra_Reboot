import requests
from bs4 import BeautifulSoup

# --- Configuration des portails de données ---
# Liste des portails de données ouverts des administrations à sonder.
# Chaque portail a sa propre configuration de scraping (sélecteurs CSS).
DATA_PORTALS = {
    "Europe": {
        "France": {
            "name": "data.gouv.fr",
            "base_url": "https://www.data.gouv.fr",
            "search_url": "https://www.data.gouv.fr/fr/datasets/?q={query}",
            "selectors": {
                "card": "div.card.dataset-card",
                "title": "h4.card-title a",
                "description": "p.card-text",
                "link_is_relative": True
            }
        },
        "United Kingdom": {
            "name": "data.gov.uk",
            "base_url": "https://www.data.gov.uk",
            "search_url": "https://www.data.gov.uk/search?q={query}",
            "selectors": {
                "card": "li.dgu-dataset-item",
                "title": "h3.dgu-dataset-item__title a",
                "description": "div.dgu-dataset-item__notes",
                "link_is_relative": True
            }
        }
    },
    "North America": {
        "USA": {
            "name": "data.gov",
            "base_url": "https://catalog.data.gov",
            "search_url": "https://catalog.data.gov/dataset?q={query}",
            "selectors": {
                "card": "li.dataset-item",
                "title": "h3.dataset-heading a",
                "description": "div.dataset-content div.notes",
                "link_is_relative": True
            }
        }
    }
}

def search_admin_data(query: str, target_country: str = None):
    """
    Recherche un mot-clé sur les portails de données administratifs configurés.
    Si target_country est spécifié, la recherche est limitée à ce pays.
    Retourne une liste de dictionnaires contenant les résultats trouvés.
    """
    all_results = []
    portals_to_search = []

    # Déterminer quels portails sonder
    if target_country:
        for continent, countries in DATA_PORTALS.items():
            if target_country in countries:
                portals_to_search.append((target_country, countries[target_country]))
                break
    else:  # Sonder tous les portails
        for continent, countries in DATA_PORTALS.items():
            for country_name, portal_details in countries.items():
                portals_to_search.append((country_name, portal_details))
    
    if not portals_to_search and target_country:
         return [{
            "title": f"Le portail pour '{target_country}' n'est pas configuré.",
            "description": "Vérifiez la configuration dans mecannique.py ou sélectionnez un autre pays.",
            "source": "Système",
            "error": True
        }]

    for country, portal in portals_to_search:
        try:
            search_url = portal["search_url"].format(query=requests.utils.quote(query))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            selectors = portal['selectors']
            dataset_cards = soup.select(selectors['card'])

            portal_results = []
            for card in dataset_cards[:5]:  # Limite aux 5 premiers résultats
                title_element = card.select_one(selectors['title'])
                description_element = card.select_one(selectors['description'])

                title = title_element.get_text(strip=True) if title_element else "Titre non trouvé"
                description = description_element.get_text(strip=True) if description_element else "Description non disponible."
                
                link_href = title_element['href'] if title_element and title_element.has_attr('href') else "#"
                
                # Gérer les liens relatifs
                if selectors.get('link_is_relative', False) and link_href.startswith('/'):
                    link = f"{portal['base_url']}{link_href}"
                else:
                    link = link_href

                portal_results.append({
                    "title": title,
                    "description": description,
                    "source": portal["name"],
                    "link": link
                })

            if portal_results:
                all_results.extend(portal_results)
            else:
                all_results.append({
                    "title": f"Aucun jeu de données trouvé pour '{query}' sur {portal['name']}",
                    "description": "Essayez un autre terme de recherche ou vérifiez l'orthographe.",
                    "source": portal["name"],
                    "link": search_url
                })

        except requests.exceptions.RequestException as e: # Gère les erreurs réseau
            all_results.append({
                "title": f"Erreur de connexion à {portal['name']}",
                "description": str(e),
                "source": portal["name"],
                "error": True
            })
        except Exception as e: # Gère les autres erreurs (ex: scraping)
            all_results.append({
                "title": f"Erreur d'analyse pour {portal['name']}",
                "description": f"Le format du site a peut-être changé. Erreur : {e}",
                "source": portal["name"],
                "error": True
            })

    return all_results