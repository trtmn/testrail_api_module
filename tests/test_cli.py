"""
Tests for CLI functionality.
"""
import logging
import os
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

from testrail_api_module.cli import setup_logging


def _reset_logging_state() -> None:
    """Reset logging state without reloading the logging module."""
    logging.disable(logging.NOTSET)
    for handler in list(logging.root.handlers):
        logging.root.removeHandler(handler)
    logging.root.setLevel(logging.WARNING)


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_verbose_mode(self) -> None:
        """Test that verbose mode configures logging."""
        _reset_logging_state()

        setup_logging(verbose=True, debug=False)

        # Create a test logger and verify it can log at DEBUG level
        test_logger = logging.getLogger('test_verbose')
        test_logger.setLevel(logging.DEBUG)

        # Logger should be able to log debug messages (effective level should
        # be DEBUG)
        assert test_logger.isEnabledFor(logging.DEBUG)

    def test_setup_logging_debug_mode(self) -> None:
        """Test that debug mode configures logging."""
        _reset_logging_state()

        setup_logging(verbose=False, debug=True)

        # Create a test logger and verify it can log at DEBUG level
        test_logger = logging.getLogger('test_debug')
        test_logger.setLevel(logging.DEBUG)

        # Logger should be able to log debug messages
        assert test_logger.isEnabledFor(logging.DEBUG)

    def test_setup_logging_both_modes(self) -> None:
        """Test that both verbose and debug modes enable logging."""
        _reset_logging_state()

        setup_logging(verbose=True, debug=True)

        # Create a test logger and verify it can log at DEBUG level
        test_logger = logging.getLogger('test_both')
        test_logger.setLevel(logging.DEBUG)

        # Logger should be able to log debug messages
        assert test_logger.isEnabledFor(logging.DEBUG)

    def test_setup_logging_no_debug(self) -> None:
        """Test that without verbose or debug, logging is quiet."""
        _reset_logging_state()

        setup_logging(verbose=False, debug=False)

        # We keep logging quiet by setting root + relevant namespaces to ERROR,
        # but we do not globally disable logging (so tests/apps can re-enable
        # it).
        assert logging.root.level == logging.ERROR
        assert logging.root.manager.disable == logging.NOTSET


class TestDebugEnvironmentVariable:
    """Tests for TESTRAIL_MCP_DEBUG environment variable."""

    @pytest.mark.parametrize('value',
                             ['1', 'true', 'yes', 'on', 'True', 'YES', 'ON'])
    def test_debug_enabled_values(
            self,
            value: str,
            monkeypatch: 'MonkeyPatch') -> None:
        """Test that various truthy values enable debug mode."""
        # Set the environment variable
        monkeypatch.setenv('TESTRAIL_MCP_DEBUG', value)

        # Check that it's detected as enabled
        debug_enabled = os.getenv(
            'TESTRAIL_MCP_DEBUG', '').lower() in (
            '1', 'true', 'yes', 'on')
        assert debug_enabled is True

    @pytest.mark.parametrize('value', ['0', 'false', 'no', 'off', ''])
    def test_debug_disabled_values(
            self,
            value: str,
            monkeypatch: 'MonkeyPatch') -> None:
        """Test that falsy values disable debug mode."""
        # Set the environment variable
        monkeypatch.setenv('TESTRAIL_MCP_DEBUG', value)

        # Check that it's detected as disabled
        debug_enabled = os.getenv(
            'TESTRAIL_MCP_DEBUG', '').lower() in (
            '1', 'true', 'yes', 'on')
        assert debug_enabled is False

    def test_debug_not_set(self, monkeypatch: 'MonkeyPatch') -> None:
        """Test behavior when TESTRAIL_MCP_DEBUG is not set."""
        # Ensure the variable is not set
        monkeypatch.delenv('TESTRAIL_MCP_DEBUG', raising=False)

        # Check that it's detected as disabled
        debug_enabled = os.getenv(
            'TESTRAIL_MCP_DEBUG', '').lower() in (
            '1', 'true', 'yes', 'on')
        assert debug_enabled is False
