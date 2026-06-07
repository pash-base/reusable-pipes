import adapters.clients.argocd_client as argocd_module
from adapters.clients.argocd_client import ArgocdClient


def test_should_post_to_argocd_sync_endpoint_when_sync_is_called(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = False
    mock_logger = mocker.MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)
    mock_requests = mocker.patch.object(argocd_module, "requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_requests.post.return_value = mock_response

    # Act
    client.sync("portal-platform-dev")

    # Assert
    mock_requests.post.assert_called_once_with(
        "https://argocd.local/api/v1/applications/portal-platform-dev/sync",
        headers={"Authorization": "Bearer test-token"},
        json={},
        verify=True,
        timeout=30,
    )
    mock_response.raise_for_status.assert_not_called()
    mock_logger.info.assert_called_once_with("Sincronizando ArgoCD app: portal-platform-dev")


def test_should_raise_error_when_argocd_returns_401_on_sync(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = False
    mock_logger = mocker.MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)
    mock_requests = mocker.patch.object(argocd_module, "requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = Exception("401 Client Error: Unauthorized")
    mock_requests.post.return_value = mock_response

    # Act
    raised = False
    try:
        client.sync("portal-platform-dev")
    except Exception:
        raised = True

    # Assert
    assert raised
    mock_requests.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


def test_should_raise_error_when_argocd_returns_500_on_sync(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = False
    mock_logger = mocker.MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)
    mock_requests = mocker.patch.object(argocd_module, "requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = Exception("500 Server Error: Internal Server Error")
    mock_requests.post.return_value = mock_response

    # Act
    raised = False
    try:
        client.sync("portal-platform-dev")
    except Exception:
        raised = True

    # Assert
    assert raised
    mock_requests.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


def test_should_skip_tls_verification_when_argocd_insecure_is_true(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = True
    mock_logger = mocker.MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)
    mock_requests = mocker.patch.object(argocd_module, "requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_requests.post.return_value = mock_response

    # Act
    client.sync("my-app")

    # Assert
    mock_requests.post.assert_called_once_with(
        "https://argocd.local/api/v1/applications/my-app/sync",
        headers={"Authorization": "Bearer test-token"},
        json={},
        verify=False,
        timeout=30,
    )
    mock_response.raise_for_status.assert_not_called()
    mock_logger.info.assert_called_once_with("Sincronizando ArgoCD app: my-app")
