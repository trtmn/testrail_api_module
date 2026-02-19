"""
This module provides functionality for managing tests in TestRail.
Tests represent individual test executions within a test run.
"""

from typing import Any

from .base import BaseAPI


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
        params = {}
        if with_data is not None:
            params["with_data"] = with_data
        return self._get(f"get_test/{test_id}", params=params)

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
        params = {}
        if status_id is not None:
            # Convert list to comma-separated string if needed
            params["status_id"] = (
                ",".join(map(str, status_id))
                if isinstance(status_id, list)
                else status_id
            )
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if label_id is not None:
            # Convert list to comma-separated string if needed
            params["label_id"] = (
                ",".join(map(str, label_id))
                if isinstance(label_id, list)
                else label_id
            )

        return self._get(f"get_tests/{run_id}", params=params)
