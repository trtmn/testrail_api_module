from .base import BaseAPI as BaseAPI
from typing import Any

class GroupsAPI(BaseAPI):
    """
    API for managing TestRail groups.
    """
    def get_group(self, group_id: int) -> dict[str, Any] | None:
        """
        Get a group by ID.
        
        Args:
            group_id (int): The ID of the group to retrieve.
            
        Returns:
            dict: The group data if successful, None otherwise.
        """
    def get_groups(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all groups for a project.
        
        Args:
            project_id (int): The ID of the project to get groups for.
            
        Returns:
            list: List of groups if successful, None otherwise.
        """
    def add_group(self, project_id: int, name: str, description: str | None = None) -> dict[str, Any] | None:
        """
        Add a new group.
        
        Args:
            project_id (int): The ID of the project to add the group to.
            name (str): The name of the group.
            description (str, optional): The description of the group.
            
        Returns:
            dict: The created group data if successful, None otherwise.
        """
    def update_group(self, group_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a group.
        
        Args:
            group_id (int): The ID of the group to update.
            **kwargs: The fields to update (name, description).
            
        Returns:
            dict: The updated group data if successful, None otherwise.
        """
    def delete_group(self, group_id: int) -> dict[str, Any] | None:
        """
        Delete a group.
        
        Args:
            group_id (int): The ID of the group to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def add_group_to_suite(self, group_id: int, suite_id: int) -> dict[str, Any] | None:
        """
        Add a group to a test suite.
        
        Args:
            group_id (int): The ID of the group to add.
            suite_id (int): The ID of the test suite to add the group to.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def remove_group_from_suite(self, group_id: int, suite_id: int) -> dict[str, Any] | None:
        """
        Remove a group from a test suite.
        
        Args:
            group_id (int): The ID of the group to remove.
            suite_id (int): The ID of the test suite to remove the group from.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_group_cases(self, group_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test cases in a group.
        
        Args:
            group_id (int): The ID of the group to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
    def get_group_suites(self, group_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test suites in a group.
        
        Args:
            group_id (int): The ID of the group to get test suites for.
            
        Returns:
            list: List of test suites if successful, None otherwise.
        """
