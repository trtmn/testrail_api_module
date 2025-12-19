"""
Tests for the PrioritiesAPI module.

This module contains comprehensive tests for all methods in the PrioritiesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.priorities import PrioritiesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


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
        assert hasattr(api, 'logger')

    def test_get_priority(self, priorities_api: PrioritiesAPI) -> None:
        """Test get_priority method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "High", "priority": 1}
            
            result = priorities_api.get_priority(priority_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_priority/1')
            assert result == {"id": 1, "name": "High", "priority": 1}

    def test_get_priorities(self, priorities_api: PrioritiesAPI) -> None:
        """Test get_priorities method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "High"},
                {"id": 2, "name": "Medium"},
                {"id": 3, "name": "Low"}
            ]
            
            result = priorities_api.get_priorities()
            
            mock_request.assert_called_once_with('GET', 'get_priorities')
            assert len(result) == 3
            assert result[0]["id"] == 1

    def test_add_priority_minimal(self, priorities_api: PrioritiesAPI) -> None:
        """Test add_priority with minimal required parameters."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Custom Priority"}
            
            result = priorities_api.add_priority(
                name="Custom Priority",
                short_name="Custom",
                color="#FF0000"
            )
            
            expected_data = {
                "name": "Custom Priority",
                "short_name": "Custom",
                "color": "#FF0000",
                "is_default": False
            }
            mock_request.assert_called_once_with('POST', 'add_priority', data=expected_data)
            assert result == {"id": 1, "name": "Custom Priority"}

    def test_add_priority_with_all_parameters(self, priorities_api: PrioritiesAPI) -> None:
        """Test add_priority with all optional parameters."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Custom Priority"}
            
            result = priorities_api.add_priority(
                name="Custom Priority",
                short_name="Custom",
                color="#FF0000",
                is_default=True
            )
            
            expected_data = {
                "name": "Custom Priority",
                "short_name": "Custom",
                "color": "#FF0000",
                "is_default": True
            }
            mock_request.assert_called_once_with('POST', 'add_priority', data=expected_data)

    def test_update_priority(self, priorities_api: PrioritiesAPI) -> None:
        """Test update_priority method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Priority"}
            
            result = priorities_api.update_priority(
                priority_id=1,
                name="Updated Priority",
                color="#00FF00"
            )
            
            expected_data = {
                "name": "Updated Priority",
                "color": "#00FF00"
            }
            mock_request.assert_called_once_with('POST', 'update_priority/1', data=expected_data)

    def test_delete_priority(self, priorities_api: PrioritiesAPI) -> None:
        """Test delete_priority method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = priorities_api.delete_priority(priority_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_priority/1')
            assert result == {}

    def test_get_priority_counts(self, priorities_api: PrioritiesAPI) -> None:
        """Test get_priority_counts method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "1": 20,
                "2": 30,
                "3": 10
            }
            
            result = priorities_api.get_priority_counts(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_priority_counts/1')
            assert result["1"] == 20

    def test_get_priority_stats(self, priorities_api: PrioritiesAPI) -> None:
        """Test get_priority_stats method."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "total": 60,
                "by_priority": {
                    "1": 20,
                    "2": 30,
                    "3": 10
                }
            }
            
            result = priorities_api.get_priority_stats(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_priority_stats/1')
            assert result["total"] == 60

    def test_api_request_failure(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                priorities_api.get_priority(priority_id=1)

    def test_authentication_error(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                priorities_api.get_priority(priority_id=1)

    def test_rate_limit_error(self, priorities_api: PrioritiesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(priorities_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                priorities_api.get_priority(priority_id=1)






