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

    def get_variable(self, variable_id: int) -> dict[str, Any]:
        """
        Get a variable by ID.

        Args:
            variable_id: The ID of the variable to retrieve.

        Returns:
            Dict containing the variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_variable/{variable_id}")

    def get_variables(
        self,
        project_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all variables for a project.

        Args:
            project_id: The ID of the project to get variables for.
            limit: Optional maximum number of variables to return.
            offset: Optional number of variables to skip for
                pagination.

        Returns:
            List of dictionaries containing variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._get(f"get_variables/{project_id}", params=params)

    def add_variable(
        self,
        project_id: int,
        name: str,
    ) -> dict[str, Any]:
        """
        Add a new variable.

        Args:
            project_id: The ID of the project to add the variable
                to.
            name: The name of the variable.

        Returns:
            Dict containing the created variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}

        return self._post(f"add_variable/{project_id}", data=data)

    def update_variable(
        self,
        variable_id: int,
        name: str,
    ) -> dict[str, Any]:
        """
        Update a variable.

        Args:
            variable_id: The ID of the variable to update.
            name: The new name for the variable.

        Returns:
            Dict containing the updated variable data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}

        return self._post(
            f"update_variable/{variable_id}",
            data=data,
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
        return self._post(f"delete_variable/{variable_id}")
