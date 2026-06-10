"""
This module provides functionality for managing test plans in TestRail.
Test plans are used to organize and schedule test runs across
configurations and milestones.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["PlansAPI"]


class PlansAPI(BaseAPI):
    """
    API for managing TestRail test plans.

    This class provides methods to create, read, update, close, and
    delete test plans and their entries (runs) in TestRail.
    """

    def get_plan(self, plan_id: int) -> dict[str, Any]:
        """
        Get a test plan by ID.

        Args:
            plan_id: The ID of the test plan to retrieve.

        Returns:
            Dict containing the test plan data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_plan/{plan_id}")

    def get_plans(
        self,
        project_id: int,
        created_after: int | None = None,
        created_before: int | None = None,
        created_by: int | None = None,
        is_completed: bool | None = None,
        milestone_id: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """
        Get all test plans for a project.

        Args:
            project_id: The ID of the project to get test plans for.
            created_after: Optional timestamp to filter plans created
                after this time.
            created_before: Optional timestamp to filter plans created
                before this time.
            created_by: Optional user ID to filter plans created by a
                specific user.
            is_completed: Optional boolean to filter by completion
                status.
            milestone_id: Optional milestone ID to filter plans by.
            limit: Optional limit on number of results to return.
            offset: Optional offset for pagination.

        Returns:
            Dict containing the pagination envelope with keys
            ``offset``, ``limit``, ``size``, ``_links``, and ``plans``
            (the list of test plan dicts).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        params = {}
        if created_after is not None:
            params["created_after"] = created_after
        if created_before is not None:
            params["created_before"] = created_before
        if created_by is not None:
            params["created_by"] = created_by
        if is_completed is not None:
            params["is_completed"] = is_completed
        if milestone_id is not None:
            params["milestone_id"] = milestone_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._get(f"get_plans/{project_id}", params=params)

    def add_plan(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        milestone_id: int | None = None,
        entries: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Add a new test plan.

        Args:
            project_id: The ID of the project to add the plan to.
            name: The name of the test plan.
            description: Optional description of the test plan.
            milestone_id: Optional ID of the milestone to link to.
            entries: Optional list of plan entries, each containing:
                - suite_id (int): The ID of the test suite
                - name (str): The name of the test run
                - assignedto_id (int, optional): User to assign to
                - include_all (bool, optional): Include all cases
                - case_ids (list, optional): Case IDs to include

        Returns:
            Dict containing the created test plan data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {"name": name}
        if description:
            data["description"] = description
        if milestone_id:
            data["milestone_id"] = milestone_id
        if entries:
            data["entries"] = entries

        return self._post(f"add_plan/{project_id}", data=data)

    def update_plan(self, plan_id: int, **kwargs: Any) -> dict[str, Any]:
        """
        Update a test plan.

        Args:
            plan_id: The ID of the test plan to update.
            **kwargs: Fields to update (name, description,
                milestone_id, entries).

        Returns:
            Dict containing the updated test plan data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"update_plan/{plan_id}", data=kwargs)

    def close_plan(self, plan_id: int) -> dict[str, Any]:
        """
        Close a test plan.

        Args:
            plan_id: The ID of the test plan to close.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"close_plan/{plan_id}")

    def delete_plan(self, plan_id: int) -> dict[str, Any]:
        """
        Delete a test plan.

        Args:
            plan_id: The ID of the test plan to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_plan/{plan_id}")

    def add_plan_entry(
        self,
        plan_id: int,
        suite_id: int,
        name: str | None = None,
        description: str | None = None,
        assignedto_id: int | None = None,
        include_all: bool = True,
        case_ids: list[int] | None = None,
        config_ids: list[int] | None = None,
        runs: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Add a new test plan entry (a test run) to an existing plan.

        Args:
            plan_id: The ID of the test plan.
            suite_id: The ID of the test suite for the entry.
            name: Optional name of the test run.
            description: Optional description of the test run.
            assignedto_id: Optional ID of the user to assign to.
            include_all: Whether to include all test cases
                (default True). Always sent explicitly in the
                payload, mirroring add_run.
            case_ids: Optional list of case IDs to include.
            config_ids: Optional list of configuration IDs.
            runs: Optional list of run objects for multi-config
                entries.

        Returns:
            Dict containing the created plan entry data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {
            "suite_id": suite_id,
            "include_all": include_all,
        }
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if assignedto_id is not None:
            data["assignedto_id"] = assignedto_id
        if case_ids is not None:
            data["case_ids"] = case_ids
        if config_ids is not None:
            data["config_ids"] = config_ids
        if runs is not None:
            data["runs"] = runs

        return self._post(f"add_plan_entry/{plan_id}", data=data)

    def update_plan_entry(
        self, plan_id: int, entry_id: str, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Update an existing test plan entry.

        Args:
            plan_id: The ID of the test plan.
            entry_id: The ID of the plan entry to update.
            **kwargs: Fields to update (name, description,
                assignedto_id, include_all, case_ids, etc.).

        Returns:
            Dict containing the updated plan entry data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(
            f"update_plan_entry/{plan_id}/{entry_id}",
            data=kwargs,
        )

    def delete_plan_entry(self, plan_id: int, entry_id: str) -> dict[str, Any]:
        """
        Delete a test plan entry.

        Args:
            plan_id: The ID of the test plan.
            entry_id: The ID of the plan entry to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_plan_entry/{plan_id}/{entry_id}")

    def add_run_to_plan_entry(
        self,
        plan_id: int,
        entry_id: str,
        config_ids: list[int],
        description: str | None = None,
        assignedto_id: int | None = None,
        include_all: bool = True,
        case_ids: list[int] | None = None,
        refs: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new test run to a plan entry that uses configurations.

        Requires TestRail 6.4 or later.

        Args:
            plan_id: The ID of the test plan.
            entry_id: The ID of the plan entry to add the run to.
            config_ids: List of configuration IDs for the new run
                (required).
            description: Optional description of the test run.
            assignedto_id: Optional ID of the user to assign to.
            include_all: Whether to include all test cases
                (default True). Always sent explicitly in the
                payload, mirroring add_run.
            case_ids: Optional list of case IDs to include.
            refs: Optional comma-separated list of references.

        Returns:
            Dict containing the updated plan entry data (same format
            as the entries field of get_plan, for a single entry).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {
            "config_ids": config_ids,
            "include_all": include_all,
        }
        if description is not None:
            data["description"] = description
        if assignedto_id is not None:
            data["assignedto_id"] = assignedto_id
        if case_ids is not None:
            data["case_ids"] = case_ids
        if refs is not None:
            data["refs"] = refs

        return self._post(
            f"add_run_to_plan_entry/{plan_id}/{entry_id}",
            data=data,
        )

    def update_run_in_plan_entry(
        self,
        run_id: int,
        description: str | None = None,
        assignedto_id: int | None = None,
        include_all: bool | None = None,
        case_ids: list[int] | None = None,
        refs: str | None = None,
    ) -> dict[str, Any]:
        """
        Update a test run inside a plan entry that uses
        configurations.

        Requires TestRail 6.4 or later. Only fields that are provided
        (not None) are sent, so partial updates are supported.

        Args:
            run_id: The ID of the test run to update.
            description: Optional new description of the test run.
            assignedto_id: Optional ID of the user to assign to.
            include_all: Optional flag to include all test cases
                (set False and pass case_ids for a custom selection).
            case_ids: Optional list of case IDs to include.
            refs: Optional comma-separated list of references.

        Returns:
            Dict containing the updated test run data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if description is not None:
            data["description"] = description
        if assignedto_id is not None:
            data["assignedto_id"] = assignedto_id
        if include_all is not None:
            data["include_all"] = include_all
        if case_ids is not None:
            data["case_ids"] = case_ids
        if refs is not None:
            data["refs"] = refs

        return self._post(
            f"update_run_in_plan_entry/{run_id}",
            data=data,
        )

    def delete_run_from_plan_entry(self, run_id: int) -> dict[str, Any]:
        """
        Delete a test run from a plan entry that uses configurations.

        Requires TestRail 6.4 or later.

        Args:
            run_id: The ID of the test run to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_run_from_plan_entry/{run_id}")
