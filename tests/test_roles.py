"""
Tests for the RolesAPI module.

This module contains comprehensive tests for all methods in the RolesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.roles import RolesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestRolesAPI:
    """Test suite for RolesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def roles_api(self, mock_client: Mock) -> RolesAPI:
        """Create a RolesAPI instance with mocked client."""
        return RolesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test RolesAPI initialization."""
        api = RolesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_role(self, roles_api: RolesAPI) -> None:
        """Test get_role method."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Admin"}
            
            result = roles_api.get_role(role_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_role/1')
            assert result == {"id": 1, "name": "Admin"}

    def test_get_roles(self, roles_api: RolesAPI) -> None:
        """Test get_roles method."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Admin"},
                {"id": 2, "name": "User"}
            ]
            
            result = roles_api.get_roles()
            
            mock_request.assert_called_once_with('GET', 'get_roles')
            assert len(result) == 2

    def test_add_role_minimal(self, roles_api: RolesAPI) -> None:
        """Test add_role with minimal required parameters."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Role"}
            
            result = roles_api.add_role(name="New Role")
            
            expected_data = {"name": "New Role"}
            mock_request.assert_called_once_with('POST', 'add_role', data=expected_data)
            assert result == {"id": 1, "name": "New Role"}

    def test_add_role_with_all_parameters(self, roles_api: RolesAPI) -> None:
        """Test add_role with all optional parameters."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Role"}
            
            permissions = {
                "view_test_cases": True,
                "edit_test_cases": True,
                "delete_test_cases": False
            }
            
            result = roles_api.add_role(
                name="New Role",
                description="Role description",
                permissions=permissions
            )
            
            expected_data = {
                "name": "New Role",
                "description": "Role description",
                "permissions": permissions
            }
            mock_request.assert_called_once_with('POST', 'add_role', data=expected_data)

    def test_update_role(self, roles_api: RolesAPI) -> None:
        """Test update_role method."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Role"}
            
            result = roles_api.update_role(
                role_id=1,
                name="Updated Role",
                description="Updated description"
            )
            
            expected_data = {
                "name": "Updated Role",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with('POST', 'update_role/1', data=expected_data)

    def test_delete_role(self, roles_api: RolesAPI) -> None:
        """Test delete_role method."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = roles_api.delete_role(role_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_role/1')
            assert result == {}

    def test_api_request_failure(self, roles_api: RolesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                roles_api.get_role(role_id=1)

    def test_authentication_error(self, roles_api: RolesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                roles_api.get_role(role_id=1)

    def test_rate_limit_error(self, roles_api: RolesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(roles_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                roles_api.get_role(role_id=1)





