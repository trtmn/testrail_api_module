"""
This module provides functionality for managing test plans in TestRail.
Test plans are used to organize and schedule test runs.
"""

from typing import Any

from .base import BaseAPI


class PlansAPI(BaseAPI):
    """
    API for managing TestRail test plans.
    """

    def get_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Get a test plan by ID.

        Args:
            plan_id (int): The ID of the test plan to retrieve.

        Returns:
            dict: The test plan data if successful, None otherwise.
        """
        return self._api_request("GET", f"get_plan/{plan_id}")

    def get_plans(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all test plans for a project.

        Args:
            project_id (int): The ID of the project to get test plans for.

        Returns:
            list: List of test plans if successful, None otherwise.
        """
        return self._api_request("GET", f"get_plans/{project_id}")

    def add_plan(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        milestone_id: int | None = None,
        entries: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        """
        Add a new test plan.

        Args:
            project_id (int): The ID of the project to add the test plan to.
            name (str): The name of the test plan.
            description (str, optional): The description of the test plan.
            milestone_id (int, optional): The ID of the milestone to add the test plan to.
            entries (list, optional): List of test plan entries, each containing:
                - suite_id (int): The ID of the test suite
                - name (str): The name of the test run
                - description (str, optional): The description of the test run
                - assignedto_id (int, optional): The ID of the user to assign the test run to
                - include_all (bool, optional): Whether to include all test cases
                - case_ids (list, optional): List of test case IDs to include

        Returns:
            dict: The created test plan data if successful, None otherwise.
        """
        data = {"name": name}
        if description:
            data["description"] = description
        if milestone_id:
            data["milestone_id"] = milestone_id
        if entries:
            data["entries"] = entries

        return self._api_request("POST", f"add_plan/{project_id}", data=data)

    def update_plan(self, plan_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a test plan.

        Args:
            plan_id (int): The ID of the test plan to update.
            **kwargs: The fields to update (name, description, milestone_id, entries).

        Returns:
            dict: The updated test plan data if successful, None otherwise.
        """
        return self._api_request("POST", f"update_plan/{plan_id}", data=kwargs)

    def close_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Close a test plan.

        Args:
            plan_id (int): The ID of the test plan to close.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request("POST", f"close_plan/{plan_id}")

    def delete_plan(self, plan_id: int) -> dict[str, Any] | None:
        """
        Delete a test plan.

        Args:
            plan_id (int): The ID of the test plan to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        return self._api_request("POST", f"delete_plan/{plan_id}")

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
    ) -> dict[str, Any] | None:
        """
        Add a new test plan entry (a test run) to an existing plan.

        Args:
            plan_id: The ID of the test plan.
            suite_id: The ID of the test suite for the entry.
            name: Optional name of the test run.
            description: Optional description of the test run.
            assignedto_id: Optional ID of the user to assign to.
            include_all: Whether to include all test cases (default True).
            case_ids: Optional list of case IDs to include.
            config_ids: Optional list of configuration IDs.
            runs: Optional list of run objects for multi-config entries.

        Returns:
            Dict containing the created plan entry data.
        """
        data: dict[str, Any] = {"suite_id": suite_id}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if assignedto_id is not None:
            data["assignedto_id"] = assignedto_id
        if not include_all:
            data["include_all"] = include_all
        if case_ids is not None:
            data["case_ids"] = case_ids
        if config_ids is not None:
            data["config_ids"] = config_ids
        if runs is not None:
            data["runs"] = runs

        return self._api_request(
            "POST", f"add_plan_entry/{plan_id}", data=data
        )

    def update_plan_entry(
        self, plan_id: int, entry_id: str, **kwargs
    ) -> dict[str, Any] | None:
        """
        Update an existing test plan entry.

        Args:
            plan_id: The ID of the test plan.
            entry_id: The ID of the plan entry to update.
            **kwargs: Fields to update (name, description,
                assignedto_id, include_all, case_ids, etc.).

        Returns:
            Dict containing the updated plan entry data.
        """
        return self._api_request(
            "POST", f"update_plan_entry/{plan_id}/{entry_id}", data=kwargs
        )

    def delete_plan_entry(
        self, plan_id: int, entry_id: str
    ) -> dict[str, Any] | None:
        """
        Delete a test plan entry.

        Args:
            plan_id: The ID of the test plan.
            entry_id: The ID of the plan entry to delete.

        Returns:
            Dict containing the response data.
        """
        return self._api_request(
            "POST", f"delete_plan_entry/{plan_id}/{entry_id}"
        )
