from typing import Dict
from interfaces.core.application.i_resolve_app_names_use_case import IResolveAppNamesUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class ResolveAppNamesUseCase(IResolveAppNamesUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> Dict[str, str]:
        self._logger.info("Executando ResolveAppNamesUseCase")
        sigla_lower = app.sigla.lower()
        repo_type = self._derive_type(app)
        shortname = self._derive_shortname(app)
        return {env: f"{sigla_lower}-{repo_type}-{shortname}-{env}" for env in app.helm.environments}

    def _derive_type(self, app: PashAppModel) -> str:
        if app.type:
            return app.type
        parts = app.repo.split("/")[-1].split("-")
        return parts[2] if len(parts) >= 3 else ""

    def _derive_shortname(self, app: PashAppModel) -> str:
        if app.shortname:
            return app.shortname
        parts = app.repo.split("/")[-1].split("-")
        return "-".join(parts[3:]) if len(parts) >= 4 else ""
