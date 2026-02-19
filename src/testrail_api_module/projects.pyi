from typing import Any

from .base import BaseAPI as BaseAPI

class ProjectsAPI(BaseAPI):
    """
    API for managing TestRail projects.
    """
    def get_project(self, project_id: int) -> dict[str, Any] | None:
        """
        Get a project by ID.

        Args:
            project_id (int): The ID of the project to retrieve.

        Returns:
            dict: The project data if successful, None otherwise.
        """
    def get_projects(self) -> list[dict[str, Any]] | None:
        """
        Get all projects.

        Returns:
            list: List of projects if successful, None otherwise.
        """
    def add_project(
        self,
        name: str,
        announcement: str | None = None,
        show_announcement: bool = False,
        is_completed: bool = False,
    ) -> dict[str, Any] | None:
        """
        Add a new project.

        Args:
            name (str): The name of the project.
            announcement (str, optional): The announcement text for the project.
            show_announcement (bool, optional): Whether to show the announcement.
            is_completed (bool, optional): Whether the project is completed.

        Returns:
            dict: The created project data if successful, None otherwise.
        """
    def update_project(
        self, project_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a project.

        Args:
            project_id (int): The ID of the project to update.
            **kwargs: The fields to update (name, announcement, show_announcement, is_completed).

        Returns:
            dict: The updated project data if successful, None otherwise.
        """
    def delete_project(self, project_id: int) -> dict[str, Any] | None:
        """
        Delete a project.

        Args:
            project_id (int): The ID of the project to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
