from typing import Any

from .base import BaseAPI as BaseAPI

class PrioritiesAPI(BaseAPI):
    def get_priorities(self) -> list[dict[str, Any]]: ...
