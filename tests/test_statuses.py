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

    @pytest.fixture
    def sample_statuses_data(self) -> list[dict]:
        """Sample statuses data for testing."""
        return [
            {"id": 1, "name": "passed", "label": "Passed"},
            {"id": 2, "name": "blocked", "label": "Blocked"},
            {"id": 3, "name": "untested", "label": "Untested"},
            {"id": 4, "name": "retest", "label": "Retest"},
            {"id": 5, "name": "failed", "label": "Failed"},
        ]

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def test_init(self, mock_client: Mock) -> None:
        """Test StatusesAPI initialization."""
        api = StatusesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    # -------------------------------------------------------------------------
    # get_statuses
    # -------------------------------------------------------------------------

    def test_get_statuses(
        self,
        statuses_api: StatusesAPI,
        sample_statuses_data: list[dict],
    ) -> None:
        """Test get_statuses returns list of status dicts."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.return_value = sample_statuses_data

            result = statuses_api.get_statuses()

            mock_get.assert_called_once_with("get_statuses")
            assert result == sample_statuses_data
            assert len(result) == 5

    def test_get_statuses_returns_list(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_statuses returns a plain list (no pagination envelope)."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "passed"},
                {"id": 5, "name": "failed"},
            ]

            result = statuses_api.get_statuses()

            assert isinstance(result, list)
            assert result[0]["id"] == 1

    def test_get_statuses_api_error(self, statuses_api: StatusesAPI) -> None:
        """Test get_statuses raises TestRailAPIError on API failure."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                statuses_api.get_statuses()

    def test_get_statuses_authentication_error(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_statuses raises TestRailAuthenticationError."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                statuses_api.get_statuses()

    def test_get_statuses_rate_limit_error(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_statuses raises TestRailRateLimitError."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                statuses_api.get_statuses()

    # -------------------------------------------------------------------------
    # get_case_statuses
    # -------------------------------------------------------------------------

    def test_get_case_statuses(self, statuses_api: StatusesAPI) -> None:
        """Test get_case_statuses returns list of case status dicts."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "open", "label": "Open"},
                {"id": 2, "name": "in_progress", "label": "In Progress"},
                {"id": 3, "name": "closed", "label": "Closed"},
            ]

            result = statuses_api.get_case_statuses()

            mock_get.assert_called_once_with("get_case_statuses")
            assert len(result) == 3
            assert result[0]["id"] == 1

    def test_get_case_statuses_returns_list(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_case_statuses returns a plain list."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "name": "open"}]

            result = statuses_api.get_case_statuses()

            assert isinstance(result, list)

    def test_get_case_statuses_empty(self, statuses_api: StatusesAPI) -> None:
        """Test get_case_statuses with an empty list response."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.return_value = []

            result = statuses_api.get_case_statuses()

            mock_get.assert_called_once_with("get_case_statuses")
            assert result == []

    def test_get_case_statuses_api_error(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_case_statuses raises TestRailAPIError on API failure."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                statuses_api.get_case_statuses()

    def test_get_case_statuses_authentication_error(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_case_statuses raises TestRailAuthenticationError."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                statuses_api.get_case_statuses()

    def test_get_case_statuses_rate_limit_error(
        self, statuses_api: StatusesAPI
    ) -> None:
        """Test get_case_statuses raises TestRailRateLimitError."""
        with patch.object(statuses_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                statuses_api.get_case_statuses()
