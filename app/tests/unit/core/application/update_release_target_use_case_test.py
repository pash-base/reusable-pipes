from core.application.update_release_target_use_case import UpdateReleaseTargetUseCase


def test_should_update_target_revision_when_app_name_and_branch_are_valid(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = UpdateReleaseTargetUseCase(logger=mock_logger)
    mock_run = mocker.patch("core.application.update_release_target_use_case.subprocess.run")
    mocker.patch("core.application.update_release_target_use_case.os.environ.get", return_value="fake-token")
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_yaml = mocker.patch("core.application.update_release_target_use_case.yaml")
    mock_yaml.safe_load.return_value = {
        "spec": {
            "sources": [
                {"targetRevision": "master"},
                {"ref": "values", "targetRevision": "release/v1.0.0"},
            ]
        }
    }

    # Act
    use_case.execute(app_name="doc-portal-platform-hom", branch="release/v1.0.13")

    # Assert
    assert mock_run.call_count >= 5
    mock_yaml.safe_load.assert_called_once()
    mock_yaml.dump.assert_called_once()
    assert mock_logger.info.call_count >= 1


def test_should_derive_sigla_and_shortname_from_app_name(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = UpdateReleaseTargetUseCase(logger=mock_logger)
    mocker.patch("core.application.update_release_target_use_case.subprocess.run")
    mocker.patch("core.application.update_release_target_use_case.os.environ.get", return_value="fake-token")
    mock_data = {"spec": {"sources": [{"ref": "values", "targetRevision": "old"}]}}
    mock_yaml = mocker.patch("core.application.update_release_target_use_case.yaml")
    mock_yaml.safe_load.return_value = mock_data
    mock_open = mocker.patch("builtins.open", mocker.mock_open())

    # Act
    use_case.execute(app_name="doc-portal-platform-hom", branch="release/v1.0.13")

    # Assert
    assert mock_open.called
    all_args = [call.args[0] for call in mock_open.call_args_list if "argocd" in str(call.args[0])]
    assert len(all_args) > 0
    assert all_args[0] == "/tmp/platform-config/argocd/applications/doc/portal/doc-portal-platform-hom.yaml"


def test_should_update_only_values_source_in_yaml(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = UpdateReleaseTargetUseCase(logger=mock_logger)
    mocker.patch("core.application.update_release_target_use_case.subprocess.run")
    mocker.patch("core.application.update_release_target_use_case.os.environ.get", return_value="fake-token")
    mock_data = {
        "spec": {
            "sources": [
                {"targetRevision": "master"},
                {"ref": "values", "targetRevision": "release/v1.0.0"},
            ]
        }
    }
    mock_yaml = mocker.patch("core.application.update_release_target_use_case.yaml")
    mock_yaml.safe_load.return_value = mock_data
    mocker.patch("builtins.open", mocker.mock_open())

    # Act
    use_case.execute(app_name="doc-portal-platform-hom", branch="release/v1.0.13")

    # Assert
    assert mock_data["spec"]["sources"][0]["targetRevision"] == "master"
    assert mock_data["spec"]["sources"][1]["targetRevision"] == "release/v1.0.13"
    mock_yaml.dump.assert_called_once_with(mock_data, mocker.ANY, default_flow_style=False)


def test_should_skip_push_when_nothing_to_commit(mocker):
    # Arrange
    mock_logger = mocker.MagicMock()
    use_case = UpdateReleaseTargetUseCase(logger=mock_logger)
    mock_run = mocker.patch("core.application.update_release_target_use_case.subprocess.run")
    mock_run.return_value.returncode = 1  # nothing to commit
    mocker.patch("core.application.update_release_target_use_case.os.environ.get", return_value="fake-token")
    mocker.patch("builtins.open", mocker.mock_open())
    mock_yaml = mocker.patch("core.application.update_release_target_use_case.yaml")
    mock_yaml.safe_load.return_value = {"spec": {"sources": [{"ref": "values", "targetRevision": "release/v1.0.15"}]}}

    # Act
    use_case.execute(app_name="doc-portal-platform-hom", branch="release/v1.0.15")

    # Assert
    push_calls = [c for c in mock_run.call_args_list if "push" in str(c.args)]
    assert len(push_calls) == 0
    mock_logger.info.assert_any_call("Nenhuma alteração para commitar — targetRevision já está atualizado")
