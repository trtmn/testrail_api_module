"""
This module provides functionality for managing statuses in TestRail.
Statuses are used to track the state of test cases and test results.
"""

from typing import Any

from .base import BaseAPI


class StatusesAPI(BaseAPI):
    """
    API for managing TestRail statuses.
    """

    def get_statuses(self) -> list[dict[str, Any]] | None:
        """
        Get all available statuses.

        Returns:
            list: List of statuses if successful, None otherwise.
        """
        return self._api_request("GET", "get_statuses")

    def get_case_statuses(self) -> list[dict[str, Any]] | None:
        """
        Get all available case statuses.

        Requires TestRail Enterprise 7.3+.

        Returns:
            List of case status dicts if successful, None otherwise.
        """
        return self._api_request("GET", "get_case_statuses")
