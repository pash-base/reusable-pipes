import subprocess
from interfaces.core.application.i_lint_use_case import ILintUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class LintUseCase(ILintUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        if app.quality is None or not app.quality.lint_command:
            self._logger.warning("Nenhum lintCommand configurado — etapa de lint ignorada.")
            return
        self._logger.info(f"Executando lint: {app.quality.lint_command}")
        subprocess.run(app.quality.lint_command, shell=True, cwd=app.quality.workdir, check=True)
