from .base import BaseAPI as BaseAPI
from typing import Any

class ReportsAPI(BaseAPI):
    """
    API for managing TestRail reports.
    """
    def get_report(self, report_id: int) -> dict[str, Any] | None:
        """
        Get a report by ID.
        
        Args:
            report_id (int): The ID of the report to retrieve.
            
        Returns:
            dict: The report data if successful, None otherwise.
        """
    def get_reports(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all reports for a project.
        
        Args:
            project_id (int): The ID of the project to get reports for.
            
        Returns:
            list: List of reports if successful, None otherwise.
        """
    def add_report(self, project_id: int, name: str, description: str | None = None, report_type: str = 'test_case', parameters: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """
        Add a new report.
        
        Args:
            project_id (int): The ID of the project to add the report to.
            name (str): The name of the report.
            description (str, optional): The description of the report.
            report_type (str, optional): The type of report:
                - test_case: Test case report
                - test_suite: Test suite report
                - test_run: Test run report
                - milestone: Milestone report
                - project: Project report
            parameters (dict, optional): Report-specific parameters:
                - For test_case reports:
                    - suite_id (int): The ID of the test suite
                    - section_id (int, optional): The ID of the section
                    - case_ids (list, optional): List of test case IDs
                - For test_suite reports:
                    - suite_id (int): The ID of the test suite
                - For test_run reports:
                    - run_id (int): The ID of the test run
                - For milestone reports:
                    - milestone_id (int): The ID of the milestone
                - For project reports:
                    - milestone_id (int, optional): The ID of the milestone
                    
        Returns:
            dict: The created report data if successful, None otherwise.
        """
    def update_report(self, report_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a report.
        
        Args:
            report_id (int): The ID of the report to update.
            **kwargs: The fields to update (name, description, parameters).
            
        Returns:
            dict: The updated report data if successful, None otherwise.
        """
    def delete_report(self, report_id: int) -> dict[str, Any] | None:
        """
        Delete a report.
        
        Args:
            report_id (int): The ID of the report to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def run_report(self, report_id: int) -> dict[str, Any] | None:
        """
        Run a report to generate results.
        
        Args:
            report_id (int): The ID of the report to run.
            
        Returns:
            dict: The report results if successful, None otherwise.
        """
    def get_report_results(self, report_id: int) -> dict[str, Any] | None:
        """
        Get the results of a report.
        
        Args:
            report_id (int): The ID of the report to get results for.
            
        Returns:
            dict: The report results if successful, None otherwise.
        """
