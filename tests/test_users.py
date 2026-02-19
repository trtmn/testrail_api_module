"""
Tests for the UsersAPI module.

This module contains comprehensive tests for all methods in the UsersAPI class,
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
from testrail_api_module.users import UsersAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestUsersAPI:
    """Test suite for UsersAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def users_api(self, mock_client: Mock) -> UsersAPI:
        """Create a UsersAPI instance with mocked client."""
        return UsersAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test UsersAPI initialization."""
        api = UsersAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_user(self, users_api: UsersAPI) -> None:
        """Test get_user method."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
            }

            result = result = users_api.get_user(user_id=1)
            mock_request.assert_called_once_with("GET", "get_user/1")
            assert result == {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
            }

    def test_get_users(self, users_api: UsersAPI) -> None:
        """Test get_users method."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "User 1"},
                {"id": 2, "name": "User 2"},
            ]

            result = users_api.get_users()

            mock_request.assert_called_once_with("GET", "get_users")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_user_by_email(self, users_api: UsersAPI) -> None:
        """Test get_user_by_email method."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "email": "test@example.com"}

            result = users_api.get_user_by_email(email="test@example.com")

            mock_request.assert_called_once_with(
                "GET", "get_user_by_email&email=test@example.com"
            )
            assert result == {"id": 1, "email": "test@example.com"}

    def test_api_request_failure(self, users_api: UsersAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                users_api.get_user(user_id=1)

    def test_authentication_error(self, users_api: UsersAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                users_api.get_user(user_id=1)

    def test_rate_limit_error(self, users_api: UsersAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                users_api.get_user(user_id=1)
