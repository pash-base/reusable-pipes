from interfaces.core.application.i_sync_argocd_use_case import ISyncArgoCDUseCase
from interfaces.adapters.clients.i_argocd_client import IArgocdClient
from infra.tools.logger_tool import LoggerTool


class SyncArgoCDUseCase(ISyncArgoCDUseCase):
    def __init__(self, argocd_client: IArgocdClient, logger: LoggerTool):
        self._argocd_client = argocd_client
        self._logger = logger

    def execute(self, app_name: str) -> None:
        self._logger.info(f"Sincronizando app ArgoCD: {app_name}")
        self._argocd_client.sync(app_name)
