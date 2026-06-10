"""
Tests for the __init__ module.

This module contains comprehensive tests for the TestRailAPI class,
including initialization, validation, and submodule setup.
"""

import subprocess
import sys
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
import requests

from testrail_api_module import (
    TestRailAPI,
    TestRailAPIError,
    TestRailAPIException,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestTestRailAPI:
    """Test suite for TestRailAPI class."""

    def test_init_with_api_key(self) -> None:
        """Test TestRailAPI initialization with API key."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert api.base_url == "https://testrail.example.com"
        assert api.username == "testuser@example.com"
        assert api.api_key == "test_api_key"
        assert api.password is None
        assert api.timeout == 30

    def test_init_with_password(self) -> None:
        """Test TestRailAPI initialization with password."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            password="test_password",
        )

        assert api.base_url == "https://testrail.example.com"
        assert api.username == "testuser@example.com"
        assert api.password == "test_password"
        assert api.api_key is None
        assert api.timeout == 30

    def test_init_with_custom_timeout(self) -> None:
        """Test TestRailAPI initialization with custom timeout."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
            timeout=60,
        )

        assert api.timeout == 60

    def test_init_with_both_api_key_and_password(self) -> None:
        """Test TestRailAPI initialization with both API key and password."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
            password="test_password",
        )

        assert api.api_key == "test_api_key"
        assert api.password == "test_password"

    def test_init_normalizes_base_url_removes_trailing_slash(self) -> None:
        """Test TestRailAPI normalizes base_url by removing trailing slash."""
        api = TestRailAPI(
            base_url="https://testrail.example.com/",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert api.base_url == "https://testrail.example.com"

    def test_init_normalizes_base_url_multiple_slashes(self) -> None:
        """Test TestRailAPI normalizes base_url with multiple trailing slashes."""
        api = TestRailAPI(
            base_url="https://testrail.example.com///",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert api.base_url == "https://testrail.example.com"

    def test_init_raises_error_no_credentials(self) -> None:
        """Test TestRailAPI raises ValueError when neither api_key nor password provided."""
        with pytest.raises(
            ValueError, match="Either api_key or password must be provided"
        ):
            TestRailAPI(
                base_url="https://testrail.example.com",
                username="testuser@example.com",
            )

    def test_init_raises_error_empty_base_url(self) -> None:
        """Test TestRailAPI raises ValueError when base_url is empty."""
        with pytest.raises(
            ValueError, match="base_url must be a valid HTTP/HTTPS URL"
        ):
            TestRailAPI(
                base_url="",
                username="testuser@example.com",
                api_key="test_api_key",
            )

    def test_init_raises_error_none_base_url(self) -> None:
        """Test TestRailAPI raises ValueError when base_url is None."""
        with pytest.raises(
            ValueError, match="base_url must be a valid HTTP/HTTPS URL"
        ):
            TestRailAPI(
                base_url=None,  # type: ignore
                username="testuser@example.com",
                api_key="test_api_key",
            )

    def test_init_raises_error_invalid_url_scheme(self) -> None:
        """Test TestRailAPI raises ValueError when base_url doesn't start with http:// or https://."""
        with pytest.raises(
            ValueError, match="base_url must be a valid HTTP/HTTPS URL"
        ):
            TestRailAPI(
                base_url="ftp://testrail.example.com",
                username="testuser@example.com",
                api_key="test_api_key",
            )

    def test_init_raises_error_invalid_url_no_scheme(self) -> None:
        """Test TestRailAPI raises ValueError when base_url has no scheme."""
        with pytest.raises(
            ValueError, match="base_url must be a valid HTTP/HTTPS URL"
        ):
            TestRailAPI(
                base_url="testrail.example.com",
                username="testuser@example.com",
                api_key="test_api_key",
            )

    def test_init_accepts_http_url(self) -> None:
        """Test TestRailAPI accepts HTTP URLs (not just HTTPS)."""
        api = TestRailAPI(
            base_url="http://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert api.base_url == "http://testrail.example.com"

    def test_init_initializes_all_submodules(self) -> None:
        """Test TestRailAPI initializes all submodule API instances."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        # Check that all submodules are initialized
        assert hasattr(api, "attachments")
        assert hasattr(api, "bdd")
        assert hasattr(api, "cases")
        assert hasattr(api, "configurations")
        assert hasattr(api, "datasets")
        assert hasattr(api, "groups")
        assert hasattr(api, "milestones")
        assert hasattr(api, "plans")
        assert hasattr(api, "priorities")
        assert hasattr(api, "projects")
        assert hasattr(api, "reports")
        assert hasattr(api, "result_fields")
        assert hasattr(api, "results")
        assert hasattr(api, "roles")
        assert hasattr(api, "runs")
        assert hasattr(api, "sections")
        assert hasattr(api, "shared_steps")
        assert hasattr(api, "statuses")
        assert hasattr(api, "suites")
        assert hasattr(api, "templates")
        assert hasattr(api, "tests")
        assert hasattr(api, "users")
        assert hasattr(api, "variables")

    def test_init_submodules_have_correct_client(self) -> None:
        """Test TestRailAPI submodules have the correct client reference."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        # Check that submodules have the client reference
        assert api.cases.client == api
        assert api.runs.client == api
        assert api.results.client == api
        assert api.projects.client == api

    def test_exception_classes_importable(self) -> None:
        """Test exception classes are importable from main module."""
        from testrail_api_module import (
            TestRailAPIError,
            TestRailAPIException,
            TestRailAuthenticationError,
            TestRailRateLimitError,
        )

        assert TestRailAPIError is not None
        assert TestRailAuthenticationError is not None
        assert TestRailRateLimitError is not None
        assert TestRailAPIException is not None

    def test_exception_classes_inheritance(self) -> None:
        """Test exception class inheritance hierarchy."""
        assert issubclass(TestRailAuthenticationError, TestRailAPIError)
        assert issubclass(TestRailRateLimitError, TestRailAPIError)
        assert issubclass(TestRailAPIException, TestRailAPIError)

    def test_init_with_empty_string_api_key(self) -> None:
        """Test TestRailAPI with empty string api_key (should still work if password provided)."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="",
            password="test_password",
        )

        assert api.api_key == ""
        assert api.password == "test_password"

    def test_init_with_empty_string_password(self) -> None:
        """Test TestRailAPI with empty string password (should still work if api_key provided)."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
            password="",
        )

        assert api.api_key == "test_api_key"
        assert api.password == ""

    def test_init_with_both_empty_credentials_raises_error(self) -> None:
        """Test TestRailAPI raises error when both api_key and password are empty strings."""
        with pytest.raises(
            ValueError, match="Either api_key or password must be provided"
        ):
            TestRailAPI(
                base_url="https://testrail.example.com",
                username="testuser@example.com",
                api_key="",
                password="",
            )

    def test_init_with_none_api_key_and_password_raises_error(self) -> None:
        """Test TestRailAPI raises error when both api_key and password are None."""
        with pytest.raises(
            ValueError, match="Either api_key or password must be provided"
        ):
            TestRailAPI(
                base_url="https://testrail.example.com",
                username="testuser@example.com",
                api_key=None,
                password=None,
            )

    def test_init_creates_shared_session(self) -> None:
        """Test TestRailAPI creates a single shared requests.Session."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert isinstance(api.session, requests.Session)
        api.close()

    def test_submodules_share_client_session(self) -> None:
        """Test all submodules reuse the client's session (one
        connection pool per client, not 24)."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        assert api.attachments.session is api.session
        assert api.bdd.session is api.session
        assert api.cases.session is api.session
        assert api.results.session is api.session
        assert api.runs.session is api.session
        assert api.variables.session is api.session
        api.close()

    def test_close_closes_session(self) -> None:
        """Test TestRailAPI.close() closes the shared session."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        with patch.object(api.session, "close") as mock_close:
            api.close()

        mock_close.assert_called_once_with()

    def test_context_manager_returns_self(self) -> None:
        """Test TestRailAPI.__enter__ returns the client itself."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        with api as entered:
            assert entered is api

    def test_context_manager_closes_on_exit(self) -> None:
        """Test TestRailAPI.__exit__ closes the shared session."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        with patch.object(api, "close") as mock_close:
            with api:
                mock_close.assert_not_called()

        mock_close.assert_called_once_with()

    def test_context_manager_closes_on_exception(self) -> None:
        """Test TestRailAPI.__exit__ closes the session on errors and
        does not suppress the exception."""
        api = TestRailAPI(
            base_url="https://testrail.example.com",
            username="testuser@example.com",
            api_key="test_api_key",
        )

        with patch.object(api, "close") as mock_close:
            with pytest.raises(RuntimeError, match="boom"):
                with api:
                    raise RuntimeError("boom")

        mock_close.assert_called_once_with()

    def test_submodules_importable_without_instantiation(self) -> None:
        """Test submodules are reachable right after a fresh import,
        without constructing a TestRailAPI client first."""
        code = (
            "import testrail_api_module as t; "
            "assert t.cases.CasesAPI; "
            "assert t.attachments.AttachmentsAPI; "
            "assert t.variables.VariablesAPI"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    def test_import_under_python_oo(self) -> None:
        """Test the package imports under `python -OO` (docstrings are
        stripped, so __doc__ is None and must not be .format()ed)."""
        result = subprocess.run(
            [sys.executable, "-OO", "-c", "import testrail_api_module"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    def test_version_attribute(self) -> None:
        """Test __version__ is exposed as a non-empty string."""
        import testrail_api_module

        assert isinstance(testrail_api_module.__version__, str)
        assert testrail_api_module.__version__
