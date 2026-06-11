"""
This module provides functionality for managing statuses in TestRail.
Statuses are used to track the state of test cases and test results.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["StatusesAPI"]


class StatusesAPI(BaseAPI):
    """
    API for managing TestRail statuses.

    This class provides methods to retrieve the available test result
    and case statuses configured in TestRail.
    """

    def get_statuses(self) -> list[dict[str, Any]]:
        """
        Get all available test result statuses.

        Returns:
            List of dictionaries containing status data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> statuses = api.statuses.get_statuses()
        """
        return self._get("get_statuses")

    def get_case_statuses(self) -> list[dict[str, Any]]:
        """
        Get all available case statuses.

        Requires TestRail Enterprise 7.3+.

        Returns:
            List of dictionaries containing case status data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> case_statuses = api.statuses.get_case_statuses()
        """
        return self._get("get_case_statuses")
