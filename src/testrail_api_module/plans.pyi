from .base import BaseAPI as BaseAPI
from typing import Any

class PlansAPI(BaseAPI):
    """
    API for managing TestRail test plans.
    """
    def get_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Get a test plan by ID.
        
        Args:
            plan_id (int): The ID of the test plan to retrieve.
            
        Returns:
            dict: The test plan data if successful, None otherwise.
        """
    def get_plans(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test plans for a project.
        
        Args:
            project_id (int): The ID of the project to get test plans for.
            
        Returns:
            list: List of test plans if successful, None otherwise.
        """
    def add_plan(self, project_id: int, name: str, description: str | None = None, milestone_id: int | None = None, entries: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
        """
        Add a new test plan.
        
        Args:
            project_id (int): The ID of the project to add the test plan to.
            name (str): The name of the test plan.
            description (str, optional): The description of the test plan.
            milestone_id (int, optional): The ID of the milestone to add the test plan to.
            entries (list, optional): List of test plan entries, each containing:
                - suite_id (int): The ID of the test suite
                - name (str): The name of the test run
                - description (str, optional): The description of the test run
                - assignedto_id (int, optional): The ID of the user to assign the test run to
                - include_all (bool, optional): Whether to include all test cases
                - case_ids (list, optional): List of test case IDs to include
                
        Returns:
            dict: The created test plan data if successful, None otherwise.
        """
    def update_plan(self, plan_id: int, **kwargs: Any) -> dict[str, Any] | None:
        """
        Update a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to update.
            **kwargs: The fields to update (name, description, milestone_id, entries).
            
        Returns:
            dict: The updated test plan data if successful, None otherwise.
        """
    def close_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Close a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to close.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def delete_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Delete a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_plan_stats(self, plan_id: int) -> dict[str, Any] | None:
        """
        Get statistics for a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to get statistics for.
            
        Returns:
            dict: The test plan statistics if successful, None otherwise.
        """
