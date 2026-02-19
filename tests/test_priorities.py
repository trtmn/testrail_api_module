"""
Tests for the PrioritiesAPI module.

This module contains comprehensive tests for all methods in the PrioritiesAPI class,
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
from testrail_api_module.priorities import PrioritiesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestPrioritiesAPI:
    """Test suite for PrioritiesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def priorities_api(self, mock_client: Mock) -> PrioritiesAPI:
        """Create a PrioritiesAPI instance with mocked client."""
        return PrioritiesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test PrioritiesAPI initialization."""
        api = PrioritiesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_priorities(self, priorities_api: PrioritiesAPI) -> None:
        """Test get_priorities method."""
        with patch.object(priorities_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "High"},
                {"id": 2, "name": "Medium"},
                {"id": 3, "name": "Low"},
            ]

            result = priorities_api.get_priorities()

            mock_request.assert_called_once_with("GET", "get_priorities")
            assert len(result) == 3
            assert result[0]["id"] == 1

    def test_api_request_failure(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(priorities_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                priorities_api.get_priorities()

    def test_authentication_error(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(priorities_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                priorities_api.get_priorities()

    def test_rate_limit_error(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(priorities_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                priorities_api.get_priorities()
