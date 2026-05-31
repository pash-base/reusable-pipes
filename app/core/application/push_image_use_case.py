import subprocess
from interfaces.core.application.i_push_image_use_case import IPushImageUseCase
from core.domain.models.pash_app_model import PashAppModel
from infra.tools.logger_tool import LoggerTool


class PushImageUseCase(IPushImageUseCase):
    def __init__(self, logger: LoggerTool):
        self._logger = logger

    def execute(self, app: PashAppModel, tag: str) -> None:
        image = f"ghcr.io/{app.repo}:{tag}"
        self._logger.info(f"Publicando imagem: {image}")
        subprocess.run(["docker", "push", image], check=True)
