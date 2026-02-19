"""
Tests for the Results module.

This module contains comprehensive tests for all methods in the ResultsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.results import ResultsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


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
            "id": 1,
            "status_id": 1,
            "comment": "Test passed successfully",
            "version": "1.0.0",
            "elapsed": "30s",
            "defects": "BUG-123",
            "assignedto_id": 1,
        }

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def test_init(self, mock_client) -> None:
        """Test ResultsAPI initialization."""
        api = ResultsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    # -------------------------------------------------------------------------
    # get_results
    # -------------------------------------------------------------------------

    def test_get_results_minimal(self, results_api: ResultsAPI) -> None:
        """Test get_results with minimal required parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5},
            ]

            result = results_api.get_results(test_id=42)

            mock_get.assert_called_once_with("get_results/42", params={})
            assert result == [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5},
            ]

    def test_get_results_with_all_parameters(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results with all optional parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "status_id": 1}]

            result = results_api.get_results(
                test_id=42,
                status_id=[1, 5],
                limit=50,
                offset=10,
            )

            expected_params = {
                "status_id": "1,5",
                "limit": 50,
                "offset": 10,
            }
            mock_get.assert_called_once_with(
                "get_results/42", params=expected_params
            )
            assert result == [{"id": 1, "status_id": 1}]

    def test_get_results_with_none_values(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results with None values for optional parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "status_id": 1}]

            result = results_api.get_results(
                test_id=42,
                status_id=None,
                limit=None,
                offset=None,
            )

            mock_get.assert_called_once_with("get_results/42", params={})
            assert result == [{"id": 1, "status_id": 1}]

    def test_get_results_with_single_status_id(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results with a single integer status_id."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "status_id": 1}]

            results_api.get_results(test_id=42, status_id=1)

            expected_params = {"status_id": 1}
            mock_get.assert_called_once_with(
                "get_results/42", params=expected_params
            )

    def test_get_results_with_list_status_id(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results with a list of status IDs converted to CSV."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results(test_id=42, status_id=[1, 2, 5])

            expected_params = {"status_id": "1,2,5"}
            mock_get.assert_called_once_with(
                "get_results/42", params=expected_params
            )

    def test_get_results_with_pagination(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results with pagination parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results(test_id=42, limit=100, offset=50)

            expected_params = {"limit": 100, "offset": 50}
            mock_get.assert_called_once_with(
                "get_results/42", params=expected_params
            )

    def test_get_results_api_error(self, results_api: ResultsAPI) -> None:
        """Test get_results raises TestRailAPIError on API failure."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.get_results(test_id=42)

    def test_get_results_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results raises TestRailAuthenticationError on auth failure."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.get_results(test_id=42)

    def test_get_results_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results raises TestRailRateLimitError on rate limit."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.get_results(test_id=42)

    # -------------------------------------------------------------------------
    # add_result
    # -------------------------------------------------------------------------

    def test_add_result_minimal(self, results_api: ResultsAPI) -> None:
        """Test add_result with minimal required parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            result = results_api.add_result(test_id=101, status_id=1)

            expected_data = {"status_id": 1}
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_with_all_parameters(
        self, results_api: ResultsAPI, sample_result_data: dict
    ) -> None:
        """Test add_result with all optional parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = sample_result_data

            result = results_api.add_result(
                test_id=101,
                status_id=1,
                comment="Test passed successfully",
                version="1.0.0",
                elapsed="30s",
                defects="BUG-123",
                assignedto_id=1,
                custom_fields={"custom_automation_type": 2},
            )

            expected_data = {
                "status_id": 1,
                "comment": "Test passed successfully",
                "version": "1.0.0",
                "elapsed": "30s",
                "defects": "BUG-123",
                "assignedto_id": 1,
                "custom_automation_type": 2,
            }
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )
            assert result == sample_result_data

    def test_add_result_with_none_values(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result with None values for optional parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            result = results_api.add_result(
                test_id=101,
                status_id=1,
                comment=None,
                version=None,
                elapsed=None,
                defects=None,
                assignedto_id=None,
                custom_fields=None,
            )

            expected_data = {"status_id": 1}
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_with_custom_fields(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result merges custom_fields into the data payload."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            results_api.add_result(
                test_id=101,
                status_id=1,
                custom_fields={
                    "custom_automation_type": 2,
                    "custom_notes": "automated",
                },
            )

            expected_data = {
                "status_id": 1,
                "custom_automation_type": 2,
                "custom_notes": "automated",
            }
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )

    def test_add_result_custom_fields_override(
        self, results_api: ResultsAPI
    ) -> None:
        """Test that custom_fields can override built-in fields."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 999}

            results_api.add_result(
                test_id=101,
                status_id=1,
                custom_fields={"status_id": 999, "custom_field": "value"},
            )

            expected_data = {
                "status_id": 999,
                "custom_field": "value",
            }
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )

    def test_add_result_api_error(self, results_api: ResultsAPI) -> None:
        """Test add_result raises TestRailAPIError on API failure."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.add_result(test_id=101, status_id=1)

    def test_add_result_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result raises TestRailAuthenticationError on auth failure."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.add_result(test_id=101, status_id=1)

    def test_add_result_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result raises TestRailRateLimitError on rate limit."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.add_result(test_id=101, status_id=1)

    @pytest.mark.parametrize("status_id", [1, 2, 3, 4, 5])
    def test_add_result_different_status_ids(
        self, results_api: ResultsAPI, status_id: int
    ) -> None:
        """Test add_result with each standard TestRail status ID."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": status_id}

            result = results_api.add_result(test_id=101, status_id=status_id)

            expected_data = {"status_id": status_id}
            mock_post.assert_called_once_with(
                "add_result/101", data=expected_data
            )
            assert result["status_id"] == status_id

    def test_add_result_large_test_id(self, results_api: ResultsAPI) -> None:
        """Test add_result with a large test_id value."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            results_api.add_result(test_id=999999, status_id=1)

            mock_post.assert_called_once_with(
                "add_result/999999", data={"status_id": 1}
            )

    # -------------------------------------------------------------------------
    # add_result_for_case
    # -------------------------------------------------------------------------

    def test_add_result_for_case_minimal(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case with minimal required parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            result = results_api.add_result_for_case(
                run_id=1, case_id=123, status_id=1
            )

            expected_data = {"status_id": 1}
            mock_post.assert_called_once_with(
                "add_result_for_case/1/123", data=expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_for_case_with_all_parameters(
        self, results_api: ResultsAPI, sample_result_data: dict
    ) -> None:
        """Test add_result_for_case with all optional parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = sample_result_data

            result = results_api.add_result_for_case(
                run_id=1,
                case_id=123,
                status_id=1,
                comment="Test passed successfully",
                version="1.0.0",
                elapsed="30s",
                defects="BUG-123",
                assignedto_id=1,
                custom_fields={"custom_automation_type": 2},
            )

            expected_data = {
                "status_id": 1,
                "comment": "Test passed successfully",
                "version": "1.0.0",
                "elapsed": "30s",
                "defects": "BUG-123",
                "assignedto_id": 1,
                "custom_automation_type": 2,
            }
            mock_post.assert_called_once_with(
                "add_result_for_case/1/123", data=expected_data
            )
            assert result == sample_result_data

    def test_add_result_for_case_with_none_values(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case with None values for optional parameters."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            result = results_api.add_result_for_case(
                run_id=1,
                case_id=123,
                status_id=1,
                comment=None,
                version=None,
                elapsed=None,
                defects=None,
                assignedto_id=None,
                custom_fields=None,
            )

            expected_data = {"status_id": 1}
            mock_post.assert_called_once_with(
                "add_result_for_case/1/123", data=expected_data
            )
            assert result == {"id": 1, "status_id": 1}

    def test_add_result_for_case_with_custom_fields(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case merges custom_fields into the data payload."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            results_api.add_result_for_case(
                run_id=1,
                case_id=123,
                status_id=1,
                custom_fields={
                    "custom_automation_type": 2,
                    "custom_notes": "automated",
                },
            )

            expected_data = {
                "status_id": 1,
                "custom_automation_type": 2,
                "custom_notes": "automated",
            }
            mock_post.assert_called_once_with(
                "add_result_for_case/1/123", data=expected_data
            )

    def test_add_result_for_case_api_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case raises TestRailAPIError on API failure."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.add_result_for_case(
                    run_id=1, case_id=123, status_id=1
                )

    def test_add_result_for_case_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case raises TestRailAuthenticationError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.add_result_for_case(
                    run_id=1, case_id=123, status_id=1
                )

    def test_add_result_for_case_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case raises TestRailRateLimitError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.add_result_for_case(
                    run_id=1, case_id=123, status_id=1
                )

    def test_add_result_for_case_large_ids(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_result_for_case with large run_id and case_id values."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "status_id": 1}

            results_api.add_result_for_case(
                run_id=999999, case_id=999999, status_id=1
            )

            mock_post.assert_called_once_with(
                "add_result_for_case/999999/999999",
                data={"status_id": 1},
            )

    # -------------------------------------------------------------------------
    # add_results_for_cases
    # -------------------------------------------------------------------------

    def test_add_results_for_cases(self, results_api: ResultsAPI) -> None:
        """Test add_results_for_cases posts results list to correct endpoint."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = [{"id": 1}, {"id": 2}]

            results_data = [
                {"case_id": 1, "status_id": 1, "comment": "Passed"},
                {"case_id": 2, "status_id": 5, "comment": "Failed"},
            ]

            result = results_api.add_results_for_cases(
                run_id=1, results=results_data
            )

            expected_data = {"results": results_data}
            mock_post.assert_called_once_with(
                "add_results_for_cases/1", data=expected_data
            )
            assert result == [{"id": 1}, {"id": 2}]

    def test_add_results_for_cases_empty_list(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results_for_cases with an empty results list."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = []

            result = results_api.add_results_for_cases(run_id=1, results=[])

            mock_post.assert_called_once_with(
                "add_results_for_cases/1", data={"results": []}
            )
            assert result == []

    def test_add_results_for_cases_api_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results_for_cases raises TestRailAPIError on failure."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.add_results_for_cases(run_id=1, results=[])

    def test_add_results_for_cases_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results_for_cases raises TestRailAuthenticationError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.add_results_for_cases(run_id=1, results=[])

    def test_add_results_for_cases_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results_for_cases raises TestRailRateLimitError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.add_results_for_cases(run_id=1, results=[])

    # -------------------------------------------------------------------------
    # get_results_for_case
    # -------------------------------------------------------------------------

    def test_get_results_for_case(self, results_api: ResultsAPI) -> None:
        """Test get_results_for_case retrieves results for a case in a run."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "status_id": 1, "case_id": 123},
                {"id": 2, "status_id": 5, "case_id": 123},
            ]

            result = results_api.get_results_for_case(run_id=1, case_id=123)

            mock_get.assert_called_once_with("get_results_for_case/1/123")
            assert result == [
                {"id": 1, "status_id": 1, "case_id": 123},
                {"id": 2, "status_id": 5, "case_id": 123},
            ]

    def test_get_results_for_case_api_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_case raises TestRailAPIError on failure."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.get_results_for_case(run_id=1, case_id=123)

    def test_get_results_for_case_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_case raises TestRailAuthenticationError."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.get_results_for_case(run_id=1, case_id=123)

    def test_get_results_for_case_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_case raises TestRailRateLimitError."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.get_results_for_case(run_id=1, case_id=123)

    def test_get_results_for_case_large_ids(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_case with large run_id and case_id values."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = []

            results_api.get_results_for_case(run_id=999999, case_id=999999)

            mock_get.assert_called_once_with(
                "get_results_for_case/999999/999999"
            )

    # -------------------------------------------------------------------------
    # get_results_for_run
    # -------------------------------------------------------------------------

    def test_get_results_for_run_minimal(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with minimal required parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5},
            ]

            result = results_api.get_results_for_run(run_id=1)

            mock_get.assert_called_once_with(
                "get_results_for_run/1", params={}
            )
            assert result == [
                {"id": 1, "status_id": 1},
                {"id": 2, "status_id": 5},
            ]

    def test_get_results_for_run_with_all_parameters(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with all optional parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "status_id": 1}]

            result = results_api.get_results_for_run(
                run_id=1,
                status_id=[1, 5],
                created_after=1000000,
                created_before=2000000,
                created_by=[1, 2],
                defects_filter="TR-123",
                limit=50,
                offset=10,
            )

            expected_params = {
                "status_id": "1,5",
                "created_after": 1000000,
                "created_before": 2000000,
                "created_by": "1,2",
                "defects_filter": "TR-123",
                "limit": 50,
                "offset": 10,
            }
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )
            assert result == [{"id": 1, "status_id": 1}]

    def test_get_results_for_run_with_none_values(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with None values for optional parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = []

            results_api.get_results_for_run(
                run_id=1,
                status_id=None,
                created_after=None,
                created_before=None,
                created_by=None,
                defects_filter=None,
                limit=None,
                offset=None,
            )

            mock_get.assert_called_once_with(
                "get_results_for_run/1", params={}
            )

    def test_get_results_for_run_with_single_status_id(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with a single integer status_id."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "status_id": 1}]

            results_api.get_results_for_run(run_id=1, status_id=1)

            expected_params = {"status_id": 1}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_list_status_id(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run converts list status_id to CSV string."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(run_id=1, status_id=[1, 5])

            expected_params = {"status_id": "1,5"}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_single_created_by(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with a single integer created_by."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(run_id=1, created_by=1)

            expected_params = {"created_by": 1}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_list_created_by(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run converts list created_by to CSV string."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(run_id=1, created_by=[1, 2])

            expected_params = {"created_by": "1,2"}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_timestamp_filters(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with created_after and created_before."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(
                run_id=1,
                created_after=1000000,
                created_before=2000000,
            )

            expected_params = {
                "created_after": 1000000,
                "created_before": 2000000,
            }
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_pagination(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with pagination parameters."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(run_id=1, limit=100, offset=50)

            expected_params = {"limit": 100, "offset": 50}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_with_defects_filter(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run with defects_filter parameter."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            results_api.get_results_for_run(run_id=1, defects_filter="TR-123")

            expected_params = {"defects_filter": "TR-123"}
            mock_get.assert_called_once_with(
                "get_results_for_run/1", params=expected_params
            )

    def test_get_results_for_run_api_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run raises TestRailAPIError on failure."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.get_results_for_run(run_id=1)

    def test_get_results_for_run_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run raises TestRailAuthenticationError."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.get_results_for_run(run_id=1)

    def test_get_results_for_run_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test get_results_for_run raises TestRailRateLimitError."""
        with patch.object(results_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.get_results_for_run(run_id=1)

    # -------------------------------------------------------------------------
    # add_results
    # -------------------------------------------------------------------------

    def test_add_results(self, results_api: ResultsAPI) -> None:
        """Test add_results posts results list to the correct endpoint."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = [{"id": 1}, {"id": 2}]

            results_data = [
                {"test_id": 101, "status_id": 1},
                {"test_id": 102, "status_id": 5},
            ]

            result = results_api.add_results(run_id=1, results=results_data)

            expected_data = {"results": results_data}
            mock_post.assert_called_once_with(
                "add_results/1", data=expected_data
            )
            assert result == [{"id": 1}, {"id": 2}]

    def test_add_results_empty_list(self, results_api: ResultsAPI) -> None:
        """Test add_results with an empty results list."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = []

            result = results_api.add_results(run_id=1, results=[])

            mock_post.assert_called_once_with(
                "add_results/1", data={"results": []}
            )
            assert result == []

    def test_add_results_api_error(self, results_api: ResultsAPI) -> None:
        """Test add_results raises TestRailAPIError on API failure."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                results_api.add_results(run_id=1, results=[])

    def test_add_results_authentication_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results raises TestRailAuthenticationError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                results_api.add_results(run_id=1, results=[])

    def test_add_results_rate_limit_error(
        self, results_api: ResultsAPI
    ) -> None:
        """Test add_results raises TestRailRateLimitError."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                results_api.add_results(run_id=1, results=[])

    def test_add_results_large_run_id(self, results_api: ResultsAPI) -> None:
        """Test add_results with a large run_id value."""
        with patch.object(results_api, "_post") as mock_post:
            mock_post.return_value = []

            results_api.add_results(run_id=999999, results=[])

            mock_post.assert_called_once_with(
                "add_results/999999", data={"results": []}
            )
