import os

def secure_path(subpath, base_path):
    """
    Construit un chemin sécurisé à l'intérieur d'un dossier de base.
    Empêche les attaques par traversée de répertoire (path traversal).
    Retourne (chemin_complet, None) en cas de succès, ou (None, message_erreur) en cas d'échec.
    """
    if not base_path:
        return None, "Le dossier de base n'est pas configuré."

    # 1. Normaliser le chemin de base pour avoir une référence fiable.
    # os.path.realpath résout les liens symboliques, ce qui est plus sûr.
    real_base_path = os.path.realpath(base_path)

    # 2. Joindre le chemin de base et le sous-chemin fourni.
    # On ne nettoie pas le subpath ici pour autoriser les sous-dossiers.
    combined_path = os.path.join(real_base_path, subpath)

    # 3. Résoudre le chemin combiné pour éliminer les '..' et autres.
    real_combined_path = os.path.realpath(combined_path)

    # 4. Vérification de sécurité : s'assurer que le chemin final est bien
    #    DANS le dossier de base.
    #    os.path.commonpath est une manière robuste de vérifier cela.
    common_path = os.path.commonpath([real_base_path, real_combined_path])

    if common_path != real_base_path:
        return None, "Accès refusé : tentative de sortie du répertoire autorisé."

    return real_combined_path, None