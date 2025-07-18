"""
Tests for the StatusesAPI module.

This module contains comprehensive tests for all methods in the StatusesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch

from testrail_api_module.statuses import StatusesAPI


class TestStatusesAPI:
    """Test suite for StatusesAPI class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def statuses_api(self, mock_client):
        """Create a StatusesAPI instance with mocked client."""
        return StatusesAPI(mock_client)

    @pytest.fixture
    def sample_status_data(self):
        """Sample status data for testing."""
        return {
            "id": 1,
            "name": "Passed",
            "short_name": "pass",
            "color": "#7bc97b",
            "is_system": True,
            "is_untested": False,
            "is_passed": True,
            "is_blocked": False,
            "is_retest": False,
            "is_failed": False,
            "is_custom": False,
        }

    def test_init(self, mock_client):
        """Test StatusesAPI initialization."""
        api = StatusesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_status(self, statuses_api, sample_status_data):
        """Test get_status method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = sample_status_data

            result = statuses_api.get_status(status_id=1)

            mock_request.assert_called_once_with("GET", "get_status/1")
            assert result == sample_status_data

    def test_get_status_with_large_id(self, statuses_api):
        """Test get_status with a large status ID."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 999999, "name": "Large ID Status"}

            result = statuses_api.get_status(status_id=999999)

            mock_request.assert_called_once_with("GET", "get_status/999999")
            assert result == {"id": 999999, "name": "Large ID Status"}

    def test_get_statuses(self, statuses_api):
        """Test get_statuses method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Passed", "color": "#7bc97b"},
                {"id": 2, "name": "Failed", "color": "#f5c6cb"},
                {"id": 3, "name": "Blocked", "color": "#ffeaa7"},
            ]

            result = statuses_api.get_statuses()

            mock_request.assert_called_once_with("GET", "get_statuses")
            assert result == [
                {"id": 1, "name": "Passed", "color": "#7bc97b"},
                {"id": 2, "name": "Failed", "color": "#f5c6cb"},
                {"id": 3, "name": "Blocked", "color": "#ffeaa7"},
            ]

    def test_add_status_minimal(self, statuses_api, sample_status_data):
        """Test add_status with minimal required parameters."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = sample_status_data

            result = statuses_api.add_status(
                name="Passed", short_name="pass", color="#7bc97b"
            )

            expected_data = {
                "name": "Passed",
                "short_name": "pass",
                "color": "#7bc97b",
                "is_system": False,
                "is_untested": False,
                "is_passed": False,
                "is_blocked": False,
                "is_retest": False,
                "is_failed": False,
                "is_custom": True,
            }
            mock_request.assert_called_once_with(
                "POST", "add_status", data=expected_data
            )
            assert result == sample_status_data

    def test_add_status_with_all_parameters(self, statuses_api, sample_status_data):
        """Test add_status with all optional parameters."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = sample_status_data

            result = statuses_api.add_status(
                name="Custom Status",
                short_name="custom",
                color="#ff6b6b",
                is_system=True,
                is_untested=False,
                is_passed=True,
                is_blocked=False,
                is_retest=False,
                is_failed=False,
                is_custom=False,
            )

            expected_data = {
                "name": "Custom Status",
                "short_name": "custom",
                "color": "#ff6b6b",
                "is_system": True,
                "is_untested": False,
                "is_passed": True,
                "is_blocked": False,
                "is_retest": False,
                "is_failed": False,
                "is_custom": False,
            }
            mock_request.assert_called_once_with(
                "POST", "add_status", data=expected_data
            )
            assert result == sample_status_data

    def test_add_status_with_different_boolean_combinations(self, statuses_api):
        """Test add_status with different boolean parameter combinations."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test Status"}

            result = statuses_api.add_status(
                name="Test Status",
                short_name="test",
                color="#000000",
                is_system=False,
                is_untested=True,
                is_passed=False,
                is_blocked=True,
                is_retest=False,
                is_failed=True,
                is_custom=True,
            )

            expected_data = {
                "name": "Test Status",
                "short_name": "test",
                "color": "#000000",
                "is_system": False,
                "is_untested": True,
                "is_passed": False,
                "is_blocked": True,
                "is_retest": False,
                "is_failed": True,
                "is_custom": True,
            }
            mock_request.assert_called_once_with(
                "POST", "add_status", data=expected_data
            )
            assert result == {"id": 1, "name": "Test Status"}

    def test_update_status(self, statuses_api, sample_status_data):
        """Test update_status method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = sample_status_data

            result = statuses_api.update_status(
                status_id=1, name="Updated Status", color="#ff0000", is_custom=True
            )

            expected_data = {
                "name": "Updated Status",
                "color": "#ff0000",
                "is_custom": True,
            }
            mock_request.assert_called_once_with(
                "POST", "update_status/1", data=expected_data
            )
            assert result == sample_status_data

    def test_update_status_with_multiple_fields(self, statuses_api):
        """Test update_status with multiple fields."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Status"}

            result = statuses_api.update_status(
                status_id=1,
                name="Updated Status",
                short_name="updated",
                color="#00ff00",
                is_system=False,
                is_passed=True,
            )

            expected_data = {
                "name": "Updated Status",
                "short_name": "updated",
                "color": "#00ff00",
                "is_system": False,
                "is_passed": True,
            }
            mock_request.assert_called_once_with(
                "POST", "update_status/1", data=expected_data
            )
            assert result == {"id": 1, "name": "Updated Status"}

    def test_delete_status(self, statuses_api):
        """Test delete_status method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"success": True}

            result = statuses_api.delete_status(status_id=1)

            mock_request.assert_called_once_with("POST", "delete_status/1")
            assert result == {"success": True}

    def test_delete_status_with_large_id(self, statuses_api):
        """Test delete_status with a large status ID."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"success": True}

            result = statuses_api.delete_status(status_id=999999)

            mock_request.assert_called_once_with("POST", "delete_status/999999")
            assert result == {"success": True}

    def test_get_status_counts(self, statuses_api):
        """Test get_status_counts method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "1": 10,  # Passed
                "2": 5,  # Failed
                "3": 2,  # Blocked
                "4": 3,  # Retest
            }

            result = statuses_api.get_status_counts(run_id=1)

            mock_request.assert_called_once_with("GET", "get_status_counts/1")
            assert result == {"1": 10, "2": 5, "3": 2, "4": 3}

    def test_get_status_counts_with_large_run_id(self, statuses_api):
        """Test get_status_counts with a large run ID."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"1": 100, "2": 50}

            result = statuses_api.get_status_counts(run_id=999999)

            mock_request.assert_called_once_with("GET", "get_status_counts/999999")
            assert result == {"1": 100, "2": 50}

    def test_get_status_history(self, statuses_api):
        """Test get_status_history method."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {
                    "id": 1,
                    "status_id": 1,
                    "comment": "Test passed",
                    "created_on": 1234567890,
                },
                {
                    "id": 2,
                    "status_id": 2,
                    "comment": "Test failed",
                    "created_on": 1234567891,
                },
            ]

            result = statuses_api.get_status_history(result_id=1)

            mock_request.assert_called_once_with("GET", "get_status_history/1")
            assert result == [
                {
                    "id": 1,
                    "status_id": 1,
                    "comment": "Test passed",
                    "created_on": 1234567890,
                },
                {
                    "id": 2,
                    "status_id": 2,
                    "comment": "Test failed",
                    "created_on": 1234567891,
                },
            ]

    def test_get_status_history_with_large_result_id(self, statuses_api):
        """Test get_status_history with a large result ID."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = []

            result = statuses_api.get_status_history(result_id=999999)

            mock_request.assert_called_once_with("GET", "get_status_history/999999")
            assert result == []

    def test_api_request_failure(self, statuses_api):
        """Test API request failure handling."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = None

            result = statuses_api.get_status(status_id=1)

            assert result is None

    @pytest.mark.parametrize("status_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_different_status_ids(self, statuses_api, status_id):
        """Test get_status with different status ID values."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": status_id, "name": f"Status {status_id}"}

            result = statuses_api.get_status(status_id=status_id)

            mock_request.assert_called_once_with("GET", f"get_status/{status_id}")
            assert result == {"id": status_id, "name": f"Status {status_id}"}

    @pytest.mark.parametrize("run_id", [1, 10, 100, 1000, 9999])
    def test_different_run_ids_for_status_counts(self, statuses_api, run_id):
        """Test get_status_counts with different run ID values."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"1": run_id, "2": run_id // 2}

            result = statuses_api.get_status_counts(run_id=run_id)

            mock_request.assert_called_once_with("GET", f"get_status_counts/{run_id}")
            assert result == {"1": run_id, "2": run_id // 2}

    def test_empty_statuses_list(self, statuses_api):
        """Test get_statuses returning empty list."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = []

            result = statuses_api.get_statuses()

            mock_request.assert_called_once_with("GET", "get_statuses")
            assert result == []

    def test_empty_status_counts(self, statuses_api):
        """Test get_status_counts returning empty dictionary."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = statuses_api.get_status_counts(run_id=1)

            mock_request.assert_called_once_with("GET", "get_status_counts/1")
            assert result == {}

    def test_empty_status_history(self, statuses_api):
        """Test get_status_history returning empty list."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = []

            result = statuses_api.get_status_history(result_id=1)

            mock_request.assert_called_once_with("GET", "get_status_history/1")
            assert result == []

    def test_complex_status_data(self, statuses_api):
        """Test add_status with complex status data."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Complex Status"}

            result = statuses_api.add_status(
                name="Complex Status with Special Characters!@#$%",
                short_name="complex",
                color="#ff6b6b",
                is_system=True,
                is_untested=False,
                is_passed=False,
                is_blocked=False,
                is_retest=True,
                is_failed=False,
                is_custom=False,
            )

            expected_data = {
                "name": "Complex Status with Special Characters!@#$%",
                "short_name": "complex",
                "color": "#ff6b6b",
                "is_system": True,
                "is_untested": False,
                "is_passed": False,
                "is_blocked": False,
                "is_retest": True,
                "is_failed": False,
                "is_custom": False,
            }
            mock_request.assert_called_once_with(
                "POST", "add_status", data=expected_data
            )
            assert result == {"id": 1, "name": "Complex Status"}

    def test_zero_values_handling(self, statuses_api):
        """Test handling of zero values for IDs."""
        with patch.object(statuses_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 0, "name": "Zero ID Status"}

            result = statuses_api.get_status(status_id=0)

            mock_request.assert_called_once_with("GET", "get_status/0")
            assert result == {"id": 0, "name": "Zero ID Status"}
