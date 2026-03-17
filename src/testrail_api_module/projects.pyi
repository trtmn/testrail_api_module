from typing import Any

from .base import BaseAPI as BaseAPI

class ProjectsAPI(BaseAPI):
    def get_project(self, project_id: int) -> dict[str, Any]: ...
    def get_projects(self) -> list[dict[str, Any]]: ...
    def add_project(
        self,
        name: str,
        announcement: str | None = None,
        show_announcement: bool = False,
        is_completed: bool = False,
    ) -> dict[str, Any]: ...
    def update_project(
        self, project_id: int, **kwargs: Any
    ) -> dict[str, Any]: ...
    def delete_project(self, project_id: int) -> dict[str, Any]: ...
