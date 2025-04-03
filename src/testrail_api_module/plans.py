"""
This module provides functionality for managing test plans in TestRail.
Test plans are used to organize and schedule test runs.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class PlansAPI(BaseAPI):
    """
    API for managing TestRail test plans.
    """
    
    def get_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a test plan by ID.
        
        Args:
            plan_id (int): The ID of the test plan to retrieve.
            
        Returns:
            dict: The test plan data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_plan/{plan_id}')
    
    def get_plans(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test plans for a project.
        
        Args:
            project_id (int): The ID of the project to get test plans for.
            
        Returns:
            list: List of test plans if successful, None otherwise.
        """
        return self._api_request('GET', f'get_plans/{project_id}')
    
    def add_plan(self, project_id: int, name: str, description: Optional[str] = None,
                 milestone_id: Optional[int] = None, entries: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
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
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if milestone_id:
            data['milestone_id'] = milestone_id
        if entries:
            data['entries'] = entries
            
        return self._api_request('POST', f'add_plan/{project_id}', data=data)
    
    def update_plan(self, plan_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to update.
            **kwargs: The fields to update (name, description, milestone_id, entries).
            
        Returns:
            dict: The updated test plan data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_plan/{plan_id}', data=kwargs)
    
    def close_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """
        Close a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to close.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'close_plan/{plan_id}')
    
    def delete_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_plan/{plan_id}')
    
    def get_plan_stats(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a test plan.
        
        Args:
            plan_id (int): The ID of the test plan to get statistics for.
            
        Returns:
            dict: The test plan statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_plan_stats/{plan_id}')