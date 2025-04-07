"""
This module provides functionality for managing shared steps in TestRail.
Shared steps are reusable test steps that can be referenced by multiple test cases.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class SharedStepsAPI(BaseAPI):
    """
    API for managing TestRail shared steps.
    """
    
    def get_shared_step(self, shared_step_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a shared step by ID.
        
        Args:
            shared_step_id: The ID of the shared step to retrieve.
            
        Returns:
            Dict containing the shared step data.
        """
        return self._api_request('GET', f'get_shared_step/{shared_step_id}')
    
    def get_shared_steps(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all shared steps for a project.
        
        Args:
            project_id: The ID of the project to get shared steps for.
            
        Returns:
            List of dictionaries containing shared step data.
        """
        return self._api_request('GET', f'get_shared_steps/{project_id}')
    
    def add_shared_step(self, project_id: int, title: str, steps: List[Dict[str, Any]],
                       description: Optional[str] = None) -> Optional[Dict[str, Any]]:
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
        data = {
            'title': title,
            'steps': steps
        }
        if description:
            data['description'] = description
            
        return self._api_request('POST', f'add_shared_step/{project_id}', data=data)
    
    def update_shared_step(self, shared_step_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a shared step.
        
        Args:
            shared_step_id: The ID of the shared step to update.
            **kwargs: The fields to update (title, steps, description).
            
        Returns:
            Dict containing the updated shared step data.
        """
        return self._api_request('POST', f'update_shared_step/{shared_step_id}', data=kwargs)
    
    def delete_shared_step(self, shared_step_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a shared step.
        
        Args:
            shared_step_id: The ID of the shared step to delete.
            
        Returns:
            Dict containing the response data.
        """
        return self._api_request('POST', f'delete_shared_step/{shared_step_id}')