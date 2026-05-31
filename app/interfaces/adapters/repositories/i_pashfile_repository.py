from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class IPashfileRepository(ABC):
    @abstractmethod
    def load(self, path: str) -> PashAppModel:
        pass
