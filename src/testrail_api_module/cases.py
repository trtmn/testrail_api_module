"""
This module provides functionality for managing test cases in TestRail.
Test cases are the fundamental building blocks for test management.
"""
from __future__ import annotations

from typing import Optional, Dict, Any, List, Union, Tuple
from .base import BaseAPI

__all__ = ['CasesAPI']

class CasesAPI(BaseAPI):
    """
    API for managing TestRail test cases.
    
    This class provides methods to create, read, update, and delete test cases
    in TestRail, following the official TestRail API patterns.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize CasesAPI with field caches."""
        super().__init__(*args, **kwargs)
        # Cache of *required* case fields (derived from get_case_fields()).
        # NOTE: Required-ness is context dependent (project/template/suite). This cache
        # stores fields that are required in *any* context, plus their configs so we
        # can re-evaluate required-ness for a specific context later.
        self._case_fields_cache: Optional[List[Dict[str, Any]]] = None
        # Cache of raw get_case_fields() response (all fields).
        self._case_fields_raw_cache: Optional[List[Dict[str, Any]]] = None
    
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
                 custom_fields: Optional[Dict[str, Any]] = None,
                 validate_required: bool = False,
                 validate_only: bool = False) -> Dict[str, Any]:
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
            custom_fields: Optional custom field values. Should use system names
                (e.g., 'custom_field_name') as keys, not display names.
                
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
            ...         'custom_automation_type': 'Automated',
            ...         'custom_steps_separated': [
            ...             {'content': 'Navigate to login page', 'expected': 'Login form visible'},
            ...             {'content': 'Enter credentials', 'expected': 'Login successful'}
            ...         ],
            ...         'custom_case_test_data_required': True,
            ...         'custom_interface_type': ['3'],  # Array of IDs as strings
            ...         'custom_module': ['5', '7']  # Array of IDs as strings
            ...     }
            ... )
            
            >>> # Validate fields without creating the case
            >>> validation = api.cases.add_case(
            ...     section_id=1,
            ...     title="Test Case",
            ...     validate_only=True
            ... )
            >>> if not validation['valid']:
            ...     print(validation['message'])
            ...     print("Missing:", validation['missing_fields'])
        """
        # Build the data dictionary with standard fields
        self.logger.debug(f"add_case called: section_id={section_id}, title={title}, validate_required={validate_required}")
        data: Dict[str, Any] = {'title': title}
        
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
        
        # Add custom fields - these should use system names as keys
        if custom_fields:
            self.logger.debug(f"Adding {len(custom_fields)} custom fields to data: {list(custom_fields.keys())}")
            data.update(custom_fields)
            self.logger.debug(f"Custom fields added. Sample values: {[(k, type(v).__name__, v) for k, v in list(custom_fields.items())[:3]]}")
        else:
            self.logger.debug("No custom fields provided")
        
        self.logger.debug(f"Data prepared for API call: {list(data.keys())}")
        self.logger.debug(f"Full data dict (for debugging): {data}")
        
        # Validate required fields if requested
        if validate_required or validate_only:
            self.logger.debug(f"Validating required fields for add_case (validate_required={validate_required}, validate_only={validate_only})")
            try:
                # Resolve context (project/suite/template) so we validate the right set of
                # required fields for this section and template.
                project_id, suite_id = self._resolve_project_and_suite_from_section(
                    section_id=section_id
                )
                effective_template_id = self._resolve_effective_template_id(
                    project_id=project_id,
                    template_id=template_id,
                )

                required_fields = self._get_required_case_fields_for_context(
                    project_id=project_id,
                    suite_id=suite_id,
                    template_id=effective_template_id,
                )
                self.logger.debug(
                    "Found %s required fields to validate for context "
                    "(project_id=%s, suite_id=%s, template_id=%s)",
                    len(required_fields),
                    project_id,
                    suite_id,
                    effective_template_id,
                )
                # Log all required field names for debugging
                required_field_names = [
                    f.get('system_name') or f.get('name') 
                    for f in required_fields 
                    if (f.get('system_name') or f.get('name')) and (f.get('system_name') or f.get('name')) != 'title'
                ]
                self.logger.debug(
                    "Required field names to check: %s",
                    required_field_names
                )
                self.logger.debug(
                    "Fields available in data dict: %s",
                    list(data.keys())
                )
                missing_fields = []
                provided_fields = []
                field_type_hints = []

                # Try to auto-apply defaults for required fields when TestRail provides
                # a default_value for that field in this context.
                for field_info in required_fields:
                    field_name = field_info.get('system_name') or field_info.get('name')
                    if not field_name or field_name == 'title':
                        continue
                    if field_name in data and not self._is_missing_required_value(
                        data.get(field_name)
                    ):
                        continue
                    default_value = self._extract_default_value(field_info)
                    if default_value is None:
                        continue
                    applied = self._apply_default_value(
                        data=data,
                        field_info=field_info,
                        default_value=default_value,
                    )
                    if applied:
                        self.logger.debug(
                            "Applied default for required field %s (type_id=%s)",
                            field_name,
                            field_info.get("type_id"),
                        )

                for field_info in required_fields:
                    field_name = field_info.get('system_name') or field_info.get('name')
                    if not field_name:
                        self.logger.debug(f"Skipping field with no name: {field_info}")
                        continue

                    # Standard fields that are always required (like title) are already handled
                    if field_name == 'title':
                        continue

                    # Check for field value in data dict
                    field_value = data.get(field_name)
                    
                    # Fallback: if field not found in data and we have custom_fields parameter,
                    # check there as well (shouldn't be necessary after data.update, but helps debug)
                    if field_value is None and custom_fields and field_name in custom_fields:
                        field_value = custom_fields[field_name]
                        self.logger.debug(
                            "Field %s found in custom_fields parameter but not in data dict - using from custom_fields",
                            field_name
                        )
                        # Add it to data for consistency
                        data[field_name] = field_value
                    
                    field_type = field_info.get('type_id')
                    
                    # Build field description with type information (dynamic hints)
                    field_desc = f"'{field_name}'"
                    type_hint = self._get_field_type_hint(
                        field_type, field_name, field_info
                    )
                    if type_hint:
                        field_desc += f" ({type_hint})"
                    
                    # Log field detection for debugging
                    self.logger.debug(
                        "Checking required field: name=%s, type_id=%s, value=%s, value_type=%s, in_data=%s",
                        field_name,
                        field_type,
                        field_value,
                        type(field_value).__name__ if field_value is not None else 'None',
                        field_name in data
                    )
                    
                    is_missing = self._is_missing_required_value(field_value)

                    if is_missing:
                        self.logger.debug(
                            "Field %s is missing (value=%s, in_data=%s)",
                            field_name,
                            field_value,
                            field_name in data
                        )
                        # Only add the base field description for missing fields
                        # Do NOT append step validation text to non-step fields
                        missing_fields.append(field_desc)
                    else:
                        # Additional validation ONLY for stepped/separated steps (type_id == 12)
                        # This validation message should ONLY apply to step fields
                        if field_type == 12 and isinstance(field_value, list):
                            if not self._validate_steps_separated(field_value):
                                # Only append step validation text for actual step fields
                                missing_fields.append(
                                    f"{field_desc} (must include at least one step with non-empty "
                                    "'content' and 'expected')"
                                )
                                continue
                        # For all other field types, if the value is present and valid, mark as provided
                        self.logger.debug(
                            "Field %s is present and valid (value type=%s, value=%s)",
                            field_name,
                            type(field_value).__name__,
                            field_value,
                        )
                        provided_fields.append(field_desc)
                
                # If validate_only, return validation results without making API call
                if validate_only:
                    is_valid = len(missing_fields) == 0
                    if is_valid:
                        message = f"✓ All {len(provided_fields)} required fields are present and valid."
                    else:
                        message = f"✗ Missing {len(missing_fields)} required field(s). Please provide all required fields."
                    
                    self.logger.debug(f"Validation only mode: valid={is_valid}, missing={len(missing_fields)}")
                    return {
                        "valid": is_valid,
                        "missing_fields": missing_fields,
                        "provided_fields": provided_fields,
                        "message": message,
                        "total_required": len(required_fields),
                        "field_type_guide": {
                            "text": "String values",
                            "dropdown_multiselect": "Arrays of string IDs (e.g., ['3', '5'])",
                            "checkbox": "Boolean values (True/False)",
                            "steps": "Array of objects with 'content' and 'expected' keys"
                        },
                        "context": {
                            "project_id": project_id,
                            "suite_id": suite_id,
                            "template_id": effective_template_id,
                        },
                    }
                
                # For regular validation (not validate_only), raise error if fields missing
                if missing_fields:
                    self.logger.debug(f"Validation failed: {len(missing_fields)} required fields are missing")
                    # Build comprehensive error message
                    error_parts = [
                        f"Missing required field(s): {', '.join(missing_fields)}.",
                        "",
                        f"Context used for validation: project_id={project_id}, suite_id={suite_id}, template_id={effective_template_id}.",
                        "",
                        "Field type guide:",
                        "  - Text fields: String values",
                        "  - Dropdown/Multi-select: Arrays of string IDs (e.g., ['3', '5'])",
                        "  - Checkboxes: Boolean values (True/False)",
                        "  - Separated steps: Array of step objects with 'content' and 'expected' keys",
                        "    Example: [{'content': 'Step 1', 'expected': 'Result 1'}]",
                        "",
                        "Use get_case_fields() to see complete field requirements and types for your project.",
                        "",
                        "Note: Custom fields must be nested in the 'custom_fields' parameter.",
                        "      Use system names (e.g., 'custom_field_name') as keys, not display names."
                    ]
                    raise ValueError('\n'.join(error_parts))
                else:
                    self.logger.debug("Validation passed: all required fields are present")
            except ValueError:
                # Re-raise ValueError directly (validation errors from missing fields)
                raise
            except Exception as e:
                # For any other exception during validation, treat it as a validation failure
                # Don't silently bypass validation - fail explicitly to prevent API errors
                error_msg = (
                    f"Field validation failed: {type(e).__name__}: {e}\n\n"
                    f"Cannot create test case without validating required fields.\n"
                    f"Common causes:\n"
                    f"  - Unable to fetch field definitions from TestRail API\n"
                    f"  - Network connectivity issues\n"
                    f"  - Invalid API credentials\n\n"
                    f"Please verify your TestRail connection and try again."
                )
                self.logger.error(f"Validation error: {error_msg}", exc_info=True)
                raise ValueError(error_msg) from e
            
        return self._post(f'add_case/{section_id}', data=data)
    
    def _is_missing_required_value(self, value: Any) -> bool:
        """
        Check whether a value should be treated as missing for a required field.

        Args:
            value: The value to validate.

        Returns:
            True if missing/empty, False otherwise.
        """
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, list) and len(value) == 0:
            return True
        return False

    def _validate_steps_separated(self, steps: List[Dict[str, Any]]) -> bool:
        """
        Validate separated steps payload for stepped fields.

        Args:
            steps: List of step objects.

        Returns:
            True if steps look valid, False otherwise.
        """
        if not steps:
            return False
        for step in steps:
            if not isinstance(step, dict):
                return False
            content = step.get("content")
            expected = step.get("expected")
            if not isinstance(content, str) or not content.strip():
                return False
            if not isinstance(expected, str) or not expected.strip():
                return False
        return True

    def _resolve_project_and_suite_from_section(
        self,
        section_id: int,
    ) -> Tuple[int, Optional[int]]:
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
        try:
            section = self.client.sections.get_section(section_id=section_id)
        except Exception as e:
            raise ValueError(
                f"Unable to resolve section context for section_id={section_id}: {e}"
            ) from e

        project_id = section.get("project_id")
        suite_id = section.get("suite_id")

        if suite_id is not None and not isinstance(suite_id, int):
            suite_id = None

        # If section doesn't include project_id directly, resolve it from suite
        if not isinstance(project_id, int):
            if suite_id is None:
                raise ValueError(
                    f"Section {section_id} did not include a valid project_id and has "
                    "no suite_id to resolve project context."
                )

            try:
                suite = self.client.suites.get_suite(suite_id=suite_id)
            except Exception as e:
                raise ValueError(
                    f"Unable to resolve suite context for suite_id={suite_id}: {e}"
                ) from e

            suite_project_id = suite.get("project_id")
            if not isinstance(suite_project_id, int):
                raise ValueError(
                    f"Suite {suite_id} did not include a valid project_id: "
                    f"{suite_project_id!r}"
                )
            project_id = suite_project_id

        return project_id, suite_id

    def _resolve_effective_template_id(
        self,
        project_id: int,
        template_id: Optional[int],
    ) -> Optional[int]:
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
        if template_id is not None:
            return template_id

        try:
            templates = self.client.templates.get_templates(project_id=project_id)
        except Exception:
            return None

        if not templates:
            return None

        for tmpl in templates:
            if tmpl.get("is_default") is True and isinstance(tmpl.get("id"), int):
                return tmpl["id"]

        # Fallback: use the first template if available.
        first_id = templates[0].get("id") if isinstance(templates[0], dict) else None
        return first_id if isinstance(first_id, int) else None

    def _get_required_case_fields_for_context(
        self,
        project_id: int,
        suite_id: Optional[int],
        template_id: Optional[int],
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
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
        required_any = self._get_required_case_fields(use_cache=use_cache)
        required_for_context: List[Dict[str, Any]] = []

        for field in required_any:
            field_name = field.get("system_name") or field.get("name")
            if not field_name:
                continue
            # Title is always required and already provided via signature.
            if field_name == "title":
                required_for_context.append(field)
                continue

            if field.get("is_required") is True and not field.get("configs"):
                # Legacy/top-level required (no configs to evaluate)
                required_for_context.append(field)
                continue

            selected_config = self._select_required_config_for_context(
                field=field,
                project_id=project_id,
                suite_id=suite_id,
                template_id=template_id,
            )
            if selected_config is not None:
                enhanced = field.copy()
                enhanced["_selected_config"] = selected_config
                required_for_context.append(enhanced)

        return required_for_context

    def _select_required_config_for_context(
        self,
        field: Dict[str, Any],
        project_id: int,
        suite_id: Optional[int],
        template_id: Optional[int],
    ) -> Optional[Dict[str, Any]]:
        """
        Pick a required config for this field that applies to the given context.

        Returns the first matching required config (options.is_required=True).
        """
        configs = field.get("configs", [])
        if not isinstance(configs, list) or not configs:
            return None

        for config in configs:
            if not isinstance(config, dict):
                continue
            options = config.get("options", {})
            if not isinstance(options, dict) or options.get("is_required") is not True:
                continue
            context = config.get("context", {})
            if self._config_applies_to_context(
                context=context,
                project_id=project_id,
                suite_id=suite_id,
                template_id=template_id,
            ):
                return config

        return None

    def _config_applies_to_context(
        self,
        context: Any,
        project_id: int,
        suite_id: Optional[int],
        template_id: Optional[int],
    ) -> bool:
        """
        Determine if a TestRail field config context applies to this create-case context.

        This is intentionally defensive: some TestRail instances only provide
        is_global/project_ids, while others may also include suite_ids/template_ids.
        """
        if not isinstance(context, dict):
            return False

        if context.get("is_global") is True:
            return True

        project_ids = context.get("project_ids")
        if isinstance(project_ids, list) and project_ids and project_id not in project_ids:
            return False

        suite_ids = context.get("suite_ids")
        if isinstance(suite_ids, list) and suite_ids:
            if suite_id is None or suite_id not in suite_ids:
                return False

        template_ids = context.get("template_ids")
        if isinstance(template_ids, list) and template_ids:
            if template_id is None or template_id not in template_ids:
                return False

        return True

    def _extract_default_value(self, field_info: Dict[str, Any]) -> Any:
        """
        Extract default_value for a field from the selected config (preferred) or
        from the first config/options if present.
        """
        selected = field_info.get("_selected_config")
        if isinstance(selected, dict):
            options = selected.get("options", {})
            if isinstance(options, dict) and "default_value" in options:
                return options.get("default_value")

        configs = field_info.get("configs", [])
        if isinstance(configs, list):
            for config in configs:
                if not isinstance(config, dict):
                    continue
                options = config.get("options", {})
                if isinstance(options, dict) and "default_value" in options:
                    return options.get("default_value")

        return None

    def _apply_default_value(
        self,
        data: Dict[str, Any],
        field_info: Dict[str, Any],
        default_value: Any,
    ) -> bool:
        """
        Apply a default value to the request payload for a required field, when safe.
        """
        field_name = field_info.get("system_name") or field_info.get("name")
        if not isinstance(field_name, str) or not field_name:
            return False

        type_id = field_info.get("type_id")

        # Don't override an explicitly provided value.
        if field_name in data and not self._is_missing_required_value(data.get(field_name)):
            return False

        # Normalize common default formats based on field type.
        if type_id in (6, 11):
            # Dropdown / Multi-select: TestRail often uses comma-separated string ids.
            if isinstance(default_value, str):
                parts = [p.strip() for p in default_value.split(",") if p.strip()]
                if parts:
                    data[field_name] = parts
                    return True
            if isinstance(default_value, list) and default_value:
                data[field_name] = default_value
                return True
            return False

        if type_id == 5:
            # Checkbox: default can be "1"/"0" or boolean.
            if isinstance(default_value, bool):
                data[field_name] = default_value
                return True
            if isinstance(default_value, str):
                if default_value.strip() in {"1", "true", "True"}:
                    data[field_name] = True
                    return True
                if default_value.strip() in {"0", "false", "False"}:
                    data[field_name] = False
                    return True
            return False

        if type_id == 2:
            if isinstance(default_value, int):
                data[field_name] = default_value
                return True
            if isinstance(default_value, str) and default_value.strip().isdigit():
                data[field_name] = int(default_value.strip())
                return True
            return False

        # For text/string/url/user/etc., default_value can be applied directly if non-empty.
        if isinstance(default_value, str) and default_value.strip():
            data[field_name] = default_value
            return True

        return False

    def _get_required_case_fields(self, use_cache: bool = True) -> List[Dict[str, Any]]:
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
        # Check cache first - only use if not None and has been populated
        # Note: We check for None explicitly, not empty list, because an empty list
        # means we fetched and there really are no required fields (which is valid)
        if use_cache and self._case_fields_cache is not None:
            self.logger.debug(f"Using cached case fields ({len(self._case_fields_cache)} fields)")
            # If cache is empty, log a warning but still return it (it means no required fields)
            if len(self._case_fields_cache) == 0:
                self.logger.warning(
                    "Cached field requirements are empty. This means either:\n"
                    "  1. Your TestRail project has no required fields (unusual), OR\n"
                    "  2. The cache was populated with empty data due to an API error.\n"
                    "  Call clear_case_fields_cache() to refresh if this seems wrong."
                )
            return self._case_fields_cache
        
        self.logger.debug("Fetching case fields from TestRail API")
        all_fields = self._get_case_fields_raw(use_cache=use_cache)
        self.logger.debug(f"Retrieved {len(all_fields)} total case fields from API")
        
        # Check if we got any fields at all
        if len(all_fields) == 0:
            self.logger.warning(
                "get_case_fields() returned 0 fields. This is unusual and may indicate:\n"
                "  1. API connection issues\n"
                "  2. Invalid project configuration\n"
                "  3. Missing permissions\n"
                "Will NOT cache this empty result to allow retry."
            )
            # Don't cache empty results from API errors - return empty but don't cache
            return []
        
        # Filter required fields - check BOTH top-level is_required AND configs
        required_fields = []
        for field in all_fields:
            field_name = field.get('system_name') or field.get('name')
            is_required = False
            required_configs: List[Dict[str, Any]] = []
            
            # Check top-level is_required flag (for backwards compatibility)
            if field.get('is_required', False):
                is_required = True
                self.logger.debug(f"  Field {field_name}: required via top-level flag")
            
            # CRITICAL: Also check configs array for project/template-specific requirements
            # TestRail returns required field info in configs[].options.is_required
            configs = field.get('configs', [])
            if isinstance(configs, list) and configs:
                for config in configs:
                    if not isinstance(config, dict):
                        continue
                    options = config.get('options', {})
                    if isinstance(options, dict) and options.get('is_required', False):
                        is_required = True
                        required_configs.append(config)
                        context = config.get('context', {})
                        context_type = (
                            context.get('is_global', False) if isinstance(context, dict) else None
                        )
                        project_ids = (
                            context.get('project_ids', []) if isinstance(context, dict) else []
                        )
                        self.logger.debug(
                            f"  Field {field_name}: required via config "
                            f"(global={context_type}, projects={project_ids})"
                        )
            
            if is_required:
                enhanced_field = field.copy()
                # Ensure downstream validation can treat this as required even if the
                # top-level field flag is False.
                enhanced_field['is_required'] = True
                if required_configs:
                    enhanced_field['_required_configs'] = required_configs
                required_fields.append(enhanced_field)
        
        self.logger.debug(f"Filtered to {len(required_fields)} required fields")
        for field in required_fields:
            field_name = field.get('system_name') or field.get('name')
            self.logger.debug(f"  Required: {field_name} (type_id={field.get('type_id')})")
        
        # Cache the results for future calls (even if empty - it's valid to have no required fields)
        self._case_fields_cache = required_fields
        self.logger.debug(f"Cached {len(required_fields)} required fields for future use")
        
        return required_fields

    def _get_case_fields_raw(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get raw case fields from TestRail with caching.

        Args:
            use_cache: Whether to use cached raw field metadata.

        Returns:
            List of field dictionaries from get_case_fields().
        """
        if use_cache and self._case_fields_raw_cache is not None:
            self.logger.debug(
                "Using cached raw case fields (%s fields)",
                len(self._case_fields_raw_cache),
            )
            return self._case_fields_raw_cache

        all_fields = self.get_case_fields()
        if not isinstance(all_fields, list):
            # Defensive: older wrappers might return dicts; normalize to empty list.
            all_fields = []
        # Only cache non-empty results. Empty responses are usually an error state and
        # we want to allow retry.
        if all_fields:
            self._case_fields_raw_cache = all_fields
        return all_fields
    
    def clear_case_fields_cache(self) -> None:
        """
        Clear the cached case field requirements.
        
        Use this if your project configuration changes and you need to
        refresh the field requirements.
        """
        self.logger.debug("Clearing case fields cache")
        self._case_fields_cache = None
        self._case_fields_raw_cache = None
    
    def get_required_case_fields(
        self,
        project_id: Optional[int] = None,
        suite_id: Optional[int] = None,
        template_id: Optional[int] = None,
        section_id: Optional[int] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
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
            >>> print(f"Found {result['field_count']} required fields")
            >>> for field in result['required_fields']:
            ...     print(f"  {field['system_name']}: {field['type_hint']}")
            
            >>> # Get required fields for a specific project
            >>> result = api.cases.get_required_case_fields(project_id=1)
            >>> print(f"Project 1 requires {result['field_count']} fields")
        """
        self.logger.debug(
            "get_required_case_fields called: project_id=%s, suite_id=%s, template_id=%s, "
            "section_id=%s, use_cache=%s",
            project_id,
            suite_id,
            template_id,
            section_id,
            use_cache,
        )

        # If section_id is provided, derive project_id/suite_id from it (unless explicitly
        # provided), and resolve default template if needed.
        resolved_project_id = project_id
        resolved_suite_id = suite_id
        if section_id is not None:
            sec_project_id, sec_suite_id = self._resolve_project_and_suite_from_section(
                section_id=section_id
            )
            if resolved_project_id is None:
                resolved_project_id = sec_project_id
            if resolved_suite_id is None:
                resolved_suite_id = sec_suite_id

        resolved_template_id = template_id
        if resolved_project_id is not None:
            resolved_template_id = self._resolve_effective_template_id(
                project_id=resolved_project_id,
                template_id=template_id,
            )
        
        # Check if cache was used BEFORE calling _get_required_case_fields
        cache_was_used = use_cache and self._case_fields_cache is not None
        
        # Get all required fields (with enhanced config context)
        all_required_fields = self._get_required_case_fields(use_cache=use_cache)
        self.logger.debug(f"Retrieved {len(all_required_fields)} required fields from cache/API")
        
        # Filter by context if provided
        filtered_fields = []
        for field in all_required_fields:
            field_name = field.get('system_name') or field.get('name')
            
            # If no context filter, include all required fields
            if resolved_project_id is None:
                # Attach a representative required config (if any) for metadata.
                selected_any = None
                if isinstance(field.get("configs"), list) and field.get("configs"):
                    for cfg in field.get("configs", []):
                        if not isinstance(cfg, dict):
                            continue
                        options = cfg.get("options", {})
                        if isinstance(options, dict) and options.get("is_required") is True:
                            selected_any = cfg
                            break
                if selected_any is not None:
                    enhanced = field.copy()
                    enhanced["_selected_config"] = selected_any
                    filtered_fields.append(enhanced)
                else:
                    filtered_fields.append(field)
                continue
            
            # Legacy/top-level required without configs always applies.
            if field.get('is_required', False) and not field.get('configs'):
                self.logger.debug(f"  Including {field_name}: top-level required flag")
                filtered_fields.append(field)
                continue

            # Otherwise, include if ANY required config applies to this context.
            selected = self._select_required_config_for_context(
                field=field,
                project_id=resolved_project_id,
                suite_id=resolved_suite_id,
                template_id=resolved_template_id,
            )
            if selected is not None:
                enhanced = field.copy()
                enhanced["_selected_config"] = selected
                filtered_fields.append(enhanced)
            else:
                self.logger.debug(
                    "  Excluding %s: no required config matched "
                    "(project_id=%s, suite_id=%s, template_id=%s)",
                    field_name,
                    resolved_project_id,
                    resolved_suite_id,
                    resolved_template_id,
                )
        
        self.logger.debug(
            "Filtered to %s fields for context (project_id=%s, suite_id=%s, template_id=%s)",
            len(filtered_fields),
            resolved_project_id,
            resolved_suite_id,
            resolved_template_id,
        )
        
        # Format the response
        formatted_fields = []
        for field in filtered_fields:
            field_name = field.get('system_name') or field.get('name')
            type_id = field.get('type_id')
            
            # Extract config context info
            matching_config = field.get('_selected_config')
            is_global = None
            project_ids = None
            if matching_config:
                context = matching_config.get('context', {})
                is_global = context.get('is_global', False)
                project_ids = context.get('project_ids')
            
            formatted_field = {
                'system_name': field_name,
                'label': field.get('label') or field.get('name') or field_name,
                'type_id': type_id,
                'type_name': self._get_field_type_name(type_id),
                'type_hint': self._get_field_type_hint(type_id, field_name, field),
                'is_global': is_global,
                'project_ids': project_ids,
                'description': field.get('description', '')
            }
            formatted_fields.append(formatted_field)
        
        return {
            'required_fields': formatted_fields,
            'field_count': len(formatted_fields),
            'project_filtered': resolved_project_id is not None,
            'cache_used': cache_was_used
        }
    
    def get_field_options(
        self,
        field_name: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get valid options for a specific custom field.
        
        This method returns the complete list of valid options for dropdown,
        multi-select, and other fields that have predefined choices. Useful
        for discovering what values are valid before creating test cases.
        
        Args:
            field_name: The system name of the field (e.g., 'custom_automation_type',
                       'custom_interface_type'). Can be specified with or without
                       the 'custom_' prefix.
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
                "format_hint": "Use the 'id' value (e.g., '1' for 'Selenium C#')"
            }
            
        Raises:
            ValueError: If the field is not found.
            
        Example:
            >>> options = api.cases.get_field_options('custom_automation_type')
            >>> print(f"Valid values for {options['label']}:")
            >>> for opt in options['options']:
            ...     print(f"  {opt['id']}: {opt['label']}")
        """
        # Normalize field name
        if not field_name.startswith('custom_'):
            field_name = f'custom_{field_name}'
        
        # Get all fields
        all_fields = self._get_case_fields_raw(use_cache=use_cache)
        
        # Find the requested field
        target_field = None
        for field in all_fields:
            sys_name = field.get('system_name') or field.get('name')
            if sys_name == field_name:
                target_field = field
                break
        
        if target_field is None:
            available = [
                f.get('system_name') or f.get('name')
                for f in all_fields
                if (f.get('system_name') or f.get('name', '')).startswith('custom_')
            ]
            raise ValueError(
                f"Field '{field_name}' not found. Available custom fields: "
                f"{', '.join(sorted(available))}"
            )
        
        type_id = target_field.get('type_id')
        label = target_field.get('label') or field_name
        
        # Extract options from configs
        configs = target_field.get('configs', [])
        config = configs[0] if isinstance(configs, list) and configs else {}
        options_dict = config.get('options', {}) if isinstance(config, dict) else {}
        
        is_required = options_dict.get('is_required', False)
        default_value = options_dict.get('default_value')
        items_str = options_dict.get('items', '')
        
        # Parse items
        parsed_options = []
        if items_str and isinstance(items_str, str):
            for line in items_str.strip().split('\n'):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',', 1)
                if len(parts) >= 2:
                    parsed_options.append({
                        'id': parts[0].strip(),
                        'label': parts[1].strip()
                    })
                elif len(parts) == 1 and parts[0].strip():
                    parsed_options.append({
                        'id': parts[0].strip(),
                        'label': parts[0].strip()
                    })
        
        # Generate format hint based on type
        if type_id == 6:
            format_hint = (
                "Single value: use the 'id' as a string "
                f"(e.g., '{parsed_options[0]['id']}' for '{parsed_options[0]['label']}')"
                if parsed_options else "Single string ID"
            )
        elif type_id in (11, 12):
            format_hint = (
                "Array of IDs: use 'id' values as integers in an array "
                f"(e.g., [{parsed_options[0]['id']}] for '{parsed_options[0]['label']}')"
                if parsed_options else "Array of integer IDs"
            )
        elif type_id == 10:
            format_hint = (
                "Array of step objects: [{'content': '...', 'expected': '...'}]"
            )
        elif type_id == 5:
            format_hint = "Boolean: True or False"
        elif type_id == 3:
            format_hint = "Text string (can be multi-line)"
        else:
            format_hint = self._get_field_type_hint(type_id, field_name, target_field)
        
        return {
            'field_name': field_name,
            'label': label,
            'type_id': type_id,
            'type_name': self._get_field_type_name(type_id),
            'options': parsed_options,
            'is_required': is_required,
            'default_value': default_value,
            'format_hint': format_hint,
            'description': target_field.get('description', '')
        }
    
    def _get_field_type_hint(
        self,
        type_id: Optional[int],
        field_name: str,
        field_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get a helpful type hint for a field based on its type ID and config.
        
        Args:
            type_id: The TestRail field type ID.
            field_name: The field name for additional context.
            field_info: Optional full field dictionary with configs for dynamic hints.
            
        Returns:
            Human-readable type hint string with valid options when available.
        """
        # TestRail field type IDs:
        # 1: String, 2: Integer, 3: Text (multi-line), 4: URL, 5: Checkbox,
        # 6: Dropdown, 7: User, 8: Date, 9: Milestone, 10: Steps, 11: Multi-select, 12: Stepped
        
        base_hints = {
            1: "string",
            2: "integer",
            3: "text",
            4: "URL string",
            5: "boolean (True/False)",
            6: "string ID",
            7: "user ID (integer)",
            8: "timestamp (Unix epoch)",
            9: "milestone ID (integer)",
            10: "array of step objects: [{'content': '...', 'expected': '...'}]",
            11: "array of IDs",
            12: "array of IDs",
        }
        
        hint = base_hints.get(type_id, "unknown")
        
        # Try to extract valid options from field config
        if field_info:
            options = self._extract_field_options(field_info)
            if options:
                if type_id == 6:
                    # Dropdown (single select) - show valid options
                    hint = f"string ID from: {options}"
                elif type_id in (11, 12):
                    # Multi-select or Stepped with items - show valid options
                    hint = f"array of IDs from: {options}"
                elif type_id == 10:
                    # Steps field - check for has_expected
                    hint = self._get_steps_hint(field_info)
        
        # Override for known step fields regardless of options
        if type_id == 10 or 'steps_separated' in field_name:
            hint = self._get_steps_hint(field_info) if field_info else (
                "array of step objects: [{'content': '...', 'expected': '...'}]"
            )
        
        return hint
    
    def _extract_field_options(self, field_info: Dict[str, Any]) -> Optional[str]:
        """
        Extract valid options from a field's config.
        
        Args:
            field_info: Full field dictionary from get_case_fields().
            
        Returns:
            Formatted string of valid options, or None if no options found.
        """
        configs = field_info.get('configs', [])
        if not isinstance(configs, list) or not configs:
            return None
        
        # Check the selected config first, then fall back to first config
        selected_config = field_info.get('_selected_config')
        config = selected_config if selected_config else (
            configs[0] if configs else None
        )
        
        if not isinstance(config, dict):
            return None
        
        options = config.get('options', {})
        if not isinstance(options, dict):
            return None
        
        items_str = options.get('items')
        if not items_str or not isinstance(items_str, str):
            return None
        
        # Parse items format: "id,label\nid,label\n..."
        parsed_options = []
        for line in items_str.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', 1)
            if len(parts) >= 2:
                item_id = parts[0].strip()
                item_label = parts[1].strip()
                parsed_options.append(f"{item_id}={item_label}")
            elif len(parts) == 1 and parts[0].strip():
                parsed_options.append(parts[0].strip())
        
        if not parsed_options:
            return None
        
        # Limit to first 5 options for readability, with ellipsis if more
        if len(parsed_options) > 5:
            display = parsed_options[:5] + [f"... ({len(parsed_options)} total)"]
        else:
            display = parsed_options
        
        return '{' + ', '.join(display) + '}'
    
    def _get_steps_hint(self, field_info: Optional[Dict[str, Any]]) -> str:
        """
        Generate hint for step-type fields based on config options.
        
        Args:
            field_info: Full field dictionary from get_case_fields().
            
        Returns:
            Formatted hint string for step fields.
        """
        base_hint = "array of step objects"
        example_parts = ["'content': '...'", "'expected': '...'"]
        
        if field_info:
            configs = field_info.get('configs', [])
            selected_config = field_info.get('_selected_config')
            config = selected_config if selected_config else (
                configs[0] if isinstance(configs, list) and configs else None
            )
            
            if isinstance(config, dict):
                options = config.get('options', {})
                if isinstance(options, dict):
                    # Check which fields are enabled
                    has_expected = options.get('has_expected', True)
                    has_additional = options.get('has_additional', False)
                    has_reference = options.get('has_reference', False)
                    
                    example_parts = ["'content': '...'"]
                    if has_expected:
                        example_parts.append("'expected': '...'")
                    if has_additional:
                        example_parts.append("'additional_info': '...'")
                    if has_reference:
                        example_parts.append("'refs': '...'")
        
        return f"{base_hint}: [" + "{" + ", ".join(example_parts) + "}]"
    
    def _get_field_type_name(self, type_id: Optional[int]) -> str:
        """
        Map TestRail type ID to human-readable type name.
        
        Args:
            type_id: The TestRail field type ID.
            
        Returns:
            Human-readable type name string.
        """
        type_names = {
            1: "String",
            2: "Integer",
            3: "Text",
            4: "URL",
            5: "Checkbox",
            6: "Dropdown",
            7: "User",
            8: "Date",
            9: "Milestone",
            10: "Steps",
            11: "Multi-select",
            12: "Stepped"
        }
        return type_names.get(type_id, "Unknown")
    
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