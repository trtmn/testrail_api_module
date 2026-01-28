"""
Tests for MCP utility functions.
"""
import logging
import os
import pytest
from typing import TYPE_CHECKING
from unittest.mock import patch

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture

from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_utils import (
    discover_api_methods,
    generate_tool_name,
    get_method_signature,
    extract_method_docstring,
    create_api_from_env
)


class TestDiscoverAPIMethods:
    """Tests for discover_api_methods function."""

    def test_discover_methods_from_api_instance(self):
        """Test that methods are discovered from API instance."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        methods = discover_api_methods(api)

        # Should discover methods from multiple modules
        assert isinstance(methods, dict)
        assert len(methods) > 0

        # Should have cases module
        assert 'cases' in methods
        assert len(methods['cases']) > 0

        # Methods should be tuples of (name, method)
        for module_name, method_list in methods.items():
            assert isinstance(method_list, list)
            for method_tuple in method_list:
                assert isinstance(method_tuple, tuple)
                assert len(method_tuple) == 2
                method_name, method = method_tuple
                assert isinstance(method_name, str)
                assert callable(method)

    def test_excludes_private_methods(self):
        """Test that private methods are excluded."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        methods = discover_api_methods(api)

        # Check that no private methods are included
        for module_name, method_list in methods.items():
            for method_name, _ in method_list:
                assert not method_name.startswith('_'), \
                    f"Private method {method_name} should not be included"

    def test_excludes_base_api_methods(self):
        """Test that base API methods are excluded."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        methods = discover_api_methods(api)

        excluded = {'_get', '_post', '_put', '_delete', '_patch',
                    '_api_request', '_build_url', '_get_auth',
                    '_handle_response'}

        for module_name, method_list in methods.items():
            for method_name, _ in method_list:
                assert method_name not in excluded, \
                    f"Base API method {method_name} should not be included"


class TestGenerateToolName:
    """Tests for generate_tool_name function."""

    def test_generates_correct_format(self):
        """Test that tool names are generated in correct format."""
        name = generate_tool_name('cases', 'get_case')
        assert name == 'testrail_cases_get_case'

    def test_handles_different_modules(self):
        """Test that different modules generate correct names."""
        assert generate_tool_name(
            'results', 'add_result') == 'testrail_results_add_result'
        assert generate_tool_name(
            'runs', 'get_runs') == 'testrail_runs_get_runs'
        assert generate_tool_name(
            'projects', 'get_project') == 'testrail_projects_get_project'


class TestGetMethodSignature:
    """Tests for get_method_signature function."""

    def test_removes_self_parameter(self):
        """Test that 'self' parameter is removed from signature."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        # Get a method from the API
        method = api.cases.get_case

        sig = get_method_signature(method)

        # Should not have 'self' parameter
        param_names = list(sig.parameters.keys())
        assert 'self' not in param_names

    def test_preserves_other_parameters(self):
        """Test that other parameters are preserved."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        method = api.cases.get_case
        sig = get_method_signature(method)

        # Should have case_id parameter
        assert 'case_id' in sig.parameters


class TestExtractMethodDocstring:
    """Tests for extract_method_docstring function."""

    def test_extracts_docstring(self):
        """Test that docstring is extracted."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        method = api.cases.get_case
        docstring = extract_method_docstring(method)

        assert isinstance(docstring, str)
        assert len(docstring) > 0

    def test_handles_missing_docstring(self):
        """Test that missing docstring returns empty string."""
        def no_docstring():
            pass

        docstring = extract_method_docstring(no_docstring)
        assert docstring == ""


class TestCreateAPIFromEnv:
    """Tests for create_api_from_env function."""

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io',
        'TESTRAIL_USERNAME': 'test-user',
        'TESTRAIL_API_KEY': 'test-key'
    })
    def test_creates_api_from_env_vars(self):
        """Test that API is created from environment variables."""
        api = create_api_from_env()

        assert isinstance(api, TestRailAPI)
        assert api.base_url == 'https://test.testrail.io'
        assert api.username == 'test-user'
        assert api.api_key == 'test-key'

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io',
        'TESTRAIL_USERNAME': 'test-user',
        'TESTRAIL_PASSWORD': 'test-password'
    }, clear=True)
    def test_creates_api_with_password(self):
        """Test that API can be created with password instead of API key."""
        api = create_api_from_env()

        assert isinstance(api, TestRailAPI)
        assert api.password == 'test-password'

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io',
        'TESTRAIL_USERNAME': 'test-user',
        'TESTRAIL_API_KEY': 'test-key',
        'TESTRAIL_TIMEOUT': '60'
    }, clear=True)
    def test_uses_custom_timeout(self):
        """Test that custom timeout is used."""
        api = create_api_from_env()

        assert api.timeout == 60

    @patch.dict(os.environ, {}, clear=True)
    def test_raises_error_missing_base_url(self):
        """Test that error is raised when base_url is missing."""
        with pytest.raises(ValueError, match="TESTRAIL_BASE_URL"):
            create_api_from_env()

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io'
    }, clear=True)
    def test_raises_error_missing_username(self):
        """Test that error is raised when username is missing."""
        with pytest.raises(ValueError, match="TESTRAIL_USERNAME"):
            create_api_from_env()

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io',
        'TESTRAIL_USERNAME': 'test-user'
    }, clear=True)
    def test_raises_error_missing_auth(self):
        """Test that error is raised when neither API key nor password is provided."""
        with pytest.raises(ValueError, match="TESTRAIL_API_KEY.*TESTRAIL_PASSWORD"):
            create_api_from_env()

    @patch.dict(os.environ, {
        'TESTRAIL_BASE_URL': 'https://test.testrail.io',
        'TESTRAIL_USERNAME': 'test-user',
        'TESTRAIL_API_KEY': 'test-key'
    }, clear=True)
    def test_debug_logging_enabled(self, caplog: 'LogCaptureFixture') -> None:
        """Test that debug logging produces log messages."""
        # Enable debug logging
        logging.getLogger(
            'testrail_api_module.mcp_utils').setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG, logger='testrail_api_module.mcp_utils'):
            create_api_from_env()  # Test function call and logging

            # Check that debug messages were logged
            assert any('Creating TestRailAPI instance' in record.message
                       for record in caplog.records)
            assert any('Base URL' in record.message
                       for record in caplog.records)


class TestDebugLogging:
    """Tests for debug logging functionality."""

    def test_discover_methods_debug_logging(
            self, caplog: 'LogCaptureFixture') -> None:
        """Test that discover_api_methods produces debug logs."""
        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        # Enable debug logging for mcp_utils
        logging.getLogger(
            'testrail_api_module.mcp_utils').setLevel(logging.DEBUG)

        with caplog.at_level(logging.DEBUG, logger='testrail_api_module.mcp_utils'):
            discover_api_methods(api)  # Test function call and logging

            # Check that debug messages were logged
            assert any('Starting API method discovery' in record.message
                       for record in caplog.records)
            assert any('Discovery complete' in record.message
                       for record in caplog.records)
            assert any('Scanning module' in record.message
                       for record in caplog.records)
