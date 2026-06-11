"""
This module provides functionality for managing templates in TestRail.
Templates are used to define the structure and fields for test cases.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["TemplatesAPI"]


class TemplatesAPI(BaseAPI):
    """
    API for managing TestRail templates.

    This class provides methods to retrieve the available test case
    templates configured for a project.
    """

    def get_templates(self, project_id: int) -> list[dict[str, Any]]:
        """
        Get all templates for a project.

        Args:
            project_id: The ID of the project to get templates for.

        Returns:
            List of dictionaries containing template data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_templates/{project_id}")
