"""
This module provides functionality for managing custom result fields in TestRail.
It allows you to retrieve custom fields for test results.
"""

from typing import Any

from .base import BaseAPI


class ResultFieldsAPI(BaseAPI):
    """API for managing custom result fields in TestRail."""

    def get_result_fields(self) -> list[dict[str, Any]]:
        """
        Get all custom result fields.

        Returns:
            List of dictionaries containing custom result field data.
        """
        return self._api_request("GET", "get_result_fields")
