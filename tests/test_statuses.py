"""
Tests for the StatusesAPI module.

This module contains comprehensive tests for all methods in the StatusesAPI class,
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
from testrail_api_module.statuses import StatusesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestStatusesAPI:
    """Test suite for StatusesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def statuses_api(self, mock_client: Mock) -> StatusesAPI:
        """Create a StatusesAPI instance with mocked client."""
        return StatusesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test StatusesAPI initialization."""
        api = StatusesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_statuses(self, statuses_api: StatusesAPI) -> None:
        """Test get_statuses method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Passed"},
                {"id": 5, "name": "Failed"},
            ]

            result = statuses_api.get_statuses()

            mock_request.assert_called_once_with("GET", "get_statuses")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_api_request_failure(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                statuses_api.get_statuses()

    def test_authentication_error(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                statuses_api.get_statuses()

    def test_rate_limit_error(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                statuses_api.get_statuses()
