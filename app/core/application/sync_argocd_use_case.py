from interfaces.core.application.i_sync_argocd_use_case import ISyncArgoCDUseCase
from interfaces.adapters.clients.i_argocd_client import IArgocdClient
from interfaces.infra.tools.i_logger_tool import ILoggerTool


class SyncArgoCDUseCase(ISyncArgoCDUseCase):
    def __init__(self, argocd_client: IArgocdClient, logger: ILoggerTool):
        self._argocd_client = argocd_client
        self._logger = logger

    def execute(self, app_name: str) -> None:
        self._logger.info(f"Sincronizando app ArgoCD: {app_name}")
        self._argocd_client.sync(app_name)
