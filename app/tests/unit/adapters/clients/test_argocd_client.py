import os
import pytest
import adapters.clients.argocd_client as argocd_module
from unittest.mock import MagicMock, patch
from adapters.clients.argocd_client import ArgocdClient


def test_should_post_to_argocd_sync_endpoint_when_sync_is_called():
    # Arrange
    mock_config = MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = False
    mock_logger = MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)

    # Act
    with patch.object(argocd_module, "requests") as mock_requests:
        mock_requests.post.return_value.raise_for_status.return_value = None
        client.sync("portal-platform-dev")

        # Assert
        mock_requests.post.assert_called_once_with(
            "https://argocd.local/api/v1/applications/portal-platform-dev/sync",
            headers={"Authorization": "Bearer test-token"},
            verify=True,
            timeout=30,
        )
        mock_requests.post.return_value.raise_for_status.assert_called_once()
        mock_logger.info.assert_called_once_with("Sincronizando ArgoCD app: portal-platform-dev")


def test_should_skip_tls_verification_when_argocd_insecure_is_true():
    # Arrange
    mock_config = MagicMock()
    mock_config.argocd_url = "https://argocd.local"
    mock_config.argocd_token = "test-token"
    mock_config.argocd_insecure = True
    mock_logger = MagicMock()
    client = ArgocdClient(config=mock_config, logger=mock_logger)

    # Act
    with patch.object(argocd_module, "requests") as mock_requests:
        mock_requests.post.return_value.raise_for_status.return_value = None
        client.sync("my-app")

        # Assert
        mock_requests.post.assert_called_once_with(
            "https://argocd.local/api/v1/applications/my-app/sync",
            headers={"Authorization": "Bearer test-token"},
            verify=False,
            timeout=30,
        )
        mock_requests.post.return_value.raise_for_status.assert_called_once()
        mock_logger.info.assert_called_once_with("Sincronizando ArgoCD app: my-app")
