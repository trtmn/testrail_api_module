from typing import Any

from .base import BaseAPI

class PlansAPI(BaseAPI):
    def get_plan(self, plan_id: int) -> dict[str, Any] | None: ...
    def get_plans(self, project_id: int) -> list[dict[str, Any]] | None: ...
    def add_plan(
        self,
        project_id: int,
        name: str,
        description: str | None = ...,
        milestone_id: int | None = ...,
        entries: list[dict[str, Any]] | None = ...,
    ) -> dict[str, Any] | None: ...
    def update_plan(
        self, plan_id: int, **kwargs: Any
    ) -> dict[str, Any] | None: ...
    def close_plan(self, plan_id: int) -> dict[str, Any] | None: ...
    def delete_plan(self, plan_id: int) -> dict[str, Any] | None: ...
    def add_plan_entry(
        self,
        plan_id: int,
        suite_id: int,
        name: str | None = ...,
        description: str | None = ...,
        assignedto_id: int | None = ...,
        include_all: bool = ...,
        case_ids: list[int] | None = ...,
        config_ids: list[int] | None = ...,
        runs: list[dict[str, Any]] | None = ...,
    ) -> dict[str, Any] | None: ...
    def update_plan_entry(
        self, plan_id: int, entry_id: str, **kwargs: Any
    ) -> dict[str, Any] | None: ...
    def delete_plan_entry(
        self, plan_id: int, entry_id: str
    ) -> dict[str, Any] | None: ...
