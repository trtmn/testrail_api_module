from typing import Any

from .base import BaseAPI as BaseAPI

class MilestonesAPI(BaseAPI):
    """
    API for managing TestRail milestones.
    """
    def get_milestone(self, milestone_id: int) -> dict[str, Any] | None:
        """
        Get a milestone by ID.

        Args:
            milestone_id (int): The ID of the milestone to retrieve.

        Returns:
            dict: The milestone data if successful, None otherwise.
        """
    def get_milestones(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all milestones for a project.

        Args:
            project_id (int): The ID of the project to get milestones for.

        Returns:
            list: List of milestones if successful, None otherwise.
        """
    def add_milestone(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        due_on: str | None = None,
        parent_id: int | None = None,
        start_on: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Add a new milestone.

        Args:
            project_id (int): The ID of the project to add the milestone to.
            name (str): The name of the milestone.
            description (str, optional): The description of the milestone.
            due_on (str, optional): The due date of the milestone (ISO 8601 format).
            parent_id (int, optional): The ID of the parent milestone.
            start_on (str, optional): The start date of the milestone (ISO 8601 format).

        Returns:
            dict: The created milestone data if successful, None otherwise.
        """
    def update_milestone(
        self, milestone_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a milestone.

        Args:
            milestone_id (int): The ID of the milestone to update.
            **kwargs: The fields to update (name, description, due_on, parent_id, start_on).

        Returns:
            dict: The updated milestone data if successful, None otherwise.
        """
    def delete_milestone(self, milestone_id: int) -> dict[str, Any] | None:
        """
        Delete a milestone.

        Args:
            milestone_id (int): The ID of the milestone to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
