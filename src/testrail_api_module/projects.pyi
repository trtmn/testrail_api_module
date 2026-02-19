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
    def get_project_stats(self, project_id: int) -> dict[str, Any] | None:
        """
        Get statistics for a project.

        Args:
            project_id (int): The ID of the project to get statistics for.

        Returns:
            dict: The project statistics if successful, None otherwise.
        """
    def get_project_activity(
        self, project_id: int
    ) -> list[dict[str, Any]] | None:
        """
        Get the activity log for a project.

        Args:
            project_id (int): The ID of the project to get activity for.

        Returns:
            list: List of activity entries if successful, None otherwise.
        """
    def get_project_attachments(
        self, project_id: int
    ) -> list[dict[str, Any]] | None:
        """
        Get all attachments for a project.

        Args:
            project_id (int): The ID of the project to get attachments for.

        Returns:
            list: List of attachments if successful, None otherwise.
        """
    def add_project_attachment(
        self, project_id: int, file_path: str, description: str | None = None
    ) -> dict[str, Any] | None:
        """
        Add an attachment to a project.

        Args:
            project_id (int): The ID of the project to add the attachment to.
            file_path (str): The path to the file to attach.
            description (str, optional): The description of the attachment.

        Returns:
            dict: The response data if successful, None otherwise.
        """
