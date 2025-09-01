from heapq import heappush, heappop

class ConteneurPriorite:
    def __init__(self, capacite_max):
        self.capacite_max = capacite_max
        self.heap = []
    
    def ajouter(self, element, priorite):
        if len(self.heap) < self.capacite_max:
            heappush(self.heap, (priorite, element))
            return True
        return False
    
    def retirer_plus_prioritaire(self):
        if self.heap:
            return heappop(self.heap)[1]
        return None
    
    def voir_plus_prioritaire(self):
        if self.heap:
            return self.heap[0][1]
        return None