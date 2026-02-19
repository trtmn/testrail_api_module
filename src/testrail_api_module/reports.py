"""
This module provides functionality for managing reports in TestRail.
Reports are used to analyze and visualize test results and metrics.
"""

from typing import Any

from .base import BaseAPI


class ReportsAPI(BaseAPI):
    """
    API for managing TestRail reports.
    """

    def get_reports(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all reports for a project.

        Args:
            project_id (int): The ID of the project to get reports for.

        Returns:
            list: List of reports if successful, None otherwise.
        """
        return self._api_request("GET", f"get_reports/{project_id}")

    def run_report(self, report_id: int) -> dict[str, Any] | None:
        """
        Run a report to generate results.

        Args:
            report_id (int): The ID of the report to run.

        Returns:
            dict: The report results if successful, None otherwise.
        """
        return self._api_request("POST", f"run_report/{report_id}")
