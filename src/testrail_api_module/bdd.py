from . import _common
_api = _common.ApiConstructor()
"""
This module provides functionalities to interact with BDD scenarios in TestRail.
"""

def get_bdd(case_id):
    """
    Export a BDD scenario from a test case as a .feature file.

    Args:
        case_id (int): The ID of the test case.

    Returns:
        dict: The response from the API.
    """
    return _api.api_request('GET', f'get_bdd/{case_id}')

def add_bdd(section_id, feature_file):
    """
    Import/upload a BDD scenario from a test case as a .feature file.

    Args:
        section_id (int): The ID of the section.
        feature_file (str): The path to the .feature file.

    Returns:
        dict: The response from the API.
    """
    with open(feature_file, 'r') as file:
        data = {
            "file": file.read()
        }
    return _api.api_request('POST', f'add_bdd/{section_id}', data)