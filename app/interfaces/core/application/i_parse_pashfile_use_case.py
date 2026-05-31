from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class IParsePashfileUseCase(ABC):
    @abstractmethod
    def execute(self, path: str) -> PashAppModel:
        pass
