import logging as _logging
from . import _common
_api = _common.ApiConstructor()

# Print initializing message for file_name
print("{0} is initializing...".format(__file__))

def add(run_id=None, case_id=None, status_id=None, comment=None, version=None, elapsed=None, defects=None, assignedto_id=None):
    """
    Add a test result for a specific test case in a test run.

    Args:
        run_id (str): The ID of the test run.
        case_id (str): The ID of the test case.
        status_id (int): The status ID of the test result.
        comment (str): A comment for the test result.
        version (str): The version of the software under test.
        elapsed (str): The time taken to execute the test.
        defects (str): A comma-separated list of defects.
        assignedto_id (int): The ID of the user the test is assigned to.

    Returns:
        bool: True if the test result was added successfully, False otherwise.
    """
    data = {
        "status_id": status_id,
        "comment": comment,
        "version": version,
        "elapsed": elapsed,
        "defects": defects,
        "assignedto_id": assignedto_id
    }
    response = _api.api_request('POST', f'add_result_for_case/{run_id}/{case_id}', data)
    print("Test result added successfully." if response else "Failed to add test result.")
    if response is not None:
        _logging.info(f"Test result added successfully. Response: {response}")
        return True
    else:
        _logging.error(f"Failed to add test result. Response: {response}")
        return False

def get_plans(project_id):
    """
    Get all test plans for a specific project.

    Args:
        project_id (str): The ID of the project.

    Returns:
        list: A list of dictionaries containing the name, ID, and description of each test plan.
    """
    response = _api.api_request('GET', f'get_plans/{project_id}')
    return [{"name": plan["name"], "id": plan["id"], "description": plan["description"]} for plan in response['plans']] if response else []

def get_run_ids_from_plan(plan_id):
    """
    Get all test run IDs from a specific test plan.

    Args:
        plan_id (str): The ID of the test plan.

    Returns:
        list: A list of dictionaries containing the name, ID, and description of each test run.
    """
    response = _api.api_request('GET', f'get_plan/{plan_id}')
    return [{"name": run["name"], "id": run["id"], "description": run["description"]} for entry in response['entries'] for run in entry['runs']] if response else []

def get_run(run_id):
    """
    Get details of a specific test run.

    Args:
        run_id (str): The ID of the test run.

    Returns:
        dict: A dictionary containing the details of the test run.
    """
    return _api.api_request('GET', f'get_run/{run_id}')

def get_case_ids_from_run(run_id):
    """
    Get all test case IDs from a specific test run.

    Args:
        run_id (str): The ID of the test run.

    Returns:
        list: A list of test case IDs.
    """
    response = _api.api_request('GET', f'get_tests/{run_id}')
    return [test['case_id'] for test in response['tests']] if response else []