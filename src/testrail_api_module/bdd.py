"""
This module provides functionality for managing BDD (Behavior-Driven
Development) scenarios in TestRail. It allows you to import and export
BDD scenarios as .feature files.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["BDDAPI"]


class BDDAPI(BaseAPI):
    """
    API for managing BDD scenarios in TestRail.

    This class provides methods to import and export BDD .feature files
    for test cases in TestRail.
    """

    def get_bdd(self, case_id: int) -> bytes:
        """
        Export a BDD scenario from a test case as a .feature file.

        Args:
            case_id: The ID of the test case to export.

        Returns:
            The raw .feature file content as bytes (Gherkin syntax).

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._get(f"get_bdd/{case_id}", raw=True)

    def add_bdd(self, section_id: int, feature_file: str) -> dict[str, Any]:
        """
        Import/upload a BDD scenario from a .feature file into a
        section.

        The file is uploaded as ``multipart/form-data`` with the file
        bytes in an ``attachment`` form field, matching the official
        TestRail API contract.

        Args:
            section_id: The ID of the section to import the BDD
                scenario into.
            feature_file: The path to the .feature file to import.

        Returns:
            Dict containing the created test case data.

        Raises:
            FileNotFoundError: If the specified feature file does
                not exist.
            TestRailAPIError: If the API request fails.
        """
        try:
            return self._post_multipart(f"add_bdd/{section_id}", feature_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Feature file not found: {feature_file}"
            ) from e
