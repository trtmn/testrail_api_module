"""
Tests for the TemplatesAPI module.

This module contains comprehensive tests for all methods in the TemplatesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.templates import TemplatesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestTemplatesAPI:
    """Test suite for TemplatesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def templates_api(self, mock_client: Mock) -> TemplatesAPI:
        """Create a TemplatesAPI instance with mocked client."""
        return TemplatesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test TemplatesAPI initialization."""
        api = TemplatesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_templates(self, templates_api: TemplatesAPI) -> None:
        """Test get_templates method."""
        with patch.object(templates_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Template 1"},
                {"id": 2, "name": "Template 2"},
            ]

            result = templates_api.get_templates(project_id=1)
            mock_request.assert_called_once_with("GET", "get_templates/1")
            assert len(result) == 2

    def test_api_request_failure(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(templates_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                templates_api.get_templates(project_id=1)

    def test_authentication_error(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(templates_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                templates_api.get_templates(project_id=1)

    def test_rate_limit_error(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(templates_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                templates_api.get_templates(project_id=1)
