from .base import BaseAPI as BaseAPI
from typing import Any

class TestsAPI(BaseAPI):
    """
    API for managing TestRail tests.
    """
    def get_test(self, test_id: int) -> dict[str, Any] | None:
        """
        Get a test by ID.
        
        Args:
            test_id: The ID of the test to retrieve.
            
        Returns:
            Dict containing the test data.
        """
    def get_tests(self, run_id: int) -> list[dict[str, Any]] | None:
        """
        Get all tests for a test run.
        
        Args:
            run_id: The ID of the test run to get tests for.
            
        Returns:
            List of dictionaries containing test data.
        """
    def get_test_results(self, test_id: int) -> list[dict[str, Any]] | None:
        """
        Get all results for a test.
        
        Args:
            test_id: The ID of the test to get results for.
            
        Returns:
            List of dictionaries containing test result data.
        """
    def add_test_result(self, test_id: int, status_id: int, comment: str | None = None, version: str | None = None, elapsed: str | None = None, defects: str | None = None, assignedto_id: int | None = None, custom_fields: dict[str, Any] | None = None) -> dict[str, Any] | None:
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
    def add_test_results(self, test_ids: list[int], results: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
        """
        Add test results for multiple tests.
        
        Args:
            test_ids: List of test IDs to add results for.
            results: List of dictionaries containing test result data.
                
        Returns:
            List of dictionaries containing the created test result data.
        """
