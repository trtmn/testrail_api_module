from typing import Any

from .base import BaseAPI as BaseAPI

class ResultFieldsAPI(BaseAPI):
    """API for managing custom result fields in TestRail."""
    def get_result_fields(self) -> list[dict[str, Any]]:
        """
        Get all custom result fields.

        Returns:
            List of dictionaries containing custom result field data.
        """
