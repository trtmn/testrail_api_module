"""
Tests for the ReportsAPI module.

This module contains comprehensive tests for all methods in the ReportsAPI class,
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
from testrail_api_module.reports import ReportsAPI

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

    @pytest.fixture
    def sample_report_data(self) -> dict:
        """Sample report data for testing."""
        return {
            "id": 1,
            "name": "Test Report",
            "description": "A test report",
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test ReportsAPI initialization."""
        api = ReportsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    # --- get_reports ---

    def test_get_reports(self, reports_api: ReportsAPI) -> None:
        """Test get_reports returns list of reports for a project."""
        with patch.object(reports_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Report 1"},
                {"id": 2, "name": "Report 2"},
            ]

            result = reports_api.get_reports(project_id=1)

            mock_get.assert_called_once_with("get_reports/1")
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["name"] == "Report 2"

    def test_get_reports_empty(self, reports_api: ReportsAPI) -> None:
        """Test get_reports with no reports for a project."""
        with patch.object(reports_api, "_get") as mock_get:
            mock_get.return_value = []

            result = reports_api.get_reports(project_id=99)

            mock_get.assert_called_once_with("get_reports/99")
            assert result == []

    def test_get_reports_api_error(self, reports_api: ReportsAPI) -> None:
        """Test get_reports raises TestRailAPIError on failure."""
        with patch.object(reports_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                reports_api.get_reports(project_id=1)

    def test_get_reports_authentication_error(
        self, reports_api: ReportsAPI
    ) -> None:
        """Test get_reports raises TestRailAuthenticationError on 401."""
        with patch.object(reports_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                reports_api.get_reports(project_id=1)

    def test_get_reports_rate_limit_error(
        self, reports_api: ReportsAPI
    ) -> None:
        """Test get_reports raises TestRailRateLimitError on 429."""
        with patch.object(reports_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                reports_api.get_reports(project_id=1)

    # --- run_report ---

    def test_run_report(self, reports_api: ReportsAPI) -> None:
        """Test run_report uses POST and returns report result URLs."""
        expected = {
            "url": "https://example.testrail.io/reports/1.html",
            "url_pdf": "https://example.testrail.io/reports/1.pdf",
        }
        with patch.object(reports_api, "_post") as mock_post:
            mock_post.return_value = expected

            result = reports_api.run_report(report_template_id=1)

            mock_post.assert_called_once_with("run_report/1", data={})
            assert result == expected

    def test_run_report_different_id(self, reports_api: ReportsAPI) -> None:
        """Test run_report with a different report template ID."""
        with patch.object(reports_api, "_post") as mock_post:
            mock_post.return_value = {
                "url": "https://example.testrail.io/reports/42.html"
            }

            result = reports_api.run_report(report_template_id=42)

            mock_post.assert_called_once_with("run_report/42", data={})
            assert "url" in result

    def test_run_report_api_error(self, reports_api: ReportsAPI) -> None:
        """Test run_report raises TestRailAPIError on failure."""
        with patch.object(reports_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                reports_api.run_report(report_template_id=1)

    def test_run_report_authentication_error(
        self, reports_api: ReportsAPI
    ) -> None:
        """Test run_report raises TestRailAuthenticationError on 401."""
        with patch.object(reports_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                reports_api.run_report(report_template_id=1)

    def test_run_report_rate_limit_error(
        self, reports_api: ReportsAPI
    ) -> None:
        """Test run_report raises TestRailRateLimitError on 429."""
        with patch.object(reports_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                reports_api.run_report(report_template_id=1)
