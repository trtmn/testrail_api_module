from typing import Any

from .base import BaseAPI as BaseAPI

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
