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
        return self._api_request("GET", f"get_reports/{project_id}")

    def run_report(self, report_id: int) -> dict[str, Any]:
        """
        Run a report to generate results.

        Args:
            report_id: The ID of the report to run.

        Returns:
            Dict containing the report results.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("POST", f"run_report/{report_id}")
