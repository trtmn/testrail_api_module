"""
This module provides functionality for managing roles in TestRail.
Roles are used to define user permissions and access levels.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["RolesAPI"]


class RolesAPI(BaseAPI):
    """
    API for managing TestRail roles.

    This class provides methods to retrieve the available user roles
    and their permission settings in TestRail.
    """

    def get_roles(self) -> list[dict[str, Any]]:
        """
        Get all roles.

        Returns:
            List of dictionaries containing role data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get("get_roles")
