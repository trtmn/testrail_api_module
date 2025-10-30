"""
This module provides functionality for managing sections in TestRail.
Sections are used to organize test cases into hierarchical structures.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

__all__ = ['SectionsAPI']

class SectionsAPI(BaseAPI):
    """
    API for managing TestRail sections.
    
    This class provides methods to create, read, update, and delete sections
    in TestRail, following the official TestRail API patterns.
    """
    
    def get_section(self, section_id: int) -> Dict[str, Any]:
        """
        Get a section by ID.
        
        Args:
            section_id: The ID of the section to retrieve.
            
        Returns:
            Dict containing the section data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> section = api.sections.get_section(123)
            >>> print(f"Section: {section['name']}")
        """
        return self._get(f'get_section/{section_id}')
    
    def get_sections(self, project_id: int, suite_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all sections for a project and optionally a specific suite.
        
        Args:
            project_id: The ID of the project to get sections for.
            suite_id: Optional ID of the suite to get sections for.
            
        Returns:
            List of dictionaries containing section data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> sections = api.sections.get_sections(project_id=1, suite_id=2)
            >>> for section in sections:
            ...     print(f"Section: {section['name']}")
        """
        params = {}
        if suite_id is not None:
            params['suite_id'] = suite_id
            
        return self._get(f'get_sections/{project_id}', params=params)
    
    def add_section(self, project_id: int, name: str, description: Optional[str] = None,
                   suite_id: Optional[int] = None, parent_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Add a new section.
        
        Args:
            project_id: The ID of the project to add the section to.
            name: The name of the section.
            description: Optional description of the section.
            suite_id: Optional ID of the suite to add the section to.
            parent_id: Optional ID of the parent section.
            
        Returns:
            Dict containing the created section data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> section = api.sections.add_section(
            ...     project_id=1,
            ...     name="New Section",
            ...     description="A new test section",
            ...     suite_id=2,
            ...     parent_id=5
            ... )
        """
        data = {'name': name}
        
        # Add optional fields only if they are provided
        optional_fields = {
            'description': description,
            'suite_id': suite_id,
            'parent_id': parent_id
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
            
        return self._post(f'add_section/{project_id}', data=data)
    
    def update_section(self, section_id: int, name: Optional[str] = None,
                     description: Optional[str] = None, parent_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Update a section.
        
        Args:
            section_id: The ID of the section to update.
            name: Optional new name for the section.
            description: Optional new description for the section.
            parent_id: Optional new parent section ID.
            
        Returns:
            Dict containing the updated section data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> updated_section = api.sections.update_section(
            ...     section_id=123,
            ...     name="Updated Section Name"
            ... )
        """
        data = {}
        
        # Add fields only if they are provided
        optional_fields = {
            'name': name,
            'description': description,
            'parent_id': parent_id
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
            
        return self._post(f'update_section/{section_id}', data=data)
    
    def delete_section(self, section_id: int) -> Dict[str, Any]:
        """
        Delete a section.
        
        Args:
            section_id: The ID of the section to delete.
            
        Returns:
            Dict containing the response data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.sections.delete_section(123)
        """
        return self._post(f'delete_section/{section_id}')
    
    def get_section_cases(self, section_id: int) -> List[Dict[str, Any]]:
        """
        Get all test cases in a section.
        
        Args:
            section_id: The ID of the section to get test cases for.
            
        Returns:
            List of dictionaries containing test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> cases = api.sections.get_section_cases(section_id=123)
            >>> for case in cases:
            ...     print(f"Case: {case['title']}")
        """
        return self._get(f'get_section_cases/{section_id}')
    
    def get_section_stats(self, section_id: int) -> Dict[str, Any]:
        """
        Get statistics for a section.
        
        Args:
            section_id: The ID of the section to get statistics for.
            
        Returns:
            Dict containing the section statistics.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> stats = api.sections.get_section_stats(123)
            >>> print(f"Total cases: {stats['total']}")
        """
        return self._get(f'get_section_stats/{section_id}')