from .base import BaseAPI as BaseAPI
from typing import Any

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
    def get_attachments(self, entity_type: str, entity_id: int) -> list[dict[str, Any]] | None:
        """
        Get all attachments for a specific entity.
        
        Args:
            entity_type: The type of entity ('case', 'run', 'plan', 'project').
            entity_id: The ID of the entity to get attachments for.
            
        Returns:
            List of dictionaries containing attachment data.
        """
    def add_attachment(self, entity_type: str, entity_id: int, file_path: str, description: str | None = None) -> dict[str, Any] | None:
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
    def delete_attachment(self, attachment_id: int) -> dict[str, Any] | None:
        """
        Delete an attachment.
        
        Args:
            attachment_id: The ID of the attachment to delete.
            
        Returns:
            Dict containing the response data.
        """
    def get_attachment_content(self, attachment_id: int) -> bytes | None:
        """
        Get the content of an attachment.
        
        Args:
            attachment_id: The ID of the attachment to get content for.
            
        Returns:
            Bytes containing the attachment content.
        """
