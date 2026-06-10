from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["MilestonesAPI"]

class MilestonesAPI(BaseAPI):
    def get_milestone(self, milestone_id: int) -> dict[str, Any]: ...
    def get_milestones(
        self,
        project_id: int,
        is_completed: bool | None = None,
        is_started: bool | None = None,
    ) -> list[dict[str, Any]]: ...
    def add_milestone(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
        due_on: int | None = None,
        parent_id: int | None = None,
        refs: str | None = None,
        start_on: int | None = None,
    ) -> dict[str, Any]: ...
    def update_milestone(
        self,
        milestone_id: int,
        name: str | None = None,
        description: str | None = None,
        due_on: int | None = None,
        is_completed: bool | None = None,
        is_started: bool | None = None,
        parent_id: int | None = None,
        refs: str | None = None,
        start_on: int | None = None,
    ) -> dict[str, Any]: ...
    def delete_milestone(self, milestone_id: int) -> dict[str, Any]: ...
