from typing import Any

from .base import BaseAPI

__all__ = ["ResultsAPI"]

class ResultsAPI(BaseAPI):
    """API for managing test results in TestRail."""
    def get_results(
        self,
        test_id: int,
        status_id: int | list[int] | None = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> list[dict[str, Any]]:
        """Get all results for a specific test."""
    def add_result(
        self,
        test_id: int,
        status_id: int,
        comment: str | None = ...,
        version: str | None = ...,
        elapsed: str | None = ...,
        defects: str | None = ...,
        assignedto_id: int | None = ...,
        custom_fields: dict[str, Any] | None = ...,
    ) -> dict[str, Any]:
        """Add a test result for a specific test (by test ID)."""
    def add_result_for_case(
        self,
        run_id: int,
        case_id: int,
        status_id: int,
        comment: str | None = ...,
        version: str | None = ...,
        elapsed: str | None = ...,
        defects: str | None = ...,
        assignedto_id: int | None = ...,
        custom_fields: dict[str, Any] | None = ...,
    ) -> dict[str, Any]:
        """Add a test result for a specific test case in a test run."""
    def add_results_for_cases(
        self, run_id: int, results: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Add multiple test results for test cases in a test run."""
    def get_results_for_case(
        self, run_id: int, case_id: int
    ) -> list[dict[str, Any]]:
        """Get all test results for a specific test case in a test run."""
    def get_results_for_run(
        self,
        run_id: int,
        status_id: int | list[int] | None = ...,
        created_after: int | None = ...,
        created_before: int | None = ...,
        created_by: int | list[int] | None = ...,
        defects_filter: str | None = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> list[dict[str, Any]]:
        """Get all test results for a test run."""
    def add_results(
        self, run_id: int, results: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Add multiple test results for tests in a run (by test ID)."""
