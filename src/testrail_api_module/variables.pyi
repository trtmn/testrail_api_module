from typing import Any

from .base import BaseAPI as BaseAPI

class VariablesAPI(BaseAPI):
    """
    API for managing TestRail variables.
    """
    def get_variable(self, variable_id: int) -> dict[str, Any] | None:
        """
        Get a variable by ID.

        Args:
            variable_id (int): The ID of the variable to retrieve.

        Returns:
            dict: The variable data if successful, None otherwise.
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
    def get_variable_groups(
        self, project_id: int
    ) -> list[dict[str, Any]] | None:
        """
        Get all variable groups for a project.

        Args:
            project_id (int): The ID of the project to get variable groups for.

        Returns:
            list: List of variable groups if successful, None otherwise.
        """
    def add_variable_group(
        self, project_id: int, name: str, description: str | None = None
    ) -> dict[str, Any] | None:
        """
        Add a new variable group.

        Args:
            project_id (int): The ID of the project to add the variable group to.
            name (str): The name of the variable group.
            description (str, optional): The description of the variable group.

        Returns:
            dict: The created variable group data if successful, None otherwise.
        """
    def update_variable_group(
        self, group_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a variable group.

        Args:
            group_id (int): The ID of the variable group to update.
            **kwargs: The fields to update (name, description).

        Returns:
            dict: The updated variable group data if successful, None otherwise.
        """
    def delete_variable_group(self, group_id: int) -> dict[str, Any] | None:
        """
        Delete a variable group.

        Args:
            group_id (int): The ID of the variable group to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
