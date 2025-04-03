"""
This module provides functionality for managing test runs in TestRail.
Test runs are used to execute test cases and track their results.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class RunsAPI(BaseAPI):
    """
    API for managing TestRail test runs.
    """
    
    def get_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a test run by ID.
        
        Args:
            run_id (int): The ID of the test run to retrieve.
            
        Returns:
            dict: The test run data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_run/{run_id}')
    
    def get_runs(self, project_id: int, suite_id: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test runs for a project and optionally a specific suite.
        
        Args:
            project_id (int): The ID of the project to get test runs for.
            suite_id (int, optional): The ID of the suite to get test runs for.
            
        Returns:
            list: List of test runs if successful, None otherwise.
        """
        endpoint = f'get_runs/{project_id}'
        if suite_id:
            endpoint += f'&suite_id={suite_id}'
        return self._api_request('GET', endpoint)
    
    def add_run(self, project_id: int, name: str, description: Optional[str] = None,
                suite_id: Optional[int] = None, milestone_id: Optional[int] = None,
                assignedto_id: Optional[int] = None, include_all: bool = True,
                case_ids: Optional[List[int]] = None) -> Optional[Dict[str, Any]]:
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
        data = {
            'name': name,
            'include_all': include_all
        }
        if description:
            data['description'] = description
        if suite_id:
            data['suite_id'] = suite_id
        if milestone_id:
            data['milestone_id'] = milestone_id
        if assignedto_id:
            data['assignedto_id'] = assignedto_id
        if case_ids:
            data['case_ids'] = case_ids
            
        return self._api_request('POST', f'add_run/{project_id}', data=data)
    
    def update_run(self, run_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a test run.
        
        Args:
            run_id (int): The ID of the test run to update.
            **kwargs: The fields to update (name, description, milestone_id, assignedto_id, etc.).
            
        Returns:
            dict: The updated test run data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_run/{run_id}', data=kwargs)
    
    def close_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        Close a test run.
        
        Args:
            run_id (int): The ID of the test run to close.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'close_run/{run_id}')
    
    def delete_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a test run.
        
        Args:
            run_id (int): The ID of the test run to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_run/{run_id}')
    
    def get_run_stats(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a test run.
        
        Args:
            run_id (int): The ID of the test run to get statistics for.
            
        Returns:
            dict: The test run statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_run_stats/{run_id}')