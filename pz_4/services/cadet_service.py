from typing import List
from ..models.cadet_model import Cadet


class CadetService:
    def __init__(self):
        self.cadets: List[Cadet] = []

    def get_all(self) -> List[Cadet]:
        return self.cadets

    def add(self, cadet: Cadet) -> Cadet:
        self.cadets.append(cadet)
        return cadet

    def delete(self, cadet_id: int) -> bool:
        initial_length = len(self.cadets)
        self.cadets = [c for c in self.cadets if c.id != cadet_id]
        return len(self.cadets) < initial_length

    def update(self, cadet_id: int, cadet: Cadet) -> bool:
        for i, c in enumerate(self.cadets):
            if c.id == cadet_id:
                self.cadets[i] = cadet
                return True
        return False