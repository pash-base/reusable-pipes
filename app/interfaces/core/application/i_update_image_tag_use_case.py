from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class IUpdateImageTagUseCase(ABC):
    @abstractmethod
    def execute(self, app: PashAppModel, env: str, tag: str) -> None:
        pass
