"""
This module provides functionality for managing tests in TestRail.
Tests represent individual test executions within a test run.
"""
from typing import Optional, Dict, Any, List, Union
from .base import BaseAPI

class TestsAPI(BaseAPI):
    """
    API for managing TestRail tests.
    """
    
    def get_test(self, test_id: int, with_data: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get a test by ID.
        
        Args:
            test_id: The ID of the test to retrieve.
            with_data: Optional parameter to include additional data in the response.
            
        Returns:
            Dict containing the test data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> test = api.tests.get_test(test_id=123)
            >>> # Include additional data
            >>> test = api.tests.get_test(test_id=123, with_data=1)
        """
        params = {}
        if with_data is not None:
            params['with_data'] = with_data
        return self._get(f'get_test/{test_id}', params=params)
    
    def get_tests(self, run_id: int,
                  status_id: Optional[Union[int, List[int]]] = None,
                  limit: Optional[int] = None,
                  offset: Optional[int] = None,
                  label_id: Optional[Union[int, List[int]]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all tests for a test run.
        
        Args:
            run_id: The ID of the test run to get tests for.
            status_id: Optional status ID(s) to filter by (comma-separated if multiple).
            limit: Optional limit on number of results to return (default 250).
            offset: Optional offset for pagination.
            label_id: Optional label ID(s) to filter by (comma-separated if multiple).
            
        Returns:
            List of dictionaries containing test data.
            
        Raises:
            TestRailAPIError: If the API request fails.
            
        Example:
            >>> tests = api.tests.get_tests(run_id=1)
            >>> # Filter by status and limit results
            >>> tests = api.tests.get_tests(
            ...     run_id=1,
            ...     status_id=[1, 5],
            ...     limit=100
            ... )
        """
        params = {}
        if status_id is not None:
            # Convert list to comma-separated string if needed
            params['status_id'] = ','.join(map(str, status_id)) if isinstance(status_id, list) else status_id
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if label_id is not None:
            # Convert list to comma-separated string if needed
            params['label_id'] = ','.join(map(str, label_id)) if isinstance(label_id, list) else label_id
            
        return self._get(f'get_tests/{run_id}', params=params)
    
    def get_test_results(self, test_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all results for a test.
        
        Args:
            test_id: The ID of the test to get results for.
            
        Returns:
            List of dictionaries containing test result data.
        """
        return self._api_request('GET', f'get_results_for_test/{test_id}')
    
    def add_test_result(self, test_id: int, status_id: int, 
                       comment: Optional[str] = None, version: Optional[str] = None,
                       elapsed: Optional[str] = None, defects: Optional[str] = None,
                       assignedto_id: Optional[int] = None, custom_fields: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Add a test result for a test.
        
        Args:
            test_id: The ID of the test to add the result for.
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
            'status_id': status_id
        }
        if comment:
            data['comment'] = comment
        if version:
            data['version'] = version
        if elapsed:
            data['elapsed'] = elapsed
        if defects:
            data['defects'] = defects
        if assignedto_id:
            data['assignedto_id'] = assignedto_id
        if custom_fields:
            data.update(custom_fields)
            
        return self._api_request('POST', f'add_result_for_test/{test_id}', data=data)
    
    def add_test_results(self, test_ids: List[int], results: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """
        Add test results for multiple tests.
        
        Args:
            test_ids: List of test IDs to add results for.
            results: List of dictionaries containing test result data.
                
        Returns:
            List of dictionaries containing the created test result data.
        """
        data = {
            'test_ids': test_ids,
            'results': results
        }
        return self._api_request('POST', 'add_results_for_tests', data=data) 