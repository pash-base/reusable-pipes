from unittest.mock import MagicMock, patch
from adapters.clients.github_client import GithubClient


def test_should_run_git_commands_when_commit_and_push_is_called():
    # Arrange
    mock_config = MagicMock()
    mock_logger = MagicMock()
    client = GithubClient(config=mock_config, logger=mock_logger)

    # Act
    with patch("adapters.clients.github_client.subprocess.run") as mock_run:
        client.commit_and_push(
            file_path="app/_environments/dev/values-dev.yaml",
            message="chore(gitops): update tag",
            branch="develop",
        )

        # Assert
        assert mock_run.call_count == 3
        calls = mock_run.call_args_list
        assert calls[0].args[0] == ["git", "add", "app/_environments/dev/values-dev.yaml"]
        assert calls[1].args[0] == ["git", "commit", "-m", "chore(gitops): update tag"]
        assert calls[2].args[0] == ["git", "push", "origin", "develop"]
    mock_logger.info.assert_called_once()


def test_should_log_commit_info_when_committing_file():
    # Arrange
    mock_config = MagicMock()
    mock_logger = MagicMock()
    client = GithubClient(config=mock_config, logger=mock_logger)

    # Act
    with patch("adapters.clients.github_client.subprocess.run"):
        client.commit_and_push(
            file_path="some/file.yaml",
            message="chore: update",
            branch="master",
        )

    # Assert
    mock_logger.info.assert_called_once_with("Commitando some/file.yaml na branch master")
