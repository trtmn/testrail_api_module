"""
This module provides functionality for managing custom result fields in TestRail.
It allows you to retrieve custom fields for test results.
"""

from typing import Dict, Any, List
from .base import BaseAPI

class ResultFieldsAPI(BaseAPI):
    """API for managing custom result fields in TestRail."""

    def get_result_field(self, field_id: int) -> Dict[str, Any]:
        """
        Get a specific custom result field.

        Args:
            field_id: The ID of the custom result field.

        Returns:
            Dict containing the custom result field data.
        """
        return self._api_request('GET', f'get_result_field/{field_id}')

    def get_result_fields(self) -> List[Dict[str, Any]]:
        """
        Get all custom result fields.

        Returns:
            List of dictionaries containing custom result field data.
        """
        return self._api_request('GET', 'get_result_fields')