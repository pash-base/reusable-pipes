import os
import tempfile
import pytest
import yaml
from adapters.repositories.pashfile_repository import PashfileRepository
from core.domain.models.pash_app_model import PashAppModel


_VALID_PASHFILE = {
    "apiVersion": "platform.io/v1",
    "kind": "PashApp",
    "metadata": {
        "sigla": "DOC",
        "appName": "portal-platform",
        "repo": "pash-doc/pash-doc-portal-platform",
    },
    "spec": {
        "pipeline": {
            "helm": {
                "chartRepo": "pash-inf/pash-inf-helm-charts",
                "chartName": "pash-stacks",
                "chartVersion": "0.1.0",
                "environments": {
                    "dev": {"valuesFile": "app/_environments/dev/values-dev.yaml"},
                    "hom": {"valuesFile": "app/_environments/hom/values-hom.yaml"},
                    "prd": {"valuesFile": "app/_environments/prd/values-prd.yaml"},
                },
            }
        }
    },
}


def test_should_return_pash_app_model_when_pashfile_is_valid(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_VALID_PASHFILE, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert isinstance(result, PashAppModel)
    assert result.sigla == "DOC"
    assert result.app_name == "portal-platform"
    assert result.repo == "pash-doc/pash-doc-portal-platform"
    assert result.helm.chart_name == "pash-stacks"
    assert result.helm.chart_version == "0.1.0"
    assert "dev" in result.helm.environments
    mock_logger.info.assert_called_once()
    os.unlink(path)


def test_should_raise_file_not_found_when_path_does_not_exist(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    repo = PashfileRepository(logger=mock_logger)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        repo.load("/nonexistent/path/.pashfile")


def test_should_load_all_environments_when_pashfile_has_three_envs(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_VALID_PASHFILE, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert set(result.helm.environments.keys()) == {"dev", "hom", "prd"}
    assert result.helm.environments["prd"].values_file == "app/_environments/prd/values-prd.yaml"
    os.unlink(path)
