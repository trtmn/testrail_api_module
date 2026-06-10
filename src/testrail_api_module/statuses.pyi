from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["StatusesAPI"]

class StatusesAPI(BaseAPI):
    def get_statuses(self) -> list[dict[str, Any]]: ...
    def get_case_statuses(self) -> list[dict[str, Any]]: ...
