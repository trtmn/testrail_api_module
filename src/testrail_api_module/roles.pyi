from typing import Any

from .base import BaseAPI as BaseAPI

class RolesAPI(BaseAPI):
    def get_roles(self) -> list[dict[str, Any]]: ...
