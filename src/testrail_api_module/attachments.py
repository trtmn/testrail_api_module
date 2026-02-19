"""
This module provides functionality for managing attachments in TestRail.
Attachments can be added to test cases, test runs, and other entities.
"""

from typing import Any

from .base import BaseAPI


class AttachmentsAPI(BaseAPI):
    """
    API for managing TestRail attachments.
    """

    def get_attachment(self, attachment_id: int) -> dict[str, Any] | None:
        """
        Get an attachment by ID.

        Args:
            attachment_id: The ID of the attachment to retrieve.

        Returns:
            Dict containing the attachment data.
        """
        return self._api_request("GET", f"get_attachment/{attachment_id}")

    def get_attachments(
        self, entity_type: str, entity_id: int
    ) -> list[dict[str, Any]] | None:
        """
        Get all attachments for a specific entity.

        Args:
            entity_type: The type of entity ('case', 'run', 'plan', 'project').
            entity_id: The ID of the entity to get attachments for.

        Returns:
            List of dictionaries containing attachment data.
        """
        return self._api_request(
            "GET", f"get_attachments/{entity_type}/{entity_id}"
        )

    def add_attachment(
        self,
        entity_type: str,
        entity_id: int,
        file_path: str,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Add an attachment to a specific entity.

        Args:
            entity_type: The type of entity ('case', 'run', 'plan', 'project').
            entity_id: The ID of the entity to add the attachment to.
            file_path: The path to the file to attach.
            description: Optional description of the attachment.

        Returns:
            Dict containing the created attachment data.
        """
        data = {"file": file_path}
        if description:
            data["description"] = description

        return self._api_request(
            "POST", f"add_attachment/{entity_type}/{entity_id}", data=data
        )

    def delete_attachment(self, attachment_id: int) -> dict[str, Any] | None:
        """
        Delete an attachment.

        Args:
            attachment_id: The ID of the attachment to delete.

        Returns:
            Dict containing the response data.
        """
        return self._api_request("POST", f"delete_attachment/{attachment_id}")
