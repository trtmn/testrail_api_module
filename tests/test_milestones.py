"""
Tests for the MilestonesAPI module.

This module contains comprehensive tests for all methods in the MilestonesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.milestones import MilestonesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestMilestonesAPI:
    """Test suite for MilestonesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def milestones_api(self, mock_client: Mock) -> MilestonesAPI:
        """Create a MilestonesAPI instance with mocked client."""
        return MilestonesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test MilestonesAPI initialization."""
        api = MilestonesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_milestone(self, milestones_api: MilestonesAPI) -> None:
        """Test get_milestone method."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Milestone 1"}
            
            result = milestones_api.get_milestone(milestone_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_milestone/1')
            assert result == {"id": 1, "name": "Milestone 1"}

    def test_get_milestones(self, milestones_api: MilestonesAPI) -> None:
        """Test get_milestones method."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Milestone 1"},
                {"id": 2, "name": "Milestone 2"}
            ]
            
            result = milestones_api.get_milestones(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_milestones/1')
            assert len(result) == 2

    def test_add_milestone_minimal(self, milestones_api: MilestonesAPI) -> None:
        """Test add_milestone with minimal required parameters."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Milestone"}
            
            result = milestones_api.add_milestone(project_id=1, name="New Milestone")
            
            expected_data = {"name": "New Milestone"}
            mock_request.assert_called_once_with('POST', 'add_milestone/1', data=expected_data)
            assert result == {"id": 1, "name": "New Milestone"}

    def test_add_milestone_with_all_parameters(self, milestones_api: MilestonesAPI) -> None:
        """Test add_milestone with all optional parameters."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Milestone"}
            
            result = milestones_api.add_milestone(
                project_id=1,
                name="New Milestone",
                description="Milestone description",
                due_on="2024-12-31",
                parent_id=2,
                start_on="2024-01-01"
            )
            
            expected_data = {
                "name": "New Milestone",
                "description": "Milestone description",
                "due_on": "2024-12-31",
                "parent_id": 2,
                "start_on": "2024-01-01"
            }
            mock_request.assert_called_once_with('POST', 'add_milestone/1', data=expected_data)

    def test_add_milestone_with_none_values(self, milestones_api: MilestonesAPI) -> None:
        """Test add_milestone with None values."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Milestone"}
            
            result = milestones_api.add_milestone(
                project_id=1,
                name="New Milestone",
                description=None,
                due_on=None,
                parent_id=None,
                start_on=None
            )
            
            expected_data = {"name": "New Milestone"}
            mock_request.assert_called_once_with('POST', 'add_milestone/1', data=expected_data)

    def test_update_milestone(self, milestones_api: MilestonesAPI) -> None:
        """Test update_milestone method."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Milestone"}
            
            result = milestones_api.update_milestone(
                milestone_id=1,
                name="Updated Milestone",
                due_on="2025-12-31"
            )
            
            expected_data = {
                "name": "Updated Milestone",
                "due_on": "2025-12-31"
            }
            mock_request.assert_called_once_with('POST', 'update_milestone/1', data=expected_data)

    def test_delete_milestone(self, milestones_api: MilestonesAPI) -> None:
        """Test delete_milestone method."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = milestones_api.delete_milestone(milestone_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_milestone/1')
            assert result == {}

    def test_get_milestone_stats(self, milestones_api: MilestonesAPI) -> None:
        """Test get_milestone_stats method."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "total": 100,
                "passed": 80,
                "failed": 20
            }
            
            result = milestones_api.get_milestone_stats(milestone_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_milestone_stats/1')
            assert result["total"] == 100

    def test_api_request_failure(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                milestones_api.get_milestone(milestone_id=1)

    def test_authentication_error(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                milestones_api.get_milestone(milestone_id=1)

    def test_rate_limit_error(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(milestones_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                milestones_api.get_milestone(milestone_id=1)






