"""
This module provides functionality for managing sections in TestRail.
Sections are used to organize test cases into hierarchical structures.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class SectionsAPI(BaseAPI):
    """
    API for managing TestRail sections.
    """
    
    def get_section(self, section_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a section by ID.
        
        Args:
            section_id (int): The ID of the section to retrieve.
            
        Returns:
            dict: The section data if successful, None otherwise.
        """
        return self._api_request('GET', f'get_section/{section_id}')
    
    def get_sections(self, project_id: int, suite_id: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all sections for a project and optionally a specific suite.
        
        Args:
            project_id (int): The ID of the project to get sections for.
            suite_id (int, optional): The ID of the suite to get sections for.
            
        Returns:
            list: List of sections if successful, None otherwise.
        """
        endpoint = f'get_sections/{project_id}'
        if suite_id:
            endpoint += f'&suite_id={suite_id}'
        return self._api_request('GET', endpoint)
    
    def add_section(self, project_id: int, name: str, description: Optional[str] = None,
                   suite_id: Optional[int] = None, parent_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Add a new section.
        
        Args:
            project_id (int): The ID of the project to add the section to.
            name (str): The name of the section.
            description (str, optional): The description of the section.
            suite_id (int, optional): The ID of the suite to add the section to.
            parent_id (int, optional): The ID of the parent section.
                
        Returns:
            dict: The created section data if successful, None otherwise.
        """
        data = {
            'name': name
        }
        if description:
            data['description'] = description
        if suite_id:
            data['suite_id'] = suite_id
        if parent_id:
            data['parent_id'] = parent_id
            
        return self._api_request('POST', f'add_section/{project_id}', data=data)
    
    def update_section(self, section_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a section.
        
        Args:
            section_id (int): The ID of the section to update.
            **kwargs: The fields to update (name, description, parent_id).
            
        Returns:
            dict: The updated section data if successful, None otherwise.
        """
        return self._api_request('POST', f'update_section/{section_id}', data=kwargs)
    
    def delete_section(self, section_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a section.
        
        Args:
            section_id (int): The ID of the section to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request('POST', f'delete_section/{section_id}')
    
    def get_section_cases(self, section_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test cases in a section.
        
        Args:
            section_id (int): The ID of the section to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
        return self._api_request('GET', f'get_section_cases/{section_id}')
    
    def get_section_stats(self, section_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a section.
        
        Args:
            section_id (int): The ID of the section to get statistics for.
            
        Returns:
            dict: The section statistics if successful, None otherwise.
        """
        return self._api_request('GET', f'get_section_stats/{section_id}')