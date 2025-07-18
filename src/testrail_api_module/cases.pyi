from .base import BaseAPI as BaseAPI
from typing import Any

class CasesAPI(BaseAPI):
    """
    API for managing TestRail test cases.
    """
    def get_case(self, case_id: int) -> dict[str, Any] | None:
        """
        Get a test case by ID.
        
        Args:
            case_id: The ID of the test case to retrieve.
            
        Returns:
            Dict containing the test case data.
        """
    def get_cases(self, project_id: int, suite_id: int | None = None, section_id: int | None = None) -> list[dict[str, Any]] | None:
        """
        Get all test cases for a project and optionally a specific suite or section.
        
        Args:
            project_id: The ID of the project to get test cases for.
            suite_id: Optional ID of the suite to get test cases for.
            section_id: Optional ID of the section to get test cases for.
            
        Returns:
            List of dictionaries containing test case data.
        """
    def add_case(self, section_id: int, title: str, template_id: int | None = None, type_id: int | None = None, priority_id: int | None = None, estimate: str | None = None, milestone_id: int | None = None, refs: str | None = None, description: str | None = None, preconditions: str | None = None, postconditions: str | None = None, custom_fields: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """
        Add a new test case.
        
        Args:
            section_id: The ID of the section to add the test case to.
            title: The title of the test case.
            template_id: Optional ID of the template to use.
            type_id: Optional type of test case:
                1: Other
                2: Functional
                3: Performance
                4: Usability
                5: Security
                6: Compliance
            priority_id: Optional priority of the test case:
                1: Critical
                2: High
                3: Medium
                4: Low
            estimate: Optional estimated time to complete the test.
            milestone_id: Optional ID of the milestone to add the test case to.
            refs: Optional references or requirements.
            description: Optional description of the test case.
            preconditions: Optional preconditions for the test case.
            postconditions: Optional postconditions for the test case.
            custom_fields: Optional custom field values.
                
        Returns:
            Dict containing the created test case data.
        """
    def update_case(self, case_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a test case.
        
        Args:
            case_id: The ID of the test case to update.
            **kwargs: The fields to update (title, template_id, type_id, priority_id, etc.).
            
        Returns:
            Dict containing the updated test case data.
        """
    def delete_case(self, case_id: int) -> dict[str, Any] | None:
        """
        Delete a test case.
        
        Args:
            case_id: The ID of the test case to delete.
            
        Returns:
            Dict containing the response data.
        """
    def get_case_fields(self) -> list[dict[str, Any]] | None:
        """
        Get all available test case fields.
        
        Returns:
            List of dictionaries containing test case field data.
        """
