import subprocess
from interfaces.adapters.clients.i_github_client import IGithubClient
from interfaces.infra.tools.i_config_tool import IConfigTool
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class GithubClient(IGithubClient):
    def __init__(self, config: IConfigTool, logger: ILoggerTool):
        self._config = config
        self._logger = logger

    def commit_and_push(self, file_path: str, message: str, branch: str) -> None:
        self._logger.info(f"Commitando {file_path} na branch {branch}")
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", branch], check=True)
