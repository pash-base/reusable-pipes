import os
import pytest
from infra.tools.config_tool import ConfigTool


def test_should_return_github_token_when_env_var_is_set(monkeypatch):
    # Arrange
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_testtoken")
    tool = ConfigTool()

    # Act
    result = tool.github_token

    # Assert
    assert result == "ghp_testtoken"


def test_should_raise_environment_error_when_github_token_is_missing(monkeypatch):
    # Arrange
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    tool = ConfigTool()

    # Act & Assert
    with pytest.raises(EnvironmentError, match="GITHUB_TOKEN"):
        _ = tool.github_token


def test_should_return_argocd_url_when_env_var_is_set(monkeypatch):
    # Arrange
    monkeypatch.setenv("ARGOCD_URL", "https://argocd.local")
    tool = ConfigTool()

    # Act
    result = tool.argocd_url

    # Assert
    assert result == "https://argocd.local"


def test_should_return_argocd_token_when_env_var_is_set(monkeypatch):
    # Arrange
    monkeypatch.setenv("ARGOCD_TOKEN", "argocd-token-123")
    tool = ConfigTool()

    # Act
    result = tool.argocd_token

    # Assert
    assert result == "argocd-token-123"


def test_should_return_registry_when_env_var_is_set(monkeypatch):
    # Arrange
    monkeypatch.setenv("REGISTRY", "ghcr.io")
    tool = ConfigTool()

    # Act
    result = tool.registry

    # Assert
    assert result == "ghcr.io"


def test_should_return_true_when_argocd_insecure_is_true(monkeypatch):
    # Arrange
    monkeypatch.setenv("ARGOCD_INSECURE", "true")
    tool = ConfigTool()

    # Act
    result = tool.argocd_insecure

    # Assert
    assert result is True


def test_should_return_false_when_argocd_insecure_is_false(monkeypatch):
    # Arrange
    monkeypatch.setenv("ARGOCD_INSECURE", "false")
    tool = ConfigTool()

    # Act
    result = tool.argocd_insecure

    # Assert
    assert result is False


def test_should_return_false_when_argocd_insecure_is_not_set(monkeypatch):
    # Arrange
    monkeypatch.delenv("ARGOCD_INSECURE", raising=False)
    tool = ConfigTool()

    # Act
    result = tool.argocd_insecure

    # Assert
    assert result is False
