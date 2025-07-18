"""
Tests for the ResultsAPI module.

This module contains comprehensive tests for all methods in the ResultsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch

from testrail_api_module.results import ResultsAPI


class TestResultsAPI:
    """Test suite for ResultsAPI class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def results_api(self, mock_client):
        """Create a ResultsAPI instance with mocked client."""
        return ResultsAPI(mock_client)

    @pytest.fixture
    def sample_result_data(self):
        """Sample test result data for testing."""
        return {
            "status_id": 1,
            "comment": "Test passed successfully",
            "version": "1.0.0",
            "elapsed": "30s",
            "defects": "BUG-123",
            "assignedto_id": 1,
            "custom_fields": {"custom1": "value1"}
        }

    def test_init(self, mock_client):
        """Test ResultsAPI initialization."""
        api = ResultsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_add_result_minimal(self, results_api):
        """Test add_result with minimal required parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = results_api.add_result(
                run_id=1, 
                case_id=1, 
                status_id=1
            )
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_with_all_parameters(self, results_api,
                                          sample_result_data):
        """Test add_result with all optional parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, **sample_result_data}
            
            result = results_api.add_result(
                run_id=1,
                case_id=1,
                status_id=1,
                comment="Test passed successfully",
                version="1.0.0",
                elapsed="30s",
                defects="BUG-123",
                assignedto_id=1,
                custom_fields={"custom1": "value1"}
            )
            
            expected_data = {
                "status_id": 1,
                "comment": "Test passed successfully",
                "version": "1.0.0",
                "elapsed": "30s",
                "defects": "BUG-123",
                "assignedto_id": 1,
                "custom1": "value1"
            }
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )
            assert result == {"id": 1, **sample_result_data}

    def test_add_result_with_none_values(self, results_api):
        """Test add_result with None values for optional parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = results_api.add_result(
                run_id=1,
                case_id=1,
                status_id=1,
                comment=None,
                version=None,
                elapsed=None,
                defects=None,
                assignedto_id=None,
                custom_fields=None
            )
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_with_empty_strings(self, results_api):
        """Test add_result with empty strings for optional parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = results_api.add_result(
                run_id=1,
                case_id=1,
                status_id=1,
                comment="",
                version="",
                elapsed="",
                defects="",
                assignedto_id=0,
                custom_fields={}
            )
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_results_for_cases(self, results_api):
        """Test add_results_for_cases method."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"results": [{"id": 1}, {"id": 2}]}
            
            results_data = [
                {"case_id": 1, "status_id": 1, "comment": "Passed"},
                {"case_id": 2, "status_id": 5, "comment": "Failed"}
            ]
            
            result = results_api.add_results_for_cases(run_id=1, results=results_data)
            
            expected_data = {"results": results_data}
            mock_request.assert_called_once_with(
                'POST', 
                'add_results_for_cases/1', 
                expected_data
            )
            assert result == {"results": [{"id": 1}, {"id": 2}]}

    def test_add_result_for_run_minimal(self, results_api):
        """Test add_result_for_run with minimal required parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = results_api.add_result_for_run(
                run_id=1, 
                status_id=1
            )
            
            expected_data = {"status_id": 1}
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_run/1', 
                expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_for_run_with_all_parameters(self, results_api, sample_result_data):
        """Test add_result_for_run with all optional parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, **sample_result_data}
            
            result = results_api.add_result_for_run(
                run_id=1,
                status_id=1,
                comment="Test passed successfully",
                version="1.0.0",
                elapsed="30s",
                defects="BUG-123",
                assignedto_id=1,
                custom_fields={"custom1": "value1"}
            )
            
            expected_data = {
                "status_id": 1,
                "comment": "Test passed successfully",
                "version": "1.0.0",
                "elapsed": "30s",
                "defects": "BUG-123",
                "assignedto_id": 1,
                "custom1": "value1"
            }
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_run/1', 
                expected_data
            )
            assert result == {"id": 1, **sample_result_data}

    def test_get_results(self, results_api):
        """Test get_results method."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]
            
            result = results_api.get_results(run_id=1)
            
            mock_request.assert_called_once_with(
                'GET', 
                'get_results_for_run/1'
            )
            assert result == [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]

    def test_get_results_for_case(self, results_api):
        """Test get_results_for_case method."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1, "case_id": 1},
                {"id": 2, "status_id": 5, "case_id": 1}
            ]
            
            result = results_api.get_results_for_case(run_id=1, case_id=1)
            
            mock_request.assert_called_once_with(
                'GET', 
                'get_results_for_case/1/1'
            )
            assert result == [
                {"id": 1, "status_id": 1, "case_id": 1},
                {"id": 2, "status_id": 5, "case_id": 1}
            ]

    def test_get_results_for_run(self, results_api):
        """Test get_results_for_run method."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]
            
            result = results_api.get_results_for_run(run_id=1)
            
            mock_request.assert_called_once_with(
                'GET', 
                'get_results_for_run/1'
            )
            assert result == [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5}
            ]

    def test_add_results(self, results_api):
        """Test add_results method."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"results": [{"id": 1}, {"id": 2}]}
            
            results_data = [
                {"case_id": 1, "status_id": 1, "comment": "Passed"},
                {"case_id": 2, "status_id": 5, "comment": "Failed"}
            ]
            
            result = results_api.add_results(run_id=1, results=results_data)
            
            expected_data = {"results": results_data}
            mock_request.assert_called_once_with(
                'POST', 
                'add_results_for_cases/1', 
                expected_data
            )
            assert result == {"results": [{"id": 1}, {"id": 2}]}

    def test_api_request_failure(self, results_api):
        """Test behavior when API request fails."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = None
            
            result = results_api.add_result(
                run_id=1, 
                case_id=1, 
                status_id=1
            )
            
            assert result is None

    def test_custom_fields_override(self, results_api):
        """Test that custom_fields properly override explicit parameters."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 999}
            
            custom_fields = {
                "status_id": 999,  # This should override the explicit status_id
                "custom_field": "custom_value"
            }
            
            result = results_api.add_result(
                run_id=1,
                case_id=1,
                status_id=1,
                custom_fields=custom_fields
            )
            
            expected_data = {
                "status_id": 999,  # Should be from custom_fields, overriding explicit status_id
                "custom_field": "custom_value"
            }
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )

    @pytest.mark.parametrize("status_id", [1, 2, 3, 4, 5])
    def test_different_status_ids(self, results_api, status_id):
        """Test add_result with different status IDs."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": status_id}
            
            result = results_api.add_result(
                run_id=1, 
                case_id=1, 
                status_id=status_id
            )
            
            expected_data = {"status_id": status_id}
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            )
            assert result["status_id"] == status_id

    def test_large_run_and_case_ids(self, results_api):
        """Test with large run and case IDs."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            result = results_api.add_result(
                run_id=999999, 
                case_id=999999, 
                status_id=1
            )
            
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/999999/999999', 
                {"status_id": 1}
            )

    def test_empty_results_list(self, results_api):
        """Test add_results with empty results list."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"results": []}
            
            result = results_api.add_results(run_id=1, results=[])
            
            expected_data = {"results": []}
            mock_request.assert_called_once_with(
                'POST', 
                'add_results_for_cases/1', 
                expected_data
            )
            assert result == {"results": []}

    def test_complex_custom_fields(self, results_api):
        """Test with complex custom fields data."""
        with patch.object(results_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "status_id": 1}
            
            complex_custom_fields = {
                "string_field": "test_value",
                "number_field": 42,
                "boolean_field": True,
                "null_field": None,
                "list_field": [1, 2, 3],
                "nested_dict": {"key": "value"}
            }
            
            result = results_api.add_result(
                run_id=1,
                case_id=1,
                status_id=1,
                custom_fields=complex_custom_fields
            )
            
            expected_data = {
                "status_id": 1,
                **complex_custom_fields
            }
            mock_request.assert_called_once_with(
                'POST', 
                'add_result_for_case/1/1', 
                expected_data
            ) 