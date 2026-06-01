import pytest
from unittest.mock import MagicMock
from core.application.validate_use_case import ValidateUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, QualityConfig


def _make_app():
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
            runtime="python",
            workdir="app/",
            install_command="pip install -r requirements.txt",
            fmt_command="black .",
            lint_command="flake8 .",
            test_command="pytest",
            cover_command="pytest --cov",
        ),
    )


def test_should_call_all_use_cases_in_order_when_execute_is_called(mocker):
    # Arrange
    manager = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    mock_install = mocker.MagicMock()
    mock_fmt = mocker.MagicMock()
    mock_lint = mocker.MagicMock()
    mock_test = mocker.MagicMock()
    mock_cover = mocker.MagicMock()
    manager.attach_mock(mock_install, "install_uc")
    manager.attach_mock(mock_fmt, "fmt_uc")
    manager.attach_mock(mock_lint, "lint_uc")
    manager.attach_mock(mock_test, "test_uc")
    manager.attach_mock(mock_cover, "cover_uc")
    use_case = ValidateUseCase(
        install_uc=mock_install,
        fmt_uc=mock_fmt,
        lint_uc=mock_lint,
        test_uc=mock_test,
        cover_uc=mock_cover,
        logger=mock_logger,
    )
    app = _make_app()

    # Act
    use_case.execute(app=app)

    # Assert
    manager.assert_has_calls(
        [
            mocker.call.install_uc.execute(app=app),
            mocker.call.fmt_uc.execute(app=app),
            mocker.call.lint_uc.execute(app=app),
            mocker.call.test_uc.execute(app=app),
            mocker.call.cover_uc.execute(app=app),
        ]
    )


def test_should_call_use_cases_exactly_once_each_when_validate_runs(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    mock_install = mocker.MagicMock()
    mock_fmt = mocker.MagicMock()
    mock_lint = mocker.MagicMock()
    mock_test = mocker.MagicMock()
    mock_cover = mocker.MagicMock()
    use_case = ValidateUseCase(
        install_uc=mock_install,
        fmt_uc=mock_fmt,
        lint_uc=mock_lint,
        test_uc=mock_test,
        cover_uc=mock_cover,
        logger=mock_logger,
    )
    app = _make_app()

    # Act
    use_case.execute(app=app)

    # Assert
    assert mock_install.execute.call_count == 1
    assert mock_fmt.execute.call_count == 1
    assert mock_lint.execute.call_count == 1
    assert mock_test.execute.call_count == 1
    assert mock_cover.execute.call_count == 1


def test_should_log_start_message_when_execute_is_called(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    mock_install = mocker.MagicMock()
    mock_fmt = mocker.MagicMock()
    mock_lint = mocker.MagicMock()
    mock_test = mocker.MagicMock()
    mock_cover = mocker.MagicMock()
    use_case = ValidateUseCase(
        install_uc=mock_install,
        fmt_uc=mock_fmt,
        lint_uc=mock_lint,
        test_uc=mock_test,
        cover_uc=mock_cover,
        logger=mock_logger,
    )
    app = _make_app()

    # Act
    use_case.execute(app=app)

    # Assert
    mock_logger.info.assert_called_once_with("Executando validate: install → fmt → lint → test → cover")


def test_should_propagate_exception_when_install_fails(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    mock_install = mocker.MagicMock()
    mock_install.execute.side_effect = Exception("install falhou")
    mock_fmt = mocker.MagicMock()
    mock_lint = mocker.MagicMock()
    mock_test = mocker.MagicMock()
    mock_cover = mocker.MagicMock()
    use_case = ValidateUseCase(
        install_uc=mock_install,
        fmt_uc=mock_fmt,
        lint_uc=mock_lint,
        test_uc=mock_test,
        cover_uc=mock_cover,
        logger=mock_logger,
    )
    app = _make_app()

    # Act / Assert
    with pytest.raises(Exception, match="install falhou"):
        use_case.execute(app=app)

    mock_fmt.execute.assert_not_called()
    mock_lint.execute.assert_not_called()
    mock_test.execute.assert_not_called()
    mock_cover.execute.assert_not_called()


def test_should_propagate_exception_when_cover_fails(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    mock_install = mocker.MagicMock()
    mock_fmt = mocker.MagicMock()
    mock_lint = mocker.MagicMock()
    mock_test = mocker.MagicMock()
    mock_cover = mocker.MagicMock()
    mock_cover.execute.side_effect = RuntimeError("Cobertura 70% abaixo do mínimo 90%")
    use_case = ValidateUseCase(
        install_uc=mock_install,
        fmt_uc=mock_fmt,
        lint_uc=mock_lint,
        test_uc=mock_test,
        cover_uc=mock_cover,
        logger=mock_logger,
    )
    app = _make_app()

    # Act / Assert
    with pytest.raises(RuntimeError, match="Cobertura 70% abaixo do mínimo 90%"):
        use_case.execute(app=app)

    mock_install.execute.assert_called_once_with(app=app)
    mock_fmt.execute.assert_called_once_with(app=app)
    mock_lint.execute.assert_called_once_with(app=app)
    mock_test.execute.assert_called_once_with(app=app)
    mock_cover.execute.assert_called_once_with(app=app)
