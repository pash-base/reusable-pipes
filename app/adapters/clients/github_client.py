import subprocess
from interfaces.adapters.clients.i_github_client import IGithubClient
from infra.tools.config_tool import ConfigTool
from infra.tools.logger_tool import LoggerTool


class GithubClient(IGithubClient):
    def __init__(self, config: ConfigTool, logger: LoggerTool):
        self._config = config
        self._logger = logger

    def commit_and_push(self, file_path: str, message: str, branch: str) -> None:
        self._logger.info(f"Commitando {file_path} na branch {branch}")
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", branch], check=True)
