import yaml
from interfaces.adapters.repositories.i_pashfile_repository import IPashfileRepository
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig
from infra.tools.logger_tool import LoggerTool


class PashfileRepository(IPashfileRepository):
    def __init__(self, logger: LoggerTool):
        self._logger = logger

    def load(self, path: str) -> PashAppModel:
        self._logger.info(f"Lendo .pashfile em: {path}")
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        metadata = data["metadata"]
        helm_data = data["spec"]["pipeline"]["helm"]
        envs = {env: EnvironmentConfig(values_file=cfg["valuesFile"]) for env, cfg in helm_data["environments"].items()}
        helm = HelmConfig(
            chart_repo=helm_data["chartRepo"],
            chart_name=helm_data["chartName"],
            chart_version=helm_data["chartVersion"],
            environments=envs,
        )
        return PashAppModel(
            sigla=metadata["sigla"],
            app_name=metadata["appName"],
            repo=metadata["repo"],
            helm=helm,
        )
