"""
This module provides functionality for managing statuses in TestRail.
Statuses are used to track the state of test cases and test results.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class StatusesAPI(BaseAPI):
    """
    API for managing TestRail statuses.
    """
    
    def get_status(self, status_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a status by ID.
        
        Args:
            status_id (int): The ID of the status to retrieve.
            
        Returns:
            dict: The status data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_status/{status_id}')
    
    def get_statuses(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all available statuses.
        
        Returns:
            list: List of statuses if successful, None otherwise.
        """
        return self._api_request('GET', 'get_statuses')
    
    def add_status(self, name: str, short_name: str, color: str,
                  is_system: bool = False, is_untested: bool = False,
                  is_passed: bool = False, is_blocked: bool = False,
                  is_retest: bool = False, is_failed: bool = False,
                  is_custom: bool = True) -> Optional[Dict[str, Any]]:
        """
        Add a new status.
        
        Args:
            name (str): The name of the status.
            short_name (str): The short name of the status.
            color (str): The color of the status (hex code).
            is_system (bool, optional): Whether this is a system status.
            is_untested (bool, optional): Whether this is the untested status.
            is_passed (bool, optional): Whether this is the passed status.
            is_blocked (bool, optional): Whether this is the blocked status.
            is_retest (bool, optional): Whether this is the retest status.
            is_failed (bool, optional): Whether this is the failed status.
            is_custom (bool, optional): Whether this is a custom status.
                
        Returns:
            dict: The created status data if successful, None otherwise.
        """
        data = {
            'name': name,
            'short_name': short_name,
            'color': color,
            'is_system': is_system,
            'is_untested': is_untested,
            'is_passed': is_passed,
            'is_blocked': is_blocked,
            'is_retest': is_retest,
            'is_failed': is_failed,
            'is_custom': is_custom
        }
            
        return self._api_request('POST', 'add_status', data=data)
    
    def update_status(self, status_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a status.
        
        Args:
            status_id (int): The ID of the status to update.
            **kwargs: The fields to update (name, short_name, color, etc.).
            
        Returns:
            dict: The updated status data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_status/{status_id}', data=kwargs)
    
    def delete_status(self, status_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a status.
        
        Args:
            status_id (int): The ID of the status to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_status/{status_id}')
    
    def get_status_counts(self, run_id: int) -> Optional[Dict[str, int]]:
        """
        Get the count of test results by status for a test run.
        
        Args:
            run_id (int): The ID of the test run to get status counts for.
            
        Returns:
            dict: Dictionary mapping status IDs to counts if successful, None otherwise.
        """
        return self._api_request('GET', f'get_status_counts/{run_id}')
    
    def get_status_history(self, result_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get the history of status changes for a test result.
        
        Args:
            result_id (int): The ID of the test result to get history for.
            
        Returns:
            list: List of status history entries if successful, None otherwise.
        """
        return self._api_request('GET', f'get_status_history/{result_id}')