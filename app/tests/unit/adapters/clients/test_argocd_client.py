import os
import pytest
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
    with patch("adapters.clients.argocd_client.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_post.return_value = mock_response
        client.sync("portal-platform-dev")

        # Assert
        mock_post.assert_called_once_with(
            "https://argocd.local/api/v1/applications/portal-platform-dev/sync",
            headers={"Authorization": "Bearer test-token"},
            verify=True,
            timeout=30,
        )
    mock_response.raise_for_status.assert_called_once()
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
    with patch("adapters.clients.argocd_client.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_post.return_value = mock_response
        client.sync("my-app")

        # Assert
        mock_post.assert_called_once_with(
            "https://argocd.local/api/v1/applications/my-app/sync",
            headers={"Authorization": "Bearer test-token"},
            verify=False,
            timeout=30,
        )
