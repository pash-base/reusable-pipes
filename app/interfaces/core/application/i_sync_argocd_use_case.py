from abc import ABC, abstractmethod


class ISyncArgoCDUseCase(ABC):
    @abstractmethod
    def execute(self, app_name: str) -> None:
        pass
