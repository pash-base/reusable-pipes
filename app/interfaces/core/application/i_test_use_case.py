from abc import ABC, abstractmethod
from core.domain.models.pash_app_model import PashAppModel


class ITestUseCase(ABC):
    @abstractmethod
    def execute(self, app: PashAppModel) -> None:
        pass
