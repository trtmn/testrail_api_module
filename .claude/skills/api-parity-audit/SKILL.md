---
name: api-parity-audit
description: >
  Use this skill when auditing the testrail_api_module for API parity against the official
  TestRail API reference, checking for missing endpoints, extra/fabricated methods, renamed
  endpoints, or structural mismatches. Also use when adding new TestRail API endpoints to
  the module, or when verifying that the module matches a new TestRail release.
---

# API Parity Audit Process

This skill documents how to audit and maintain parity between `testrail_api_module` and
the official TestRail API v2 reference.

## Official API Reference

The authoritative source is the TestRail API v2 reference:

- **URL**: <https://support.testrail.com/hc/en-us/sections/7077196685204-Reference>
- **Note**: There is NO official OpenAPI/Swagger spec (JSON/YAML). The docs are HTML only.
- **Note**: The support site returns 403 for direct fetches; use WebSearch instead.

### API Sections (26 total)

The official API is organized into these sections:

| Section | Key Endpoints |
|---------|--------------|
| Attachments | add_attachment_to_*, get_attachments_for_*, delete_attachment |
| BDDs | get_bdd, add_bdd |
| Cases | get_case, get_cases, add_case, update_case, delete_case, get_history_for_case, copy_cases_to_section, move_cases_to_section |
| Case Fields | get_case_fields, add_case_field |
| Case Types | get_case_types |
| Configurations | get_configs, add_config_group, add_config, update_config_group, update_config, delete_config_group, delete_config |
| Datasets | get_dataset, get_datasets, add_dataset, update_dataset, delete_dataset |
| Groups | get_group, get_groups, add_group, update_group, delete_group |
| Labels | get_label, get_labels, add_label, update_label, delete_label |
| Milestones | get_milestone, get_milestones, add_milestone, update_milestone, delete_milestone |
| Plans | get_plan, get_plans, add_plan, update_plan, close_plan, delete_plan, add_plan_entry, update_plan_entry, delete_plan_entry |
| Priorities | get_priorities |
| Projects | get_project, get_projects, add_project, update_project, delete_project |
| Reports | get_reports |
| Results | get_results, get_results_for_case, get_results_for_run, add_result, add_result_for_case, add_results, add_results_for_cases |
| Result Fields | get_result_fields |
| Roles | get_roles |
| Runs | get_run, get_runs, add_run, update_run, close_run, delete_run |
| Sections | get_section, get_sections, add_section, update_section, move_section, delete_section |
| Shared Steps | get_shared_step, get_shared_steps, add_shared_step, update_shared_step, delete_shared_step |
| Statuses | get_statuses, get_case_statuses |
| Suites | get_suite, get_suites, add_suite, update_suite, delete_suite |
| Templates | get_templates |
| Tests | get_test, get_tests |
| Users | get_user, get_users, get_user_by_email, get_current_user |
| Variables | get_variable, get_variables, add_variable, update_variable, delete_variable |

## How to Gather Endpoint Information

Since there's no machine-readable spec, use this approach:

### Step 1: Web Search per Section

For each API section, search for the specific endpoints:

```
WebSearch: "TestRail API v2 get_configs add_config_group site:support.testrail.com"
```

This returns the HTML doc pages. Parse the endpoint signatures from the search results.

### Step 2: Verify with WebFetch (when possible)

Try fetching individual doc pages directly. Note that some pages return 403;
if that happens, fall back to WebSearch results.

```
WebFetch: https://support.testrail.com/hc/en-us/articles/<article-id>
```

### Step 3: Cross-Reference the Module

For each section, inventory the module's methods:

```python
# Read the source file
Read: src/testrail_api_module/<module>.py

# Check the endpoint strings in _get() and _post() calls
Grep: pattern="self\._(?:get|post)\(" path="src/testrail_api_module/<module>.py"
```

### Step 4: Compare

For each official endpoint, check:

1. Does the module have a method that calls this endpoint?
2. Does the method name match the endpoint name?
3. Do the parameters match what the API expects?
4. Is the HTTP method correct (GET vs POST)?

## Common Mismatches Found

These are patterns discovered during the initial audit (issue #70):

### Fabricated Endpoints (methods that call non-existent API endpoints)

- Methods returning "stats" or "counts" (e.g., `get_plan_stats`, `get_status_counts`)
- Methods returning "history" or "activity" (e.g., `get_user_activity`, `get_status_history`)
- CRUD methods for read-only resources (e.g., `add_status`, `delete_status` for built-in statuses)
- See issue #71 for the full cleanup list

### Structural Mismatches

- **Configurations**: The API has a two-level structure (groups contain configs). Old module
  treated it as flat.
- **Results**: The API has distinct endpoints for test_id vs case_id. Old module conflated them.

### Naming Mismatches

- `get_case_history` should be `get_history_for_case`
- Method parameters should match the API docs exactly

## How to Add a New Endpoint

When TestRail adds new endpoints, follow this process:

### 1. Add the method to the source module

```python
# In src/testrail_api_module/<module>.py
def new_method(self, param1: int, param2: str | None = None) -> dict[str, Any]:
    """Docstring matching the official API description."""
    data: dict[str, Any] = {}
    if param2 is not None:
        data["param2"] = param2
    return self._post(f"endpoint_name/{param1}", data=data)
```

Rules:

- GET endpoints use `self._get(endpoint, params={})`
- POST endpoints use `self._post(endpoint, data={})`
- DELETE operations in TestRail use POST and return empty bodies
- Only include non-None optional params in the request
- Line length: 79 chars

### 2. Update the type stub

Add the method signature to `src/testrail_api_module/<module>.pyi`.

### 3. Wire into **init**.py (for new modules only)

If adding a whole new module:

- Add `from . import <module>` to `__init__.py`
- Add `self.<module> = <module>.<ClassName>API(self)` in `__init__`
- Add `'<module>'` to `__all__`
- Update `__init__.pyi` similarly

### 4. Write tests

Follow `tests/test-writing-standards.mdc`. Required tests per method:

- init, minimal params, all params, None values
- Error handling (APIError, AuthError, RateLimitError)
- Edge cases

### 5. Run checks

```bash
uv run ruff check . --fix && uv run ruff format .
uv run pytest tests/
```

## Tracking Issues

- **Issue #70**: Endpoint audit — confirm module matches TestRail API exactly
- **Issue #71**: Extra methods cleanup — remove fabricated endpoints that don't exist in the real API
