"""
Tests for the GroupsAPI module.

This module contains comprehensive tests for all methods in the GroupsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.groups import GroupsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestGroupsAPI:
    """Test suite for GroupsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def groups_api(self, mock_client: Mock) -> GroupsAPI:
        """Create a GroupsAPI instance with mocked client."""
        return GroupsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test GroupsAPI initialization."""
        api = GroupsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_group(self, groups_api: GroupsAPI) -> None:
        """Test get_group method."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.return_value = {"id": 1, "name": "Test Group"}
            
            result = groups_api.get_group(group_id=1)
            
            mock_get.assert_called_once_with('get_group/1')
            assert result == {"id": 1, "name": "Test Group"}

    def test_get_groups(self, groups_api: GroupsAPI) -> None:
        """Test get_groups method."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Group 1"},
                {"id": 2, "name": "Group 2"}
            ]
            
            result = groups_api.get_groups(project_id=1)
            
            mock_get.assert_called_once_with('get_groups/1')
            assert len(result) == 2

    def test_add_group_minimal(self, groups_api: GroupsAPI) -> None:
        """Test add_group with minimal required parameters."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Group"}
            
            result = groups_api.add_group(project_id=1, name="New Group")
            
            expected_data = {"name": "New Group"}
            mock_post.assert_called_once_with('add_group/1', data=expected_data)
            assert result == {"id": 1, "name": "New Group"}

    def test_add_group_with_description(self, groups_api: GroupsAPI) -> None:
        """Test add_group with description."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Group"}
            
            result = groups_api.add_group(
                project_id=1,
                name="New Group",
                description="Group description"
            )
            
            expected_data = {
                "name": "New Group",
                "description": "Group description"
            }
            mock_post.assert_called_once_with('add_group/1', data=expected_data)

    def test_update_group_minimal(self, groups_api: GroupsAPI) -> None:
        """Test update_group with minimal parameters."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1}
            
            result = groups_api.update_group(group_id=1)
            
            expected_data = {}
            mock_post.assert_called_once_with('update_group/1', data=expected_data)

    def test_update_group_with_all_parameters(self, groups_api: GroupsAPI) -> None:
        """Test update_group with all optional parameters."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Group"}
            
            result = groups_api.update_group(
                group_id=1,
                name="Updated Group",
                description="Updated description"
            )
            
            expected_data = {
                "name": "Updated Group",
                "description": "Updated description"
            }
            mock_post.assert_called_once_with('update_group/1', data=expected_data)

    def test_delete_group(self, groups_api: GroupsAPI) -> None:
        """Test delete_group method."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {}
            
            result = groups_api.delete_group(group_id=1)
            
            mock_post.assert_called_once_with('delete_group/1')
            assert result == {}

    def test_add_group_to_suite(self, groups_api: GroupsAPI) -> None:
        """Test add_group_to_suite method."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {}
            
            result = groups_api.add_group_to_suite(group_id=1, suite_id=2)
            
            mock_post.assert_called_once_with('add_group_to_suite/2/1')
            assert result == {}

    def test_remove_group_from_suite(self, groups_api: GroupsAPI) -> None:
        """Test remove_group_from_suite method."""
        with patch.object(groups_api, '_post') as mock_post:
            mock_post.return_value = {}
            
            result = groups_api.remove_group_from_suite(group_id=1, suite_id=2)
            
            mock_post.assert_called_once_with('remove_group_from_suite/2/1')
            assert result == {}

    def test_get_group_cases(self, groups_api: GroupsAPI) -> None:
        """Test get_group_cases method."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]
            
            result = groups_api.get_group_cases(group_id=1)
            
            mock_get.assert_called_once_with('get_group_cases/1')
            assert len(result) == 2

    def test_get_group_suites(self, groups_api: GroupsAPI) -> None:
        """Test get_group_suites method."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Suite 1"},
                {"id": 2, "name": "Suite 2"}
            ]
            
            result = groups_api.get_group_suites(group_id=1)
            
            mock_get.assert_called_once_with('get_group_suites/1')
            assert len(result) == 2

    def test_api_request_failure(self, groups_api: GroupsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                groups_api.get_group(group_id=1)

    def test_authentication_error(self, groups_api: GroupsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                groups_api.get_group(group_id=1)

    def test_rate_limit_error(self, groups_api: GroupsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(groups_api, '_get') as mock_get:
            mock_get.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                groups_api.get_group(group_id=1)





