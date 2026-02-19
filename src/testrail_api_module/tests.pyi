from typing import Any

from .base import BaseAPI as BaseAPI

class TestsAPI(BaseAPI):
    """
    API for managing TestRail tests.
    """
    def get_test(
        self, test_id: int, with_data: int | None = None
    ) -> dict[str, Any] | None:
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
    def get_tests(
        self,
        run_id: int,
        status_id: int | list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        label_id: int | list[int] | None = None,
    ) -> list[dict[str, Any]] | None:
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
