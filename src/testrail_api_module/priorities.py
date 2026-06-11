"""
This module provides functionality for managing priorities in TestRail.
Priorities are used to indicate the importance of test cases.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["PrioritiesAPI"]


class PrioritiesAPI(BaseAPI):
    """
    API for managing TestRail priorities.

    This class provides methods to retrieve the available priority
    levels configured in TestRail.
    """

    def get_priorities(self) -> list[dict[str, Any]]:
        """
        Get all available priorities.

        Returns:
            List of dictionaries containing priority data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get("get_priorities")
