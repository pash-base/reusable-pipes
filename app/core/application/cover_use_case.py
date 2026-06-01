import re
import subprocess
from interfaces.core.application.i_cover_use_case import ICoverUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class CoverUseCase(ICoverUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        if app.quality is None or not app.quality.cover_command or app.quality.coverage_threshold == 0:
            self._logger.warning("Nenhum coverCommand configurado ou threshold zero — etapa de cobertura ignorada.")
            return

        threshold = app.quality.coverage_threshold
        self._logger.info(f"Executando cover: {app.quality.cover_command}")

        result = subprocess.run(
            app.quality.cover_command,
            shell=True,
            cwd=app.quality.workdir,
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr

        coverage = self._parse_coverage(output, app.quality.runtime)
        if coverage is None:
            self._logger.warning("Não foi possível determinar a cobertura a partir da saída do comando.")
            return

        self._logger.info(f"Cobertura: {coverage}% (mínimo: {threshold}%)")
        if coverage < threshold:
            raise RuntimeError(f"Cobertura {coverage}% abaixo do mínimo {threshold}%")

    def _parse_coverage(self, output: str, runtime: str) -> float | None:
        if runtime == "node":
            match = re.search(r"All files\s+\|\s+(\d+(?:\.\d+)?)\s+\|", output)
        elif runtime == "python":
            match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
        else:
            match = re.search(r"(\d+(?:\.\d+)?)%", output)

        if match:
            return float(match.group(1))
        return None
