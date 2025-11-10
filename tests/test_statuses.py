"""
Tests for the StatusesAPI module.

This module contains comprehensive tests for all methods in the StatusesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.statuses import StatusesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


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
        assert hasattr(api, 'logger')

    def test_get_status(self, statuses_api: StatusesAPI) -> None:
        """Test get_status method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Passed", "label": "Passed"}
            
            result = statuses_api.get_status(status_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_status/1')
            assert result == {"id": 1, "name": "Passed", "label": "Passed"}

    def test_get_statuses(self, statuses_api: StatusesAPI) -> None:
        """Test get_statuses method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Passed"},
                {"id": 5, "name": "Failed"}
            ]
            
            result = statuses_api.get_statuses()
            
            mock_request.assert_called_once_with('GET', 'get_statuses')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_add_status_minimal(self, statuses_api: StatusesAPI) -> None:
        """Test add_status with minimal required parameters."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Custom Status"}
            
            result = statuses_api.add_status(
                name="Custom Status",
                short_name="Custom",
                color="#FF0000"
            )
            
            expected_data = {
                "name": "Custom Status",
                "short_name": "Custom",
                "color": "#FF0000",
                "is_system": False,
                "is_untested": False,
                "is_passed": False,
                "is_blocked": False,
                "is_retest": False,
                "is_failed": False,
                "is_custom": True
            }
            mock_request.assert_called_once_with('POST', 'add_status', data=expected_data)
            assert result == {"id": 1, "name": "Custom Status"}

    def test_add_status_with_all_parameters(self, statuses_api: StatusesAPI) -> None:
        """Test add_status with all optional parameters."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Custom Status"}
            
            result = statuses_api.add_status(
                name="Custom Status",
                short_name="Custom",
                color="#FF0000",
                is_system=True,
                is_untested=False,
                is_passed=True,
                is_blocked=False,
                is_retest=False,
                is_failed=False,
                is_custom=False
            )
            
            expected_data = {
                "name": "Custom Status",
                "short_name": "Custom",
                "color": "#FF0000",
                "is_system": True,
                "is_untested": False,
                "is_passed": True,
                "is_blocked": False,
                "is_retest": False,
                "is_failed": False,
                "is_custom": False
            }
            mock_request.assert_called_once_with('POST', 'add_status', data=expected_data)

    def test_update_status(self, statuses_api: StatusesAPI) -> None:
        """Test update_status method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Status"}
            
            result = statuses_api.update_status(
                status_id=1,
                name="Updated Status",
                color="#00FF00"
            )
            
            expected_data = {
                "name": "Updated Status",
                "color": "#00FF00"
            }
            mock_request.assert_called_once_with('POST', 'update_status/1', data=expected_data)

    def test_delete_status(self, statuses_api: StatusesAPI) -> None:
        """Test delete_status method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = statuses_api.delete_status(status_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_status/1')
            assert result == {}

    def test_get_status_counts(self, statuses_api: StatusesAPI) -> None:
        """Test get_status_counts method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "1": 10,
                "5": 2,
                "2": 5
            }
            
            result = statuses_api.get_status_counts(run_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_status_counts/1')
            assert result["1"] == 10

    def test_get_status_history(self, statuses_api: StatusesAPI) -> None:
        """Test get_status_history method."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1, "created_on": 1000000},
                {"id": 2, "status_id": 5, "created_on": 2000000}
            ]
            
            result = statuses_api.get_status_history(result_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_status_history/1')
            assert len(result) == 2

    def test_api_request_failure(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                statuses_api.get_status(status_id=1)

    def test_authentication_error(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                statuses_api.get_status(status_id=1)

    def test_rate_limit_error(self, statuses_api: StatusesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(statuses_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                statuses_api.get_status(status_id=1)





