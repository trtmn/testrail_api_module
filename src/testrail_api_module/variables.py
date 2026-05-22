"""
This module provides functionality for managing variables in TestRail.
Variables are used to store and manage test parameters and
configuration values for parameterized testing.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["VariablesAPI"]


class VariablesAPI(BaseAPI):
    """
    API for managing TestRail variables.

    This class provides methods to create, read, update, and delete
    variables used for parameterized testing in TestRail.
    """

    def get_variables(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all variables for a project.

        Args:
            project_id: The ID of the project to get variables for.

        Returns:
            List of dictionaries containing variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_variables/{project_id}")

    def add_variable(
        self,
        project_id: int,
        name: str,
        value: str,
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new variable.

        Args:
            project_id: The ID of the project to add the variable
                to.
            name: The name of the variable.
            value: The value of the variable.
            description: Optional description of the variable.

        Returns:
            Dict containing the created variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name, "value": value}
        if description:
            data["description"] = description

        return self._api_request(
            "POST", f"add_variable/{project_id}", data=data
        )

    def update_variable(
        self, variable_id: int, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Update a variable.

        Args:
            variable_id: The ID of the variable to update.
            **kwargs: Fields to update (name, value, description).

        Returns:
            Dict containing the updated variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request(
            "POST",
            f"update_variable/{variable_id}",
            data=kwargs,
        )

    def delete_variable(self, variable_id: int) -> dict[str, Any]:
        """
        Delete a variable.

        Args:
            variable_id: The ID of the variable to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("POST", f"delete_variable/{variable_id}")
