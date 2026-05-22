"""
This module provides functionality for managing projects in TestRail.
Projects are the top-level containers for test cases, suites, and
other test management entities.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["ProjectsAPI"]


class ProjectsAPI(BaseAPI):
    """
    API for managing TestRail projects.

    This class provides methods to create, read, update, and delete
    projects in TestRail, following the official TestRail API patterns.
    """

    def get_project(self, project_id: int) -> dict[str, Any]:
        """
        Get a project by ID.

        Args:
            project_id: The ID of the project to retrieve.

        Returns:
            Dict containing the project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_project/{project_id}")

    def get_projects(self) -> list[dict[str, Any]]:
        """
        Get all projects.

        Returns:
            List of dictionaries containing project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", "get_projects")

    def add_project(
        self,
        name: str,
        announcement: str | None = None,
        show_announcement: bool = False,
        is_completed: bool = False,
    ) -> dict[str, Any]:
        """
        Add a new project.

        Args:
            name: The name of the project.
            announcement: Optional announcement text for the project.
            show_announcement: Whether to show the announcement.
            is_completed: Whether the project is completed.

        Returns:
            Dict containing the created project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {
            "name": name,
            "show_announcement": show_announcement,
            "is_completed": is_completed,
        }
        if announcement:
            data["announcement"] = announcement

        return self._api_request("POST", "add_project", data=data)

    def update_project(self, project_id: int, **kwargs: Any) -> dict[str, Any]:
        """
        Update a project.

        Args:
            project_id: The ID of the project to update.
            **kwargs: Fields to update (name, announcement,
                show_announcement, is_completed).

        Returns:
            Dict containing the updated project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request(
            "POST", f"update_project/{project_id}", data=kwargs
        )

    def delete_project(self, project_id: int) -> dict[str, Any]:
        """
        Delete a project.

        Args:
            project_id: The ID of the project to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("POST", f"delete_project/{project_id}")
