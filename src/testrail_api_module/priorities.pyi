from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["PrioritiesAPI"]

class PrioritiesAPI(BaseAPI):
    def get_priorities(self) -> list[dict[str, Any]]: ...
