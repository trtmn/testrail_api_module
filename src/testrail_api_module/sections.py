"""
This module provides functionality for managing sections in TestRail.
Sections are used to organize test cases into hierarchical structures.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["SectionsAPI"]


class SectionsAPI(BaseAPI):
    """
    API for managing TestRail sections.

    This class provides methods to create, read, update, and delete sections
    in TestRail, following the official TestRail API patterns.
    """

    def get_section(self, section_id: int) -> dict[str, Any]:
        """
        Get a section by ID.

        Args:
            section_id: The ID of the section to retrieve.

        Returns:
            Dict containing the section data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> section = api.sections.get_section(123)
            >>> print(f"Section: {section['name']}")
        """
        return self._get(f"get_section/{section_id}")

    def get_sections(
        self, project_id: int, suite_id: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get all sections for a project and optionally a specific suite.

        Args:
            project_id: The ID of the project to get sections for.
            suite_id: Optional ID of the suite to get sections for.

        Returns:
            List of dictionaries containing section data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> sections = api.sections.get_sections(project_id=1, suite_id=2)
            >>> for section in sections:
            ...     print(f"Section: {section['name']}")
        """
        params = {}
        if suite_id is not None:
            params["suite_id"] = suite_id

        return self._get(f"get_sections/{project_id}", params=params)

    def add_section(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        suite_id: int | None = None,
        parent_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Add a new section.

        Args:
            project_id: The ID of the project to add the section to.
            name: The name of the section.
            description: Optional description of the section.
            suite_id: Optional ID of the suite to add the section to.
            parent_id: Optional ID of the parent section.

        Returns:
            Dict containing the created section data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> section = api.sections.add_section(
            ...     project_id=1,
            ...     name="New Section",
            ...     description="A new test section",
            ...     suite_id=2,
            ...     parent_id=5
            ... )
        """
        data = {"name": name}

        # Add optional fields only if they are provided
        optional_fields = {
            "description": description,
            "suite_id": suite_id,
            "parent_id": parent_id,
        }

        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value

        return self._post(f"add_section/{project_id}", data=data)

    def update_section(
        self,
        section_id: int,
        name: str | None = None,
        description: str | None = None,
        parent_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Update a section.

        Args:
            section_id: The ID of the section to update.
            name: Optional new name for the section.
            description: Optional new description for the section.
            parent_id: Optional new parent section ID.

        Returns:
            Dict containing the updated section data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> updated_section = api.sections.update_section(
            ...     section_id=123,
            ...     name="Updated Section Name"
            ... )
        """
        data = {}

        # Add fields only if they are provided
        optional_fields = {
            "name": name,
            "description": description,
            "parent_id": parent_id,
        }

        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value

        return self._post(f"update_section/{section_id}", data=data)

    def move_section(
        self,
        section_id: int,
        parent_id: int | None = None,
        after_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Move a section to a different parent or position.

        Requires TestRail 6.5.2+.

        Args:
            section_id: The ID of the section to move.
            parent_id: Optional new parent section ID. Use None or
                omit for top-level.
            after_id: Optional ID of the section to place this
                section after. Use None to place first.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> api.sections.move_section(
            ...     section_id=10,
            ...     parent_id=5,
            ...     after_id=8
            ... )
        """
        data: dict[str, Any] = {}
        if parent_id is not None:
            data["parent_id"] = parent_id
        if after_id is not None:
            data["after_id"] = after_id

        return self._post(f"move_section/{section_id}", data=data)

    def delete_section(self, section_id: int) -> dict[str, Any]:
        """
        Delete a section.

        Args:
            section_id: The ID of the section to delete.

        Returns:
            Dict containing the response data.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> result = api.sections.delete_section(123)
        """
        return self._post(f"delete_section/{section_id}")
