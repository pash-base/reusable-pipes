import pytest
from core.application.test_use_case import TestUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, QualityConfig


def _make_app(test_command="pytest", runtime="python"):
    return PashAppModel(
        sigla="SVC",
        app_name="my-service",
        repo="pash-svc/my-service",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={},
        ),
        quality=QualityConfig(
            runtime=runtime,
            workdir="app/",
            test_command=test_command,
        ),
    )


def _make_app_without_quality():
    return PashAppModel(
        sigla="SVC",
        app_name="my-service",
        repo="pash-svc/my-service",
        helm=HelmConfig(
            chart_repo="pash-inf/pash-inf-helm-charts",
            chart_name="pash-stacks",
            chart_version="0.1.0",
            environments={},
        ),
    )


def test_should_run_test_command_when_quality_and_test_command_are_set(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = TestUseCase(logger=mock_logger)
    app = _make_app(test_command="pytest")
    mock_run = mocker.patch("core.application.test_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_called_once_with("pytest", shell=True, cwd="app/", check=True)
    mock_logger.info.assert_called_once_with("Executando test: pytest")


def test_should_skip_test_when_quality_is_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = TestUseCase(logger=mock_logger)
    app = _make_app_without_quality()
    mock_run = mocker.patch("core.application.test_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_test_when_test_command_is_empty(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = TestUseCase(logger=mock_logger)
    app = _make_app(test_command="")
    mock_run = mocker.patch("core.application.test_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_test_when_test_command_is_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = TestUseCase(logger=mock_logger)
    app = _make_app(test_command=None)
    mock_run = mocker.patch("core.application.test_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_propagate_exception_when_subprocess_fails(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = TestUseCase(logger=mock_logger)
    app = _make_app(test_command="pytest")
    mock_run = mocker.patch("core.application.test_use_case.subprocess.run", side_effect=Exception("falha"))

    # Act / Assert
    with pytest.raises(Exception, match="falha"):
        use_case.execute(app=app)

    mock_run.assert_called_once_with("pytest", shell=True, cwd="app/", check=True)
