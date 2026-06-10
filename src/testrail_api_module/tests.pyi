from typing import Any

from .base import BaseAPI as BaseAPI

__all__ = ["TestsAPI"]

class TestsAPI(BaseAPI):
    def get_test(
        self, test_id: int, with_data: int | None = None
    ) -> dict[str, Any]: ...
    def get_tests(
        self,
        run_id: int,
        status_id: int | list[int] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        label_id: int | list[int] | None = None,
    ) -> list[dict[str, Any]]: ...
