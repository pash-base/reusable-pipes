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
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


def test_should_raise_file_not_found_when_path_does_not_exist(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    repo = PashfileRepository(logger=mock_logger)

    path = "/nonexistent/path/.pashfile"

    # Act
    with pytest.raises(FileNotFoundError):
        repo.load(path)

    # Assert
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")


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
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


def test_should_derive_type_from_repo_name_when_type_not_in_metadata(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_VALID_PASHFILE, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.type == "portal"
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


def test_should_derive_shortname_from_repo_name_when_shortname_not_in_metadata(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_VALID_PASHFILE, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.shortname == "platform"
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


def test_should_use_explicit_type_when_type_is_in_metadata(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    pashfile_with_type = dict(_VALID_PASHFILE)
    pashfile_with_type["metadata"] = dict(_VALID_PASHFILE["metadata"])
    pashfile_with_type["metadata"]["type"] = "py-mcp"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(pashfile_with_type, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.type == "py-mcp"
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


def test_should_use_explicit_shortname_when_shortname_is_in_metadata(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    pashfile_with_shortname = dict(_VALID_PASHFILE)
    pashfile_with_shortname["metadata"] = dict(_VALID_PASHFILE["metadata"])
    pashfile_with_shortname["metadata"]["shortname"] = "override"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(pashfile_with_shortname, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.shortname == "override"
    mock_logger.info.assert_called_once_with(f"Lendo .pashfile em: {path}")
    os.unlink(path)


_PASHFILE_WITH_QUALITY = {
    "apiVersion": "platform.io/v1",
    "kind": "PashApp",
    "metadata": {
        "sigla": "DOC",
        "appName": "portal-platform",
        "repo": "pash-doc/pash-doc-portal-platform",
    },
    "spec": {
        "pipeline": {
            "runtime": "node",
            "workdir": "app/",
            "installCommand": "npm install",
            "fmtCommand": "npm run fmt",
            "lintCommand": "npm run lint",
            "testCommand": "",
            "coverCommand": "",
            "buildCommand": "npm run build",
            "lintConfig": "app/eslint.config.mjs",
            "coverConfig": "",
            "ignorePatterns": [],
            "coverageThreshold": 0,
            "helm": {
                "chartRepo": "pash-inf/pash-inf-helm-charts",
                "chartName": "pash-stacks",
                "chartVersion": "0.1.0",
                "environments": {
                    "dev": {"valuesFile": "app/_environments/dev/values-dev.yaml"},
                },
            },
        }
    },
}


def test_should_return_quality_config_when_pashfile_has_runtime(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_PASHFILE_WITH_QUALITY, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.quality is not None
    assert result.quality.runtime == "node"
    assert result.quality.workdir == "app/"
    assert result.quality.install_command == "npm install"
    assert result.quality.fmt_command == "npm run fmt"
    assert result.quality.lint_command == "npm run lint"
    assert result.quality.test_command is None
    assert result.quality.cover_command is None
    assert result.quality.build_command == "npm run build"
    assert result.quality.lint_config == "app/eslint.config.mjs"
    assert result.quality.cover_config is None
    assert result.quality.ignore_patterns == []
    assert result.quality.coverage_threshold == 0
    os.unlink(path)


def test_should_return_quality_none_when_pashfile_has_no_runtime(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(_VALID_PASHFILE, f)
        path = f.name

    repo = PashfileRepository(logger=mock_logger)

    # Act
    result = repo.load(path)

    # Assert
    assert result.quality is None
    os.unlink(path)
