"""
This module provides functionality for managing BDD (Behavior-Driven Development) scenarios in TestRail.
It allows you to import and export BDD scenarios as .feature files.
"""

from typing import Dict, Any, Optional
from .base import BaseAPI

class BDDAPI(BaseAPI):
    """API for managing BDD scenarios in TestRail."""

    def get_bdd(self, case_id: int) -> Dict[str, Any]:
        """
        Export a BDD scenario from a test case as a .feature file.

        Args:
            case_id: The ID of the test case to export.

        Returns:
            Dict containing the BDD scenario data in .feature file format.
        """
        return self._api_request('GET', f'get_bdd/{case_id}')

    def add_bdd(self, section_id: int, feature_file: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Import/upload a BDD scenario from a .feature file into a section.

        Args:
            section_id: The ID of the section to import the BDD scenario into.
            feature_file: The path to the .feature file to import.
            description: Optional description for the BDD scenario.

        Returns:
            Dict containing the created BDD scenario data.

        Raises:
            FileNotFoundError: If the specified feature file does not exist.
        """
        try:
            with open(feature_file, 'r') as file:
                data = {
                    "file": file.read()
                }
                if description:
                    data["description"] = description
                return self._api_request('POST', f'add_bdd/{section_id}', data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Feature file not found: {feature_file}")