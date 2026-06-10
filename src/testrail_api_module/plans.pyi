from typing import Any

from .base import BaseAPI as BaseAPI

class PlansAPI(BaseAPI):
    def get_plan(self, plan_id: int) -> dict[str, Any]: ...
    def get_plans(
        self,
        project_id: int,
        created_after: int | None = ...,
        created_before: int | None = ...,
        created_by: int | None = ...,
        is_completed: bool | None = ...,
        milestone_id: int | None = ...,
        limit: int | None = ...,
        offset: int | None = ...,
    ) -> dict[str, Any]: ...
    def add_plan(
        self,
        project_id: int,
        name: str,
        description: str | None = ...,
        milestone_id: int | None = ...,
        entries: list[dict[str, Any]] | None = ...,
    ) -> dict[str, Any]: ...
    def update_plan(self, plan_id: int, **kwargs: Any) -> dict[str, Any]: ...
    def close_plan(self, plan_id: int) -> dict[str, Any]: ...
    def delete_plan(self, plan_id: int) -> dict[str, Any]: ...
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
    ) -> dict[str, Any]: ...
    def update_plan_entry(
        self, plan_id: int, entry_id: str, **kwargs: Any
    ) -> dict[str, Any]: ...
    def delete_plan_entry(
        self, plan_id: int, entry_id: str
    ) -> dict[str, Any]: ...
    def add_run_to_plan_entry(
        self,
        plan_id: int,
        entry_id: str,
        config_ids: list[int],
        description: str | None = ...,
        assignedto_id: int | None = ...,
        include_all: bool = ...,
        case_ids: list[int] | None = ...,
        refs: str | None = ...,
    ) -> dict[str, Any]: ...
    def update_run_in_plan_entry(
        self,
        run_id: int,
        description: str | None = ...,
        assignedto_id: int | None = ...,
        include_all: bool | None = ...,
        case_ids: list[int] | None = ...,
        refs: str | None = ...,
    ) -> dict[str, Any]: ...
    def delete_run_from_plan_entry(self, run_id: int) -> dict[str, Any]: ...
