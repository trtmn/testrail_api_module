"""
This module provides functionality for managing test runs in TestRail.
Test runs are used to execute test cases and track their results.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

__all__ = ['RunsAPI']

class RunsAPI(BaseAPI):
    """
    API for managing TestRail test runs.
    
    This class provides methods to create, read, update, and manage test runs
    in TestRail, following the official TestRail API patterns.
    """
    
    def get_run(self, run_id: int) -> Dict[str, Any]:
        """
        Get a test run by ID.
        
        Args:
            run_id: The ID of the test run to retrieve.
            
        Returns:
            Dict containing the test run data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> run = api.runs.get_run(123)
            >>> print(f"Run: {run['name']}")
        """
        return self._get(f'get_run/{run_id}')
    
    def get_runs(self, project_id: int, suite_id: Optional[int] = None,
                 created_after: Optional[int] = None,
                 created_before: Optional[int] = None,
                 created_by: Optional[int] = None,
                 is_completed: Optional[bool] = None,
                 limit: Optional[int] = None,
                 offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all test runs for a project and optionally a specific suite.
        
        Args:
            project_id: The ID of the project to get test runs for.
            suite_id: Optional ID of the suite to get test runs for.
            created_after: Optional timestamp to filter runs created after this time.
            created_before: Optional timestamp to filter runs created before this time.
            created_by: Optional user ID to filter runs created by specific user.
            is_completed: Optional boolean to filter by completion status.
            limit: Optional limit on number of results to return.
            offset: Optional offset for pagination.
            
        Returns:
            List of dictionaries containing test run data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> runs = api.runs.get_runs(project_id=1, suite_id=2)
            >>> for run in runs:
            ...     print(f"Run: {run['name']}")
        """
        params = {}
        if suite_id is not None:
            params['suite_id'] = suite_id
        if created_after is not None:
            params['created_after'] = created_after
        if created_before is not None:
            params['created_before'] = created_before
        if created_by is not None:
            params['created_by'] = created_by
        if is_completed is not None:
            params['is_completed'] = is_completed
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        return self._get(f'get_runs/{project_id}', params=params)
    
    def add_run(self, project_id: int, name: str, description: Optional[str] = None,
                suite_id: Optional[int] = None, milestone_id: Optional[int] = None,
                assignedto_id: Optional[int] = None, include_all: bool = True,
                case_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Add a new test run.
        
        Args:
            project_id: The ID of the project to add the test run to.
            name: The name of the test run.
            description: Optional description of the test run.
            suite_id: Optional ID of the suite to add the test run to.
            milestone_id: Optional ID of the milestone to add the test run to.
            assignedto_id: Optional ID of the user to assign the test run to.
            include_all: Whether to include all test cases from the suite.
            case_ids: Optional list of test case IDs to include in the run.
            
        Returns:
            Dict containing the created test run data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> run = api.runs.add_run(
            ...     project_id=1,
            ...     name="Test Run",
            ...     description="Automated test run",
            ...     suite_id=2,
            ...     include_all=True
            ... )
        """
        data = {
            'name': name,
            'include_all': include_all
        }
        
        # Add optional fields only if they are provided
        optional_fields = {
            'description': description,
            'suite_id': suite_id,
            'milestone_id': milestone_id,
            'assignedto_id': assignedto_id,
            'case_ids': case_ids
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
            
        return self._post(f'add_run/{project_id}', data=data)
    
    def update_run(self, run_id: int, name: Optional[str] = None,
                  description: Optional[str] = None, milestone_id: Optional[int] = None,
                  assignedto_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Update a test run.
        
        Args:
            run_id: The ID of the test run to update.
            name: Optional new name for the test run.
            description: Optional new description for the test run.
            milestone_id: Optional new milestone ID.
            assignedto_id: Optional new assigned user ID.
            
        Returns:
            Dict containing the updated test run data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> updated_run = api.runs.update_run(
            ...     run_id=123,
            ...     name="Updated Run Name",
            ...     assignedto_id=456
            ... )
        """
        data = {}
        
        # Add fields only if they are provided
        optional_fields = {
            'name': name,
            'description': description,
            'milestone_id': milestone_id,
            'assignedto_id': assignedto_id
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
            
        return self._post(f'update_run/{run_id}', data=data)
    
    def close_run(self, run_id: int) -> Dict[str, Any]:
        """
        Close a test run.
        
        Args:
            run_id: The ID of the test run to close.
            
        Returns:
            Dict containing the response data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.runs.close_run(123)
        """
        return self._post(f'close_run/{run_id}')
    
    def delete_run(self, run_id: int) -> Dict[str, Any]:
        """
        Delete a test run.
        
        Args:
            run_id: The ID of the test run to delete.
            
        Returns:
            Dict containing the response data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.runs.delete_run(123)
        """
        return self._post(f'delete_run/{run_id}')
    
    def get_run_stats(self, run_id: int) -> Dict[str, Any]:
        """
        Get statistics for a test run.
        
        Args:
            run_id: The ID of the test run to get statistics for.
            
        Returns:
            Dict containing the test run statistics.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> stats = api.runs.get_run_stats(123)
            >>> print(f"Passed: {stats['passed']}, Failed: {stats['failed']}")
        """
        return self._get(f'get_run_stats/{run_id}')