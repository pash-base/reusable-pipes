import yaml
from interfaces.adapters.repositories.i_pashfile_repository import IPashfileRepository
from interfaces.infra.tools.i_logger_tool import ILoggerTool
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig, QualityConfig


class PashfileRepository(IPashfileRepository):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def _derive_from_repo_name(self, sigla: str, repo: str) -> tuple:
        """Deriva tipo e shortname do nome do repositório no padrão pash-<sigla>-<tipo>-<shortname>."""
        repo_name = repo.split("/")[-1] if "/" in repo else repo
        prefix = f"pash-{sigla.lower()}-"
        if repo_name.startswith(prefix):
            start = len(prefix)
            remainder = repo_name[start:]
            parts = remainder.split("-", 1)
            if len(parts) == 2:
                return parts[0], parts[1]
        return None, None

    def _parse_quality(self, pipeline: dict) -> QualityConfig | None:
        """Parse quality config from pipeline if runtime is present."""
        runtime = pipeline.get("runtime")
        if not runtime:
            return None

        def _val(key: str) -> str | None:
            v = pipeline.get(key)
            return v if v else None

        return QualityConfig(
            runtime=runtime,
            workdir=pipeline.get("workdir", ""),
            install_command=_val("installCommand"),
            fmt_command=_val("fmtCommand"),
            lint_command=_val("lintCommand"),
            test_command=_val("testCommand"),
            cover_command=_val("coverCommand"),
            build_command=_val("buildCommand"),
            lint_config=_val("lintConfig"),
            cover_config=_val("coverConfig"),
            ignore_patterns=pipeline.get("ignorePatterns", []),
            coverage_threshold=pipeline.get("coverageThreshold", 90),
        )

    def load(self, path: str) -> PashAppModel:
        self._logger.info(f"Lendo .pashfile em: {path}")
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        metadata = data["metadata"]
        pipeline = data["spec"]["pipeline"]
        helm_data = pipeline["helm"]
        envs = {env: EnvironmentConfig(values_file=cfg["valuesFile"]) for env, cfg in helm_data["environments"].items()}
        helm = HelmConfig(
            chart_repo=helm_data["chartRepo"],
            chart_name=helm_data["chartName"],
            chart_version=helm_data["chartVersion"],
            environments=envs,
        )

        sigla = metadata["sigla"]
        repo = metadata["repo"]
        explicit_type = metadata.get("type")
        explicit_shortname = metadata.get("shortname")

        if explicit_type and explicit_shortname:
            obj_type, obj_shortname = explicit_type, explicit_shortname
        else:
            derived_type, derived_shortname = self._derive_from_repo_name(sigla, repo)
            obj_type = explicit_type or derived_type
            obj_shortname = explicit_shortname or derived_shortname

        return PashAppModel(
            sigla=sigla,
            app_name=metadata["appName"],
            repo=repo,
            helm=helm,
            type=obj_type,
            shortname=obj_shortname,
            quality=self._parse_quality(pipeline),
        )
