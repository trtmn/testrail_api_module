from .base import BaseAPI
from typing import Any

__all__ = ['SectionsAPI']

class SectionsAPI(BaseAPI):
    """
    API for managing TestRail sections.
    
    This class provides methods to create, read, update, and delete sections
    in TestRail, following the official TestRail API patterns.
    """
    def get_section(self, section_id: int) -> dict[str, Any]:
        '''
        Get a section by ID.
        
        Args:
            section_id: The ID of the section to retrieve.
            
        Returns:
            Dict containing the section data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> section = api.sections.get_section(123)
            >>> print(f"Section: {section[\'name\']}")
        '''
    def get_sections(self, project_id: int, suite_id: int | None = None) -> list[dict[str, Any]]:
        '''
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
            ...     print(f"Section: {section[\'name\']}")
        '''
    def add_section(self, project_id: int, name: str, description: str | None = None, suite_id: int | None = None, parent_id: int | None = None) -> dict[str, Any]:
        '''
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
        '''
    def update_section(self, section_id: int, name: str | None = None, description: str | None = None, parent_id: int | None = None) -> dict[str, Any]:
        '''
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
        '''
    def delete_section(self, section_id: int) -> dict[str, Any]:
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
    def get_section_cases(self, section_id: int) -> list[dict[str, Any]]:
        '''
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
            ...     print(f"Case: {case[\'title\']}")
        '''
    def get_section_stats(self, section_id: int) -> dict[str, Any]:
        '''
        Get statistics for a section.
        
        Args:
            section_id: The ID of the section to get statistics for.
            
        Returns:
            Dict containing the section statistics.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> stats = api.sections.get_section_stats(123)
            >>> print(f"Total cases: {stats[\'total\']}")
        '''
