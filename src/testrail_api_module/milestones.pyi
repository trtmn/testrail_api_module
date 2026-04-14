from typing import Any

from .base import BaseAPI as BaseAPI

class MilestonesAPI(BaseAPI):
    def get_milestone(self, milestone_id: int) -> dict[str, Any]: ...
    def get_milestones(self, project_id: int) -> list[dict[str, Any]]: ...
    def add_milestone(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        due_on: str | None = None,
        parent_id: int | None = None,
        start_on: str | None = None,
    ) -> dict[str, Any]: ...
    def update_milestone(
        self, milestone_id: int, **kwargs: Any
    ) -> dict[str, Any]: ...
    def delete_milestone(self, milestone_id: int) -> dict[str, Any]: ...
