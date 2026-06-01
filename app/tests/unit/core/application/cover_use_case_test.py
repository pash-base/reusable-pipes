import pytest
from unittest.mock import MagicMock
from core.application.cover_use_case import CoverUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, QualityConfig


def _make_app(cover_command="pytest --cov", runtime="python", coverage_threshold=90):
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
            cover_command=cover_command,
            coverage_threshold=coverage_threshold,
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


def test_should_pass_when_python_coverage_meets_threshold(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="pytest --cov", runtime="python", coverage_threshold=90)
    mock_result = MagicMock()
    mock_result.stdout = "TOTAL                     100      5     95%\n"
    mock_result.stderr = ""
    mock_run = mocker.patch("core.application.cover_use_case.subprocess.run", return_value=mock_result)

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_called_once_with(
        "pytest --cov",
        shell=True,
        cwd="app/",
        check=True,
        capture_output=True,
        text=True,
    )
    mock_logger.info.assert_any_call("Cobertura: 95.0% (mínimo: 90%)")


def test_should_raise_when_python_coverage_is_below_threshold(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="pytest --cov", runtime="python", coverage_threshold=90)
    mock_result = MagicMock()
    mock_result.stdout = "TOTAL                     100     30     70%\n"
    mock_result.stderr = ""
    mocker.patch("core.application.cover_use_case.subprocess.run", return_value=mock_result)

    # Act / Assert
    with pytest.raises(RuntimeError, match="Cobertura 70.0% abaixo do mínimo 90%"):
        use_case.execute(app=app)


def test_should_pass_when_node_coverage_meets_threshold(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="npm run cover", runtime="node", coverage_threshold=80)
    mock_result = MagicMock()
    mock_result.stdout = "All files                 |      92 |      85 |      91 |\n"
    mock_result.stderr = ""
    mock_run = mocker.patch("core.application.cover_use_case.subprocess.run", return_value=mock_result)

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_called_once()
    mock_logger.info.assert_any_call("Cobertura: 92.0% (mínimo: 80%)")


def test_should_skip_cover_when_threshold_is_zero(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="pytest --cov", runtime="python", coverage_threshold=0)
    mock_run = mocker.patch("core.application.cover_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_cover_when_cover_command_is_empty(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="", runtime="python", coverage_threshold=90)
    mock_run = mocker.patch("core.application.cover_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_skip_cover_when_quality_is_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app_without_quality()
    mock_run = mocker.patch("core.application.cover_use_case.subprocess.run")

    # Act
    use_case.execute(app=app)

    # Assert
    mock_run.assert_not_called()
    mock_logger.warning.assert_called_once()


def test_should_warn_when_coverage_cannot_be_parsed(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = CoverUseCase(logger=mock_logger)
    app = _make_app(cover_command="go test ./...", runtime="go", coverage_threshold=90)
    mock_result = MagicMock()
    mock_result.stdout = "ok  my/package [no test files]\n"
    mock_result.stderr = ""
    mocker.patch("core.application.cover_use_case.subprocess.run", return_value=mock_result)

    # Act
    use_case.execute(app=app)

    # Assert
    mock_logger.warning.assert_called_once()
