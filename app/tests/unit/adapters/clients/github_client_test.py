from adapters.clients.github_client import GithubClient


def test_should_run_git_commands_when_commit_and_push_is_called(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    client = GithubClient(config=mock_config, logger=mock_logger)
    mock_run = mocker.patch("adapters.clients.github_client.subprocess.run")

    # Act
    client.commit_and_push(
        file_path="app/_environments/dev/values-dev.yaml",
        message="chore(gitops): update tag",
        branch="develop",
    )

    # Assert
    assert mock_run.call_count == 5
    calls = mock_run.call_args_list
    assert calls[0].args[0] == ["git", "checkout", "develop"]
    assert calls[1].args[0] == ["git", "pull", "--rebase", "--autostash", "origin", "develop"]
    assert calls[2].args[0] == ["git", "add", "app/_environments/dev/values-dev.yaml"]
    assert calls[3].args[0] == ["git", "commit", "-m", "chore(gitops): update tag"]
    assert calls[4].args[0] == ["git", "push", "origin", "develop"]
    mock_logger.info.assert_called_once()


def test_should_log_commit_info_when_committing_file(mocker):
    # Arrange
    mock_config = mocker.MagicMock()
    mock_logger = mocker.MagicMock()
    client = GithubClient(config=mock_config, logger=mock_logger)
    mocker.patch("adapters.clients.github_client.subprocess.run")

    # Act
    client.commit_and_push(
        file_path="some/file.yaml",
        message="chore: update",
        branch="master",
    )

    # Assert
    mock_logger.info.assert_called_once_with("Commitando some/file.yaml na branch master")
