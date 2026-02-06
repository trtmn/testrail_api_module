---
name: testrail
description: >
  Use this skill when the user asks to interact with TestRail in any way: manage test cases,
  create test runs, add test results, check TestRail, get test plans, explore TestRail projects,
  record test execution, query test cases, update test cases, get run results, manage milestones,
  manage test suites, manage test sections, upload attachments to TestRail, get TestRail users,
  manage configurations, create BDD scenarios, manage shared steps, manage variables, manage
  templates, manage priorities, manage roles, manage groups, or any task involving TestRail
  test management. This skill provides guidance for using the testrail_api_module Python package
  directly to interact with TestRail via Python scripts.
---

# TestRail Python API

Use the `testrail_api_module` Python package to interact with TestRail directly via Python scripts.

## Setup

Install the package (first time only):
```bash
uv pip install testrail-api-module
```

## Client Initialization

Before making any API calls, check for the `.env` file at the project root. If it does not exist
or is missing TestRail variables, handle it before proceeding:

1. **Look for `.env`** at the project root using the Glob tool.
2. **If found**, read it and verify it contains `TESTRAIL_BASE_URL`, `TESTRAIL_USERNAME`, and
   `TESTRAIL_API_KEY` (or `TESTRAIL_PASSWORD`) with actual values (not empty/placeholder).
3. **If `.env` is missing or incomplete**, use AskUserQuestion to ask the user for the missing
   credentials (base URL, username, API key). Then create or update the `.env` file with their
   answers before continuing.

Once the `.env` is confirmed valid, initialize the client:

```python
import os
from dotenv import load_dotenv
load_dotenv()  # Loads TESTRAIL_BASE_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY

from testrail_api_module.mcp_utils import create_api_from_env
api = create_api_from_env()
```

Required `.env` variables:
- `TESTRAIL_BASE_URL` - e.g. `https://your-instance.testrail.io`
- `TESTRAIL_USERNAME` - email address
- `TESTRAIL_API_KEY` - API key (or `TESTRAIL_PASSWORD`)

Template for creating a new `.env` (exclude any non-TestRail variables already present):
```
TESTRAIL_BASE_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-email@example.com
TESTRAIL_API_KEY=your-api-key
```

## API Access Pattern

All 23 modules are properties on the `api` object:

```python
api.projects.get_projects()
api.cases.get_case(case_id=123)
api.runs.add_run(project_id=1, name="Sprint 42")
api.results.add_result(run_id=1, case_id=123, status_id=1)
```

## Return Types

- **GET methods**: Return `dict` or `list[dict]`
- **POST/PATCH methods**: Return `dict` (the created/updated resource)
- **DELETE methods**: Return `{}` on success
- Methods never return `None` -- they raise exceptions on failure

## Exception Handling

```python
from testrail_api_module import (
    TestRailAPIError,              # Base exception
    TestRailAuthenticationError,   # 401
    TestRailRateLimitError,        # 429
    TestRailAPIException           # General errors with status_code and response_text
)

try:
    case = api.cases.get_case(case_id=123)
except TestRailAuthenticationError:
    print("Invalid credentials")
except TestRailAPIException as e:
    print(f"API error {e.status_code}: {e.response_text}")
```

## TestRail Data Hierarchy

```
Project
├── Suites (test organization containers)
│   └── Sections (folders within suites)
│       └── Cases (individual test definitions)
├── Milestones (release/sprint tracking)
├── Plans (collections of test runs)
│   └── Runs (execution instances)
│       └── Tests (case instances within a run)
│           └── Results (execution outcomes)
└── Configurations, Groups, Variables, Templates
```

## Status Codes

| ID | Status   | Meaning                        |
|----|----------|--------------------------------|
| 1  | Passed   | Test executed successfully     |
| 2  | Blocked  | Cannot execute (dependency)    |
| 3  | Untested | Not yet executed               |
| 4  | Retest   | Needs re-execution             |
| 5  | Failed   | Test execution failed          |

## Critical: Creating Test Cases

Before creating or updating test cases, ALWAYS discover required fields first. Skipping this causes repeated validation errors.

**Mandatory workflow:**

1. Discover required fields:
   ```python
   fields = api.cases.get_required_case_fields(section_id=123)
   ```

2. Get dropdown options for multi-select/dropdown fields:
   ```python
   options = api.cases.get_field_options(field_name="custom_interface_type")
   ```

3. Create the case with all required fields:
   ```python
   case = api.cases.add_case(
       section_id=123,
       title="Test title",
       custom_fields={
           "custom_automation_type": "Manual",
           "custom_interface_type": ["3", "5"],  # STRING IDs, not ints!
           "custom_steps_separated": [
               {"content": "Step 1", "expected": "Result 1"}
           ],
           "custom_case_test_data_required": False
       }
   )
   ```

### Custom Field Format Rules

- **Dropdown/Multi-select**: Arrays of STRING IDs -- `["3", "5"]` NOT `[3, 5]`
- **Separated steps**: `[{"content": "...", "expected": "..."}]` -- both keys required, non-empty
- **Checkboxes**: `True` / `False`
- **Text fields**: Plain string values
- **Nesting**: Always pass custom fields under the `custom_fields={}` parameter

## Common Operations

```python
# List projects
projects = api.projects.get_projects()

# Get cases for a project
cases = api.cases.get_cases(project_id=1, suite_id=2)

# Create a run
run = api.runs.add_run(project_id=1, name="Regression", suite_id=2, include_all=True)

# Record a result
api.results.add_result(run_id=run['id'], case_id=123, status_id=1, comment="Passed")

# Bulk results
api.results.add_results_for_cases(run_id=run['id'], results=[
    {"case_id": 1, "status_id": 1, "comment": "Passed"},
    {"case_id": 2, "status_id": 5, "comment": "Failed", "defects": "BUG-123"}
])

# Close a run
api.runs.close_run(run_id=run['id'])

# Get run stats
stats = api.runs.get_run_stats(run_id=run['id'])
```

## Elapsed Time Format

Use strings: `"30s"`, `"2m"`, `"1h 30m"`, `"2h 15m 30s"`

## Reference Files

For detailed information, consult these reference files as needed:

- **`references/modules-quick-reference.md`** -- All 23 modules with methods and required params
- **`references/cases-and-custom-fields.md`** -- Custom field types, validation, and complete examples
- **`references/workflows.md`** -- Full Python script examples for common multi-step workflows
