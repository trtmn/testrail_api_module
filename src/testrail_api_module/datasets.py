"""
This module provides functionality for managing datasets in TestRail.
Datasets are collections of values for test variables, enabling
parameterized/data-driven testing. This functionality is available in
TestRail Enterprise version 7.6 or later.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["DatasetsAPI"]


class DatasetsAPI(BaseAPI):
    """
    API for managing TestRail datasets.

    Datasets enable parameterized testing by providing collections of
    variable values. Up to 100 datasets per project are supported
    (one default plus up to 99 additional). Requires TestRail
    Enterprise 7.6+.
    """

    def get_dataset(self, dataset_id: int) -> dict[str, Any]:
        """
        Get a dataset by ID.

        Args:
            dataset_id: The ID of the dataset to retrieve.

        Returns:
            Dict containing the dataset data with id, name, and
            variables array.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> dataset = api.datasets.get_dataset(dataset_id=1)
        """
        return self._get(f"get_dataset/{dataset_id}")

    def get_datasets(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all datasets for a project.

        Args:
            project_id: The ID of the project to get datasets for.

        Returns:
            List of dictionaries containing dataset data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> datasets = api.datasets.get_datasets(project_id=1)
        """
        return self._get(f"get_datasets/{project_id}")

    def add_dataset(
        self,
        project_id: int,
        name: str,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
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

        Example:
            >>> dataset = api.datasets.add_dataset(
            ...     project_id=1,
            ...     name="My Dataset",
            ...     variables=[{"id": 1, "value": "test"}]
            ... )
        """
        data: dict[str, Any] = {"name": name}
        if variables is not None:
            data["variables"] = variables
        return self._post(f"add_dataset/{project_id}", data=data)

    def update_dataset(
        self,
        dataset_id: int,
        name: str | None = None,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Update a dataset.

        Args:
            dataset_id: The ID of the dataset to update.
            name: Optional new name for the dataset.
            variables: Optional list of variable dicts to update.

        Returns:
            Dict containing the updated dataset data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> dataset = api.datasets.update_dataset(
            ...     dataset_id=1,
            ...     name="Updated Dataset"
            ... )
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if variables is not None:
            data["variables"] = variables
        return self._post(f"update_dataset/{dataset_id}", data=data)

    def delete_dataset(self, dataset_id: int) -> dict[str, Any]:
        """
        Delete a dataset.

        Args:
            dataset_id: The ID of the dataset to delete.

        Returns:
            Empty dict (TestRail returns an empty body on success).

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> api.datasets.delete_dataset(dataset_id=1)
        """
        return self._post(f"delete_dataset/{dataset_id}")
