import requests
import time

def search_leaked_databases(query: str, api_key: str):
    """
    Interroge l'API "Have I Been Pwned" (HIBP) pour trouver des fuites de données
    associées à un email ou un nom d'utilisateur.
    """
    if not api_key or 'YOUR_HIBP_API_KEY' in api_key:
        return {"error": "Clé API 'Have I Been Pwned' non configurée. Veuillez l'ajouter dans les paramètres."}

    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "Megastructure-OSINT-Tool"
    }
    # HIBP API v3 pour les comptes compromis
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{requests.utils.quote(query)}"

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            # Succès, des fuites ont été trouvées
            return response.json()
        elif response.status_code == 404:
            # Aucune fuite trouvée pour ce compte, ce qui est une "réussite" de recherche
            return []
        else:
            # Gérer les autres erreurs API (clé invalide, etc.)
            return {"error": f"Erreur API HIBP : {response.status_code} - {response.text}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de connexion à l'API HIBP : {e}"}