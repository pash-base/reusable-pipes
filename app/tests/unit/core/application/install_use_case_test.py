import pytest
from core.application.install_use_case import InstallUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, QualityConfig


def _make_app(install_command="npm install", runtime="node"):
    return PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={},
        ),
        quality=QualityConfig(
            runtime=runtime,
            workdir="app/",
            install_command=install_command,
        ),
    )


def _make_app_without_quality():
    return PashAppModel(
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


def test_should_run_install_command_when_quality_and_install_command_are_set(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = InstallUseCase(logger=mock_logger)
    app = _make_app(install_command="npm install")
    mock_run = mocker.patch("core.application.install_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_called_once_with("npm install", shell=True, cwd="app/", check=True)
    mock_logger.info.assert_called_once_with("Executando install: npm install")


def test_should_skip_install_when_quality_is_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = InstallUseCase(logger=mock_logger)
    app = _make_app_without_quality()
    mock_run = mocker.patch("core.application.install_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_install_when_install_command_is_empty(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = InstallUseCase(logger=mock_logger)
    app = _make_app(install_command="")
    mock_run = mocker.patch("core.application.install_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_install_when_install_command_is_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = InstallUseCase(logger=mock_logger)
    app = _make_app(install_command=None)
    mock_run = mocker.patch("core.application.install_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_propagate_exception_when_subprocess_fails(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = InstallUseCase(logger=mock_logger)
    app = _make_app(install_command="npm install")
    mock_run = mocker.patch("core.application.install_use_case.subprocess.run", side_effect=Exception("falha"))

    # Act / Assert
    with pytest.raises(Exception, match="falha"):
        use_case.execute(app=app)

    mock_run.assert_called_once_with("npm install", shell=True, cwd="app/", check=True)
