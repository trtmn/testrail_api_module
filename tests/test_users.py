"""
Tests for the UsersAPI module.

This module contains comprehensive tests for all methods in the UsersAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.users import UsersAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


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
        assert hasattr(api, 'logger')

    def test_get_user(self, users_api: UsersAPI) -> None:
        """Test get_user method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
            
            result = users_api.get_user(user_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_user/1')
            assert result == {"id": 1, "name": "Test User", "email": "test@example.com"}

    def test_get_users(self, users_api: UsersAPI) -> None:
        """Test get_users method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "User 1"},
                {"id": 2, "name": "User 2"}
            ]
            
            result = users_api.get_users()
            
            mock_request.assert_called_once_with('GET', 'get_users')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_user_by_email(self, users_api: UsersAPI) -> None:
        """Test get_user_by_email method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "email": "test@example.com"}
            
            result = users_api.get_user_by_email(email="test@example.com")
            
            mock_request.assert_called_once_with('GET', 'get_user_by_email&email=test@example.com')
            assert result == {"id": 1, "email": "test@example.com"}

    def test_add_user_minimal(self, users_api: UsersAPI) -> None:
        """Test add_user with minimal required parameters."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New User"}
            
            result = users_api.add_user(
                name="New User",
                email="newuser@example.com",
                password="password123"
            )
            
            expected_data = {
                "name": "New User",
                "email": "newuser@example.com",
                "password": "password123",
                "is_active": True
            }
            mock_request.assert_called_once_with('POST', 'add_user', data=expected_data)
            assert result == {"id": 1, "name": "New User"}

    def test_add_user_with_all_parameters(self, users_api: UsersAPI) -> None:
        """Test add_user with all optional parameters."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New User"}
            
            result = users_api.add_user(
                name="New User",
                email="newuser@example.com",
                password="password123",
                role_id=2,
                is_active=False
            )
            
            expected_data = {
                "name": "New User",
                "email": "newuser@example.com",
                "password": "password123",
                "role_id": 2,
                "is_active": False
            }
            mock_request.assert_called_once_with('POST', 'add_user', data=expected_data)

    def test_add_user_without_role_id(self, users_api: UsersAPI) -> None:
        """Test add_user without role_id."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1}
            
            result = users_api.add_user(
                name="New User",
                email="newuser@example.com",
                password="password123",
                role_id=None
            )
            
            expected_data = {
                "name": "New User",
                "email": "newuser@example.com",
                "password": "password123",
                "is_active": True
            }
            mock_request.assert_called_once_with('POST', 'add_user', data=expected_data)

    def test_update_user(self, users_api: UsersAPI) -> None:
        """Test update_user method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated User"}
            
            result = users_api.update_user(
                user_id=1,
                name="Updated User",
                email="updated@example.com"
            )
            
            expected_data = {
                "name": "Updated User",
                "email": "updated@example.com"
            }
            mock_request.assert_called_once_with('POST', 'update_user/1', data=expected_data)

    def test_delete_user(self, users_api: UsersAPI) -> None:
        """Test delete_user method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = users_api.delete_user(user_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_user/1')
            assert result == {}

    def test_get_user_activity(self, users_api: UsersAPI) -> None:
        """Test get_user_activity method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "action": "created"},
                {"id": 2, "action": "updated"}
            ]
            
            result = users_api.get_user_activity(user_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_user_activity/1')
            assert len(result) == 2

    def test_get_user_projects(self, users_api: UsersAPI) -> None:
        """Test get_user_projects method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Project 1"},
                {"id": 2, "name": "Project 2"}
            ]
            
            result = users_api.get_user_projects(user_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_user_projects/1')
            assert len(result) == 2

    def test_get_user_roles(self, users_api: UsersAPI) -> None:
        """Test get_user_roles method."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Admin"},
                {"id": 2, "name": "User"}
            ]
            
            result = users_api.get_user_roles(user_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_user_roles/1')
            assert len(result) == 2

    def test_api_request_failure(self, users_api: UsersAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                users_api.get_user(user_id=1)

    def test_authentication_error(self, users_api: UsersAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                users_api.get_user(user_id=1)

    def test_rate_limit_error(self, users_api: UsersAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(users_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                users_api.get_user(user_id=1)






