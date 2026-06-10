from typing import Any

from .base import BaseAPI as BaseAPI

class BDDAPI(BaseAPI):
    """API for managing BDD scenarios in TestRail."""
    def get_bdd(self, case_id: int) -> bytes:
        """
        Export a BDD scenario from a test case as a .feature file.

        Args:
            case_id: The ID of the test case to export.

        Returns:
            The raw .feature file content as bytes (Gherkin syntax).
        """
    def add_bdd(self, section_id: int, feature_file: str) -> dict[str, Any]:
        """
        Import/upload a BDD scenario from a .feature file into a section.

        Args:
            section_id: The ID of the section to import the BDD scenario into.
            feature_file: The path to the .feature file to import.

        Returns:
            Dict containing the created test case data.

        Raises:
            FileNotFoundError: If the specified feature file does not exist.
        """
