"""
This module provides functionality for managing variables in TestRail.
Variables are used to store and manage test parameters and configuration values.
"""

from typing import Any

from .base import BaseAPI


class VariablesAPI(BaseAPI):
    """
    API for managing TestRail variables.
    """

    def get_variables(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all variables for a project.

        Args:
            project_id (int): The ID of the project to get variables for.

        Returns:
            list: List of variables if successful, None otherwise.
        """
        return self._api_request("GET", f"get_variables/{project_id}")

    def add_variable(
        self,
        project_id: int,
        name: str,
        value: str,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Add a new variable.

        Args:
            project_id (int): The ID of the project to add the variable to.
            name (str): The name of the variable.
            value (str): The value of the variable.
            description (str, optional): The description of the variable.

        Returns:
            dict: The created variable data if successful, None otherwise.
        """
        data = {"name": name, "value": value}
        if description:
            data["description"] = description

        return self._api_request(
            "POST", f"add_variable/{project_id}", data=data
        )

    def update_variable(
        self, variable_id: int, **kwargs
    ) -> dict[str, Any] | None:
        """
        Update a variable.

        Args:
            variable_id (int): The ID of the variable to update.
            **kwargs: The fields to update (name, value, description).

        Returns:
            dict: The updated variable data if successful, None otherwise.
        """
        return self._api_request(
            "POST", f"update_variable/{variable_id}", data=kwargs
        )

    def delete_variable(self, variable_id: int) -> dict[str, Any] | None:
        """
        Delete a variable.

        Args:
            variable_id (int): The ID of the variable to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request("POST", f"delete_variable/{variable_id}")
