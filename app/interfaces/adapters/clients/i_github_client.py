from abc import ABC, abstractmethod


class IGithubClient(ABC):
    @abstractmethod
    def commit_and_push(self, file_path: str, message: str, branch: str) -> None:
        pass
