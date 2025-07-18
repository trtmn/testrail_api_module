from .base import BaseAPI as BaseAPI
from typing import Any

class RunsAPI(BaseAPI):
    """
    API for managing TestRail test runs.
    """
    def get_run(self, run_id: int) -> dict[str, Any] | None:
        """
        Get a test run by ID.
        
        Args:
            run_id (int): The ID of the test run to retrieve.
            
        Returns:
            dict: The test run data if successful, None otherwise.
        """
    def get_runs(self, project_id: int, suite_id: int | None = None) -> list[dict[str, Any]] | None:
        """
        Get all test runs for a project and optionally a specific suite.
        
        Args:
            project_id (int): The ID of the project to get test runs for.
            suite_id (int, optional): The ID of the suite to get test runs for.
            
        Returns:
            list: List of test runs if successful, None otherwise.
        """
    def add_run(self, project_id: int, name: str, description: str | None = None, suite_id: int | None = None, milestone_id: int | None = None, assignedto_id: int | None = None, include_all: bool = True, case_ids: list[int] | None = None) -> dict[str, Any] | None:
        """
        Add a new test run.
        
        Args:
            project_id (int): The ID of the project to add the test run to.
            name (str): The name of the test run.
            description (str, optional): The description of the test run.
            suite_id (int, optional): The ID of the suite to add the test run to.
            milestone_id (int, optional): The ID of the milestone to add the test run to.
            assignedto_id (int, optional): The ID of the user to assign the test run to.
            include_all (bool, optional): Whether to include all test cases from the suite.
            case_ids (list, optional): List of test case IDs to include in the run.
            
        Returns:
            dict: The created test run data if successful, None otherwise.
        """
    def update_run(self, run_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a test run.
        
        Args:
            run_id (int): The ID of the test run to update.
            **kwargs: The fields to update (name, description, milestone_id, assignedto_id, etc.).
            
        Returns:
            dict: The updated test run data if successful, None otherwise.
        """
    def close_run(self, run_id: int) -> dict[str, Any] | None:
        """
        Close a test run.
        
        Args:
            run_id (int): The ID of the test run to close.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def delete_run(self, run_id: int) -> dict[str, Any] | None:
        """
        Delete a test run.
        
        Args:
            run_id (int): The ID of the test run to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_run_stats(self, run_id: int) -> dict[str, Any] | None:
        """
        Get statistics for a test run.
        
        Args:
            run_id (int): The ID of the test run to get statistics for.
            
        Returns:
            dict: The test run statistics if successful, None otherwise.
        """
