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
        return self._get(f"get_project/{project_id}")

    def get_projects(
        self,
        is_completed: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all projects.

        Args:
            is_completed: Optional filter to return only completed or
                active projects.

        Returns:
            List of dictionaries containing project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if is_completed is not None:
            params["is_completed"] = is_completed
        return self._get("get_projects", params=params)

    def add_project(
        self,
        name: str,
        announcement: str | None = None,
        show_announcement: bool | None = None,
        suite_mode: int | None = None,
    ) -> dict[str, Any]:
        """
        Add a new project.

        Args:
            name: The name of the project.
            announcement: Optional announcement text for the project.
            show_announcement: Whether to show the announcement.
            suite_mode: The suite mode of the project (1 for single
                suite, 2 for single suite with baselines, 3 for
                multiple suites).

        Returns:
            Dict containing the created project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}
        if announcement is not None:
            data["announcement"] = announcement
        if show_announcement is not None:
            data["show_announcement"] = show_announcement
        if suite_mode is not None:
            data["suite_mode"] = suite_mode

        return self._post("add_project", data=data)

    def update_project(
        self,
        project_id: int,
        name: str | None = None,
        announcement: str | None = None,
        show_announcement: bool | None = None,
        is_completed: bool | None = None,
        suite_mode: int | None = None,
    ) -> dict[str, Any]:
        """
        Update a project.

        Args:
            project_id: The ID of the project to update.
            name: Optional new name for the project.
            announcement: Optional announcement text for the project.
            show_announcement: Whether to show the announcement.
            is_completed: Whether the project is completed.
            suite_mode: The suite mode of the project.

        Returns:
            Dict containing the updated project data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if announcement is not None:
            data["announcement"] = announcement
        if show_announcement is not None:
            data["show_announcement"] = show_announcement
        if is_completed is not None:
            data["is_completed"] = is_completed
        if suite_mode is not None:
            data["suite_mode"] = suite_mode

        return self._post(f"update_project/{project_id}", data=data)

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
        return self._post(f"delete_project/{project_id}")
