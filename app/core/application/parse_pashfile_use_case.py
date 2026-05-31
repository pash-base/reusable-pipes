from interfaces.core.application.i_parse_pashfile_use_case import IParsePashfileUseCase
from interfaces.adapters.repositories.i_pashfile_repository import IPashfileRepository
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class ParsePashfileUseCase(IParsePashfileUseCase):
    def __init__(self, pashfile_repo: IPashfileRepository, logger: ILoggerTool):
        self._pashfile_repo = pashfile_repo
        self._logger = logger

    def execute(self, path: str) -> PashAppModel:
        self._logger.info("Executando ParsePashfileUseCase")
        return self._pashfile_repo.load(path)
