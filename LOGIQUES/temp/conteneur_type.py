from typing import Generic, TypeVar, List

T = TypeVar('T')

class ConteneurType(Generic[T]):
    def __init__(self, capacite_max: int):
        self.capacite_max = capacite_max
        self.elements: List[T] = []
    
    def ajouter(self, element: T) -> bool:
        if len(self.elements) < self.capacite_max:
            self.elements.append(element)
            return True
        return False
    
    def retirer_par_index(self, index: int) -> T:
        if 0 <= index < len(self.elements):
            return self.elements.pop(index)
        raise IndexError("Index hors limites")
    
    def obtenir(self, index: int) -> T:
        if 0 <= index < len(self.elements):
            return self.elements[index]
        raise IndexError("Index hors limites")
    
    def __iter__(self):
        return iter(self.elements)
    
    def __getitem__(self, index):
        return self.elements[index]
    
    def __setitem__(self, index, value):
        self.elements[index] = value