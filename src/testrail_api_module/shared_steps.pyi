from .base import BaseAPI as BaseAPI
from typing import Any

class SharedStepsAPI(BaseAPI):
    """
    API for managing TestRail shared steps.
    """
    def get_shared_step(self, shared_step_id: int) -> dict[str, Any] | None:
        """
        Get a shared step by ID.
        
        Args:
            shared_step_id: The ID of the shared step to retrieve.
            
        Returns:
            Dict containing the shared step data.
        """
    def get_shared_steps(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all shared steps for a project.
        
        Args:
            project_id: The ID of the project to get shared steps for.
            
        Returns:
            List of dictionaries containing shared step data.
        """
    def add_shared_step(self, project_id: int, title: str, steps: list[dict[str, Any]], description: str | None = None) -> dict[str, Any] | None:
        """
        Add a new shared step.
        
        Args:
            project_id: The ID of the project to add the shared step to.
            title: The title of the shared step.
            steps: List of dictionaries containing step data.
            description: Optional description of the shared step.
                
        Returns:
            Dict containing the created shared step data.
        """
    def update_shared_step(self, shared_step_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a shared step.
        
        Args:
            shared_step_id: The ID of the shared step to update.
            **kwargs: The fields to update (title, steps, description).
            
        Returns:
            Dict containing the updated shared step data.
        """
    def delete_shared_step(self, shared_step_id: int) -> dict[str, Any] | None:
        """
        Delete a shared step.
        
        Args:
            shared_step_id: The ID of the shared step to delete.
            
        Returns:
            Dict containing the response data.
        """
