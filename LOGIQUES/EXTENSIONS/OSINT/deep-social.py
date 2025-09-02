import asyncio
from sherlock.sherlock import sherlock

def search_social_media(target, callback):
    """
    Utilise la bibliothèque Sherlock pour trouver des profils sur les réseaux sociaux.
    Retourne une liste de dictionnaires contenant les profils trouvés.
    """
    # Sherlock est asynchrone, nous devons donc le lancer dans une boucle d'événements.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Sherlock écrit sur la sortie standard, nous le redirigeons pour le capturer si besoin.
    # Pour l'instant, nous nous contentons des résultats retournés.
    results = loop.run_until_complete(sherlock(
        [target],
        timeout=10,
        print_found=False, # On ne veut pas que Sherlock imprime les résultats lui-même
        print_errors=False
    ))
    loop.close()

    # Formatter les résultats pour le frontend
    found_profiles = []
    for site, data in results.items():
        if data.get("status") == "FOUND":
            found_profiles.append({
                "site": site,
                "url": data.get("url_user")
            })

    callback({'type': 'log', 'message': f'// [SOCIAL] Scan Sherlock terminé. {len(found_profiles)} profils trouvés.'})
    return found_profiles

