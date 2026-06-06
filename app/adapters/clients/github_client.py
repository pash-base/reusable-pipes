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
        # Salva o conteúdo modificado, descarta mudanças locais, troca de branch
        with open(file_path) as f:
            content = f.read()
        subprocess.run(["git", "checkout", "--", file_path], check=False)
        subprocess.run(["git", "checkout", branch], check=False)
        subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", branch], check=False)
        # Reescreve o arquivo com nosso conteúdo e commit
        with open(file_path, "w") as f:
            f.write(content)
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=False)
        subprocess.run(["git", "push", "origin", branch], check=True)
