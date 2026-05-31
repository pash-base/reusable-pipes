from core.application.parse_pashfile_use_case import ParsePashfileUseCase


def test_should_return_pash_app_model_when_pashfile_is_valid(mocker):
    # Arrange
    mock_repo = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    expected_model = mocker.MagicMock()
    mock_repo.load.return_value = expected_model
    use_case = ParsePashfileUseCase(pashfile_repo=mock_repo, logger=mock_logger)

    # Act
    result = use_case.execute(".pashfile")

    # Assert
    mock_repo.load.assert_called_once_with(".pashfile")
    mock_logger.info.assert_called_once()
    assert result == expected_model


def test_should_call_repo_with_custom_path_when_path_is_provided(mocker):
    # Arrange
    mock_repo = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    expected_model = mocker.MagicMock()
    mock_repo.load.return_value = expected_model
    use_case = ParsePashfileUseCase(pashfile_repo=mock_repo, logger=mock_logger)

    # Act
    result = use_case.execute("custom/.pashfile")

    # Assert
    mock_repo.load.assert_called_once_with("custom/.pashfile")
    mock_logger.info.assert_called_once_with("Executando ParsePashfileUseCase")
    assert result == expected_model
