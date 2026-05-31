from abc import ABC, abstractmethod


class IArgocdClient(ABC):
    @abstractmethod
    def sync(self, app_name: str) -> None:
        pass
