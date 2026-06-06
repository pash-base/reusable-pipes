from infra.tools.logger_tool import LoggerTool
from infra.tools.config_tool import ConfigTool
from adapters.clients.github_client import GithubClient
from adapters.clients.argocd_client import ArgocdClient
from adapters.repositories.pashfile_repository import PashfileRepository
from core.application.parse_pashfile_use_case import ParsePashfileUseCase
from core.application.build_image_use_case import BuildImageUseCase
from core.application.push_image_use_case import PushImageUseCase
from core.application.update_image_tag_use_case import UpdateImageTagUseCase
from core.application.sync_argocd_use_case import SyncArgoCDUseCase
from core.application.update_release_target_use_case import UpdateReleaseTargetUseCase
from core.application.resolve_app_names_use_case import ResolveAppNamesUseCase
from core.application.install_use_case import InstallUseCase
from core.application.fmt_use_case import FmtUseCase
from core.application.lint_use_case import LintUseCase
from core.application.test_use_case import TestUseCase
from core.application.cover_use_case import CoverUseCase
from core.application.validate_use_case import ValidateUseCase
from infra.init.cli_init import CliInit


class IocInit:
    def get_cli_init(self) -> CliInit:
        logger = LoggerTool()
        config = ConfigTool()
        github_client = GithubClient(config=config, logger=logger)
        argocd_client = ArgocdClient(config=config, logger=logger)
        pashfile_repo = PashfileRepository(logger=logger)

        parse_uc = ParsePashfileUseCase(pashfile_repo=pashfile_repo, logger=logger)
        build_uc = BuildImageUseCase(logger=logger)
        push_uc = PushImageUseCase(logger=logger)
        update_uc = UpdateImageTagUseCase(github_client=github_client, logger=logger)
        sync_uc = SyncArgoCDUseCase(argocd_client=argocd_client, logger=logger)
        update_release_target_uc = UpdateReleaseTargetUseCase(logger=logger)
        resolve_uc = ResolveAppNamesUseCase(logger=logger)
        install_uc = InstallUseCase(logger=logger)
        fmt_uc = FmtUseCase(logger=logger)
        lint_uc = LintUseCase(logger=logger)
        test_uc = TestUseCase(logger=logger)
        cover_uc = CoverUseCase(logger=logger)
        validate_uc = ValidateUseCase(
            install_uc=install_uc,
            fmt_uc=fmt_uc,
            lint_uc=lint_uc,
            test_uc=test_uc,
            cover_uc=cover_uc,
            logger=logger,
        )

        return CliInit(
            parse_uc=parse_uc,
            build_uc=build_uc,
            push_uc=push_uc,
            update_uc=update_uc,
            sync_uc=sync_uc,
            resolve_uc=resolve_uc,
            install_uc=install_uc,
            fmt_uc=fmt_uc,
            lint_uc=lint_uc,
            test_uc=test_uc,
            cover_uc=cover_uc,
            validate_uc=validate_uc,
            update_release_target_uc=update_release_target_uc,
            logger=logger,
        )
