from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["RolesAPI"]

class RolesAPI(BaseAPI):
    def get_roles(self) -> list[dict[str, Any]]: ...
