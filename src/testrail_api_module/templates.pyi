from typing import Any

from .base import BaseAPI as BaseAPI

class TemplatesAPI(BaseAPI):
    """
    API for managing TestRail templates.
    """
    def get_templates(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all templates for a project.

        Args:
            project_id (int): The ID of the project to get templates for.

        Returns:
            list: List of templates if successful, None otherwise.
        """
