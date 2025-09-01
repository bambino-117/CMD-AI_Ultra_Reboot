class BoiteConteneur:
    def __init__(self, capacite_max):
        self.capacite_max = capacite_max
        self.contenu = []
    
    def ajouter(self, element):
        if len(self.contenu) < self.capacite_max:
            self.contenu.append(element)
            return True
        return False
    
    def retirer(self, element):
        if element in self.contenu:
            self.contenu.remove(element)
            return True
        return False
    
    def est_pleine(self):
        return len(self.contenu) >= self.capacite_max
    
    def est_vide(self):
        return len(self.contenu) == 0
    
    def capacite_restante(self):
        return self.capacite_max - len(self.contenu)
    
    def vider(self):
        self.contenu.clear()
    
    def __str__(self):
        return f"Boite [{len(self.contenu)}/{self.capacite_max}]: {self.contenu}"
    
    def __len__(self):
        return len(self.contenu)