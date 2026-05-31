import logging
import os


class LoggerTool:
    def __init__(self):
        level = os.environ.get("PASH_LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=getattr(logging, level, logging.INFO),
        )
        self._logger = logging.getLogger("pash-pipe")

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def debug(self, msg: str) -> None:
        self._logger.debug(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)
