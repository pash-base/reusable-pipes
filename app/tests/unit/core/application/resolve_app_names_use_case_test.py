import pytest
from core.application.resolve_app_names_use_case import ResolveAppNamesUseCase
from core.domain.models.pash_app_model import PashAppModel, HelmConfig, EnvironmentConfig


def _make_helm(envs=None):
    if envs is None:
        envs = {"dev": EnvironmentConfig(values_file="app/_environments/dev/values-dev.yaml")}
    return HelmConfig(
        chart_repo="pash-inf/pash-inf-helm-charts",
        chart_name="pash-stacks",
        chart_version="0.1.0",
        environments=envs,
    )


def test_should_return_app_name_for_each_env_when_type_and_shortname_are_explicit(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm(
        {
            "dev": EnvironmentConfig("dev.yaml"),
            "hom": EnvironmentConfig("hom.yaml"),
            "prd": EnvironmentConfig("prd.yaml"),
        }
    )
    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=helm,
        type="portal",
        shortname="platform",
    )

    # Act
    result = use_case.execute(app)

    # Assert
    assert result == {
        "dev": "doc-portal-platform-dev",
        "hom": "doc-portal-platform-hom",
        "prd": "doc-portal-platform-prd",
    }
    mock_logger.info.assert_called_once_with("Executando ResolveAppNamesUseCase")


def test_should_derive_type_and_shortname_from_repo_when_fields_are_none(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm({"dev": EnvironmentConfig("dev.yaml")})
    app = PashAppModel(sigla="DOC", app_name="portal-platform", repo="pash-doc/pash-doc-portal-platform", helm=helm)

    # Act
    result = use_case.execute(app)

    # Assert
    assert result == {"dev": "doc-portal-platform-dev"}


def test_should_return_single_env_when_only_one_environment_exists(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm({"prd": EnvironmentConfig("prd.yaml")})
    app = PashAppModel(
        sigla="INF",
        app_name="mcp-data",
        repo="pash-inf/pash-inf-py-mcp-data",
        helm=helm,
        type="py-mcp",
        shortname="data",
    )

    # Act
    result = use_case.execute(app)

    # Assert
    assert result == {"prd": "inf-py-mcp-data-prd"}


def test_should_lowercase_sigla_when_sigla_is_uppercase(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm({"dev": EnvironmentConfig("dev.yaml")})
    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=helm,
        type="portal",
        shortname="platform",
    )

    # Act
    result = use_case.execute(app)

    # Assert
    assert all(name.startswith("doc-") for name in result.values())


def test_should_handle_compound_shortname_when_derived_from_repo(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm({"dev": EnvironmentConfig("dev.yaml"), "hom": EnvironmentConfig("hom.yaml")})
    app = PashAppModel(sigla="INF", app_name="mcp-my-service", repo="pash-inf/pash-inf-py-mcp-my-service", helm=helm)

    # Act
    result = use_case.execute(app)

    # Assert
    assert result == {"dev": "inf-py-mcp-my-service-dev", "hom": "inf-py-mcp-my-service-hom"}


def test_should_call_logger_exactly_once_when_execute_is_called(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = ResolveAppNamesUseCase(logger=mock_logger)
    helm = _make_helm(
        {
            "dev": EnvironmentConfig("dev.yaml"),
            "hom": EnvironmentConfig("hom.yaml"),
            "prd": EnvironmentConfig("prd.yaml"),
        }
    )
    app = PashAppModel(
        sigla="DOC",
        app_name="portal-platform",
        repo="pash-doc/pash-doc-portal-platform",
        helm=helm,
        type="portal",
        shortname="platform",
    )

    # Act
    use_case.execute(app)

    # Assert
    mock_logger.info.assert_called_once()
    assert mock_logger.info.call_count == 1
