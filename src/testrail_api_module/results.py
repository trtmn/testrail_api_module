"""
This module provides functionality for managing test results in TestRail.
It allows you to add, update, and retrieve test results for test cases and runs.
"""

from typing import Dict, Any, Optional, List, Union
from .base import BaseAPI

__all__ = ['ResultsAPI']

class ResultsAPI(BaseAPI):
    """
    API for managing test results in TestRail.
    
    This class provides methods to create, read, and manage test results
    in TestRail, following the official TestRail API patterns.
    """

    def add_result(self, run_id: int, case_id: int, status_id: int, 
                  comment: Optional[str] = None, version: Optional[str] = None,
                  elapsed: Optional[str] = None, defects: Optional[str] = None,
                  assignedto_id: Optional[int] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a test result for a specific test case in a test run.

        Args:
            run_id: The ID of the test run.
            case_id: The ID of the test case.
            status_id: The status ID of the test result (1: Passed, 2: Blocked, 3: Untested, 4: Retest, 5: Failed).
            comment: Optional comment for the test result.
            version: Optional version of the software under test.
            elapsed: Optional time taken to execute the test (e.g., "30s", "2m 30s").
            defects: Optional comma-separated list of defects.
            assignedto_id: Optional ID of the user the test is assigned to.
            custom_fields: Optional dictionary of custom field values.

        Returns:
            Dict containing the created test result data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.results.add_result(
            ...     run_id=1,
            ...     case_id=123,
            ...     status_id=1,
            ...     comment="Test passed successfully",
            ...     elapsed="30s"
            ... )
        """
        data = {"status_id": status_id}
        
        # Add optional fields only if they are provided
        optional_fields = {
            "comment": comment,
            "version": version,
            "elapsed": elapsed,
            "defects": defects,
            "assignedto_id": assignedto_id
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
        
        # Add custom fields
        if custom_fields:
            data.update(custom_fields)
            
        return self._post(f'add_result_for_case/{run_id}/{case_id}', data=data)

    def add_results_for_cases(self, run_id: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> results_data = [
            ...     {"case_id": 1, "status_id": 1, "comment": "Passed"},
            ...     {"case_id": 2, "status_id": 5, "comment": "Failed"}
            ... ]
            >>> result = api.results.add_results_for_cases(run_id=1, results=results_data)
        """
        return self._post(f'add_results_for_cases/{run_id}', data={"results": results})

    def add_result_for_run(self, run_id: int, status_id: int,
                          comment: Optional[str] = None, version: Optional[str] = None,
                          elapsed: Optional[str] = None, defects: Optional[str] = None,
                          assignedto_id: Optional[int] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a test result for an entire test run.

        Args:
            run_id: The ID of the test run.
            status_id: The status ID of the test result (1: Passed, 2: Blocked, 3: Untested, 4: Retest, 5: Failed).
            comment: Optional comment for the test result.
            version: Optional version of the software under test.
            elapsed: Optional time taken to execute the test (e.g., "30s", "2m 30s").
            defects: Optional comma-separated list of defects.
            assignedto_id: Optional ID of the user the test is assigned to.
            custom_fields: Optional dictionary of custom field values.

        Returns:
            Dict containing the created test result data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> result = api.results.add_result_for_run(
            ...     run_id=1,
            ...     status_id=1,
            ...     comment="All tests passed"
            ... )
        """
        data = {"status_id": status_id}
        
        # Add optional fields only if they are provided
        optional_fields = {
            "comment": comment,
            "version": version,
            "elapsed": elapsed,
            "defects": defects,
            "assignedto_id": assignedto_id
        }
        
        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value
        
        # Add custom fields
        if custom_fields:
            data.update(custom_fields)
            
        return self._post(f'add_result_for_run/{run_id}', data=data)

    def get_results(self, run_id: int,
                   status_id: Optional[Union[int, List[int]]] = None,
                   created_after: Optional[int] = None,
                   created_before: Optional[int] = None,
                   created_by: Optional[Union[int, List[int]]] = None,
                   defects_filter: Optional[str] = None,
                   limit: Optional[int] = None,
                   offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.
            status_id: Optional status ID(s) to filter by (comma-separated if multiple).
            created_after: Optional timestamp to filter results created after this time.
            created_before: Optional timestamp to filter results created before this time.
            created_by: Optional user ID(s) to filter results created by specific users.
            defects_filter: Optional defect ID to filter by (e.g., 'TR-1', '4291').
            limit: Optional limit on number of results to return (default 250).
            offset: Optional offset for pagination.

        Returns:
            List of dictionaries containing test result data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> results = api.results.get_results(run_id=1)
            >>> for result in results:
            ...     print(f"Case {result['case_id']}: Status {result['status_id']}")
            >>> # Filter by status and limit results
            >>> results = api.results.get_results(
            ...     run_id=1,
            ...     status_id=[1, 5],
            ...     limit=100
            ... )
        """
        params = {}
        if status_id is not None:
            # Convert list to comma-separated string if needed
            params['status_id'] = ','.join(map(str, status_id)) if isinstance(status_id, list) else status_id
        if created_after is not None:
            params['created_after'] = created_after
        if created_before is not None:
            params['created_before'] = created_before
        if created_by is not None:
            # Convert list to comma-separated string if needed
            params['created_by'] = ','.join(map(str, created_by)) if isinstance(created_by, list) else created_by
        if defects_filter is not None:
            params['defects_filter'] = defects_filter
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        return self._get(f'get_results_for_run/{run_id}', params=params)

    def get_results_for_case(self, run_id: int, case_id: int) -> List[Dict[str, Any]]:
        """
        Get all test results for a specific test case in a test run.

        Args:
            run_id: The ID of the test run.
            case_id: The ID of the test case.

        Returns:
            List of dictionaries containing test result data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> results = api.results.get_results_for_case(run_id=1, case_id=123)
            >>> for result in results:
            ...     print(f"Result: {result['status_id']} - {result['comment']}")
        """
        return self._get(f'get_results_for_case/{run_id}/{case_id}')

    def get_results_for_run(self, run_id: int,
                           status_id: Optional[Union[int, List[int]]] = None,
                           created_after: Optional[int] = None,
                           created_before: Optional[int] = None,
                           created_by: Optional[Union[int, List[int]]] = None,
                           defects_filter: Optional[str] = None,
                           limit: Optional[int] = None,
                           offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.
            status_id: Optional status ID(s) to filter by (comma-separated if multiple).
            created_after: Optional timestamp to filter results created after this time.
            created_before: Optional timestamp to filter results created before this time.
            created_by: Optional user ID(s) to filter results created by specific users.
            defects_filter: Optional defect ID to filter by (e.g., 'TR-1', '4291').
            limit: Optional limit on number of results to return (default 250).
            offset: Optional offset for pagination.

        Returns:
            List of dictionaries containing test result data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> results = api.results.get_results_for_run(run_id=1)
            >>> # Filter by status and created date
            >>> results = api.results.get_results_for_run(
            ...     run_id=1,
            ...     status_id=[1, 5],
            ...     created_after=1609459200,
            ...     limit=50
            ... )
        """
        params = {}
        if status_id is not None:
            # Convert list to comma-separated string if needed
            params['status_id'] = ','.join(map(str, status_id)) if isinstance(status_id, list) else status_id
        if created_after is not None:
            params['created_after'] = created_after
        if created_before is not None:
            params['created_before'] = created_before
        if created_by is not None:
            # Convert list to comma-separated string if needed
            params['created_by'] = ','.join(map(str, created_by)) if isinstance(created_by, list) else created_by
        if defects_filter is not None:
            params['defects_filter'] = defects_filter
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        return self._get(f'get_results_for_run/{run_id}', params=params)

    def add_results(self, run_id: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple test results for test cases in a test run (alias for add_results_for_cases).

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
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> results_data = [
            ...     {"case_id": 1, "status_id": 1, "comment": "Passed"},
            ...     {"case_id": 2, "status_id": 5, "comment": "Failed"}
            ... ]
            >>> result = api.results.add_results(run_id=1, results=results_data)
        """
        return self._post(f'add_results_for_cases/{run_id}', data={"results": results})