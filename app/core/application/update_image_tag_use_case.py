import yaml
from interfaces.core.application.i_update_image_tag_use_case import IUpdateImageTagUseCase
from interfaces.adapters.clients.i_github_client import IGithubClient
from core.domain.models.pash_app_model import PashAppModel
from infra.tools.logger_tool import LoggerTool


class UpdateImageTagUseCase(IUpdateImageTagUseCase):
    def __init__(self, github_client: IGithubClient, logger: LoggerTool):
        self._github_client = github_client
        self._logger = logger

    def execute(self, app: PashAppModel, env: str, tag: str) -> None:
        env_cfg = app.helm.environments[env]
        values_path = env_cfg.values_file
        self._logger.info(f"Atualizando image.tag para {tag} em {values_path}")

        with open(values_path, "r") as f:
            values = yaml.safe_load(f)

        values["image"]["tag"] = tag

        with open(values_path, "w") as f:
            yaml.dump(values, f, default_flow_style=False, allow_unicode=True)

        self._github_client.commit_and_push(
            file_path=values_path,
            message=f"chore(gitops): atualizar image.tag para {tag} em {env}",
            branch="develop" if env == "dev" else ("release/current" if env == "hom" else "master"),
        )
