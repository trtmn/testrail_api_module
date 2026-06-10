from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["TemplatesAPI"]

class TemplatesAPI(BaseAPI):
    def get_templates(self, project_id: int) -> list[dict[str, Any]]: ...
