from typing import Any

from .base import BaseAPI as BaseAPI

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
    def update_variable(
        self, variable_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a variable.

        Args:
            variable_id (int): The ID of the variable to update.
            **kwargs: The fields to update (name, value, description).

        Returns:
            dict: The updated variable data if successful, None otherwise.
        """
    def delete_variable(self, variable_id: int) -> dict[str, Any] | None:
        """
        Delete a variable.

        Args:
            variable_id (int): The ID of the variable to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
