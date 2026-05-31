import os
import tempfile
from unittest.mock import MagicMock, patch, call
import yaml
from core.application.update_image_tag_use_case import UpdateImageTagUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig


def _make_app(env_values_file: str) -> PashAppModel:
    return PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={
                "dev": EnvironmentConfig(values_file=env_values_file),
            },
        ),
    )


def test_should_update_image_tag_and_commit_when_env_is_dev():
    # Arrange
    mock_github = MagicMock()
    mock_logger = MagicMock()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"image": {"tag": "old-tag", "repository": "ghcr.io/test"}}, f)
        values_path = f.name

    app = _make_app(values_path)
    use_case = UpdateImageTagUseCase(github_client=mock_github, logger=mock_logger)

    # Act
    use_case.execute(app=app, env="dev", tag="new-sha")

    # Assert
    with open(values_path, "r") as f:
        saved = yaml.safe_load(f)
    assert saved["image"]["tag"] == "new-sha"
    mock_github.commit_and_push.assert_called_once_with(
        file_path=values_path,
        message="chore(gitops): atualizar image.tag para new-sha em dev",
        branch="develop",
    )
    mock_logger.info.assert_called_once()
    os.unlink(values_path)


def test_should_push_to_master_when_env_is_prd():
    # Arrange
    mock_github = MagicMock()
    mock_logger = MagicMock()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"image": {"tag": "old-tag", "repository": "ghcr.io/test"}}, f)
        values_path = f.name

    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={
                "prd": EnvironmentConfig(values_file=values_path),
            },
        ),
    )
    use_case = UpdateImageTagUseCase(github_client=mock_github, logger=mock_logger)

    # Act
    use_case.execute(app=app, env="prd", tag="v1.0.0")

    # Assert
    mock_github.commit_and_push.assert_called_once_with(
        file_path=values_path,
        message="chore(gitops): atualizar image.tag para v1.0.0 em prd",
        branch="master",
    )
    os.unlink(values_path)


def test_should_push_to_release_current_when_env_is_hom():
    # Arrange
    mock_github = MagicMock()
    mock_logger = MagicMock()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"image": {"tag": "old", "repository": "ghcr.io/test"}}, f)
        values_path = f.name

    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=HelmConfig(
            chart_repo="repo",
            chart_name="chart",
            chart_version="1.0.0",
            environments={
                "hom": EnvironmentConfig(values_file=values_path),
            },
        ),
    )
    use_case = UpdateImageTagUseCase(github_client=mock_github, logger=mock_logger)

    # Act
    use_case.execute(app=app, env="hom", tag="hom-sha")

    # Assert
    mock_github.commit_and_push.assert_called_once_with(
        file_path=values_path,
        message="chore(gitops): atualizar image.tag para hom-sha em hom",
        branch="release/current",
    )
    os.unlink(values_path)
