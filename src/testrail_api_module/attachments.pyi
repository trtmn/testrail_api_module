from typing import Any

from .base import BaseAPI as BaseAPI

class AttachmentsAPI(BaseAPI):
    def get_attachment(self, attachment_id: int) -> dict[str, Any]: ...
    def get_attachments(
        self, entity_type: str, entity_id: int
    ) -> list[dict[str, Any]]: ...
    def add_attachment(
        self,
        entity_type: str,
        entity_id: int,
        file_path: str,
        description: str | None = None,
    ) -> dict[str, Any]: ...
    def delete_attachment(self, attachment_id: int) -> dict[str, Any]: ...
