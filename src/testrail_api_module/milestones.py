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
        return self._get(f"get_milestone/{milestone_id}")

    def get_milestones(
        self,
        project_id: int,
        is_completed: bool | None = None,
        is_started: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all milestones for a project.

        Args:
            project_id: The ID of the project to get milestones for.
            is_completed: Optional filter to return only completed or
                active milestones.
            is_started: Optional filter to return only started or
                not-yet-started milestones.

        Returns:
            List of dictionaries containing milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if is_completed is not None:
            params["is_completed"] = is_completed
        if is_started is not None:
            params["is_started"] = is_started
        return self._get(f"get_milestones/{project_id}", params=params)

    def add_milestone(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        due_on: int | None = None,
        parent_id: int | None = None,
        refs: str | None = None,
        start_on: int | None = None,
    ) -> dict[str, Any]:
        """
        Add a new milestone.

        Args:
            project_id: The ID of the project to add the milestone
                to.
            name: The name of the milestone.
            description: Optional description of the milestone.
            due_on: Optional due date as a UNIX timestamp.
            parent_id: Optional ID of the parent milestone.
            refs: Optional comma-separated list of references.
            start_on: Optional start date as a UNIX timestamp.

        Returns:
            Dict containing the created milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}
        if description is not None:
            data["description"] = description
        if due_on is not None:
            data["due_on"] = due_on
        if parent_id is not None:
            data["parent_id"] = parent_id
        if refs is not None:
            data["refs"] = refs
        if start_on is not None:
            data["start_on"] = start_on

        return self._post(f"add_milestone/{project_id}", data=data)

    def update_milestone(
        self,
        milestone_id: int,
        name: str | None = None,
        description: str | None = None,
        due_on: int | None = None,
        is_completed: bool | None = None,
        is_started: bool | None = None,
        parent_id: int | None = None,
        refs: str | None = None,
        start_on: int | None = None,
    ) -> dict[str, Any]:
        """
        Update a milestone.

        Args:
            milestone_id: The ID of the milestone to update.
            name: Optional new name for the milestone.
            description: Optional description of the milestone.
            due_on: Optional due date as a UNIX timestamp.
            is_completed: Whether the milestone is completed.
            is_started: Whether the milestone has been started.
            parent_id: Optional ID of the parent milestone.
            refs: Optional comma-separated list of references.
            start_on: Optional start date as a UNIX timestamp.

        Returns:
            Dict containing the updated milestone data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if due_on is not None:
            data["due_on"] = due_on
        if is_completed is not None:
            data["is_completed"] = is_completed
        if is_started is not None:
            data["is_started"] = is_started
        if parent_id is not None:
            data["parent_id"] = parent_id
        if refs is not None:
            data["refs"] = refs
        if start_on is not None:
            data["start_on"] = start_on

        return self._post(
            f"update_milestone/{milestone_id}",
            data=data,
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
        return self._post(f"delete_milestone/{milestone_id}")
