"""
Tests for the SuitesAPI module.

This module contains comprehensive tests for all methods in the SuitesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.suites import SuitesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestSuitesAPI:
    """Test suite for SuitesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def suites_api(self, mock_client: Mock) -> SuitesAPI:
        """Create a SuitesAPI instance with mocked client."""
        return SuitesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test SuitesAPI initialization."""
        api = SuitesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_suite(self, suites_api: SuitesAPI) -> None:
        """Test get_suite method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test Suite"}
            
            result = suites_api.get_suite(suite_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_suite/1')
            assert result == {"id": 1, "name": "Test Suite"}

    def test_get_suites(self, suites_api: SuitesAPI) -> None:
        """Test get_suites method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Suite 1"},
                {"id": 2, "name": "Suite 2"}
            ]
            
            result = suites_api.get_suites(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_suites/1')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_add_suite_minimal(self, suites_api: SuitesAPI) -> None:
        """Test add_suite with minimal required parameters."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Suite"}
            
            result = suites_api.add_suite(project_id=1, name="New Suite")
            
            expected_data = {"name": "New Suite"}
            mock_request.assert_called_once_with('POST', 'add_suite/1', data=expected_data)
            assert result == {"id": 1, "name": "New Suite"}

    def test_add_suite_with_all_parameters(self, suites_api: SuitesAPI) -> None:
        """Test add_suite with all optional parameters."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Suite"}
            
            result = suites_api.add_suite(
                project_id=1,
                name="New Suite",
                description="Suite description",
                url="https://example.com"
            )
            
            expected_data = {
                "name": "New Suite",
                "description": "Suite description",
                "url": "https://example.com"
            }
            mock_request.assert_called_once_with('POST', 'add_suite/1', data=expected_data)

    def test_add_suite_with_none_values(self, suites_api: SuitesAPI) -> None:
        """Test add_suite with None values for optional parameters."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Suite"}
            
            result = suites_api.add_suite(
                project_id=1,
                name="New Suite",
                description=None,
                url=None
            )
            
            expected_data = {"name": "New Suite"}
            mock_request.assert_called_once_with('POST', 'add_suite/1', data=expected_data)

    def test_update_suite(self, suites_api: SuitesAPI) -> None:
        """Test update_suite method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Suite"}
            
            result = suites_api.update_suite(
                suite_id=1,
                name="Updated Suite",
                description="Updated description"
            )
            
            expected_data = {
                "name": "Updated Suite",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with('POST', 'update_suite/1', data=expected_data)

    def test_delete_suite(self, suites_api: SuitesAPI) -> None:
        """Test delete_suite method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = suites_api.delete_suite(suite_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_suite/1')
            assert result == {}

    def test_get_suite_cases(self, suites_api: SuitesAPI) -> None:
        """Test get_suite_cases method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]
            
            result = suites_api.get_suite_cases(suite_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_suite_cases/1')
            assert len(result) == 2

    def test_get_suite_stats(self, suites_api: SuitesAPI) -> None:
        """Test get_suite_stats method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "total": 50,
                "passed": 40,
                "failed": 10
            }
            
            result = suites_api.get_suite_stats(suite_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_suite_stats/1')
            assert result["total"] == 50

    def test_get_suite_runs(self, suites_api: SuitesAPI) -> None:
        """Test get_suite_runs method."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Run 1"},
                {"id": 2, "name": "Run 2"}
            ]
            
            result = suites_api.get_suite_runs(suite_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_suite_runs/1')
            assert len(result) == 2

    def test_api_request_failure(self, suites_api: SuitesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                suites_api.get_suite(suite_id=1)

    def test_authentication_error(self, suites_api: SuitesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                suites_api.get_suite(suite_id=1)

    def test_rate_limit_error(self, suites_api: SuitesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(suites_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                suites_api.get_suite(suite_id=1)






