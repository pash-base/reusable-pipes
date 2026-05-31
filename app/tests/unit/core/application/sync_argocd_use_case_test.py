from core.application.sync_argocd_use_case import SyncArgoCDUseCase


def test_should_call_argocd_sync_when_app_name_is_valid(mocker):
    # Arrange
    mock_argocd = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    use_case = SyncArgoCDUseCase(argocd_client=mock_argocd, logger=mock_logger)

    # Act
    use_case.execute(app_name="portal-platform-dev")

    # Assert
    mock_argocd.sync.assert_called_once_with("portal-platform-dev")
    mock_logger.info.assert_called_once_with("Sincronizando app ArgoCD: portal-platform-dev")


def test_should_log_app_name_when_syncing(mocker):
    # Arrange
    mock_argocd = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    use_case = SyncArgoCDUseCase(argocd_client=mock_argocd, logger=mock_logger)

    # Act
    use_case.execute(app_name="my-app-prd")

    # Assert
    mock_logger.info.assert_called_once_with("Sincronizando app ArgoCD: my-app-prd")
    mock_argocd.sync.assert_called_once_with("my-app-prd")
