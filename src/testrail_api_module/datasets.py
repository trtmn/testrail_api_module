"""
This module provides functionality for managing datasets in TestRail.
Datasets are collections of values for test variables, enabling
parameterized/data-driven testing. This functionality is available in
TestRail Enterprise version 7.6 or later.
"""

from typing import Any

from .base import BaseAPI


class DatasetsAPI(BaseAPI):
    """
    API for managing TestRail datasets.

    Datasets enable parameterized testing by providing collections of
    variable values. Up to 100 datasets per project are supported
    (one default plus up to 99 additional). Requires TestRail
    Enterprise 7.6+.
    """

    def get_dataset(self, dataset_id: int) -> dict[str, Any] | None:
        """
        Get a dataset by ID.

        Args:
            dataset_id: The ID of the dataset to retrieve.

        Returns:
            Dict containing the dataset data with id, name, and
            variables array. Each variable in the array contains id,
            name, and value. Returns None if the request fails.

        Raises:
            TestRailAPIError: If the API request fails (e.g., invalid
                dataset_id).
            TestRailAuthenticationError: If authentication fails.
            TestRailRateLimitError: If rate limit is exceeded.

        Note:
            Requires TestRail Enterprise 7.6+. Returns 403 for
            non-Enterprise instances.
        """
        return self._api_request("GET", f"get_dataset/{dataset_id}")

    def get_datasets(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all datasets for a project.

        Args:
            project_id: The ID of the project to get datasets for.

        Returns:
            List of dictionaries containing dataset data. Each dataset
            contains id, name, and variables array. Returns None if the
            request fails.

            Note: The API returns a paginated result with offset,
            limit, size, _links, and datasets array. This method
            returns the datasets array directly.

        Raises:
            TestRailAPIError: If the API request fails (e.g., invalid
                project_id).
            TestRailAuthenticationError: If authentication fails.
            TestRailRateLimitError: If rate limit is exceeded.

        Note:
            Requires TestRail Enterprise 7.6+. Returns 403 for
            non-Enterprise instances.
        """
        return self._api_request("GET", f"get_datasets/{project_id}")

    def add_dataset(
        self,
        project_id: int,
        name: str,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        """
        Add a new dataset to a project.

        Args:
            project_id: The ID of the project.
            name: The name of the dataset.
            variables: Optional list of variable dicts, each with
                'id' and 'value' keys.

        Returns:
            Dict containing the created dataset data.

        Raises:
            TestRailAPIError: If the API request fails.

        Note:
            Requires TestRail Enterprise 7.6+.
        """
        data: dict[str, Any] = {"name": name}
        if variables is not None:
            data["variables"] = variables
        return self._api_request(
            "POST", f"add_dataset/{project_id}", data=data
        )

    def update_dataset(
        self, dataset_id: int, **kwargs
    ) -> dict[str, Any] | None:
        """
        Update a dataset.

        Args:
            dataset_id: The ID of the dataset to update.
            **kwargs: Fields to update (name, variables).

        Returns:
            Dict containing the updated dataset data.

        Raises:
            TestRailAPIError: If the API request fails.

        Note:
            Requires TestRail Enterprise 7.6+.
        """
        return self._api_request(
            "POST", f"update_dataset/{dataset_id}", data=kwargs
        )

    def delete_dataset(self, dataset_id: int) -> dict[str, Any] | None:
        """
        Delete a dataset.

        Args:
            dataset_id: The ID of the dataset to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Note:
            Requires TestRail Enterprise 7.6+.
        """
        return self._api_request("POST", f"delete_dataset/{dataset_id}")
