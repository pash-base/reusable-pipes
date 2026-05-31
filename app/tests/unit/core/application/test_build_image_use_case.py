from unittest.mock import MagicMock, patch
from core.application.build_image_use_case import BuildImageUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig


def test_should_run_docker_build_when_app_and_tag_are_valid():
    # Arrange
    mock_logger = MagicMock()
    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={},
        ),
    )
    use_case = BuildImageUseCase(logger=mock_logger)

    # Act
    with patch("core.application.build_image_use_case.subprocess.run") as mock_run:
        use_case.execute(app=app, tag="abc123")

        # Assert
        mock_run.assert_called_once_with(
            ["docker", "build", "-t", "ghcr.io/pash-doc/pash-doc-portal-platform:abc123", "app/"],
            check=True,
        )
    mock_logger.info.assert_called_once_with("Construindo imagem: ghcr.io/pash-doc/pash-doc-portal-platform:abc123")


def test_should_build_with_correct_image_tag_when_tag_is_sha():
    # Arrange
    mock_logger = MagicMock()
    app = PashAppModel(
        sigla="TEST",
        app_name="my-app",
        repo="org/my-app",
        helm=HelmConfig(
            chart_repo="repo/charts",
            chart_name="chart",
            chart_version="1.0.0",
            environments={},
        ),
    )
    use_case = BuildImageUseCase(logger=mock_logger)

    # Act
    with patch("core.application.build_image_use_case.subprocess.run") as mock_run:
        use_case.execute(app=app, tag="deadbeef")

        # Assert
        mock_run.assert_called_once_with(
            ["docker", "build", "-t", "ghcr.io/org/my-app:deadbeef", "app/"],
            check=True,
        )
