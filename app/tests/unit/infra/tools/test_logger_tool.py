import pytest
from infra.tools.logger_tool import LoggerTool


def test_should_create_logger_when_log_level_is_info(monkeypatch):
    # Arrange
    monkeypatch.setenv("PASH_LOG_LEVEL", "INFO")

    # Act
    tool = LoggerTool()

    # Assert
    assert tool._logger is not None
    assert tool._logger.name == "pash-pipe"


def test_should_call_info_without_error_when_message_is_provided():
    # Arrange
    tool = LoggerTool()

    # Act & Assert
    tool.info("mensagem de info")


def test_should_call_error_without_error_when_message_is_provided():
    # Arrange
    tool = LoggerTool()

    # Act & Assert
    tool.error("mensagem de erro")


def test_should_call_debug_without_error_when_message_is_provided():
    # Arrange
    tool = LoggerTool()

    # Act & Assert
    tool.debug("mensagem de debug")


def test_should_call_warning_without_error_when_message_is_provided():
    # Arrange
    tool = LoggerTool()

    # Act & Assert
    tool.warning("mensagem de aviso")


def test_should_use_debug_level_when_pash_log_level_env_is_debug(monkeypatch):
    # Arrange
    monkeypatch.setenv("PASH_LOG_LEVEL", "DEBUG")

    # Act
    tool = LoggerTool()

    # Assert
    assert tool._logger is not None
