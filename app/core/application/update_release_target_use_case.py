import os
import subprocess
import yaml
from interfaces.core.application.i_update_release_target_use_case import IUpdateReleaseTargetUseCase
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class UpdateReleaseTargetUseCase(IUpdateReleaseTargetUseCase):
    def __init__(self, logger: ILoggerTool):
        self._logger = logger

    def execute(self, app_name: str, branch: str) -> None:
        self._logger.info(f"Atualizando {app_name} targetRevision → {branch} via GitOps")
        token = os.environ.get("GH_TOKEN", "")
        sigla = app_name.split("-")[0]
        shortname = "-".join(app_name.split("-")[1:3])
        config_file = f"argocd/applications/{sigla}/{shortname}/{app_name}.yaml"
        clone_url = f"https://x-access-token:{token}@github.com/pash-base/platform-config.git"

        subprocess.run(["rm", "-rf", "/tmp/platform-config"], check=True)
        subprocess.run(["git", "clone", "--depth", "1", clone_url, "/tmp/platform-config"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                "/tmp/platform-config",
                "config",
                "user.email",
                "github-actions[bot]@users.noreply.github.com",
            ],
            check=True,
        )
        subprocess.run(["git", "-C", "/tmp/platform-config", "config", "user.name", "github-actions[bot]"], check=True)

        path = f"/tmp/platform-config/{config_file}"
        with open(path) as f:
            data = yaml.safe_load(f)
        for source in data["spec"]["sources"]:
            if source.get("ref") == "values":
                source["targetRevision"] = branch
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

        subprocess.run(["git", "-C", "/tmp/platform-config", "add", "-A"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                "/tmp/platform-config",
                "commit",
                "-m",
                f"chore(gitops): update {app_name} targetRevision → {branch}",
            ],
            check=True,
        )
        subprocess.run(["git", "-C", "/tmp/platform-config", "push"], check=True)
