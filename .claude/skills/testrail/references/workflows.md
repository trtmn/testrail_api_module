# TestRail Python API Workflow Examples

## Table of Contents

- [Initialize the API Client](#initialize-the-api-client)
- [Explore Project Structure](#explore-project-structure)
- [Full Test Execution Cycle](#full-test-execution-cycle)
- [Bulk Result Recording](#bulk-result-recording)
- [Create and Manage a Test Plan](#create-and-manage-a-test-plan)
- [Retrieve Results and Statistics](#retrieve-results-and-statistics)
- [Create Test Cases](#create-test-cases)
- [User Management](#user-management)
- [Milestone Management](#milestone-management)
- [Shared Steps](#shared-steps)
- [BDD Scenarios](#bdd-scenarios)

## Initialize the API Client

Before running any script, ensure a valid `.env` exists at the project root with
`TESTRAIL_BASE_URL`, `TESTRAIL_USERNAME`, and `TESTRAIL_API_KEY`. If it is missing or
incomplete, prompt the user for credentials or create the `.env` for them to fill in
(see SKILL.md "Client Initialization" for the full procedure).

Every script starts with this pattern:

```python
import os
from dotenv import load_dotenv
load_dotenv()  # Loads .env from project root

from testrail_api_module import (
    TestRailAPI,
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
    TestRailAPIException
)

api = TestRailAPI(
    base_url=os.environ["TESTRAIL_BASE_URL"],
    username=os.environ["TESTRAIL_USERNAME"],
    api_key=os.environ.get("TESTRAIL_API_KEY"),
    password=os.environ.get("TESTRAIL_PASSWORD"),
)
```

## Explore Project Structure

Navigate a project's complete hierarchy:

```python
# 1. List all projects
projects = api.projects.get_projects()
for p in projects:
    print(f"Project: {p['name']} (ID: {p['id']})")

# 2. Get project details and stats
project = api.projects.get_project(project_id=1)
stats = api.projects.get_project_stats(project_id=1)

# 3. List suites in the project
suites = api.suites.get_suites(project_id=1)
for s in suites:
    print(f"  Suite: {s['name']} (ID: {s['id']})")

# 4. List sections in a suite
sections = api.sections.get_sections(project_id=1, suite_id=suites[0]['id'])
for sec in sections:
    print(f"    Section: {sec['name']} (ID: {sec['id']})")

# 5. List cases in a section
cases = api.cases.get_cases(
    project_id=1,
    suite_id=suites[0]['id'],
    section_id=sections[0]['id']
)
for c in cases:
    print(f"      Case: {c['title']} (ID: {c['id']})")
```

## Full Test Execution Cycle

Create a run, execute tests, record results, and close the run:

```python
# 1. Create a test run
run = api.runs.add_run(
    project_id=1,
    name="Sprint 42 Regression",
    suite_id=5,
    include_all=True,         # Include all cases from the suite
    description="Automated regression test"
)
run_id = run['id']
print(f"Created run: {run['name']} (ID: {run_id})")

# 2. Get tests in the run
tests = api.tests.get_tests(run_id=run_id)
print(f"Run has {len(tests)} tests")

# 3. Record results for individual tests
for test in tests:
    result = api.results.add_result(
        run_id=run_id,
        case_id=test['case_id'],
        status_id=1,                    # 1=Passed
        comment="All assertions passed",
        elapsed="2m 30s",
        version="1.2.0"
    )

# 4. Check run progress
stats = api.runs.get_run_stats(run_id=run_id)
print(f"Progress: {stats}")

# 5. Close the run
api.runs.close_run(run_id=run_id)
print("Run closed")
```

To include only specific cases instead of all:

```python
run = api.runs.add_run(
    project_id=1,
    name="Targeted Test Run",
    suite_id=5,
    include_all=False,
    case_ids=[101, 102, 103]    # Only these cases
)
```

## Bulk Result Recording

Record results for multiple cases in a single API call:

```python
api.results.add_results_for_cases(
    run_id=run_id,
    results=[
        {
            "case_id": 101,
            "status_id": 1,
            "comment": "Passed - all checks green",
            "elapsed": "1m 20s",
            "version": "2.0.0"
        },
        {
            "case_id": 102,
            "status_id": 5,
            "comment": "Failed - assertion error on line 42",
            "elapsed": "3m",
            "defects": "BUG-789"
        },
        {
            "case_id": 103,
            "status_id": 2,
            "comment": "Blocked by BUG-789"
        },
        {
            "case_id": 104,
            "status_id": 4,
            "comment": "Needs retest after fix"
        }
    ]
)
```

Status codes: 1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed

## Create and Manage a Test Plan

Plans group multiple test runs together:

```python
# 1. Create the plan
plan = api.plans.add_plan(
    project_id=1,
    name="Release 2.0 Test Plan",
    milestone_id=10,
    description="Comprehensive testing for Release 2.0"
)
plan_id = plan['id']

# 2. Monitor plan progress
stats = api.plans.get_plan_stats(plan_id=plan_id)

# 3. Get full plan details (includes entries/runs)
plan_details = api.plans.get_plan(plan_id=plan_id)

# 4. Close the plan when done
api.plans.close_plan(plan_id=plan_id)
```

## Retrieve Results and Statistics

Get comprehensive results data for analysis:

```python
# All results for a run
results = api.results.get_results_for_run(run_id=1)
for r in results:
    print(f"Case {r['case_id']}: status={r['status_id']}, comment={r.get('comment', '')}")

# Results for a specific case in a run
case_results = api.results.get_results_for_case(run_id=1, case_id=123)

# Run statistics
run_stats = api.runs.get_run_stats(run_id=1)

# Status counts
status_counts = api.statuses.get_status_counts(run_id=1)
```

## Create Test Cases

Always discover required fields first (see cases-and-custom-fields.md for details):

```python
# 1. Discover required fields
required = api.cases.get_required_case_fields(section_id=123)
print("Required fields:")
for field in required['required_fields']:
    print(f"  {field['system_name']} ({field['type_name']})")

# 2. Get options for dropdown fields
options = api.cases.get_field_options(field_name="custom_interface_type")
print(f"Options: {options}")

# 3. Create the case
case = api.cases.add_case(
    section_id=123,
    title="Verify login with valid credentials",
    type_id=1,
    priority_id=3,
    custom_fields={
        "custom_automation_type": "Manual",
        "custom_interface_type": ["3"],
        "custom_steps_separated": [
            {"content": "Open login page", "expected": "Login form displayed"},
            {"content": "Enter credentials", "expected": "Fields populated"},
            {"content": "Click Sign In", "expected": "Dashboard loads"}
        ],
        "custom_case_test_data_required": False
    }
)
print(f"Created case: {case['title']} (ID: {case['id']})")
```

## User Management

```python
# List all users
users = api.users.get_users()
for u in users:
    print(f"{u['name']} ({u['email']})")

# Find user by email
user = api.users.get_user_by_email(email="user@company.com")

# Get user activity
activity = api.users.get_user_activity(user_id=user['id'])

# Get user's projects
projects = api.users.get_user_projects(user_id=user['id'])

# Get user's roles
roles = api.users.get_user_roles(user_id=user['id'])
```

## Milestone Management

```python
# List milestones
milestones = api.milestones.get_milestones(project_id=1)

# Create milestone
milestone = api.milestones.add_milestone(
    project_id=1,
    name="Sprint 42"
)

# Get milestone stats
stats = api.milestones.get_milestone_stats(milestone_id=milestone['id'])

# Complete a milestone
api.milestones.update_milestone(
    milestone_id=milestone['id'],
    is_completed=True
)
```

## Shared Steps

```python
# List shared steps
steps = api.shared_steps.get_shared_steps(project_id=1)

# Create shared step
shared = api.shared_steps.add_shared_step(
    project_id=1,
    title="Login as admin",
    steps=[
        {"content": "Navigate to login page", "expected": "Login form shown"},
        {"content": "Enter admin credentials", "expected": "Dashboard loads"}
    ]
)
```

## BDD Scenarios

```python
# Import a BDD feature file
api.bdd.add_bdd(section_id=123, feature_file="/path/to/login.feature")

# Export a BDD scenario from a case
scenario = api.bdd.get_bdd(case_id=456)
```
