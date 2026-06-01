import subprocess
from interfaces.core.application.i_install_use_case import IInstallUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class InstallUseCase(IInstallUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        if app.quality is None or not app.quality.install_command:
            self._logger.warning("Nenhum installCommand configurado — etapa de instalação ignorada.")
            return
        self._logger.info(f"Executando install: {app.quality.install_command}")
        subprocess.run(app.quality.install_command, shell=True, cwd=app.quality.workdir, check=True)
