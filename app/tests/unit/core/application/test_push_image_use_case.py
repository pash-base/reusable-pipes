from unittest.mock import MagicMock, patch
from core.application.push_image_use_case import PushImageUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig


def test_should_run_docker_push_when_app_and_tag_are_valid():
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
    use_case = PushImageUseCase(logger=mock_logger)

    # Act
    with patch("core.application.push_image_use_case.subprocess.run") as mock_run:
        use_case.execute(app=app, tag="abc123")

        # Assert
        mock_run.assert_called_once_with(
            ["docker", "push", "ghcr.io/pash-doc/pash-doc-portal-platform:abc123"],
            check=True,
        )
    mock_logger.info.assert_called_once_with("Publicando imagem: ghcr.io/pash-doc/pash-doc-portal-platform:abc123")


def test_should_push_with_correct_image_name_when_repo_has_org():
    # Arrange
    mock_logger = MagicMock()
    app = PashAppModel(
        sigla="SVC",
        app_name="my-service",
        repo="my-org/my-service",
        helm=HelmConfig(
            chart_repo="repo",
            chart_name="chart",
            chart_version="1.0.0",
            environments={},
        ),
    )
    use_case = PushImageUseCase(logger=mock_logger)

    # Act
    with patch("core.application.push_image_use_case.subprocess.run") as mock_run:
        use_case.execute(app=app, tag="v1.2.3")

        # Assert
        mock_run.assert_called_once_with(
            ["docker", "push", "ghcr.io/my-org/my-service:v1.2.3"],
            check=True,
        )
    mock_logger.info.assert_called_once_with("Publicando imagem: ghcr.io/my-org/my-service:v1.2.3")
