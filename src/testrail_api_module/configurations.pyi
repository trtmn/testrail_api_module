from .base import BaseAPI as BaseAPI
from typing import Any

class ConfigurationsAPI(BaseAPI):
    """
    API for managing TestRail configurations.
    """
    def get_configuration(self, config_id: int) -> dict[str, Any] | None:
        """
        Get a configuration by ID.
        
        Args:
            config_id: The ID of the configuration to retrieve.
            
        Returns:
            Dict containing the configuration data.
        """
    def get_configurations(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all configurations for a project.
        
        Args:
            project_id: The ID of the project to get configurations for.
            
        Returns:
            List of dictionaries containing configuration data.
        """
    def add_configuration(self, project_id: int, name: str, description: str | None = None, group_id: int | None = None) -> dict[str, Any] | None:
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
    def update_configuration(self, config_id: int, **kwargs: Any) -> dict[str, Any] | None:
        """
        Update a configuration.
        
        Args:
            config_id: The ID of the configuration to update.
            **kwargs: The fields to update (name, description, group_id).
            
        Returns:
            Dict containing the updated configuration data.
        """
    def delete_configuration(self, config_id: int) -> dict[str, Any] | None:
        """
        Delete a configuration.
        
        Args:
            config_id: The ID of the configuration to delete.
            
        Returns:
            Dict containing the response data.
        """
