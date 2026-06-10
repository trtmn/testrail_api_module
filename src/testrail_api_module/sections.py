"""
This module provides functionality for managing sections in TestRail.
Sections are used to organize test cases into hierarchical structures.
"""

from typing import Any, Final

from .base import BaseAPI

__all__ = ["SectionsAPI"]


class _UnsetType:
    """Sentinel type distinguishing omitted arguments from ``None``."""

    def __repr__(self) -> str:
        return "UNSET"


#: Sentinel default for ``move_section`` arguments. Arguments left at
#: ``UNSET`` are omitted from the request body entirely, while an
#: explicit ``None`` is sent as JSON ``null``.
UNSET: Final = _UnsetType()


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
        return self._get(f"get_section/{section_id}")  # type: ignore[return-value]

    def get_sections(
        self,
        project_id: int,
        suite_id: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """
        Get all sections for a project and optionally a specific suite.

        Args:
            project_id: The ID of the project to get sections for.
            suite_id: Optional ID of the suite to get sections for.
            limit: Optional limit on number of results to return
                (TestRail returns up to 250 by default).
            offset: Optional offset for pagination.

        Returns:
            On TestRail 6.7+ this endpoint returns a pagination
            envelope ``{"offset": ..., "limit": ..., "size": ...,
            "_links": ..., "sections": [...]}``; older TestRail
            versions return a plain list of section dictionaries.

        Raises:
            TestRailAPIError: If the API request fails.

        Example:
            >>> response = api.sections.get_sections(
            ...     project_id=1, suite_id=2
            ... )
            >>> for section in response["sections"]:
            ...     print(f"Section: {section['name']}")
        """
        params = {}
        if suite_id is not None:
            params["suite_id"] = suite_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

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
        data: dict[str, Any] = {"name": name}

        # Add optional fields only if they are provided
        optional_fields = {
            "description": description,
            "suite_id": suite_id,
            "parent_id": parent_id,
        }

        for field, value in optional_fields.items():
            if value is not None:
                data[field] = value

        return self._post(f"add_section/{project_id}", data=data)  # type: ignore[return-value]

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

        return self._post(f"update_section/{section_id}", data=data)  # type: ignore[return-value]

    def move_section(
        self,
        section_id: int,
        parent_id: int | None | _UnsetType = UNSET,
        after_id: int | None | _UnsetType = UNSET,
    ) -> dict[str, Any]:
        """
        Move a section to a different parent or position.

        Requires TestRail 6.5.2+.

        Arguments left at their defaults are omitted from the request
        body. Passing an explicit ``None`` sends a JSON ``null``, which
        TestRail interprets as described below.

        Args:
            section_id: The ID of the section to move.
            parent_id: New parent section ID. Pass ``None`` explicitly
                to move the section to the top level (sent as JSON
                ``null``). Omit to leave the parent unspecified.
            after_id: ID of the section to place this section after.
                Pass ``None`` explicitly to place it first (sent as
                JSON ``null``). Omit to leave the position unspecified.

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
            >>> # Move to top level, first position:
            >>> api.sections.move_section(
            ...     section_id=10, parent_id=None, after_id=None
            ... )
        """
        data: dict[str, Any] = {}
        if not isinstance(parent_id, _UnsetType):
            data["parent_id"] = parent_id
        if not isinstance(after_id, _UnsetType):
            data["after_id"] = after_id

        return self._post(f"move_section/{section_id}", data=data)  # type: ignore[return-value]

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
        return self._post(f"delete_section/{section_id}")  # type: ignore[return-value]
