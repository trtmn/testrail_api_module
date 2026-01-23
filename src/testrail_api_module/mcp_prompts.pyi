"""
Type stubs for MCP prompts module.
"""
from typing import Optional, List, Dict, Any

def add_test_cases_prompt(
    section_id: int,
    title: str,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List[Any]: ...

def retrieve_test_run_data_prompt(
    run_id: int
) -> List[Any]: ...

def create_test_run_prompt(
    project_id: int,
    name: str,
    suite_id: Optional[int] = None,
    milestone_id: Optional[int] = None,
    description: Optional[str] = None,
    assignedto_id: Optional[int] = None,
    include_all: bool = True,
    case_ids: Optional[List[int]] = None
) -> List[Any]: ...

def create_test_plan_prompt(
    project_id: int,
    name: str,
    description: Optional[str] = None,
    milestone_id: Optional[int] = None,
    entries: Optional[List[Dict[str, Any]]] = None
) -> List[Any]: ...

def add_test_results_prompt(
    run_id: int,
    case_id: int,
    status_id: int,
    comment: Optional[str] = None,
    version: Optional[str] = None,
    elapsed: Optional[str] = None,
    defects: Optional[str] = None
) -> List[Any]: ...

def get_test_case_details_prompt(
    case_id: int
) -> List[Any]: ...

def update_test_case_prompt(
    case_id: int,
    title: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List[Any]: ...

def get_test_plan_details_prompt(
    plan_id: int
) -> List[Any]: ...

def get_project_info_prompt(
    project_id: int
) -> List[Any]: ...

def get_run_results_prompt(
    run_id: int
) -> List[Any]: ...
