import subprocess
from interfaces.core.application.i_test_use_case import ITestUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class TestUseCase(ITestUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        if app.quality is None or not app.quality.test_command:
            self._logger.warning("Nenhum testCommand configurado — sem testes configurados.")
            return
        self._logger.info(f"Executando test: {app.quality.test_command}")
        subprocess.run(app.quality.test_command, shell=True, cwd=app.quality.workdir, check=True)
