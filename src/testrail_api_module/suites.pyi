from typing import Any

from .base import BaseAPI as BaseAPI

class SuitesAPI(BaseAPI):
    """
    API for managing TestRail test suites.
    """
    def get_suite(self, suite_id: int) -> dict[str, Any] | None:
        """
        Get a test suite by ID.

        Args:
            suite_id (int): The ID of the test suite to retrieve.

        Returns:
            dict: The test suite data if successful, None otherwise.
        """
    def get_suites(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test suites for a project.

        Args:
            project_id (int): The ID of the project to get test suites for.

        Returns:
            list: List of test suites if successful, None otherwise.
        """
    def add_suite(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        url: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Add a new test suite.

        Args:
            project_id (int): The ID of the project to add the test suite to.
            name (str): The name of the test suite.
            description (str, optional): The description of the test suite.
            url (str, optional): The URL of the test suite.

        Returns:
            dict: The created test suite data if successful, None otherwise.
        """
    def update_suite(
        self, suite_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a test suite.

        Args:
            suite_id (int): The ID of the test suite to update.
            **kwargs: The fields to update (name, description, url).

        Returns:
            dict: The updated test suite data if successful, None otherwise.
        """
    def delete_suite(self, suite_id: int) -> dict[str, Any] | None:
        """
        Delete a test suite.

        Args:
            suite_id (int): The ID of the test suite to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
