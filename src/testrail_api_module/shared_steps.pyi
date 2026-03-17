from typing import Any

from .base import BaseAPI as BaseAPI

class SharedStepsAPI(BaseAPI):
    def get_shared_step(self, shared_step_id: int) -> dict[str, Any]: ...
    def get_shared_steps(self, project_id: int) -> list[dict[str, Any]]: ...
    def add_shared_step(
        self,
        project_id: int,
        title: str,
        steps: list[dict[str, Any]],
        description: str | None = None,
    ) -> dict[str, Any]: ...
    def update_shared_step(
        self, shared_step_id: int, **kwargs: Any
    ) -> dict[str, Any]: ...
    def delete_shared_step(self, shared_step_id: int) -> dict[str, Any]: ...
