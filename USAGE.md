# TRAM Consumer Usage Guide

This guide covers how to use `testrail-api-module` (TRAM) in your own code to interact with the
TestRail API. For contributor setup, branching strategy, and release process, see
[CLAUDE.md](CLAUDE.md) and [CONTRIBUTING](https://github.com/trtmn/testrail_api_module).

## Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Client Initialization](#client-initialization)
- [API Surface Overview](#api-surface-overview)
- [Response Shapes](#response-shapes)
- [Common Workflows](#common-workflows)
  - [Explore project structure](#explore-project-structure)
  - [Create a test run and record results](#create-a-test-run-and-record-results)
  - [Bulk result recording](#bulk-result-recording)
  - [Create a test plan](#create-a-test-plan)
  - [Create a test case](#create-a-test-case)
  - [Upload an attachment](#upload-an-attachment)
- [Exception Handling](#exception-handling)
- [Gotchas](#gotchas)
- [Context Manager](#context-manager)

---

## Installation

```bash
pip install testrail-api-module
```

Requires Python 3.11+. Runtime dependency: `requests` (pulled in automatically).

---

## Authentication

TestRail supports two authentication methods:

| Method | Parameter | When to use |
|---|---|---|
| API key | `api_key="..."` | Recommended -- generate one in TestRail under **My Settings > API Keys** |
| Password | `password="..."` | Legacy -- works but API key is preferred |

Exactly one of `api_key` or `password` must be supplied. Credentials are sent as HTTP Basic Auth
on every request.

**Recommended: store credentials in environment variables** (never hard-code them):

```bash
# .env (add to .gitignore)
TESTRAIL_BASE_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=you@example.com
TESTRAIL_API_KEY=your-api-key
```

---

## Client Initialization

```python
import os
from testrail_api_module import TestRailAPI

api = TestRailAPI(
    base_url=os.environ["TESTRAIL_BASE_URL"],
    username=os.environ["TESTRAIL_USERNAME"],
    api_key=os.environ.get("TESTRAIL_API_KEY"),
    password=os.environ.get("TESTRAIL_PASSWORD"),
    timeout=30,  # optional, seconds (default: 30)
)
```

Or with `python-dotenv` to load `.env` automatically:

```python
from dotenv import load_dotenv
load_dotenv()

import os
from testrail_api_module import TestRailAPI

api = TestRailAPI(
    base_url=os.environ["TESTRAIL_BASE_URL"],
    username=os.environ["TESTRAIL_USERNAME"],
    api_key=os.environ.get("TESTRAIL_API_KEY"),
)
```

The client validates `base_url` format and raises `ValueError` immediately if neither
`api_key` nor `password` is provided.

---

## API Surface Overview

All 24 submodule APIs are attributes on the `api` object. Every method uses keyword arguments
and returns either `dict` or `list[dict]`. No method returns `None` -- failures raise exceptions.

| Attribute | Purpose |
|---|---|
| `api.attachments` | Upload, download, and list file attachments |
| `api.bdd` | Import/export BDD (Gherkin) feature files |
| `api.cases` | CRUD for test cases, custom field handling |
| `api.configurations` | Manage config groups and individual configs |
| `api.datasets` | Manage test datasets |
| `api.groups` | Manage TestRail user groups |
| `api.labels` | Manage labels (tags for cases/runs) |
| `api.milestones` | Track milestones and sprints |
| `api.plans` | Create and manage test plans (groups of runs) |
| `api.priorities` | Manage test case priorities |
| `api.projects` | Top-level project management |
| `api.reports` | Create and run reports |
| `api.result_fields` | Inspect custom result field definitions |
| `api.results` | Record and retrieve test results |
| `api.roles` | Manage user roles |
| `api.runs` | Create and manage test runs |
| `api.sections` | Manage sections (folders) within suites |
| `api.shared_steps` | Reusable step libraries |
| `api.statuses` | Inspect and manage test statuses |
| `api.suites` | Manage test suites |
| `api.templates` | Manage case templates |
| `api.tests` | Query and record results for test instances |
| `api.users` | Manage TestRail users |
| `api.variables` | Manage test variables |

---

## Response Shapes

### Standard responses

- **Single resource** (`get_case`, `get_run`, etc.): returns `dict`
- **List resources** (`get_cases`, `get_runs`, etc.): returns `list[dict]`
- **Create/update**: returns `dict` of the created/updated resource
- **Delete**: returns `{}` (empty dict)

### Pagination

Some list endpoints (notably `get_projects`) may return a pagination envelope on newer TestRail
versions instead of a plain list:

```python
response = api.projects.get_projects()
# Newer TestRail: {"offset": 0, "limit": 250, "size": 5, "_links": {...}, "projects": [...]}
# Older TestRail: [{"id": 1, ...}, ...]
projects = response.get("projects", response) if isinstance(response, dict) else response
```

### Status IDs

| ID | Label    | Meaning                    |
|----|----------|----------------------------|
| 1  | Passed   | Test executed successfully |
| 2  | Blocked  | Cannot execute             |
| 3  | Untested | Not yet executed           |
| 4  | Retest   | Needs re-execution         |
| 5  | Failed   | Test execution failed      |

Custom statuses have IDs above 5. Use `api.statuses.get_statuses()` to discover them.

### Elapsed time format

Pass as strings: `"30s"`, `"2m"`, `"1h 30m"`, `"2h 15m 30s"`.

---

## Common Workflows

### Explore project structure

```python
# List projects
response = api.projects.get_projects()
projects = response.get("projects", response) if isinstance(response, dict) else response
for p in projects:
    print(f"{p['name']} (ID: {p['id']})")

# Suites in a project
suites = api.suites.get_suites(project_id=1)

# Sections in a suite
sections = api.sections.get_sections(project_id=1, suite_id=suites[0]["id"])

# Cases in a section
cases = api.cases.get_cases(
    project_id=1,
    suite_id=suites[0]["id"],
    section_id=sections[0]["id"],
)
```

### Create a test run and record results

```python
# Create the run (include_all=True pulls in all cases from the suite)
run = api.runs.add_run(
    project_id=1,
    name="Sprint 42 Regression",
    suite_id=5,
    include_all=True,
    description="Automated regression",
    milestone_id=3,          # optional
)

# Record a result for a specific case in the run
result = api.results.add_result_for_case(
    run_id=run["id"],
    case_id=101,
    status_id=1,             # 1 = Passed
    comment="All assertions passed",
    elapsed="2m 30s",
    version="1.2.0",
)

# Or record a result by test ID (test instance ID within the run)
tests = api.tests.get_tests(run_id=run["id"])
api.results.add_result(
    test_id=tests[0]["id"],
    status_id=1,
)

# Check progress -- pass/fail counts are on the run object itself
updated_run = api.runs.get_run(run_id=run["id"])
print(
    f"Passed: {updated_run['passed_count']}, "
    f"Failed: {updated_run['failed_count']}, "
    f"Untested: {updated_run['untested_count']}"
)

# Close the run
api.runs.close_run(run_id=run["id"])
```

### Bulk result recording

Record multiple results in a single API call (much faster than looping):

```python
api.results.add_results_for_cases(
    run_id=run["id"],
    results=[
        {"case_id": 101, "status_id": 1, "comment": "Passed", "elapsed": "1m"},
        {"case_id": 102, "status_id": 5, "comment": "Failed", "defects": "BUG-789"},
        {"case_id": 103, "status_id": 2, "comment": "Blocked by BUG-789"},
    ],
)
```

### Create a test plan

Plans group multiple runs together, useful for multi-config or multi-environment testing.

```python
plan = api.plans.add_plan(
    project_id=1,
    name="Release 2.0 Test Plan",
    milestone_id=10,
    description="Full coverage for Release 2.0",
)

# Add an entry (a run or set of runs) to the plan
entry = api.plans.add_plan_entry(
    plan_id=plan["id"],
    suite_id=5,
    name="Smoke tests",
    include_all=True,
)

# Close the plan when testing is complete
api.plans.close_plan(plan_id=plan["id"])
```

### Create a test case

TestRail instances can have required custom fields. Skipping field discovery causes validation
errors. Always discover requirements first:

```python
# Step 1: discover required fields for this section's context
required = api.cases.get_required_case_fields(section_id=123)
# Returns: {"required_fields": [...], "format_guide": {...}, "context": {...}}

# Step 2: for dropdown/multi-select fields, get option IDs
options = api.cases.get_field_options(field_name="custom_interface_type")
# Returns: {"1": "Web", "2": "Mobile", "3": "API", ...}

# Step 3: create the case
case = api.cases.add_case(
    section_id=123,
    title="Verify login with valid credentials",
    type_id=1,
    priority_id=3,
    estimate="15m",
    refs="JIRA-456",
    custom_fields={
        "custom_automation_type": "Manual",
        "custom_interface_type": ["3"],       # STRING IDs, not ints
        "custom_steps_separated": [
            {"content": "Open login page", "expected": "Login form is shown"},
            {"content": "Enter credentials", "expected": "Fields are populated"},
            {"content": "Click Sign In",    "expected": "Dashboard loads"},
        ],
        "custom_case_test_data_required": False,
    },
)
print(f"Created case {case['id']}: {case['title']}")
```

**Custom field format rules:**

| Field type | Python format |
|---|---|
| String / Text | `"plain text"` |
| Integer | `42` |
| Checkbox | `True` or `False` |
| Dropdown | `"3"` (single string ID) |
| Multi-select | `["3", "5"]` (array of string IDs, NOT integers) |
| Separated steps | `[{"content": "...", "expected": "..."}]` -- both keys required and non-empty |
| Date | `"2026-01-15"` |
| User | `5` (integer user ID) |

### Upload an attachment

```python
# Attach a file to a test case
result = api.attachments.add_attachment_to_case(
    case_id=123,
    file_path="path/to/screenshot.png",
)
print(f"Attachment ID: {result['attachment_id']}")

# Other entity targets
api.attachments.add_attachment_to_run(run_id=456, file_path="report.html")
api.attachments.add_attachment_to_result(result_id=789, file_path="error.png")
api.attachments.add_attachment_to_plan(plan_id=10, file_path="spec.pdf")
api.attachments.add_attachment_to_plan_entry(plan_id=10, entry_id=5, file_path="log.txt")

# List attachments
attachments = api.attachments.get_attachments_for_case(case_id=123)
attachments = api.attachments.get_attachments_for_run(run_id=456, limit=50)

# Download raw bytes
data = api.attachments.get_attachment(attachment_id=443)
with open("downloaded.png", "wb") as f:
    f.write(data)

# Delete
api.attachments.delete_attachment(attachment_id=443)
```

---

## Exception Handling

```python
from testrail_api_module import (
    TestRailAPIError,             # base -- catch-all for any API error
    TestRailAuthenticationError,  # 401 -- bad credentials
    TestRailRateLimitError,       # 429 -- slow down
    TestRailAPIException,         # other 4xx/5xx -- has .status_code and .response_text
)

try:
    case = api.cases.get_case(case_id=123)
except TestRailAuthenticationError:
    print("Invalid credentials -- check TESTRAIL_USERNAME and TESTRAIL_API_KEY")
except TestRailRateLimitError:
    print("Rate limit hit -- back off and retry")
except TestRailAPIException as e:
    print(f"API error {e.status_code}: {e.response_text}")
except TestRailAPIError as e:
    print(f"Unexpected TestRail error: {e}")
```

The client has built-in retry logic: up to 3 retries with exponential backoff for 429 and 5xx
responses on GET requests. POST requests are only retried on connection errors (before the
request reaches the server), never on 429/5xx (to avoid double-writes).

---

## Gotchas

**`get_projects()` may return a pagination envelope.** On newer TestRail versions the response
is `{"projects": [...], "offset": 0, "limit": 250, ...}` rather than a plain list. Always
extract the inner list (see [Response Shapes](#response-shapes)).

**Configurations API is two-level** (groups containing individual configs). The old flat
`get_configurations(project_id)` was removed in v0.6.3. Use:

```python
config_groups = api.configurations.get_configs(project_id=1)
# Each group has {"id": ..., "name": ..., "configs": [...]}
group = api.configurations.add_config_group(project_id=1, name="Browser")
config = api.configurations.add_config(config_group_id=group["id"], name="Chrome")
```

**`add_result` vs `add_result_for_case`.** These target different TestRail endpoints:

- `api.results.add_result(test_id=..., status_id=...)` -- records by *test instance ID* (the
  `id` from `api.tests.get_tests()`)
- `api.results.add_result_for_case(run_id=..., case_id=..., status_id=...)` -- records by
  *case ID* within a run (more convenient when you already know the case ID)

**Multi-select custom fields require string IDs.** `["3", "5"]` is correct; `[3, 5]` causes a
validation error.

**Custom fields must be nested under `custom_fields={}`.** Passing them as top-level keyword
arguments does nothing.

**Suites are optional for single-suite projects.** In single-suite mode `suite_id` can be
omitted; multi-suite projects require it.

**The `cases.py` field cache.** `add_case` caches field definitions in memory for performance.
If you change required field definitions on the TestRail server mid-session, call
`api.cases.clear_case_fields_cache()` before the next `add_case` call.

---

## Context Manager

The client supports use as a context manager, which closes the underlying HTTP session
automatically:

```python
with TestRailAPI(
    base_url=os.environ["TESTRAIL_BASE_URL"],
    username=os.environ["TESTRAIL_USERNAME"],
    api_key=os.environ["TESTRAIL_API_KEY"],
) as api:
    projects = api.projects.get_projects()
# session is closed when the block exits
```

Or call `api.close()` explicitly when you are done.
