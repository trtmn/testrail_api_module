from typing import Any

from .base import BaseAPI as BaseAPI

class AttachmentsAPI(BaseAPI):
    def add_attachment_to_case(
        self, case_id: int, file_path: str
    ) -> dict[str, Any]: ...
    def add_attachment_to_plan(
        self, plan_id: int, file_path: str
    ) -> dict[str, Any]: ...
    def add_attachment_to_plan_entry(
        self, plan_id: int, entry_id: int, file_path: str
    ) -> dict[str, Any]: ...
    def add_attachment_to_result(
        self, result_id: int, file_path: str
    ) -> dict[str, Any]: ...
    def add_attachment_to_run(
        self, run_id: int, file_path: str
    ) -> dict[str, Any]: ...
    def get_attachments_for_case(
        self,
        case_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    def get_attachments_for_plan(
        self,
        plan_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    def get_attachments_for_plan_entry(
        self, plan_id: int, entry_id: int
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    def get_attachments_for_run(
        self,
        run_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    def get_attachments_for_test(
        self, test_id: int
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    def get_attachment(self, attachment_id: int | str) -> bytes: ...
    def delete_attachment(
        self, attachment_id: int | str
    ) -> dict[str, Any]: ...
