"""
This module provides functionality for managing test cases in TestRail.
Test cases are the fundamental building blocks for test management.
"""
from typing import Optional, Dict, Any, List, Union
from .base import BaseAPI

__all__ = ['CasesAPI']

class CasesAPI(BaseAPI):
    """
    API for managing TestRail test cases.
    
    This class provides methods to create, read, update, and delete test cases
    in TestRail, following the official TestRail API patterns.
    """
    
    def get_case(self, case_id: int) -> Dict[str, Any]:
        """
        Get a test case by ID.
        
        Args:
            case_id: The ID of the test case to retrieve.
            
        Returns:
            Dict containing the test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> case = api.cases.get_case(123)
            >>> print(case['title'])
        """
        return self._get(f'get_case/{case_id}')
    
    def get_cases(self, project_id: int, suite_id: Optional[int] = None,
                 section_id: Optional[int] = None, 
                 created_after: Optional[int] = None,
                 created_before: Optional[int] = None,
                 created_by: Optional[Union[int, List[int]]] = None,
                 milestone_id: Optional[Union[int, List[int]]] = None,
                 priority_id: Optional[Union[int, List[int]]] = None,
                 type_id: Optional[Union[int, List[int]]] = None,
                 updated_after: Optional[int] = None,
                 updated_before: Optional[int] = None,
                 updated_by: Optional[Union[int, List[int]]] = None,
                 limit: Optional[int] = None,
                 offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all test cases for a project and optionally a specific suite or section.
        
        Args:
            project_id: The ID of the project to get test cases for.
            suite_id: Optional ID of the suite to get test cases for.
            section_id: Optional ID of the section to get test cases for.
            created_after: Optional timestamp to filter cases created after this time.
            created_before: Optional timestamp to filter cases created before this time.
            created_by: Optional user ID(s) to filter cases created by specific users.
            milestone_id: Optional milestone ID(s) to filter cases by milestone.
            priority_id: Optional priority ID(s) to filter cases by priority.
            type_id: Optional type ID(s) to filter cases by type.
            updated_after: Optional timestamp to filter cases updated after this time.
            updated_before: Optional timestamp to filter cases updated before this time.
            updated_by: Optional user ID(s) to filter cases updated by specific users.
            limit: Optional limit on number of results to return.
            offset: Optional offset for pagination.
            
        Returns:
            List of dictionaries containing test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> cases = api.cases.get_cases(project_id=1, suite_id=2)
            >>> for case in cases:
            ...     print(f"Case {case['id']}: {case['title']}")
        """
        params = {}
        if suite_id is not None:
            params['suite_id'] = suite_id
        if section_id is not None:
            params['section_id'] = section_id
        if created_after is not None:
            params['created_after'] = created_after
        if created_before is not None:
            params['created_before'] = created_before
        if created_by is not None:
            params['created_by'] = created_by
        if milestone_id is not None:
            params['milestone_id'] = milestone_id
        if priority_id is not None:
            params['priority_id'] = priority_id
        if type_id is not None:
            params['type_id'] = type_id
        if updated_after is not None:
            params['updated_after'] = updated_after
        if updated_before is not None:
            params['updated_before'] = updated_before
        if updated_by is not None:
            params['updated_by'] = updated_by
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        return self._get(f'get_cases/{project_id}', params=params)
    
    def add_case(self, section_id: int, title: str, template_id: Optional[int] = None,
                 type_id: Optional[int] = None, priority_id: Optional[int] = None,
                 estimate: Optional[str] = None, milestone_id: Optional[int] = None,
                 refs: Optional[str] = None, description: Optional[str] = None,
                 preconditions: Optional[str] = None, postconditions: Optional[str] = None,
                 custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a new test case.
        
        Args:
            section_id: The ID of the section to add the test case to.
            title: The title of the test case.
            template_id: Optional ID of the template to use.
            type_id: Optional type of test case:
                1: Other, 2: Functional, 3: Performance, 4: Usability, 5: Security, 6: Compliance
            priority_id: Optional priority of the test case:
                1: Critical, 2: High, 3: Medium, 4: Low
            estimate: Optional estimated time to complete the test.
            milestone_id: Optional ID of the milestone to add the test case to.
            refs: Optional references or requirements.
            description: Optional description of the test case.
            preconditions: Optional preconditions for the test case.
            postconditions: Optional postconditions for the test case.
            custom_fields: Optional custom field values.
                
        Returns:
            Dict containing the created test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> case = api.cases.add_case(
            ...     section_id=1,
            ...     title="Login Test",
            ...     type_id=2,
            ...     priority_id=2,
            ...     description="Test user login functionality"
            ... )
        """
        data = {'title': title}
        
        # Add optional fields only if they are provided
        optional_fields = {
            'template_id': template_id,
            'type_id': type_id,
            'priority_id': priority_id,
            'estimate': estimate,
            'milestone_id': milestone_id,
            'refs': refs,
            'description': description,
            'preconditions': preconditions,
            'postconditions': postconditions
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
        
        # Add custom fields
        if custom_fields:
            data.update(custom_fields)
            
        return self._post(f'add_case/{section_id}', data=data)
    
    def update_case(self, case_id: int, title: Optional[str] = None,
                   template_id: Optional[int] = None, type_id: Optional[int] = None,
                   priority_id: Optional[int] = None, estimate: Optional[str] = None,
                   milestone_id: Optional[int] = None, refs: Optional[str] = None,
                   description: Optional[str] = None, preconditions: Optional[str] = None,
                   postconditions: Optional[str] = None,
                   custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update a test case.
        
        Args:
            case_id: The ID of the test case to update.
            title: Optional new title for the test case.
            template_id: Optional new template ID.
            type_id: Optional new type ID.
            priority_id: Optional new priority ID.
            estimate: Optional new estimate.
            milestone_id: Optional new milestone ID.
            refs: Optional new references.
            description: Optional new description.
            preconditions: Optional new preconditions.
            postconditions: Optional new postconditions.
            custom_fields: Optional custom field values to update.
            
        Returns:
            Dict containing the updated test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> updated_case = api.cases.update_case(
            ...     case_id=123,
            ...     title="Updated Login Test",
            ...     priority_id=1
            ... )
        """
        data = {}
        
        # Add fields only if they are provided
        optional_fields = {
            'title': title,
            'template_id': template_id,
            'type_id': type_id,
            'priority_id': priority_id,
            'estimate': estimate,
            'milestone_id': milestone_id,
            'refs': refs,
            'description': description,
            'preconditions': preconditions,
            'postconditions': postconditions
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
        
        # Add custom fields
        if custom_fields:
            data.update(custom_fields)
            
        return self._post(f'update_case/{case_id}', data=data)
    
    def delete_case(self, case_id: int) -> Dict[str, Any]:
        """
        Delete a test case.
        
        Args:
            case_id: The ID of the test case to delete.
            
        Returns:
            Dict containing the response data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.cases.delete_case(123)
        """
        return self._post(f'delete_case/{case_id}')
    
    def get_case_fields(self) -> List[Dict[str, Any]]:
        """
        Get all available test case fields.
        
        Returns:
            List of dictionaries containing test case field data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> fields = api.cases.get_case_fields()
            >>> for field in fields:
            ...     print(f"Field: {field['name']}, Type: {field['type']}")
        """
        return self._get('get_case_fields')
    
    def get_case_types(self) -> List[Dict[str, Any]]:
        """
        Get all available test case types.
        
        Returns:
            List of dictionaries containing test case type data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> types = api.cases.get_case_types()
            >>> for case_type in types:
            ...     print(f"Type {case_type['id']}: {case_type['name']}")
        """
        return self._get('get_case_types')
    
    def get_case_history(self, case_id: int) -> List[Dict[str, Any]]:
        """
        Get the change history of a test case.
        
        Args:
            case_id: The ID of the test case to get history for.
            
        Returns:
            List of dictionaries containing change history data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> history = api.cases.get_case_history(123)
            >>> for change in history:
            ...     print(f"Changed by {change['user']} on {change['created_on']}")
        """
        return self._get(f'get_case_history/{case_id}')
    
    def copy_cases_to_section(self, case_ids: List[int], section_id: int) -> List[Dict[str, Any]]:
        """
        Copy test cases to a different section.
        
        Args:
            case_ids: List of test case IDs to copy.
            section_id: The ID of the target section.
            
        Returns:
            List of dictionaries containing the copied test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> copied_cases = api.cases.copy_cases_to_section([1, 2, 3], 5)
        """
        data = {'case_ids': case_ids}
        return self._post(f'copy_cases_to_section/{section_id}', data=data)
    
    def move_cases_to_section(self, case_ids: List[int], section_id: int) -> List[Dict[str, Any]]:
        """
        Move test cases to a different section.
        
        Args:
            case_ids: List of test case IDs to move.
            section_id: The ID of the target section.
            
        Returns:
            List of dictionaries containing the moved test case data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> moved_cases = api.cases.move_cases_to_section([1, 2, 3], 5)
        """
        data = {'case_ids': case_ids}
        return self._post(f'move_cases_to_section/{section_id}', data=data)