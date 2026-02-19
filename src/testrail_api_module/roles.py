"""
This module provides functionality for managing roles in TestRail.
Roles are used to define user permissions and access levels.
"""

from typing import Any

from .base import BaseAPI


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
        return self._api_request("GET", "get_roles")
