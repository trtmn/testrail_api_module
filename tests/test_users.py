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

    @pytest.fixture
    def sample_user_data(self) -> dict:
        """Sample user data for testing."""
        return {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "is_active": True,
            "role_id": 3,
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test UsersAPI initialization."""
        api = UsersAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_user(
        self, users_api: UsersAPI, sample_user_data: dict
    ) -> None:
        """Test get_user method."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = sample_user_data

            result = users_api.get_user(user_id=1)

            mock_request.assert_called_once_with("GET", "get_user/1")
            assert result == sample_user_data

    def test_get_users_minimal(self, users_api: UsersAPI) -> None:
        """Test get_users with minimal required parameters."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "User 1"},
                {"id": 2, "name": "User 2"},
            ]

            result = users_api.get_users()

            mock_request.assert_called_once_with("GET", "get_users")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_users_with_project_id(self, users_api: UsersAPI) -> None:
        """Test get_users with the optional project_id parameter."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1, "name": "User 1"}]

            result = users_api.get_users(project_id=5)

            mock_request.assert_called_once_with("GET", "get_users/5")
            assert result == [{"id": 1, "name": "User 1"}]

    def test_get_users_with_none_project_id(self, users_api: UsersAPI) -> None:
        """Test get_users with project_id explicitly set to None."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1, "name": "User 1"}]

            result = users_api.get_users(project_id=None)

            mock_request.assert_called_once_with("GET", "get_users")
            assert result == [{"id": 1, "name": "User 1"}]

    @pytest.mark.parametrize("project_id", [1, 42, 999999])
    def test_get_users_with_different_project_ids(
        self, users_api: UsersAPI, project_id: int
    ) -> None:
        """Test get_users builds the endpoint for different project IDs."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = []

            result = users_api.get_users(project_id=project_id)

            mock_request.assert_called_once_with(
                "GET", f"get_users/{project_id}"
            )
            assert result == []

    def test_get_users_api_request_failure(self, users_api: UsersAPI) -> None:
        """Test get_users behavior when API request fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                users_api.get_users()

    def test_get_users_authentication_error(self, users_api: UsersAPI) -> None:
        """Test get_users behavior when authentication fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                users_api.get_users(project_id=1)

    def test_get_users_rate_limit_error(self, users_api: UsersAPI) -> None:
        """Test get_users behavior when rate limit is exceeded."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                users_api.get_users(project_id=1)

    def test_get_current_user(
        self, users_api: UsersAPI, sample_user_data: dict
    ) -> None:
        """Test get_current_user method."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = sample_user_data

            result = users_api.get_current_user()

            mock_request.assert_called_once_with("GET", "get_current_user")
            assert result == sample_user_data

    def test_get_current_user_api_request_failure(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_current_user behavior when API request fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                users_api.get_current_user()

    def test_get_current_user_authentication_error(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_current_user behavior when authentication fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                users_api.get_current_user()

    def test_get_current_user_rate_limit_error(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_current_user behavior when rate limit is exceeded."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                users_api.get_current_user()

    def test_get_user_by_email(self, users_api: UsersAPI) -> None:
        """Test get_user_by_email passes the email via params."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "email": "test@example.com"}

            result = users_api.get_user_by_email(email="test@example.com")

            mock_request.assert_called_once_with(
                "GET",
                "get_user_by_email",
                params={"email": "test@example.com"},
            )
            assert result == {"id": 1, "email": "test@example.com"}

    def test_get_user_by_email_with_plus_alias(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_user_by_email passes plus-aliased emails via params.

        Regression test for issue #144: the endpoint previously embedded
        the raw email in the endpoint string, so characters like '+'
        decoded server-side as a space. Passing the email via params lets
        _build_url urlencode it correctly.
        """
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 2,
                "email": "user+qa@example.com",
            }

            result = users_api.get_user_by_email(email="user+qa@example.com")

            mock_request.assert_called_once_with(
                "GET",
                "get_user_by_email",
                params={"email": "user+qa@example.com"},
            )
            assert result == {"id": 2, "email": "user+qa@example.com"}

    def test_get_user_by_email_url_is_encoded(
        self, users_api: UsersAPI
    ) -> None:
        """Test that _build_url urlencodes emails passed via params."""
        url = users_api._build_url(
            "get_user_by_email", params={"email": "user+qa@example.com"}
        )
        assert url == (
            "https://testrail.example.com/index.php?"
            "/api/v2/get_user_by_email&email=user%2Bqa%40example.com"
        )

    def test_get_user_by_email_api_request_failure(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_user_by_email behavior when API request fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                users_api.get_user_by_email(email="test@example.com")

    def test_get_user_by_email_authentication_error(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_user_by_email behavior when authentication fails."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                users_api.get_user_by_email(email="test@example.com")

    def test_get_user_by_email_rate_limit_error(
        self, users_api: UsersAPI
    ) -> None:
        """Test get_user_by_email behavior when rate limit is exceeded."""
        with patch.object(users_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                users_api.get_user_by_email(email="test@example.com")

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
