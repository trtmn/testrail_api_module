"""
Type stubs for MCP prompts module.
"""
from typing import Optional, List, Dict, Any

def add_test_cases_prompt(
    project_name: str,
    section_name: str,
    title: str,
    suite_name: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List[Any]: ...

def retrieve_test_run_data_prompt(
    run_name: str,
    project_name: Optional[str] = None
) -> List[Any]: ...

def create_test_run_prompt(
    project_name: str,
    name: str,
    suite_name: Optional[str] = None,
    milestone_name: Optional[str] = None,
    description: Optional[str] = None,
    include_all: bool = True,
    case_titles: Optional[List[str]] = None
) -> List[Any]: ...

def create_test_plan_prompt(
    project_name: str,
    name: str,
    description: Optional[str] = None,
    milestone_name: Optional[str] = None
) -> List[Any]: ...

def add_test_results_prompt(
    run_name: str,
    case_title: str,
    status_id: int,
    project_name: Optional[str] = None,
    comment: Optional[str] = None,
    version: Optional[str] = None,
    elapsed: Optional[str] = None,
    defects: Optional[str] = None
) -> List[Any]: ...

def get_test_case_details_prompt(
    case_title: str,
    project_name: Optional[str] = None
) -> List[Any]: ...

def update_test_case_prompt(
    case_title: str,
    project_name: Optional[str] = None,
    title: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List[Any]: ...

def get_test_plan_details_prompt(
    plan_name: str,
    project_name: Optional[str] = None
) -> List[Any]: ...

def get_project_info_prompt(
    project_name: str
) -> List[Any]: ...

def get_run_results_prompt(
    run_name: str,
    project_name: Optional[str] = None
) -> List[Any]: ...
