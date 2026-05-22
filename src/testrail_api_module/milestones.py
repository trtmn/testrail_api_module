"""
This module provides functionality for managing milestones in TestRail.
Milestones are used to track project progress and organize test runs.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["MilestonesAPI"]


class MilestonesAPI(BaseAPI):
    """
    API for managing TestRail milestones.

    This class provides methods to create, read, update, and delete
    milestones in TestRail, following the official TestRail API
    patterns.
    """

    def get_milestone(self, milestone_id: int) -> dict[str, Any]:
        """
        Get a milestone by ID.

        Args:
            milestone_id: The ID of the milestone to retrieve.

        Returns:
            Dict containing the milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_milestone/{milestone_id}")

    def get_milestones(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all milestones for a project.

        Args:
            project_id: The ID of the project to get milestones for.

        Returns:
            List of dictionaries containing milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_milestones/{project_id}")

    def add_milestone(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        due_on: str | None = None,
        parent_id: int | None = None,
        start_on: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new milestone.

        Args:
            project_id: The ID of the project to add the milestone
                to.
            name: The name of the milestone.
            description: Optional description of the milestone.
            due_on: Optional due date (ISO 8601 format).
            parent_id: Optional ID of the parent milestone.
            start_on: Optional start date (ISO 8601 format).

        Returns:
            Dict containing the created milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}
        if description:
            data["description"] = description
        if due_on:
            data["due_on"] = due_on
        if parent_id:
            data["parent_id"] = parent_id
        if start_on:
            data["start_on"] = start_on

        return self._api_request(
            "POST", f"add_milestone/{project_id}", data=data
        )

    def update_milestone(
        self, milestone_id: int, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Update a milestone.

        Args:
            milestone_id: The ID of the milestone to update.
            **kwargs: Fields to update (name, description, due_on,
                parent_id, start_on).

        Returns:
            Dict containing the updated milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request(
            "POST",
            f"update_milestone/{milestone_id}",
            data=kwargs,
        )

    def delete_milestone(self, milestone_id: int) -> dict[str, Any]:
        """
        Delete a milestone.

        Args:
            milestone_id: The ID of the milestone to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("POST", f"delete_milestone/{milestone_id}")
