"""
This module provides functionality for managing priorities in TestRail.
Priorities are used to indicate the importance of test cases.
"""

from typing import Any

from .base import BaseAPI


class PrioritiesAPI(BaseAPI):
    """
    API for managing TestRail priorities.
    """

    def get_priorities(self) -> list[dict[str, Any]] | None:
        """
        Get all available priorities.

        Returns:
            list: List of priorities if successful, None otherwise.
        """
        return self._api_request("GET", "get_priorities")
