from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["VariablesAPI"]

class VariablesAPI(BaseAPI):
    def get_variables(self, project_id: int) -> list[dict[str, Any]]: ...
    def add_variable(
        self,
        project_id: int,
        name: str,
        value: str,
        description: str | None = None,
    ) -> dict[str, Any]: ...
    def update_variable(
        self, variable_id: int, **kwargs: Any
    ) -> dict[str, Any]: ...
    def delete_variable(self, variable_id: int) -> dict[str, Any]: ...
