import subprocess
from interfaces.core.application.i_build_image_use_case import IBuildImageUseCase
from core.domain.models.pash_app_model import PashAppModel
from infra.tools.logger_tool import LoggerTool


class BuildImageUseCase(IBuildImageUseCase):
    def __init__(self, logger: LoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel, tag: str) -> None:
        image = f"ghcr.io/{app.repo}:{tag}"
        self._logger.info(f"Construindo imagem: {image}")
        subprocess.run(["docker", "build", "-t", image, "app/"], check=True)
