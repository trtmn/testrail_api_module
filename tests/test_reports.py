"""
Tests for the ReportsAPI module.

This module contains comprehensive tests for all methods in the ReportsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.reports import ReportsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestReportsAPI:
    """Test suite for ReportsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def reports_api(self, mock_client: Mock) -> ReportsAPI:
        """Create a ReportsAPI instance with mocked client."""
        return ReportsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test ReportsAPI initialization."""
        api = ReportsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_report(self, reports_api: ReportsAPI) -> None:
        """Test get_report method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test Report"}

            result = reports_api.get_report(report_id=1)

            mock_request.assert_called_once_with('GET', 'get_report/1')
            assert result == {"id": 1, "name": "Test Report"}

    def test_get_reports(self, reports_api: ReportsAPI) -> None:
        """Test get_reports method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Report 1"},
                {"id": 2, "name": "Report 2"}
            ]

            result = reports_api.get_reports(project_id=1)

            mock_request.assert_called_once_with('GET', 'get_reports/1')
            assert len(result) == 2

    def test_add_report_minimal(self, reports_api: ReportsAPI) -> None:
        """Test add_report with minimal required parameters."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Report"}

            result = reports_api.add_report(project_id=1, name="New Report")

            expected_data = {
                "name": "New Report",
                "report_type": "test_case"
            }
            mock_request.assert_called_once_with(
                'POST', 'add_report/1', data=expected_data)
            assert result == {"id": 1, "name": "New Report"}

    def test_add_report_with_all_parameters(
            self, reports_api: ReportsAPI) -> None:
        """Test add_report with all optional parameters."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Report"}

            parameters = {
                "suite_id": 1,
                "section_id": 2,
                "case_ids": [1, 2, 3]
            }

            reports_api.add_report(
                project_id=1,
                name="New Report",
                description="Report description",
                report_type="test_case",
                parameters=parameters
            )

            expected_data = {
                "name": "New Report",
                "report_type": "test_case",
                "description": "Report description",
                "parameters": parameters
            }
            mock_request.assert_called_once_with(
                'POST', 'add_report/1', data=expected_data)

    def test_update_report(self, reports_api: ReportsAPI) -> None:
        """Test update_report method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Report"}

            reports_api.update_report(
                report_id=1,
                name="Updated Report",
                description="Updated description"
            )

            expected_data = {
                "name": "Updated Report",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with(
                'POST', 'update_report/1', data=expected_data)

    def test_delete_report(self, reports_api: ReportsAPI) -> None:
        """Test delete_report method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {}

            result = reports_api.delete_report(report_id=1)

            mock_request.assert_called_once_with('POST', 'delete_report/1')
            assert result == {}

    def test_run_report(self, reports_api: ReportsAPI) -> None:
        """Test run_report method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {"status": "completed", "results": {}}

            result = reports_api.run_report(report_id=1)

            mock_request.assert_called_once_with('POST', 'run_report/1')
            assert result["status"] == "completed"

    def test_get_report_results(self, reports_api: ReportsAPI) -> None:
        """Test get_report_results method."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "total": 100,
                "passed": 80,
                "failed": 20
            }

            result = reports_api.get_report_results(report_id=1)

            mock_request.assert_called_once_with('GET', 'get_report_results/1')
            assert result["total"] == 100

    def test_api_request_failure(self, reports_api: ReportsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                reports_api.get_report(report_id=1)

    def test_authentication_error(self, reports_api: ReportsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed")

            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                reports_api.get_report(report_id=1)

    def test_rate_limit_error(self, reports_api: ReportsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(reports_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded")

            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                reports_api.get_report(report_id=1)
