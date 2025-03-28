from . import _common
_api = _common.ApiConstructor()
"""

"""
# Print initializing message for file_name
print("{0} is initializing...".format(__file__))

def get_test(test_id):
    """
    Get details of a specific test.

    Args:
        test_id (str): The ID of the test.

    Returns:
        dict: A dictionary containing the details of the test.
    """
    return _api.api_request('GET', f'get_test/{test_id}')

def get_tests(run_id, status_id=None, limit=None, offset=None):
    """
    Get all tests for a specific test run, optionally filtered by status, limit, and offset.

    Args:
        run_id (str): The ID of the test run.
        status_id (int, optional): The status ID to filter the tests.
        limit (int, optional): The maximum number of tests to return.
        offset (int, optional): The number of tests to skip before starting to collect the result set.

    Returns:
        list: A list of dictionaries containing the details of each test.
    """
    endpoint = f'get_tests/{run_id}'
    if status_id:
        endpoint += f'&status_id={status_id}'
    if limit:
        endpoint += f'&limit={limit}'
    if offset:
        endpoint += f'&offset={offset}'
    return _api.api_request('GET', endpoint)