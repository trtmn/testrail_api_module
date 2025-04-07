"""
This module provides functionality for managing priorities in TestRail.
Priorities are used to indicate the importance of test cases.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class PrioritiesAPI(BaseAPI):
    """
    API for managing TestRail priorities.
    """
    
    def get_priority(self, priority_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a priority by ID.
        
        Args:
            priority_id (int): The ID of the priority to retrieve.
            
        Returns:
            dict: The priority data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_priority/{priority_id}')
    
    def get_priorities(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all available priorities.
        
        Returns:
            list: List of priorities if successful, None otherwise.
        """
        return self._api_request('GET', 'get_priorities')
    
    def add_priority(self, name: str, short_name: str, color: str,
                    is_default: bool = False) -> Optional[Dict[str, Any]]:
        """
        Add a new priority.
        
        Args:
            name (str): The name of the priority.
            short_name (str): The short name of the priority.
            color (str): The color of the priority (hex code).
            is_default (bool, optional): Whether this is the default priority.
                
        Returns:
            dict: The created priority data if successful, None otherwise.
        """
        data = {
            'name': name,
            'short_name': short_name,
            'color': color,
            'is_default': is_default
        }
            
        return self._api_request('POST', 'add_priority', data=data)
    
    def update_priority(self, priority_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a priority.
        
        Args:
            priority_id (int): The ID of the priority to update.
            **kwargs: The fields to update (name, short_name, color, is_default).
            
        Returns:
            dict: The updated priority data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_priority/{priority_id}', data=kwargs)
    
    def delete_priority(self, priority_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a priority.
        
        Args:
            priority_id (int): The ID of the priority to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_priority/{priority_id}')
    
    def get_priority_counts(self, project_id: int) -> Optional[Dict[str, int]]:
        """
        Get the count of test cases by priority for a project.
        
        Args:
            project_id (int): The ID of the project to get priority counts for.
            
        Returns:
            dict: Dictionary mapping priority IDs to counts if successful, None otherwise.
        """
        return self._api_request('GET', f'get_priority_counts/{project_id}')
    
    def get_priority_stats(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics about priorities in a project.
        
        Args:
            project_id (int): The ID of the project to get priority statistics for.
            
        Returns:
            dict: The priority statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_priority_stats/{project_id}')