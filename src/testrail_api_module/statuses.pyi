from typing import Any

from .base import BaseAPI as BaseAPI

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
    def get_case_statuses(self) -> list[dict[str, Any]] | None:
        """Get all available case statuses. Requires TestRail Enterprise 7.3+."""
