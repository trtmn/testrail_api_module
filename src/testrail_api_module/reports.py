"""
This module provides functionality for managing reports in TestRail.
Reports are used to analyze and visualize test results and metrics.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["ReportsAPI"]


class ReportsAPI(BaseAPI):
    """
    API for managing TestRail reports.

    This class provides methods to retrieve and run reports for
    analyzing test results and project metrics.
    """

    def get_reports(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all reports for a project.

        Args:
            project_id: The ID of the project to get reports for.

        Returns:
            List of dictionaries containing report data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_reports/{project_id}")

    def run_report(self, report_template_id: int) -> dict[str, Any]:
        """
        Run a report to generate results.

        The TestRail API requires POST for this endpoint. Returns URLs
        to the generated report in HTML and PDF formats.

        Args:
            report_template_id: The ID of the report template to run.

        Returns:
            Dict containing the report results including URLs to the
            generated report.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"run_report/{report_template_id}", data={})
