"""
This module provides functionality for managing user groups in
TestRail. Groups are instance-level collections of users (requires
TestRail 7.5 or later).
"""

from typing import Any

from .base import BaseAPI

__all__ = ["GroupsAPI"]


class GroupsAPI(BaseAPI):
    """
    API for managing TestRail user groups.

    This class provides methods to create, read, update, and delete
    user groups in TestRail, following the official TestRail API
    patterns. Groups are instance-level (not project-scoped) and
    require TestRail 7.5 or later.
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

    def get_groups(self) -> list[dict[str, Any]]:
        """
        Get all groups on the TestRail instance.

        Returns:
            List of dictionaries containing group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> groups = api.groups.get_groups()
            >>> for group in groups:
            ...     print(f"Group: {group['name']}")
        """
        return self._get("get_groups")

    def add_group(
        self, name: str, user_ids: list[int] | None = None
    ) -> dict[str, Any]:
        """
        Add a new group.

        Args:
            name: The name of the group.
            user_ids: Optional list of user IDs to add as members of
                the group.

        Returns:
            Dict containing the created group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> group = api.groups.add_group(
            ...     name="Test Group",
            ...     user_ids=[1, 2, 3]
            ... )
        """
        data: dict[str, Any] = {"name": name}
        if user_ids is not None:
            data["user_ids"] = user_ids

        return self._post("add_group", data=data)

    def update_group(
        self,
        group_id: int,
        name: str | None = None,
        user_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        Update a group.

        Args:
            group_id: The ID of the group to update.
            name: Optional new name for the group.
            user_ids: Optional full list of user IDs for the group.
                TestRail replaces the group's membership with this
                list, so always pass the complete member list.

        Returns:
            Dict containing the updated group data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> updated_group = api.groups.update_group(
            ...     group_id=123,
            ...     name="Updated Group Name",
            ...     user_ids=[1, 2, 3]
            ... )
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if user_ids is not None:
            data["user_ids"] = user_ids

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
