from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["VariablesAPI"]

class VariablesAPI(BaseAPI):
    def get_variable(self, variable_id: int) -> dict[str, Any]: ...
    def get_variables(
        self,
        project_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]: ...
    def add_variable(
        self,
        project_id: int,
        name: str,
    ) -> dict[str, Any]: ...
    def update_variable(
        self,
        variable_id: int,
        name: str,
    ) -> dict[str, Any]: ...
    def delete_variable(self, variable_id: int) -> dict[str, Any]: ...
