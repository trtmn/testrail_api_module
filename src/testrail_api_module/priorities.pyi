from .base import BaseAPI as BaseAPI
from typing import Any

class PrioritiesAPI(BaseAPI):
    """
    API for managing TestRail priorities.
    """
    def get_priority(self, priority_id: int) -> dict[str, Any] | None:
        """
        Get a priority by ID.
        
        Args:
            priority_id (int): The ID of the priority to retrieve.
            
        Returns:
            dict: The priority data if successful, None otherwise.
        """
    def get_priorities(self) -> list[dict[str, Any]] | None:
        """
        Get all available priorities.
        
        Returns:
            list: List of priorities if successful, None otherwise.
        """
    def add_priority(self, name: str, short_name: str, color: str, is_default: bool = False) -> dict[str, Any] | None:
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
    def update_priority(self, priority_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a priority.
        
        Args:
            priority_id (int): The ID of the priority to update.
            **kwargs: The fields to update (name, short_name, color, is_default).
            
        Returns:
            dict: The updated priority data if successful, None otherwise.
        """
    def delete_priority(self, priority_id: int) -> dict[str, Any] | None:
        """
        Delete a priority.
        
        Args:
            priority_id (int): The ID of the priority to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_priority_counts(self, project_id: int) -> dict[str, int] | None:
        """
        Get the count of test cases by priority for a project.
        
        Args:
            project_id (int): The ID of the project to get priority counts for.
            
        Returns:
            dict: Dictionary mapping priority IDs to counts if successful, None otherwise.
        """
    def get_priority_stats(self, project_id: int) -> dict[str, Any] | None:
        """
        Get statistics about priorities in a project.
        
        Args:
            project_id (int): The ID of the project to get priority statistics for.
            
        Returns:
            dict: The priority statistics if successful, None otherwise.
        """
