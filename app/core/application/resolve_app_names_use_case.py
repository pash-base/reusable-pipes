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
        repo_type = app.type or ""
        shortname = app.shortname or ""
        return {env: f"{sigla_lower}-{repo_type}-{shortname}-{env}" for env in app.helm.environments}
