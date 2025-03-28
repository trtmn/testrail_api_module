from . import _common
_api = _common.ApiConstructor()


def add_case(section_id, title, template_id=None, type_id=None, priority_id=None, estimate=None, milestone_id=None, refs=None):
    """
    Add a new test case to  a specific section.

    Args:
        section_id (str): The ID of the section.
        title (str): The title of the test case.
        template_id (int, optional): The ID of the template.
        type_id (int, optional): The ID of the type.
        priority_id (int, optional): The ID of the priority.
        estimate (str, optional): The estimate for the test case.
        milestone_id (int, optional): The ID of the milestone.
        refs (str, optional): A comma-separated list of references.

    Returns:
        dict: The response from the API.
    """
    data = {
        "title": title,
        "template_id": template_id,
        "type_id": type_id,
        "priority_id": priority_id,
        "estimate": estimate,
        "milestone_id": milestone_id,
        "refs": refs
    }
    return _api.api_request('POST', f'add_case/{section_id}', data)

def get_case(case_id):
    """
    Get details of a specific test case.

    Args:
        case_id (str): The ID of the test case.

    Returns:
        dict: The response from the API.
    """
    return _api.api_request('GET', f'get_case/{case_id}')

def get_cases(project_id, suite_id=None, section_id=None, filters=None):
    """
    Get all test cases for a specific project, optionally filtered by suite, section, and other filters.

    Args:
        project_id (str): The ID of the project.
        suite_id (str, optional): The ID of the suite.
        section_id (str, optional): The ID of the section.
        filters (dict, optional): Additional filters for the request.

    Returns:
        list: A list of dictionaries containing the details of each test case.
    """
    endpoint = f'get_cases/{project_id}'
    if suite_id:
        endpoint += f'&suite_id={suite_id}'
    if section_id:
        endpoint += f'&section_id={section_id}'
    if filters:
        for key, value in filters.items():
            endpoint += f'&{key}={value}'
    return _api.api_request('GET', endpoint)

def update_case(case_id, title=None, template_id=None, type_id=None, priority_id=None, estimate=None, milestone_id=None, refs=None):
    """
    Update an existing test case.

    Args:
        case_id (str): The ID of the test case.
        title (str, optional): The title of the test case.
        template_id (int, optional): The ID of the template.
        type_id (int, optional): The ID of the type.
        priority_id (int, optional): The ID of the priority.
        estimate (str, optional): The estimate for the test case.
        milestone_id (int, optional): The ID of the milestone.
        refs (str, optional): A comma-separated list of references.

    Returns:
        dict: The response from the API.
    """
    data = {
        "title": title,
        "template_id": template_id,
        "type_id": type_id,
        "priority_id": priority_id,
        "estimate": estimate,
        "milestone_id": milestone_id,
        "refs": refs
    }
    return _api.api_request('POST', f'update_case/{case_id}', data)

def delete_case(case_id):
    """
    Delete a specific test case.

    Args:
        case_id (str): The ID of the test case.

    Returns:
        dict: The response from the API.
    """
    return _api.api_request('POST', f'delete_case/{case_id}')

def get_case_fields():
    """
    Get all available test case fields.

    Returns:
        list: A list of dictionaries containing the details of each test case field.
    """
    return _api.api_request('GET', 'get_case_fields')

def get_case_types():
    """
    Get all available test case types.

    Returns:
        list: A list of dictionaries containing the details of each test case type.
    """
    return _api.api_request('GET', 'get_case_types')

def get_history_for_case(case_id, limit=None, offset=None):
    """
    Get the history for a specific test case.

    Args:
        case_id (str): The ID of the test case.
        limit (int, optional): The maximum number of history entries to return.
        offset (int, optional): The number of history entries to skip before starting to collect the result set.

    Returns:
        list: A list of dictionaries containing the history of the test case.
    """
    endpoint = f'get_history_for_case/{case_id}'
    if limit:
        endpoint += f'&limit={limit}'
    if offset:
        endpoint += f'&offset={offset}'
    return _api.api_request('GET', endpoint)

def copy_cases_to_section(section_id, case_ids=None):
    """
    Copy test cases to a specific section.

    Args:
        section_id (str): The ID of the section.
        case_ids (list, optional): A list of test case IDs to copy.

    Returns:
        dict: The response from the API.
    """
    data = {
        "case_ids": case_ids
    }
    return _api.api_request('POST', f'copy_cases_to_section/{section_id}', data)

def update_cases(suite_id, case_ids, section_id=None, title=None, template_id=None, type_id=None, priority_id=None, estimate=None, milestone_id=None, refs=None):
    """
    Update multiple test cases.

    Args:
        suite_id (str): The ID of the suite.
        case_ids (list): A list of test case IDs to update.
        section_id (str, optional): The ID of the section.
        title (str, optional): The title of the test cases.
        template_id (int, optional): The ID of the template.
        type_id (int, optional): The ID of the type.
        priority_id (int, optional): The ID of the priority.
        estimate (str, optional): The estimate for the test cases.
        milestone_id (int, optional): The ID of the milestone.
        refs (str, optional): A comma-separated list of references.

    Returns:
        dict: The response from the API.
    """
    data = {
        "case_ids": case_ids,
        "section_id": section_id,
        "title": title,
        "template_id": template_id,
        "type_id": type_id,
        "priority_id": priority_id,
        "estimate": estimate,
        "milestone_id": milestone_id,
        "refs": refs
    }
    return _api.api_request('POST', f'update_cases/{suite_id}', data)

def move_cases_to_section(section_id, suite_id, case_ids):
    """
    Move test cases to a specific section.

    Args:
        section_id (str): The ID of the section.
        suite_id (str): The ID of the suite.
        case_ids (list): A list of test case IDs to move.

    Returns:
        dict: The response from the API.
    """
    data = {
        "suite_id": suite_id,
        "case_ids": case_ids
    }
    return _api.api_request('POST', f'move_cases_to_section/{section_id}', data)

def delete_cases(suite_id, case_ids, project_id, soft=0):
    """
    Delete multiple test cases.

    Args:
        suite_id (str): The ID of the suite.
        case_ids (list): A list of test case IDs to delete.
        project_id (str): The ID of the project.
        soft (int, optional): Whether to perform a soft delete (default is 0).

    Returns:
        dict: The response from the API.
    """
    data = {
        "case_ids": case_ids,
        "project_id": project_id,
        "soft": soft
    }
    return _api.api_request('POST', f'delete_cases/{suite_id}', data)