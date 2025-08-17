from abc import ABC, abstractmethod
from typing import List
from src.models import User, DigitalFootprintItem

class WebScraper(ABC):
    @abstractmethod
    def scan(self, user: User, identity: str) -> List[DigitalFootprintItem]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
