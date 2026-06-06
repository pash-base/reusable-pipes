from abc import ABC, abstractmethod


class IUpdateReleaseTargetUseCase(ABC):
    @abstractmethod
    def execute(self, app_name: str, branch: str) -> None:
        pass
