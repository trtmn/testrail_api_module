from .base import BaseAPI as BaseAPI
from typing import Any

class SectionsAPI(BaseAPI):
    """
    API for managing TestRail sections.
    """
    def get_section(self, section_id: int) -> dict[str, Any] | None:
        """
        Get a section by ID.
        
        Args:
            section_id (int): The ID of the section to retrieve.
            
        Returns:
            dict: The section data if successful, None otherwise.
        """
    def get_sections(self, project_id: int, suite_id: int | None = None) -> list[dict[str, Any]] | None:
        """
        Get all sections for a project and optionally a specific suite.
        
        Args:
            project_id (int): The ID of the project to get sections for.
            suite_id (int, optional): The ID of the suite to get sections for.
            
        Returns:
            list: List of sections if successful, None otherwise.
        """
    def add_section(self, project_id: int, name: str, description: str | None = None, suite_id: int | None = None, parent_id: int | None = None) -> dict[str, Any] | None:
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
    def update_section(self, section_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a section.
        
        Args:
            section_id (int): The ID of the section to update.
            **kwargs: The fields to update (name, description, parent_id).
            
        Returns:
            dict: The updated section data if successful, None otherwise.
        """
    def delete_section(self, section_id: int) -> dict[str, Any] | None:
        """
        Delete a section.
        
        Args:
            section_id (int): The ID of the section to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_section_cases(self, section_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test cases in a section.
        
        Args:
            section_id (int): The ID of the section to get test cases for.
            
        Returns:
            list: List of test cases if successful, None otherwise.
        """
    def get_section_stats(self, section_id: int) -> dict[str, Any] | None:
        """
        Get statistics for a section.
        
        Args:
            section_id (int): The ID of the section to get statistics for.
            
        Returns:
            dict: The section statistics if successful, None otherwise.
        """
