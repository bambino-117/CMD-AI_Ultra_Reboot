class BaseExtension:
    """
    Classe de base abstraite pour toutes les extensions du Portail Conteneur.
    Chaque extension doit hériter de cette classe et surcharger ses propriétés
    et sa méthode `execute`.
    """
    
    # Propriétés à surcharger par les extensions filles
    NAME = "Extension non définie"
    DESCRIPTION = "Aucune description fournie."
    
    def execute(self, *args, **kwargs):
        """
        La méthode principale que l'interface appellera pour lancer l'extension.
        Doit retourner un dictionnaire sérialisable en JSON.
        """
        raise NotImplementedError("La méthode execute() doit être implémentée par la sous-classe.")