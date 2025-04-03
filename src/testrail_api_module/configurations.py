"""
This module provides functionality for managing configurations in TestRail.
Configurations are used to define different test environments and settings.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class ConfigurationsAPI(BaseAPI):
    """
    API for managing TestRail configurations.
    """
    
    def get_configuration(self, config_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a configuration by ID.
        
        Args:
            config_id: The ID of the configuration to retrieve.
            
        Returns:
            Dict containing the configuration data.
        """
        return self._api_request('GET', f'get_configuration/{config_id}')
    
    def get_configurations(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all configurations for a project.
        
        Args:
            project_id: The ID of the project to get configurations for.
            
        Returns:
            List of dictionaries containing configuration data.
        """
        return self._api_request('GET', f'get_configurations/{project_id}')
    
    def add_configuration(self, project_id: int, name: str, description: Optional[str] = None,
                         group_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Add a new configuration.
        
        Args:
            project_id: The ID of the project to add the configuration to.
            name: The name of the configuration.
            description: Optional description of the configuration.
            group_id: Optional ID of the configuration group.
            
        Returns:
            Dict containing the created configuration data.
        """
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if group_id:
            data['group_id'] = group_id
            
        return self._api_request('POST', f'add_configuration/{project_id}', data=data)
    
    def update_configuration(self, config_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a configuration.
        
        Args:
            config_id: The ID of the configuration to update.
            **kwargs: The fields to update (name, description, group_id).
            
        Returns:
            Dict containing the updated configuration data.
        """
        return self._api_request('POST', f'update_configuration/{config_id}', data=kwargs)
    
    def delete_configuration(self, config_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a configuration.
        
        Args:
            config_id: The ID of the configuration to delete.
            
        Returns:
            Dict containing the response data.
        """
        return self._api_request('POST', f'delete_configuration/{config_id}')