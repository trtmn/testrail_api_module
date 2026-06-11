"""
This module provides functionality for managing custom result fields
in TestRail. It allows you to retrieve the custom fields configured
for test results.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["ResultFieldsAPI"]


class ResultFieldsAPI(BaseAPI):
    """
    API for managing custom result fields in TestRail.

    This class provides methods to retrieve the custom fields
    available for test results.
    """

    def get_result_fields(self) -> list[dict[str, Any]]:
        """
        Get all custom result fields.

        Returns:
            List of dictionaries containing custom result field data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get("get_result_fields")
