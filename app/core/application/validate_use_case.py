from interfaces.core.application.i_validate_use_case import IValidateUseCase
from interfaces.core.application.i_install_use_case import IInstallUseCase
from interfaces.core.application.i_fmt_use_case import IFmtUseCase
from interfaces.core.application.i_lint_use_case import ILintUseCase
from interfaces.core.application.i_test_use_case import ITestUseCase
from interfaces.core.application.i_cover_use_case import ICoverUseCase
from core.domain.models.pash_app_model import PashAppModel
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class ValidateUseCase(IValidateUseCase):
    def __init__(
        self,
        install_uc: IInstallUseCase,
        fmt_uc: IFmtUseCase,
        lint_uc: ILintUseCase,
        test_uc: ITestUseCase,
        cover_uc: ICoverUseCase,
        logger: ILoggerTool,
    ):
        self._install_uc = install_uc
        self._fmt_uc = fmt_uc
        self._lint_uc = lint_uc
        self._test_uc = test_uc
        self._cover_uc = cover_uc
        self._logger = logger

    def execute(self, app: PashAppModel) -> None:
        self._logger.info("Executando validate: install → fmt → lint → test → cover")
        self._install_uc.execute(app=app)
        self._fmt_uc.execute(app=app)
        self._lint_uc.execute(app=app)
        self._test_uc.execute(app=app)
        self._cover_uc.execute(app=app)
