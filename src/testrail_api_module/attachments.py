"""
This module provides functionality for managing attachments in TestRail.
Attachments can be added to test cases, test plans, test plan entries,
test results, and test runs, and retrieved for cases, plans, plan
entries, runs, and tests.

Uploads are sent as ``multipart/form-data`` with the file bytes in an
``attachment`` form field, matching the official TestRail API contract.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["AttachmentsAPI"]


class AttachmentsAPI(BaseAPI):
    """
    API for managing TestRail attachments.

    This class provides methods to add, retrieve, and delete file
    attachments on test cases, plans, plan entries, results, and runs.
    """

    def add_attachment_to_case(
        self, case_id: int, file_path: str
    ) -> dict[str, Any]:
        """
        Add an attachment to a test case.

        Args:
            case_id: The ID of the test case.
            file_path: The path to the file to attach.

        Returns:
            Dict containing the created attachment ID, e.g.
            ``{"attachment_id": 443}``.

        Raises:
            FileNotFoundError: If the file does not exist.
            TestRailAPIError: If the API request fails.
        """
        return self._post_multipart(
            f"add_attachment_to_case/{case_id}", file_path
        )

    def add_attachment_to_plan(
        self, plan_id: int, file_path: str
    ) -> dict[str, Any]:
        """
        Add an attachment to a test plan.

        Args:
            plan_id: The ID of the test plan.
            file_path: The path to the file to attach.

        Returns:
            Dict containing the created attachment ID, e.g.
            ``{"attachment_id": 443}``.

        Raises:
            FileNotFoundError: If the file does not exist.
            TestRailAPIError: If the API request fails.
        """
        return self._post_multipart(
            f"add_attachment_to_plan/{plan_id}", file_path
        )

    def add_attachment_to_plan_entry(
        self, plan_id: int, entry_id: int, file_path: str
    ) -> dict[str, Any]:
        """
        Add an attachment to a test plan entry.

        Args:
            plan_id: The ID of the test plan containing the entry.
            entry_id: The ID of the test plan entry.
            file_path: The path to the file to attach.

        Returns:
            Dict containing the created attachment ID, e.g.
            ``{"attachment_id": 443}``.

        Raises:
            FileNotFoundError: If the file does not exist.
            TestRailAPIError: If the API request fails.
        """
        return self._post_multipart(
            f"add_attachment_to_plan_entry/{plan_id}/{entry_id}",
            file_path,
        )

    def add_attachment_to_result(
        self, result_id: int, file_path: str
    ) -> dict[str, Any]:
        """
        Add an attachment to a test result.

        Args:
            result_id: The ID of the test result.
            file_path: The path to the file to attach.

        Returns:
            Dict containing the created attachment ID, e.g.
            ``{"attachment_id": 443}``.

        Raises:
            FileNotFoundError: If the file does not exist.
            TestRailAPIError: If the API request fails.
        """
        return self._post_multipart(
            f"add_attachment_to_result/{result_id}", file_path
        )

    def add_attachment_to_run(
        self, run_id: int, file_path: str
    ) -> dict[str, Any]:
        """
        Add an attachment to a test run.

        Args:
            run_id: The ID of the test run.
            file_path: The path to the file to attach.

        Returns:
            Dict containing the created attachment ID, e.g.
            ``{"attachment_id": 443}``.

        Raises:
            FileNotFoundError: If the file does not exist.
            TestRailAPIError: If the API request fails.
        """
        return self._post_multipart(
            f"add_attachment_to_run/{run_id}", file_path
        )

    def get_attachments_for_case(
        self,
        case_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get all attachments for a test case.

        Args:
            case_id: The ID of the test case.
            limit: The number of attachments to return (max 250).
            offset: The offset to start returning attachments from.

        Returns:
            Attachment data (paginated dict on TestRail 6.7+, plain
            list on older versions).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._get(f"get_attachments_for_case/{case_id}", params=params)

    def get_attachments_for_plan(
        self,
        plan_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get all attachments for a test plan.

        Args:
            plan_id: The ID of the test plan.
            limit: The number of attachments to return (max 250).
            offset: The offset to start returning attachments from.

        Returns:
            Attachment data (paginated dict on TestRail 6.7+, plain
            list on older versions).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._get(f"get_attachments_for_plan/{plan_id}", params=params)

    def get_attachments_for_plan_entry(
        self, plan_id: int, entry_id: int
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get all attachments for a test plan entry.

        Args:
            plan_id: The ID of the test plan containing the entry.
            entry_id: The ID of the test plan entry.

        Returns:
            Attachment data (paginated dict on TestRail 6.7+, plain
            list on older versions).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(
            f"get_attachments_for_plan_entry/{plan_id}/{entry_id}"
        )

    def get_attachments_for_run(
        self,
        run_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get all attachments for a test run.

        Args:
            run_id: The ID of the test run.
            limit: The number of attachments to return (max 250).
            offset: The offset to start returning attachments from.

        Returns:
            Attachment data (paginated dict on TestRail 6.7+, plain
            list on older versions).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._get(f"get_attachments_for_run/{run_id}", params=params)

    def get_attachments_for_test(
        self, test_id: int
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get all attachments for a test.

        Args:
            test_id: The ID of the test.

        Returns:
            Attachment data (paginated dict on TestRail 6.7+, plain
            list on older versions).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_attachments_for_test/{test_id}")

    def get_attachment(self, attachment_id: int | str) -> bytes:
        """
        Download an attachment by ID.

        Args:
            attachment_id: The ID of the attachment to retrieve.
                Newer TestRail versions use UUID strings, older ones
                use integers.

        Returns:
            The raw file content as bytes.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_attachment/{attachment_id}", raw=True)

    def delete_attachment(self, attachment_id: int | str) -> dict[str, Any]:
        """
        Delete an attachment.

        Args:
            attachment_id: The ID of the attachment to delete.
                Newer TestRail versions use UUID strings, older ones
                use integers.

        Returns:
            Empty dict on success (TestRail returns an empty body).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_attachment/{attachment_id}")
