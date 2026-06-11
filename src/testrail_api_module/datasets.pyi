from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["DatasetsAPI"]

class DatasetsAPI(BaseAPI):
    def get_dataset(self, dataset_id: int) -> dict[str, Any]: ...
    def get_datasets(self, project_id: int) -> list[dict[str, Any]]: ...
    def add_dataset(
        self,
        project_id: int,
        name: str,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]: ...
    def update_dataset(
        self,
        dataset_id: int,
        name: str | None = None,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]: ...
    def delete_dataset(self, dataset_id: int) -> dict[str, Any]: ...
