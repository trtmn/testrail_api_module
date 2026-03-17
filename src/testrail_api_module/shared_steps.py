"""
This module provides functionality for managing shared steps in
TestRail. Shared steps are reusable test steps that can be referenced
by multiple test cases.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["SharedStepsAPI"]


class SharedStepsAPI(BaseAPI):
    """
    API for managing TestRail shared steps.

    This class provides methods to create, read, update, and delete
    shared steps that can be reused across multiple test cases.
    """

    def get_shared_step(self, shared_step_id: int) -> dict[str, Any]:
        """
        Get a shared step by ID.

        Args:
            shared_step_id: The ID of the shared step to retrieve.

        Returns:
            Dict containing the shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_shared_step/{shared_step_id}")

    def get_shared_steps(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all shared steps for a project.

        Args:
            project_id: The ID of the project to get shared steps
                for.

        Returns:
            List of dictionaries containing shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_shared_steps/{project_id}")

    def add_shared_step(
        self,
        project_id: int,
        title: str,
        steps: list[dict[str, Any]],
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new shared step.

        Args:
            project_id: The ID of the project to add the shared
                step to.
            title: The title of the shared step.
            steps: List of dictionaries containing step data.
            description: Optional description of the shared step.

        Returns:
            Dict containing the created shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"title": title, "steps": steps}
        if description:
            data["description"] = description

        return self._api_request(
            "POST", f"add_shared_step/{project_id}", data=data
        )

    def update_shared_step(
        self, shared_step_id: int, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Update a shared step.

        Args:
            shared_step_id: The ID of the shared step to update.
            **kwargs: Fields to update (title, steps, description).

        Returns:
            Dict containing the updated shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request(
            "POST",
            f"update_shared_step/{shared_step_id}",
            data=kwargs,
        )

    def delete_shared_step(self, shared_step_id: int) -> dict[str, Any]:
        """
        Delete a shared step.

        Args:
            shared_step_id: The ID of the shared step to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request(
            "POST", f"delete_shared_step/{shared_step_id}"
        )
