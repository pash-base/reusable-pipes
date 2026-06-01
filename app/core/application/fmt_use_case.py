import subprocess
from interfaces.core.application.i_fmt_use_case import IFmtUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class FmtUseCase(IFmtUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        if app.quality is None or not app.quality.fmt_command:
            self._logger.warning("Nenhum fmtCommand configurado — etapa de formatação ignorada.")
            return
        self._logger.info(f"Executando fmt: {app.quality.fmt_command}")
        subprocess.run(app.quality.fmt_command, shell=True, cwd=app.quality.workdir, check=True)
