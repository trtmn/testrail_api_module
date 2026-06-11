from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["SharedStepsAPI"]

class SharedStepsAPI(BaseAPI):
    def get_shared_step(self, shared_step_id: int) -> dict[str, Any]: ...
    def get_shared_steps(
        self,
        project_id: int,
        created_after: int | None = ...,
        created_before: int | None = ...,
        created_by: int | list[int] | None = ...,
        limit: int | None = ...,
        offset: int | None = ...,
        updated_after: int | None = ...,
        updated_before: int | None = ...,
    ) -> dict[str, Any]: ...
    def add_shared_step(
        self,
        project_id: int,
        title: str,
        custom_steps_separated: list[dict[str, Any]] | None = ...,
    ) -> dict[str, Any]: ...
    def update_shared_step(
        self,
        shared_step_id: int,
        title: str | None = ...,
        custom_steps_separated: list[dict[str, Any]] | None = ...,
    ) -> dict[str, Any]: ...
    def delete_shared_step(
        self,
        shared_step_id: int,
        keep_in_cases: bool | None = ...,
    ) -> dict[str, Any]: ...
