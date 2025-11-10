"""
Tests for the TestsAPI module.

This module contains comprehensive tests for all methods in the TestsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.tests import TestsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestTestsAPI:
    """Test suite for TestsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def tests_api(self, mock_client: Mock) -> TestsAPI:
        """Create a TestsAPI instance with mocked client."""
        return TestsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test TestsAPI initialization."""
        api = TestsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_test_minimal(self, tests_api: TestsAPI) -> None:
        """Test get_test with minimal required parameters."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = {"id": 1, "title": "Test Case"}
            
            result = tests_api.get_test(test_id=1)
            
            mock_get.assert_called_once_with('get_test/1', params={})
            assert result == {"id": 1, "title": "Test Case"}

    def test_get_test_with_data(self, tests_api: TestsAPI) -> None:
        """Test get_test with with_data parameter."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = {"id": 1, "title": "Test Case", "data": {}}
            
            result = tests_api.get_test(test_id=1, with_data=1)
            
            expected_params = {'with_data': 1}
            mock_get.assert_called_once_with('get_test/1', params=expected_params)

    def test_get_tests_minimal(self, tests_api: TestsAPI) -> None:
        """Test get_tests with minimal required parameters."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "title": "Test 1"},
                {"id": 2, "title": "Test 2"}
            ]
            
            result = tests_api.get_tests(run_id=1)
            
            mock_get.assert_called_once_with('get_tests/1', params={})
            assert len(result) == 2

    def test_get_tests_with_single_status_id(self, tests_api: TestsAPI) -> None:
        """Test get_tests with single status_id (int)."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = tests_api.get_tests(run_id=1, status_id=1)
            
            expected_params = {'status_id': 1}
            mock_get.assert_called_once_with('get_tests/1', params=expected_params)

    def test_get_tests_with_list_status_id(self, tests_api: TestsAPI) -> None:
        """Test get_tests with list status_id."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = tests_api.get_tests(run_id=1, status_id=[1, 5])
            
            expected_params = {'status_id': '1,5'}
            mock_get.assert_called_once_with('get_tests/1', params=expected_params)

    def test_get_tests_with_single_label_id(self, tests_api: TestsAPI) -> None:
        """Test get_tests with single label_id (int)."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = tests_api.get_tests(run_id=1, label_id=1)
            
            expected_params = {'label_id': 1}
            mock_get.assert_called_once_with('get_tests/1', params=expected_params)

    def test_get_tests_with_list_label_id(self, tests_api: TestsAPI) -> None:
        """Test get_tests with list label_id."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = tests_api.get_tests(run_id=1, label_id=[1, 2, 3])
            
            expected_params = {'label_id': '1,2,3'}
            mock_get.assert_called_once_with('get_tests/1', params=expected_params)

    def test_get_tests_with_all_parameters(self, tests_api: TestsAPI) -> None:
        """Test get_tests with all optional parameters."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = tests_api.get_tests(
                run_id=1,
                status_id=[1, 5],
                limit=50,
                offset=10,
                label_id=[1, 2]
            )
            
            expected_params = {
                'status_id': '1,5',
                'limit': 50,
                'offset': 10,
                'label_id': '1,2'
            }
            mock_get.assert_called_once_with('get_tests/1', params=expected_params)

    def test_get_test_results(self, tests_api: TestsAPI) -> None:
        """Test get_test_results method."""
        with patch.object(tests_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]
            
            result = tests_api.get_test_results(test_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_results_for_test/1')
            assert len(result) == 2

    def test_add_test_result_minimal(self, tests_api: TestsAPI) -> None:
        """Test add_test_result with minimal required parameters."""
        with patch.object(tests_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = tests_api.add_test_result(test_id=1, status_id=1)
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with('POST', 'add_result_for_test/1', data=expected_data)
            assert result == {"id": 1, "status_id": 1}

    def test_add_test_result_with_all_parameters(self, tests_api: TestsAPI) -> None:
        """Test add_test_result with all optional parameters."""
        with patch.object(tests_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = tests_api.add_test_result(
                test_id=1,
                status_id=1,
                comment="Test passed",
                version="1.0.0",
                elapsed="30s",
                defects="BUG-123",
                assignedto_id=1,
                custom_fields={"custom1": "value1"}
            )
            
            expected_data = {
                "status_id": 1,
                "comment": "Test passed",
                "version": "1.0.0",
                "elapsed": "30s",
                "defects": "BUG-123",
                "assignedto_id": 1,
                "custom1": "value1"
            }
            mock_request.assert_called_once_with('POST', 'add_result_for_test/1', data=expected_data)

    def test_add_test_result_with_none_values(self, tests_api: TestsAPI) -> None:
        """Test add_test_result with None values."""
        with patch.object(tests_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = tests_api.add_test_result(
                test_id=1,
                status_id=1,
                comment=None,
                version=None,
                elapsed=None,
                defects=None,
                assignedto_id=None,
                custom_fields=None
            )
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with('POST', 'add_result_for_test/1', data=expected_data)

    def test_add_test_results(self, tests_api: TestsAPI) -> None:
        """Test add_test_results method."""
        with patch.object(tests_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]
            
            test_ids = [1, 2]
            results = [
                {"status_id": 1, "comment": "Passed"},
                {"status_id": 5, "comment": "Failed"}
            ]
            
            result = tests_api.add_test_results(test_ids=test_ids, results=results)
            
            expected_data = {
                "test_ids": test_ids,
                "results": results
            }
            mock_request.assert_called_once_with('POST', 'add_results_for_tests', data=expected_data)

    def test_api_request_failure(self, tests_api: TestsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                tests_api.get_test(test_id=1)

    def test_authentication_error(self, tests_api: TestsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                tests_api.get_test(test_id=1)

    def test_rate_limit_error(self, tests_api: TestsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(tests_api, '_get') as mock_get:
            mock_get.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                tests_api.get_test(test_id=1)





