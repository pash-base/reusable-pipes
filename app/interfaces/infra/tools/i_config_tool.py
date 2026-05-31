from abc import ABC, abstractmethod


class IConfigTool(ABC):
    @property
    @abstractmethod
    def github_token(self) -> str:
        pass

    @property
    @abstractmethod
    def argocd_url(self) -> str:
        pass

    @property
    @abstractmethod
    def argocd_token(self) -> str:
        pass

    @property
    @abstractmethod
    def registry(self) -> str:
        pass

    @property
    @abstractmethod
    def argocd_insecure(self) -> bool:
        pass
