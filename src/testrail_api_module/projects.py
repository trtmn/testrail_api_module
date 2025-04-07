"""
This module provides functionality for managing projects in TestRail.
Projects are the top-level containers for test cases, suites, and other test management entities.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class ProjectsAPI(BaseAPI):
    """
    API for managing TestRail projects.
    """
    
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a project by ID.
        
        Args:
            project_id (int): The ID of the project to retrieve.
            
        Returns:
            dict: The project data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_project/{project_id}')
    
    def get_projects(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all projects.
        
        Returns:
            list: List of projects if successful, None otherwise.
        """
        return self._api_request('GET', 'get_projects')
    
    def add_project(self, name: str, announcement: Optional[str] = None,
                   show_announcement: bool = False, is_completed: bool = False) -> Optional[Dict[str, Any]]:
        """
        Add a new project.
        
        Args:
            name (str): The name of the project.
            announcement (str, optional): The announcement text for the project.
            show_announcement (bool, optional): Whether to show the announcement.
            is_completed (bool, optional): Whether the project is completed.
                
        Returns:
            dict: The created project data if successful, None otherwise.
        """
        data = {
            'name': name,
            'show_announcement': show_announcement,
            'is_completed': is_completed
        }
        if announcement:
            data['announcement'] = announcement
            
        return self._api_request('POST', 'add_project', data=data)
    
    def update_project(self, project_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a project.
        
        Args:
            project_id (int): The ID of the project to update.
            **kwargs: The fields to update (name, announcement, show_announcement, is_completed).
            
        Returns:
            dict: The updated project data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_project/{project_id}', data=kwargs)
    
    def delete_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a project.
        
        Args:
            project_id (int): The ID of the project to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_project/{project_id}')
    
    def get_project_stats(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a project.
        
        Args:
            project_id (int): The ID of the project to get statistics for.
            
        Returns:
            dict: The project statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_project_stats/{project_id}')
    
    def get_project_activity(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get the activity log for a project.
        
        Args:
            project_id (int): The ID of the project to get activity for.
            
        Returns:
            list: List of activity entries if successful, None otherwise.
        """
        return self._api_request('GET', f'get_project_activity/{project_id}')
    
    def get_project_attachments(self, project_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all attachments for a project.
        
        Args:
            project_id (int): The ID of the project to get attachments for.
            
        Returns:
            list: List of attachments if successful, None otherwise.
        """
        return self._api_request('GET', f'get_project_attachments/{project_id}')
    
    def add_project_attachment(self, project_id: int, file_path: str,
                             description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Add an attachment to a project.
        
        Args:
            project_id (int): The ID of the project to add the attachment to.
            file_path (str): The path to the file to attach.
            description (str, optional): The description of the attachment.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        data = {
            'file': file_path
        }
        if description:
            data['description'] = description
            
        return self._api_request('POST', f'add_project_attachment/{project_id}', data=data)