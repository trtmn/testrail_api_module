from typing import Any

from .base import BaseAPI as BaseAPI

class SuitesAPI(BaseAPI):
    def get_suite(self, suite_id: int) -> dict[str, Any]: ...
    def get_suites(self, project_id: int) -> list[dict[str, Any]]: ...
    def add_suite(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
    ) -> dict[str, Any]: ...
    def update_suite(
        self,
        suite_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]: ...
    def delete_suite(self, suite_id: int) -> dict[str, Any]: ...
