import requests
from interfaces.adapters.clients.i_argocd_client import IArgocdClient
from infra.tools.config_tool import ConfigTool
from infra.tools.logger_tool import LoggerTool


class ArgocdClient(IArgocdClient):
    def __init__(self, config: ConfigTool, logger: LoggerTool):
        self._config = config
        self._logger = logger

    def sync(self, app_name: str) -> None:
        url = f"{self._config.argocd_url}/api/v1/applications/{app_name}/sync"
        headers = {"Authorization": f"Bearer {self._config.argocd_token}"}
        verify_tls = not self._config.argocd_insecure
        self._logger.info(f"Sincronizando ArgoCD app: {app_name}")
        response = requests.post(url, headers=headers, verify=verify_tls, timeout=30)
        response.raise_for_status()
