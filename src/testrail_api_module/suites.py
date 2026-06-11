"""
This module provides functionality for managing test suites in
TestRail. Test suites are used to organize and group related test
cases.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["SuitesAPI"]


class SuitesAPI(BaseAPI):
    """
    API for managing TestRail test suites.

    This class provides methods to create, read, update, and delete
    test suites in TestRail, following the official TestRail API
    patterns.
    """

    def get_suite(self, suite_id: int) -> dict[str, Any]:
        """
        Get a test suite by ID.

        Args:
            suite_id: The ID of the test suite to retrieve.

        Returns:
            Dict containing the test suite data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_suite/{suite_id}")

    def get_suites(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all test suites for a project.

        Args:
            project_id: The ID of the project to get test suites
                for.

        Returns:
            List of dictionaries containing test suite data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_suites/{project_id}")

    def add_suite(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new test suite.

        Args:
            project_id: The ID of the project to add the suite to.
            name: The name of the test suite.
            description: Optional description of the test suite.

        Returns:
            Dict containing the created test suite data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}
        if description is not None:
            data["description"] = description

        return self._post(f"add_suite/{project_id}", data=data)

    def update_suite(
        self,
        suite_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Update a test suite.

        Args:
            suite_id: The ID of the test suite to update.
            name: Optional new name for the test suite.
            description: Optional description of the test suite.

        Returns:
            Dict containing the updated test suite data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        return self._post(f"update_suite/{suite_id}", data=data)

    def delete_suite(self, suite_id: int) -> dict[str, Any]:
        """
        Delete a test suite.

        Args:
            suite_id: The ID of the test suite to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_suite/{suite_id}")
