"""
This module provides functionality for managing test suites in TestRail.
Test suites are used to organize and group related test cases.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class SuitesAPI(BaseAPI):
    """
    API for managing TestRail test suites.
    """
    
    def get_suite(self, suite_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a test suite by ID.
        
        Args:
            suite_id (int): The ID of the test suite to retrieve.
            
        Returns:
            dict: The test suite data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_suite/{suite_id}')
    
    def get_suites(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test suites for a project.
        
        Args:
            project_id (int): The ID of the project to get test suites for.
            
        Returns:
            list: List of test suites if successful, None otherwise.
        """
        return self._api_request('GET', f'get_suites/{project_id}')
    
    def add_suite(self, project_id: int, name: str, description: Optional[str] = None,
                 url: Optional[str] = None) -> Optional[Dict[str, Any]]:
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
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if url:
            data['url'] = url
            
        return self._api_request('POST', f'add_suite/{project_id}', data=data)
    
    def update_suite(self, suite_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to update.
            **kwargs: The fields to update (name, description, url).
            
        Returns:
            dict: The updated test suite data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_suite/{suite_id}', data=kwargs)
    
    def delete_suite(self, suite_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_suite/{suite_id}')
    
    def get_suite_cases(self, suite_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test cases in a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
        return self._api_request('GET', f'get_suite_cases/{suite_id}')
    
    def get_suite_stats(self, suite_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get statistics for.
            
        Returns:
            dict: The test suite statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_suite_stats/{suite_id}')
    
    def get_suite_runs(self, suite_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test runs for a test suite.
        
        Args:
            suite_id (int): The ID of the test suite to get test runs for.
            
        Returns:
            list: List of test runs if successful, None otherwise.
        """
        return self._api_request('GET', f'get_suite_runs/{suite_id}')