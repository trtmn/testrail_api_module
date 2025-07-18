from .base import BaseAPI as BaseAPI
from typing import Any

class ResultsAPI(BaseAPI):
    """API for managing test results in TestRail."""
    def add_result(self, run_id: int, case_id: int, status_id: int, comment: str | None = None, version: str | None = None, elapsed: str | None = None, defects: str | None = None, assignedto_id: int | None = None, custom_fields: dict[str, Any] | None = None) -> dict[str, Any]:
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
    def add_results_for_cases(self, run_id: int, results: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Add multiple test results for test cases in a test run.

        Args:
            run_id: The ID of the test run.
            results: List of dictionaries containing test result data for each case.

        Returns:
            Dict containing the created test results data.
        """
    def add_result_for_run(self, run_id: int, status_id: int, comment: str | None = None, version: str | None = None, elapsed: str | None = None, defects: str | None = None, assignedto_id: int | None = None, custom_fields: dict[str, Any] | None = None) -> dict[str, Any]:
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
    def get_results(self, run_id: int) -> list[dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.

        Returns:
            List of dictionaries containing test result data.
        """
    def get_results_for_case(self, run_id: int, case_id: int) -> list[dict[str, Any]]:
        """
        Get all test results for a specific test case in a test run.

        Args:
            run_id: The ID of the test run.
            case_id: The ID of the test case.

        Returns:
            List of dictionaries containing test result data.
        """
    def get_results_for_run(self, run_id: int) -> list[dict[str, Any]]:
        """
        Get all test results for a test run.

        Args:
            run_id: The ID of the test run.

        Returns:
            List of dictionaries containing test result data.
        """
    def add_results(self, run_id: int, results: list[dict[str, Any]]) -> dict[str, Any]:
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
