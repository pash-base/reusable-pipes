from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class IBuildImageUseCase(ABC):
    @abstractmethod
    def execute(self, app: PashAppModel, tag: str) -> None:
        pass
