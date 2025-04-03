"""
This module provides functionality for managing variables in TestRail.
Variables are used to store and manage test parameters and configuration values.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class VariablesAPI(BaseAPI):
    """
    API for managing TestRail variables.
    """
    
    def get_variable(self, variable_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a variable by ID.
        
        Args:
            variable_id (int): The ID of the variable to retrieve.
            
        Returns:
            dict: The variable data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_variable/{variable_id}')
    
    def get_variables(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all variables for a project.
        
        Args:
            project_id (int): The ID of the project to get variables for.
            
        Returns:
            list: List of variables if successful, None otherwise.
        """
        return self._api_request('GET', f'get_variables/{project_id}')
    
    def add_variable(self, project_id: int, name: str, value: str,
                    description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Add a new variable.
        
        Args:
            project_id (int): The ID of the project to add the variable to.
            name (str): The name of the variable.
            value (str): The value of the variable.
            description (str, optional): The description of the variable.
            
        Returns:
            dict: The created variable data if successful, None otherwise.
        """
        data = {
            'name': name,
            'value': value
        }
        if description:
            data['description'] = description
            
        return self._api_request('POST', f'add_variable/{project_id}', data=data)
    
    def update_variable(self, variable_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a variable.
        
        Args:
            variable_id (int): The ID of the variable to update.
            **kwargs: The fields to update (name, value, description).
            
        Returns:
            dict: The updated variable data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_variable/{variable_id}', data=kwargs)
    
    def delete_variable(self, variable_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a variable.
        
        Args:
            variable_id (int): The ID of the variable to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_variable/{variable_id}')
    
    def get_variable_groups(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all variable groups for a project.
        
        Args:
            project_id (int): The ID of the project to get variable groups for.
            
        Returns:
            list: List of variable groups if successful, None otherwise.
        """
        return self._api_request('GET', f'get_variable_groups/{project_id}')
    
    def add_variable_group(self, project_id: int, name: str,
                          description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Add a new variable group.
        
        Args:
            project_id (int): The ID of the project to add the variable group to.
            name (str): The name of the variable group.
            description (str, optional): The description of the variable group.
            
        Returns:
            dict: The created variable group data if successful, None otherwise.
        """
        data = {
            'name': name
        }
        if description:
            data['description'] = description
            
        return self._api_request('POST', f'add_variable_group/{project_id}', data=data)
    
    def update_variable_group(self, group_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a variable group.
        
        Args:
            group_id (int): The ID of the variable group to update.
            **kwargs: The fields to update (name, description).
            
        Returns:
            dict: The updated variable group data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_variable_group/{group_id}', data=kwargs)
    
    def delete_variable_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a variable group.
        
        Args:
            group_id (int): The ID of the variable group to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_variable_group/{group_id}')