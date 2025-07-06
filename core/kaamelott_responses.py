import random

class KaamelottResponses:
    """Répliques de Kaamelott pour l'impatience"""
    
    IMPATIENCE = [
        "C'est pas faux... mais c'est pas vrai non plus !",
        "Bon, on fait quoi maintenant ?",
        "J'attends toujours votre réponse...",
        "Vous comptez rester planté là longtemps ?",
        "C'est pas compliqué pourtant !",
        "Alors, on se décide ?",
        "Le temps passe et rien ne se passe...",
        "Faut que ça bouge un peu !",
        "On peut pas rester comme ça éternellement !",
        "Allez, un petit effort !"
    ]
    
    ERREURS = [
        "C'est du grand n'importe quoi !",
        "Ça, c'est de la belle ouvrage !",
        "Vous vous foutez de moi ?",
        "C'est pas possible d'être aussi nul !",
        "Mais qu'est-ce que c'est que ce bordel ?",
        "Vous avez pas compris le principe !",
        "C'est du joli travail, bravo !",
        "Faut vraiment tout vous expliquer ?"
    ]
    
    ENCOURAGEMENTS = [
        "Allez-y, vous y êtes presque !",
        "C'est mieux, continuez !",
        "Voilà, c'est ça l'idée !",
        "Pas mal, pas mal du tout !",
        "Enfin ! On progresse !",
        "C'est déjà plus cohérent !",
        "Vous commencez à piger le truc !"
    ]
    
    @staticmethod
    def get_impatience():
        return random.choice(KaamelottResponses.IMPATIENCE)
    
    @staticmethod
    def get_error():
        return random.choice(KaamelottResponses.ERREURS)
    
    @staticmethod
    def get_encouragement():
        return random.choice(KaamelottResponses.ENCOURAGEMENTS)