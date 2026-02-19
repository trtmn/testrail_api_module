from typing import Any

from .base import BaseAPI

__all__ = ["RunsAPI"]

class RunsAPI(BaseAPI):
    """
    API for managing TestRail test runs.

    This class provides methods to create, read, update, and manage test runs
    in TestRail, following the official TestRail API patterns.
    """
    def get_run(self, run_id: int) -> dict[str, Any]:
        """
        Get a test run by ID.

        Args:
            run_id: The ID of the test run to retrieve.

        Returns:
            Dict containing the test run data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> run = api.runs.get_run(123)
            >>> print(f"Run: {run[\'name\']}")
        """
    def get_runs(
        self,
        project_id: int,
        suite_id: int | None = None,
        created_after: int | None = None,
        created_before: int | None = None,
        created_by: int | None = None,
        is_completed: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all test runs for a project and optionally a specific suite.

        Args:
            project_id: The ID of the project to get test runs for.
            suite_id: Optional ID of the suite to get test runs for.
            created_after: Optional timestamp to filter runs created after this time.
            created_before: Optional timestamp to filter runs created before this time.
            created_by: Optional user ID to filter runs created by specific user.
            is_completed: Optional boolean to filter by completion status.
            limit: Optional limit on number of results to return.
            offset: Optional offset for pagination.

        Returns:
            List of dictionaries containing test run data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> runs = api.runs.get_runs(project_id=1, suite_id=2)
            >>> for run in runs:
            ...     print(f"Run: {run[\'name\']}")
        """
    def add_run(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        suite_id: int | None = None,
        milestone_id: int | None = None,
        assignedto_id: int | None = None,
        include_all: bool = True,
        case_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """
        Add a new test run.

        Args:
            project_id: The ID of the project to add the test run to.
            name: The name of the test run.
            description: Optional description of the test run.
            suite_id: Optional ID of the suite to add the test run to.
            milestone_id: Optional ID of the milestone to add the test run to.
            assignedto_id: Optional ID of the user to assign the test run to.
            include_all: Whether to include all test cases from the suite.
            case_ids: Optional list of test case IDs to include in the run.

        Returns:
            Dict containing the created test run data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> run = api.runs.add_run(
            ...     project_id=1,
            ...     name="Test Run",
            ...     description="Automated test run",
            ...     suite_id=2,
            ...     include_all=True
            ... )
        """
    def update_run(
        self,
        run_id: int,
        name: str | None = None,
        description: str | None = None,
        milestone_id: int | None = None,
        assignedto_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Update a test run.

        Args:
            run_id: The ID of the test run to update.
            name: Optional new name for the test run.
            description: Optional new description for the test run.
            milestone_id: Optional new milestone ID.
            assignedto_id: Optional new assigned user ID.

        Returns:
            Dict containing the updated test run data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> updated_run = api.runs.update_run(
            ...     run_id=123,
            ...     name="Updated Run Name",
            ...     assignedto_id=456
            ... )
        """
    def close_run(self, run_id: int) -> dict[str, Any]:
        """
        Close a test run.

        Args:
            run_id: The ID of the test run to close.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> result = api.runs.close_run(123)
        """
    def delete_run(self, run_id: int) -> dict[str, Any]:
        """
        Delete a test run.

        Args:
            run_id: The ID of the test run to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> result = api.runs.delete_run(123)
        """
    def get_run_stats(self, run_id: int) -> dict[str, Any]:
        """
        Get statistics for a test run.

        Args:
            run_id: The ID of the test run to get statistics for.

        Returns:
            Dict containing the test run statistics.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> stats = api.runs.get_run_stats(123)
            >>> print(f"Passed: {stats[\'passed\']}, Failed: {stats[\'failed\']}")
        """
