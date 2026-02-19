"""
This module provides functionality for managing configurations in TestRail.
Configurations are used to define different test environments and settings.
The API distinguishes between configuration groups and individual configs.
Requires TestRail 5.2+.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["ConfigurationsAPI"]


class ConfigurationsAPI(BaseAPI):
    """
    API for managing TestRail configurations.

    TestRail organizes configurations into groups (e.g., "Browsers",
    "Operating Systems") that contain individual configs (e.g.,
    "Chrome", "Firefox"). This class provides CRUD operations for
    both groups and configs.
    """

    def get_configs(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all configuration groups and their configs for a project.

        Args:
            project_id: The ID of the project.

        Returns:
            List of configuration group dicts, each containing a
            'configs' array of individual configurations.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_configs/{project_id}")

    def add_config_group(self, project_id: int, name: str) -> dict[str, Any]:
        """
        Add a new configuration group to a project.

        Args:
            project_id: The ID of the project.
            name: The name of the configuration group.

        Returns:
            Dict containing the created configuration group data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name}
        return self._post(f"add_config_group/{project_id}", data=data)

    def add_config(self, config_group_id: int, name: str) -> dict[str, Any]:
        """
        Add a new configuration to a configuration group.

        Args:
            config_group_id: The ID of the configuration group.
            name: The name of the configuration.

        Returns:
            Dict containing the created configuration data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name}
        return self._post(f"add_config/{config_group_id}", data=data)

    def update_config_group(
        self, config_group_id: int, name: str
    ) -> dict[str, Any]:
        """
        Update a configuration group.

        Args:
            config_group_id: The ID of the configuration group.
            name: The new name for the configuration group.

        Returns:
            Dict containing the updated configuration group data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name}
        return self._post(f"update_config_group/{config_group_id}", data=data)

    def update_config(self, config_id: int, name: str) -> dict[str, Any]:
        """
        Update a configuration.

        Args:
            config_id: The ID of the configuration to update.
            name: The new name for the configuration.

        Returns:
            Dict containing the updated configuration data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        data = {"name": name}
        return self._post(f"update_config/{config_id}", data=data)

    def delete_config_group(self, config_group_id: int) -> dict[str, Any]:
        """
        Delete a configuration group and all its configurations.

        Args:
            config_group_id: The ID of the configuration group.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_config_group/{config_group_id}")

    def delete_config(self, config_id: int) -> dict[str, Any]:
        """
        Delete a configuration.

        Args:
            config_id: The ID of the configuration to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._post(f"delete_config/{config_id}")
