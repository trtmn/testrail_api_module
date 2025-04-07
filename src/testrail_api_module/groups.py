"""
This module provides functionality for managing groups in TestRail.
Groups are used to organize test cases and test suites.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class GroupsAPI(BaseAPI):
    """
    API for managing TestRail groups.
    """
    
    def get_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a group by ID.
        
        Args:
            group_id (int): The ID of the group to retrieve.
            
        Returns:
            dict: The group data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_group/{group_id}')
    
    def get_groups(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all groups for a project.
        
        Args:
            project_id (int): The ID of the project to get groups for.
            
        Returns:
            list: List of groups if successful, None otherwise.
        """
        return self._api_request('GET', f'get_groups/{project_id}')
    
    def add_group(self, project_id: int, name: str, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Add a new group.
        
        Args:
            project_id (int): The ID of the project to add the group to.
            name (str): The name of the group.
            description (str, optional): The description of the group.
            
        Returns:
            dict: The created group data if successful, None otherwise.
        """
        data = {
            'name': name
        }
        if description:
            data['description'] = description
            
        return self._api_request('POST', f'add_group/{project_id}', data=data)
    
    def update_group(self, group_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a group.
        
        Args:
            group_id (int): The ID of the group to update.
            **kwargs: The fields to update (name, description).
            
        Returns:
            dict: The updated group data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_group/{group_id}', data=kwargs)
    
    def delete_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a group.
        
        Args:
            group_id (int): The ID of the group to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_group/{group_id}')
    
    def add_group_to_suite(self, group_id: int, suite_id: int) -> Optional[Dict[str, Any]]:
        """
        Add a group to a test suite.
        
        Args:
            group_id (int): The ID of the group to add.
            suite_id (int): The ID of the test suite to add the group to.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'add_group_to_suite/{suite_id}/{group_id}')
    
    def remove_group_from_suite(self, group_id: int, suite_id: int) -> Optional[Dict[str, Any]]:
        """
        Remove a group from a test suite.
        
        Args:
            group_id (int): The ID of the group to remove.
            suite_id (int): The ID of the test suite to remove the group from.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'remove_group_from_suite/{suite_id}/{group_id}')
    
    def get_group_cases(self, group_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test cases in a group.
        
        Args:
            group_id (int): The ID of the group to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
        return self._api_request('GET', f'get_group_cases/{group_id}')
    
    def get_group_suites(self, group_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test suites in a group.
        
        Args:
            group_id (int): The ID of the group to get test suites for.
            
        Returns:
            list: List of test suites if successful, None otherwise.
        """
        return self._api_request('GET', f'get_group_suites/{group_id}')