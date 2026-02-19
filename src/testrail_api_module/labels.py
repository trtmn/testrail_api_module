"""
This module provides functionality for managing labels in TestRail.
Labels are used to categorize and tag test cases for organization
and filtering purposes.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["LabelsAPI"]


class LabelsAPI(BaseAPI):
    """
    API for managing TestRail labels.

    This class provides methods to create, read, update, and delete
    labels in TestRail, following the official TestRail API patterns.
    """

    def get_label(self, label_id: int) -> dict[str, Any]:
        """
        Get a label by ID.

        Args:
            label_id: The ID of the label to retrieve.

        Returns:
            Dict containing the label data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_label/{label_id}")

    def get_labels(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all labels for a project.

        Args:
            project_id: The ID of the project to get labels for.

        Returns:
            List of dictionaries containing label data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_labels/{project_id}")

    def add_label(
        self, project_id: int, name: str, color: str | None = None
    ) -> dict[str, Any]:
        """
        Add a new label.

        Args:
            project_id: The ID of the project to add the label to.
            name: The name of the label.
            color: Optional color for the label (hex code).

        Returns:
            Dict containing the created label data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name}
        if color is not None:
            data["color"] = color

        return self._post(f"add_label/{project_id}", data=data)

    def update_label(self, label_id: int, **kwargs) -> dict[str, Any]:
        """
        Update a label.

        Args:
            label_id: The ID of the label to update.
            **kwargs: The fields to update (name, color).

        Returns:
            Dict containing the updated label data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"update_label/{label_id}", data=kwargs)

    def delete_label(self, label_id: int) -> dict[str, Any]:
        """
        Delete a label.

        Args:
            label_id: The ID of the label to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_label/{label_id}")
