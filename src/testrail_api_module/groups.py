"""
This module provides functionality for managing groups in TestRail.
Groups are used to organize test cases and test suites.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["GroupsAPI"]


class GroupsAPI(BaseAPI):
    """
    API for managing TestRail groups.

    This class provides methods to create, read, update, and delete groups
    in TestRail, following the official TestRail API patterns.
    """

    def get_group(self, group_id: int) -> dict[str, Any]:
        """
        Get a group by ID.

        Args:
            group_id: The ID of the group to retrieve.

        Returns:
            Dict containing the group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> group = api.groups.get_group(123)
            >>> print(group['name'])
        """
        return self._get(f"get_group/{group_id}")

    def get_groups(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all groups for a project.

        Args:
            project_id: The ID of the project to get groups for.

        Returns:
            List of dictionaries containing group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> groups = api.groups.get_groups(project_id=1)
            >>> for group in groups:
            ...     print(f"Group: {group['name']}")
        """
        return self._get(f"get_groups/{project_id}")

    def add_group(
        self, project_id: int, name: str, description: str | None = None
    ) -> dict[str, Any]:
        """
        Add a new group.

        Args:
            project_id: The ID of the project to add the group to.
            name: The name of the group.
            description: Optional description of the group.

        Returns:
            Dict containing the created group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> group = api.groups.add_group(
            ...     project_id=1,
            ...     name="Test Group",
            ...     description="A test group for organizing cases"
            ... )
        """
        data = {"name": name}
        if description:
            data["description"] = description

        return self._post(f"add_group/{project_id}", data=data)

    def update_group(
        self,
        group_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Update a group.

        Args:
            group_id: The ID of the group to update.
            name: Optional new name for the group.
            description: Optional new description for the group.

        Returns:
            Dict containing the updated group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> updated_group = api.groups.update_group(
            ...     group_id=123,
            ...     name="Updated Group Name"
            ... )
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        return self._post(f"update_group/{group_id}", data=data)

    def delete_group(self, group_id: int) -> dict[str, Any]:
        """
        Delete a group.

        Args:
            group_id: The ID of the group to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> result = api.groups.delete_group(123)
        """
        return self._post(f"delete_group/{group_id}")

