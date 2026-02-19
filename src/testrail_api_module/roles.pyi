from typing import Any

from .base import BaseAPI as BaseAPI

class RolesAPI(BaseAPI):
    """
    API for managing TestRail roles.
    """
    def get_roles(self) -> list[dict[str, Any]] | None:
        """
        Get all roles.

        Returns:
            list: List of roles if successful, None otherwise.
        """
