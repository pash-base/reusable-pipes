from abc import ABC, abstractmethod
from typing import Dict
from core.domain.models.pash_app_model import PashAppModel


class IResolveAppNamesUseCase(ABC):
    @abstractmethod
    def execute(self, app: PashAppModel) -> Dict[str, str]:
        pass
