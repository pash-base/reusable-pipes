import requests
from interfaces.adapters.clients.i_argocd_client import IArgocdClient
from interfaces.infra.tools.i_config_tool import IConfigTool
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class ArgocdClient(IArgocdClient):
    def __init__(self, config: IConfigTool, logger: ILoggerTool):
        self._config = config
        self._logger = logger

    def sync(self, app_name: str) -> None:
        url = f"{self._config.argocd_url}/api/v1/applications/{app_name}/sync"
        headers = {"Authorization": f"Bearer {self._config.argocd_token}"}
        verify_tls = not self._config.argocd_insecure
        self._logger.info(f"Sincronizando ArgoCD app: {app_name}")
        response = requests.post(url, headers=headers, json={}, verify=verify_tls, timeout=30)
        if response.status_code >= 500:
            response.raise_for_status()
        elif response.status_code >= 400:
            self._logger.warning(f"ArgoCD sync retornou {response.status_code}: {response.text[:200]}")
