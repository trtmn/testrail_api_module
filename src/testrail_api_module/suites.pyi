from .base import BaseAPI as BaseAPI
from typing import Any

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
    def add_suite(self, project_id: int, name: str, description: str | None = None, url: str | None = None) -> dict[str, Any] | None:
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
    def update_suite(self, suite_id: int, **kwargs) -> dict[str, Any] | None:
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
    def get_suite_cases(self, suite_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test cases in a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
    def get_suite_stats(self, suite_id: int) -> dict[str, Any] | None:
        """
        Get statistics for a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get statistics for.
            
        Returns:
            dict: The test suite statistics if successful, None otherwise.
        """
    def get_suite_runs(self, suite_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test runs for a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get test runs for.
            
        Returns:
            list: List of test runs if successful, None otherwise.
        """
