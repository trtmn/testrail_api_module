"""
This module provides functionality for managing test results in TestRail.
It allows you to add, update, and retrieve test results for test cases and runs.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI

__all__ = ['ResultsAPI']

class ResultsAPI(BaseAPI):
    """API for managing test results in TestRail."""

    def add_result(self, run_id: int, case_id: int, status_id: int, 
                  comment: Optional[str] = None, version: Optional[str] = None,
                  elapsed: Optional[str] = None, defects: Optional[str] = None,
                  assignedto_id: Optional[int] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a test result for a specific test case in a test run.

        Args:
            run_id: The ID of the test run.
            case_id: The ID of the test case.
            status_id: The status ID of the test result.
            comment: Optional comment for the test result.
            version: Optional version of the software under test.
            elapsed: Optional time taken to execute the test.
            defects: Optional comma-separated list of defects.
            assignedto_id: Optional ID of the user the test is assigned to.
            custom_fields: Optional dictionary of custom field values.

        Returns:
            Dict containing the created test result data.
        """
        data = {
            "status_id": status_id
        }
        if comment:
            data["comment"] = comment
        if version:
            data["version"] = version
        if elapsed:
            data["elapsed"] = elapsed
        if defects:
            data["defects"] = defects
        if assignedto_id:
            data["assignedto_id"] = assignedto_id
        if custom_fields:
            data.update(custom_fields)
        return self._api_request('POST', f'add_result_for_case/{run_id}/{case_id}', data)

    def add_results_for_cases(self, run_id: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple test results for test cases in a test run.

        Args:
            run_id: The ID of the test run.
            results: List of dictionaries containing test result data for each case.

        Returns:
            Dict containing the created test results data.
        """
        return self._api_request('POST', f'add_results_for_cases/{run_id}', {"results": results})

    def add_result_for_run(self, run_id: int, status_id: int,
                          comment: Optional[str] = None, version: Optional[str] = None,
                          elapsed: Optional[str] = None, defects: Optional[str] = None,
                          assignedto_id: Optional[int] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a test result for an entire test run.

        Args:
            run_id: The ID of the test run.
            status_id: The status ID of the test result.
            comment: Optional comment for the test result.
            version: Optional version of the software under test.
            elapsed: Optional time taken to execute the test.
            defects: Optional comma-separated list of defects.
            assignedto_id: Optional ID of the user the test is assigned to.
            custom_fields: Optional dictionary of custom field values.

        Returns:
            Dict containing the created test result data.
        """
        data = {
            "status_id": status_id
        }
        if comment:
            data["comment"] = comment
        if version:
            data["version"] = version
        if elapsed:
            data["elapsed"] = elapsed
        if defects:
            data["defects"] = defects
        if assignedto_id:
            data["assignedto_id"] = assignedto_id
        if custom_fields:
            data.update(custom_fields)
        return self._api_request('POST', f'add_result_for_run/{run_id}', data)

    def get_results(self, run_id: int) -> List[Dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.

        Returns:
            List of dictionaries containing test result data.
        """
        return self._api_request('GET', f'get_results_for_run/{run_id}')

    def get_results_for_case(self, run_id: int, case_id: int) -> List[Dict[str, Any]]:
        """
        Get all test results for a specific test case in a test run.

        Args:
            run_id: The ID of the test run.
            case_id: The ID of the test case.

        Returns:
            List of dictionaries containing test result data.
        """
        return self._api_request('GET', f'get_results_for_case/{run_id}/{case_id}')

    def get_results_for_run(self, run_id: int) -> List[Dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.

        Returns:
            List of dictionaries containing test result data.
        """
        return self._api_request('GET', f'get_results_for_run/{run_id}')

    def add_results(self, run_id: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple test results for test cases in a test run.

        Args:
            run_id: The ID of the test run.
            results: List of dictionaries containing test result data for each case.
                    Each result should include:
                    - case_id: The ID of the test case
                    - status_id: The status ID of the test result
                    - comment: Optional comment for the test result
                    - version: Optional version of the software under test
                    - elapsed: Optional time taken to execute the test
                    - defects: Optional comma-separated list of defects
                    - assignedto_id: Optional ID of the user the test is assigned to
                    - custom_fields: Optional dictionary of custom field values

        Returns:
            Dict containing the created test results data.
        """
        return self._api_request('POST', f'add_results_for_cases/{run_id}', {"results": results})