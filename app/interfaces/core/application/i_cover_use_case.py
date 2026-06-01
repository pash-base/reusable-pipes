from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class ICoverUseCase(ABC):
    @abstractmethod
    def execute(self, app: PashAppModel) -> None:
        pass
