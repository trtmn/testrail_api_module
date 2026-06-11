"""
This module provides functionality for managing shared steps in
TestRail. Shared steps are reusable test steps that can be referenced
by multiple test cases.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["SharedStepsAPI"]


class SharedStepsAPI(BaseAPI):
    """
    API for managing TestRail shared steps.

    This class provides methods to create, read, update, and delete
    shared steps that can be reused across multiple test cases.
    """

    def get_shared_step(self, shared_step_id: int) -> dict[str, Any]:
        """
        Get a shared step by ID.

        Args:
            shared_step_id: The ID of the shared step to retrieve.

        Returns:
            Dict containing the shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_shared_step/{shared_step_id}")

    def get_shared_steps(
        self,
        project_id: int,
        created_after: int | None = None,
        created_before: int | None = None,
        created_by: int | list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        updated_after: int | None = None,
        updated_before: int | None = None,
    ) -> dict[str, Any]:
        """
        Get all shared steps for a project.

        Args:
            project_id: The ID of the project to get shared steps for.
            created_after: Optional Unix timestamp to return only
                shared steps created after this date.
            created_before: Optional Unix timestamp to return only
                shared steps created before this date.
            created_by: Optional user ID or list of user IDs to filter
                by the user who created the shared step.
            limit: Optional maximum number of shared steps to return.
            offset: Optional offset for pagination.
            updated_after: Optional Unix timestamp to return only
                shared steps updated after this date.
            updated_before: Optional Unix timestamp to return only
                shared steps updated before this date.

        Returns:
            Dict containing the pagination envelope with keys
            ``offset``, ``limit``, ``size``, ``_links``, and
            ``shared_steps`` (the list of shared step dicts).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params: dict[str, Any] = {}
        if created_after is not None:
            params["created_after"] = created_after
        if created_before is not None:
            params["created_before"] = created_before
        if created_by is not None:
            params["created_by"] = created_by
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if updated_after is not None:
            params["updated_after"] = updated_after
        if updated_before is not None:
            params["updated_before"] = updated_before

        return self._get(f"get_shared_steps/{project_id}", params=params)

    def add_shared_step(
        self,
        project_id: int,
        title: str,
        custom_steps_separated: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Add a new shared step to a project.

        Args:
            project_id: The ID of the project to add the shared step
                to.
            title: The title of the shared step.
            custom_steps_separated: Optional list of step objects.
                Each step is a dict with keys ``content``,
                ``expected``, and optionally ``refs``.

        Returns:
            Dict containing the created shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"title": title}
        if custom_steps_separated is not None:
            data["custom_steps_separated"] = custom_steps_separated

        return self._post(f"add_shared_step/{project_id}", data=data)

    def update_shared_step(
        self,
        shared_step_id: int,
        title: str | None = None,
        custom_steps_separated: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Update an existing shared step.

        Args:
            shared_step_id: The ID of the shared step to update.
            title: Optional new title for the shared step.
            custom_steps_separated: Optional updated list of step
                objects. Each step is a dict with keys ``content``,
                ``expected``, and optionally ``refs``.

        Returns:
            Dict containing the updated shared step data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if custom_steps_separated is not None:
            data["custom_steps_separated"] = custom_steps_separated

        return self._post(f"update_shared_step/{shared_step_id}", data=data)

    def delete_shared_step(
        self,
        shared_step_id: int,
        keep_in_cases: bool | None = None,
    ) -> dict[str, Any]:
        """
        Delete a shared step.

        Args:
            shared_step_id: The ID of the shared step to delete.
            keep_in_cases: Optional boolean. If ``True``, the steps
                are kept in cases that reference this shared step
                instead of being removed.

        Returns:
            Empty dict (TestRail returns an empty body on success).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if keep_in_cases is not None:
            data["keep_in_cases"] = keep_in_cases

        return self._post(
            f"delete_shared_step/{shared_step_id}",
            data=data if data else None,
        )
