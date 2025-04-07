"""
This module provides functionality for managing test cases in TestRail.
Test cases are the fundamental building blocks for test management.
"""
from typing import Optional, Dict, Any, List
from .base import BaseAPI

class CasesAPI(BaseAPI):
    """
    API for managing TestRail test cases.
    """
    
    def get_case(self, case_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a test case by ID.
        
        Args:
            case_id: The ID of the test case to retrieve.
            
        Returns:
            Dict containing the test case data.
        """
        return self._api_request('GET', f'get_case/{case_id}')
    
    def get_cases(self, project_id: int, suite_id: Optional[int] = None,
                 section_id: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all test cases for a project and optionally a specific suite or section.
        
        Args:
            project_id: The ID of the project to get test cases for.
            suite_id: Optional ID of the suite to get test cases for.
            section_id: Optional ID of the section to get test cases for.
            
        Returns:
            List of dictionaries containing test case data.
        """
        endpoint = f'get_cases/{project_id}'
        if suite_id:
            endpoint += f'&suite_id={suite_id}'
        if section_id:
            endpoint += f'&section_id={section_id}'
        return self._api_request('GET', endpoint)
    
    def add_case(self, section_id: int, title: str, template_id: Optional[int] = None,
                 type_id: Optional[int] = None, priority_id: Optional[int] = None,
                 estimate: Optional[str] = None, milestone_id: Optional[int] = None,
                 refs: Optional[str] = None, description: Optional[str] = None,
                 preconditions: Optional[str] = None, postconditions: Optional[str] = None,
                 custom_fields: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
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
        data = {
            'title': title
        }
        if template_id:
            data['template_id'] = template_id
        if type_id:
            data['type_id'] = type_id
        if priority_id:
            data['priority_id'] = priority_id
        if estimate:
            data['estimate'] = estimate
        if milestone_id:
            data['milestone_id'] = milestone_id
        if refs:
            data['refs'] = refs
        if description:
            data['description'] = description
        if preconditions:
            data['preconditions'] = preconditions
        if postconditions:
            data['postconditions'] = postconditions
        if custom_fields:
            data.update(custom_fields)
            
        return self._api_request('POST', f'add_case/{section_id}', data=data)
    
    def update_case(self, case_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update a test case.
        
        Args:
            case_id: The ID of the test case to update.
            **kwargs: The fields to update (title, template_id, type_id, priority_id, etc.).
            
        Returns:
            Dict containing the updated test case data.
        """
        return self._api_request('POST', f'update_case/{case_id}', data=kwargs)
    
    def delete_case(self, case_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a test case.
        
        Args:
            case_id: The ID of the test case to delete.
            
        Returns:
            Dict containing the response data.
        """
        return self._api_request('POST', f'delete_case/{case_id}')
    
    def get_case_fields(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all available test case fields.
        
        Returns:
            List of dictionaries containing test case field data.
        """
        return self._api_request('GET', 'get_case_fields')