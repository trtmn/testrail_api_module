from typing import Any

from .base import BaseAPI as BaseAPI

class ReportsAPI(BaseAPI):
    def get_reports(self, project_id: int) -> list[dict[str, Any]]: ...
    def run_report(self, report_template_id: int) -> dict[str, Any]: ...
