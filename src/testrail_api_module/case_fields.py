# src/testrail_api_module/case_fields.py
"""
This module provides functionalities to interact with test case fields in TestRail.
"""
from . import _common
_api = _common.ApiConstructor()

def get_case_fields():
    """
    Get all available test case fields.

    Returns:
        list: A list of dictionaries containing the details of each test case field.
    """
    return _api.api_request('GET', 'get_case_fields')

def add_case_field(field_type, name, label, description=None, include_all=False, template_ids=None, configs=None):
    """
    Create a new test case custom field.

    Args:
        field_type (str): The type identifier for the new custom field.
        name (str): The name for the new custom field.
        label (str): The label for the new custom field.
        description (str, optional): The description for the new custom field.
        include_all (bool, optional): Flag to include the new custom field for all templates.
        template_ids (list, optional): IDs of templates the new custom field will apply to if include_all is False.
        configs (list, optional): A list of configuration objects for the new custom field.

    Returns:
        dict: The response from the API.
    """
    data = {
        "type": field_type,
        "name": name,
        "label": label,
        "description": description,
        "include_all": include_all,
        "template_ids": template_ids,
        "configs": configs
    }
    return _api.api_request('POST', 'add_case_field', data)