from .base import BaseAPI
from typing import Any

__all__ = ['CasesAPI']

class CasesAPI(BaseAPI):
    """
    API for managing TestRail test cases.
    
    This class provides methods to create, read, update, and delete test cases
    in TestRail, following the official TestRail API patterns.
    """
    _case_fields_cache: list[dict[str, Any]] | None
    _case_fields_raw_cache: list[dict[str, Any]] | None
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize CasesAPI with field caches."""
    def get_case(self, case_id: int) -> dict[str, Any]:
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
    def get_cases(self, project_id: int, suite_id: int | None = None, section_id: int | None = None, created_after: int | None = None, created_before: int | None = None, created_by: int | list[int] | None = None, milestone_id: int | list[int] | None = None, priority_id: int | list[int] | None = None, type_id: int | list[int] | None = None, updated_after: int | None = None, updated_before: int | None = None, updated_by: int | list[int] | None = None, limit: int | None = None, offset: int | None = None) -> list[dict[str, Any]]:
        '''
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
            ...     print(f"Case {case[\'id\']}: {case[\'title\']}")
        '''
    def add_case(self, section_id: int, title: str, template_id: int | None = None, type_id: int | None = None, priority_id: int | None = None, estimate: str | None = None, milestone_id: int | None = None, refs: str | None = None, description: str | None = None, preconditions: str | None = None, postconditions: str | None = None, custom_fields: dict[str, Any] | None = None, validate_required: bool = False, validate_only: bool = False) -> dict[str, Any]:
        '''
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
            custom_fields: Optional custom field values. Should use system names
                (e.g., \'custom_field_name\') as keys, not display names.
                
                Common custom field types and formats:
                - Text fields: String values (e.g., custom_automation_type: "Automated")
                - Dropdown/Multi-select: Arrays of string IDs (e.g., custom_module: ["3", "5"])
                - Checkboxes: Boolean values (e.g., custom_case_test_data_required: True)
                - Separated steps: Array of objects with content/expected keys:
                    custom_steps_separated: [
                        {"content": "Step 1", "expected": "Result 1"},
                        {"content": "Step 2", "expected": "Result 2"}
                    ]
                
            validate_required: If True, validate that all required fields
                are provided before sending the request. Default is False (validation disabled).
                Set to True to enable validation and catch missing fields before API call.
                When False, TestRail API will handle validation and return errors.
            validate_only: If True, only validate the fields without creating the case.
                Returns validation results instead of making the API call.
                Useful for checking requirements before submission.
                
        Returns:
            Dict containing the created test case data, or validation results if validate_only=True.
            
            When validate_only=True, returns:
            {
                "valid": bool,  # True if all required fields are present
                "missing_fields": [...],  # List of missing required fields with type hints
                "provided_fields": [...],  # List of fields that were provided
                "message": str  # Human-readable validation summary
            }
            
        Raises:
            TestRailAPIError: If the API request fails.
            ValueError: If required fields are missing and validate_required is True.
            
        Note:
            Required fields vary by project configuration. Use get_case_fields() to see
            which fields are required and their expected data types for your project.
            Common required custom fields include:
            - custom_automation_type (string)
            - custom_steps_separated (array of step objects)
            - custom_case_test_data_required (boolean)
            - custom_interface_type (array of string IDs)
            - custom_module (array of string IDs)
            
        Example:
            >>> # Basic case with standard fields
            >>> case = api.cases.add_case(
            ...     section_id=1,
            ...     title="Login Test",
            ...     type_id=2,
            ...     priority_id=2,
            ...     description="Test user login functionality"
            ... )
            
            >>> # Case with custom fields
            >>> case = api.cases.add_case(
            ...     section_id=1,
            ...     title="Automated Login Test",
            ...     custom_fields={
            ...         \'custom_automation_type\': \'Automated\',
            ...         \'custom_steps_separated\': [
            ...             {\'content\': \'Navigate to login page\', \'expected\': \'Login form visible\'},
            ...             {\'content\': \'Enter credentials\', \'expected\': \'Login successful\'}
            ...         ],
            ...         \'custom_case_test_data_required\': True,
            ...         \'custom_interface_type\': [\'3\'],  # Array of IDs as strings
            ...         \'custom_module\': [\'5\', \'7\']  # Array of IDs as strings
            ...     }
            ... )
            
            >>> # Validate fields without creating the case
            >>> validation = api.cases.add_case(
            ...     section_id=1,
            ...     title="Test Case",
            ...     validate_only=True
            ... )
            >>> if not validation[\'valid\']:
            ...     print(validation[\'message\'])
            ...     print("Missing:", validation[\'missing_fields\'])
        '''
    def _is_missing_required_value(self, value: Any) -> bool:
        """
        Check whether a value should be treated as missing for a required field.

        Args:
            value: The value to validate.

        Returns:
            True if missing/empty, False otherwise.
        """
    def _validate_steps_separated(self, steps: list[dict[str, Any]]) -> bool:
        """
        Validate separated steps payload for stepped fields.

        Args:
            steps: List of step objects.

        Returns:
            True if steps look valid, False otherwise.
        """
    def _resolve_project_and_suite_from_section(self, section_id: int) -> tuple[int, int | None]:
        """
        Resolve project_id and suite_id from a section_id.

        Args:
            section_id: TestRail section ID where the case will be created.

        Returns:
            Tuple of (project_id, suite_id). suite_id may be None for single-suite
            mode depending on the TestRail instance.

        Raises:
            ValueError: If required context cannot be resolved.
        """
    def _resolve_effective_template_id(self, project_id: int, template_id: int | None) -> int | None:
        """
        Resolve the effective template_id used for case creation.

        If template_id is provided, it is used. Otherwise, this attempts to select
        the project's default template (when available).

        Args:
            project_id: Project ID.
            template_id: Optional template id supplied by the caller.

        Returns:
            The effective template_id or None if it cannot be resolved.
        """
    def _get_required_case_fields_for_context(self, project_id: int, suite_id: int | None, template_id: int | None, use_cache: bool = True) -> list[dict[str, Any]]:
        """
        Get required case fields for a specific creation context.

        Args:
            project_id: Project ID.
            suite_id: Optional suite ID.
            template_id: Optional template ID.
            use_cache: Whether to use cached field metadata.

        Returns:
            List of field dicts that are required in this context. Each item may
            include a helper key `_selected_config` when requirement comes from a
            specific config entry.
        """
    def _select_required_config_for_context(self, field: dict[str, Any], project_id: int, suite_id: int | None, template_id: int | None) -> dict[str, Any] | None:
        """
        Pick a required config for this field that applies to the given context.

        Returns the first matching required config (options.is_required=True).
        """
    def _config_applies_to_context(self, context: Any, project_id: int, suite_id: int | None, template_id: int | None) -> bool:
        """
        Determine if a TestRail field config context applies to this create-case context.

        This is intentionally defensive: some TestRail instances only provide
        is_global/project_ids, while others may also include suite_ids/template_ids.
        """
    def _extract_default_value(self, field_info: dict[str, Any]) -> Any:
        """
        Extract default_value for a field from the selected config (preferred) or
        from the first config/options if present.
        """
    def _apply_default_value(self, data: dict[str, Any], field_info: dict[str, Any], default_value: Any) -> bool:
        """
        Apply a default value to the request payload for a required field, when safe.
        """
    def _get_required_case_fields(self, use_cache: bool = True) -> list[dict[str, Any]]:
        """
        Get list of required case fields from TestRail with caching.
        
        Args:
            use_cache: If True (default), use cached field data if available.
                      If False, always fetch fresh data from the API.
        
        Returns:
            List of field dictionaries, filtered to only include required fields.
            
        Raises:
            Exception: If unable to fetch case fields from TestRail API.
                      This ensures validation failures are explicit rather than silently bypassed.
        """
    def _get_case_fields_raw(self, use_cache: bool = True) -> list[dict[str, Any]]:
        """
        Get raw case fields from TestRail with caching.

        Args:
            use_cache: Whether to use cached raw field metadata.

        Returns:
            List of field dictionaries from get_case_fields().
        """
    def clear_case_fields_cache(self) -> None:
        """
        Clear the cached case field requirements.
        
        Use this if your project configuration changes and you need to
        refresh the field requirements.
        """
    def get_required_case_fields(self, project_id: int | None = None, suite_id: int | None = None, template_id: int | None = None, section_id: int | None = None, use_cache: bool = True) -> dict[str, Any]:
        '''
        Get required case fields for creating test cases, optionally filtered by project.
        
        This method queries TestRail to determine which fields are required when creating
        a new test case. Field requirements can vary by project configuration.
        
        Args:
            project_id: Optional project ID to filter requirements. If provided, only returns
                       fields required for that specific project. If None, returns all required
                       fields across all projects.
            use_cache: Whether to use cached field data (default: True). Set to False to
                      fetch fresh data from TestRail API.
        
        Returns:
            Dictionary with required field information:
            {
                "required_fields": [
                    {
                        "system_name": "custom_automation_type",
                        "label": "Automation Type",
                        "type_id": 1,
                        "type_name": "String",
                        "type_hint": "string",
                        "is_global": True,
                        "project_ids": None,
                        "description": "The automation type for the test case"
                    },
                    ...
                ],
                "field_count": 5,
                "project_filtered": True/False,
                "cache_used": True/False
            }
            
        Raises:
            Exception: If unable to fetch case fields from TestRail API.
            
        Example:
            >>> # Get all required fields
            >>> result = api.cases.get_required_case_fields()
            >>> print(f"Found {result[\'field_count\']} required fields")
            >>> for field in result[\'required_fields\']:
            ...     print(f"  {field[\'system_name\']}: {field[\'type_hint\']}")
            
            >>> # Get required fields for a specific project
            >>> result = api.cases.get_required_case_fields(project_id=1)
            >>> print(f"Project 1 requires {result[\'field_count\']} fields")
        '''
    def get_field_options(self, field_name: str, use_cache: bool = True) -> dict[str, Any]:
        '''
        Get valid options for a specific custom field.
        
        This method returns the complete list of valid options for dropdown,
        multi-select, and other fields that have predefined choices. Useful
        for discovering what values are valid before creating test cases.
        
        Args:
            field_name: The system name of the field (e.g., \'custom_automation_type\',
                       \'custom_interface_type\'). Can be specified with or without
                       the \'custom_\' prefix.
            use_cache: Whether to use cached field data (default: True).
        
        Returns:
            Dictionary with field options:
            {
                "field_name": "custom_automation_type",
                "label": "Automation Type",
                "type_id": 6,
                "type_name": "Dropdown",
                "options": [
                    {"id": "0", "label": "None"},
                    {"id": "1", "label": "Selenium C#"},
                    ...
                ],
                "is_required": True,
                "default_value": "0",
                "format_hint": "Use the \'id\' value (e.g., \'1\' for \'Selenium C#\')"
            }
            
        Raises:
            ValueError: If the field is not found.
            
        Example:
            >>> options = api.cases.get_field_options(\'custom_automation_type\')
            >>> print(f"Valid values for {options[\'label\']}:")
            >>> for opt in options[\'options\']:
            ...     print(f"  {opt[\'id\']}: {opt[\'label\']}")
        '''
    def _get_field_type_hint(self, type_id: int | None, field_name: str, field_info: dict[str, Any] | None = None) -> str:
        """
        Get a helpful type hint for a field based on its type ID and config.
        
        Args:
            type_id: The TestRail field type ID.
            field_name: The field name for additional context.
            field_info: Optional full field dictionary with configs for dynamic hints.
            
        Returns:
            Human-readable type hint string with valid options when available.
        """
    def _extract_field_options(self, field_info: dict[str, Any]) -> str | None:
        """
        Extract valid options from a field's config.
        
        Args:
            field_info: Full field dictionary from get_case_fields().
            
        Returns:
            Formatted string of valid options, or None if no options found.
        """
    def _get_steps_hint(self, field_info: dict[str, Any] | None) -> str:
        """
        Generate hint for step-type fields based on config options.
        
        Args:
            field_info: Full field dictionary from get_case_fields().
            
        Returns:
            Formatted hint string for step fields.
        """
    def _get_field_type_name(self, type_id: int | None) -> str:
        """
        Map TestRail type ID to human-readable type name.
        
        Args:
            type_id: The TestRail field type ID.
            
        Returns:
            Human-readable type name string.
        """
    def update_case(self, case_id: int, title: str | None = None, template_id: int | None = None, type_id: int | None = None, priority_id: int | None = None, estimate: str | None = None, milestone_id: int | None = None, refs: str | None = None, description: str | None = None, preconditions: str | None = None, postconditions: str | None = None, custom_fields: dict[str, Any] | None = None) -> dict[str, Any]:
        '''
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
        '''
    def delete_case(self, case_id: int) -> dict[str, Any]:
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
    def get_case_fields(self) -> list[dict[str, Any]]:
        '''
        Get all available test case fields.
        
        Returns:
            List of dictionaries containing test case field data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> fields = api.cases.get_case_fields()
            >>> for field in fields:
            ...     print(f"Field: {field[\'name\']}, Type: {field[\'type\']}")
        '''
    def get_case_types(self) -> list[dict[str, Any]]:
        '''
        Get all available test case types.
        
        Returns:
            List of dictionaries containing test case type data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> types = api.cases.get_case_types()
            >>> for case_type in types:
            ...     print(f"Type {case_type[\'id\']}: {case_type[\'name\']}")
        '''
    def get_case_history(self, case_id: int) -> list[dict[str, Any]]:
        '''
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
            ...     print(f"Changed by {change[\'user\']} on {change[\'created_on\']}")
        '''
    def copy_cases_to_section(self, case_ids: list[int], section_id: int) -> list[dict[str, Any]]:
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
    def move_cases_to_section(self, case_ids: list[int], section_id: int) -> list[dict[str, Any]]:
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
