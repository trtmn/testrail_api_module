from typing import Any

from .base import BaseAPI as BaseAPI

class ProjectsAPI(BaseAPI):
    def get_project(self, project_id: int) -> dict[str, Any]: ...
    def get_projects(
        self,
        is_completed: bool | None = None,
    ) -> list[dict[str, Any]]: ...
    def add_project(
        self,
        name: str,
        announcement: str | None = None,
        show_announcement: bool | None = None,
        suite_mode: int | None = None,
    ) -> dict[str, Any]: ...
    def update_project(
        self,
        project_id: int,
        name: str | None = None,
        announcement: str | None = None,
        show_announcement: bool | None = None,
        is_completed: bool | None = None,
        suite_mode: int | None = None,
    ) -> dict[str, Any]: ...
    def delete_project(self, project_id: int) -> dict[str, Any]: ...
