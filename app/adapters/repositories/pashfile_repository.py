import yaml
from interfaces.adapters.repositories.i_pashfile_repository import IPashfileRepository
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class PashfileRepository(IPashfileRepository):
    def __init__(self, logger: ILoggerTool):
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

        repo_name = metadata.get("repo", "")
        parts = repo_name.split("/")[-1].split("-") if repo_name else []
        repo_type = metadata.get("type") or (parts[2] if len(parts) >= 3 else None)
        shortname = metadata.get("shortname") or ("-".join(parts[3:]) if len(parts) >= 4 else None)

        return PashAppModel(
            sigla=metadata["sigla"],
            app_name=metadata["appName"],
            repo=repo_name,
            helm=helm,
            type=repo_type,
            shortname=shortname,
        )
