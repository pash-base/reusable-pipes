from unittest.mock import MagicMock
from core.application.parse_pashfile_use_case import ParsePashfileUseCase


def test_should_return_pash_app_model_when_pashfile_is_valid():
    # Arrange
    mock_repo = MagicMock()
    mock_logger = MagicMock()
    expected_model = MagicMock()
    mock_repo.load.return_value = expected_model
    use_case = ParsePashfileUseCase(pashfile_repo=mock_repo, logger=mock_logger)

    # Act
    result = use_case.execute(".pashfile")

    # Assert
    mock_repo.load.assert_called_once_with(".pashfile")
    mock_logger.info.assert_called_once()
    assert result == expected_model


def test_should_call_repo_with_custom_path_when_path_is_provided():
    # Arrange
    mock_repo = MagicMock()
    mock_logger = MagicMock()
    expected_model = MagicMock()
    mock_repo.load.return_value = expected_model
    use_case = ParsePashfileUseCase(pashfile_repo=mock_repo, logger=mock_logger)

    # Act
    result = use_case.execute("custom/.pashfile")

    # Assert
    mock_repo.load.assert_called_once_with("custom/.pashfile")
    mock_logger.info.assert_called_once_with("Executando ParsePashfileUseCase")
    assert result == expected_model
