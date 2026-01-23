"""
MCP (Model Context Protocol) prompts for TestRail API.

This module provides reusable prompt templates that guide users through
common TestRail workflows. Prompts are instruction templates that help users
accomplish tasks more efficiently than using tools directly.

Prompts use FastMCP's @prompt decorator and return formatted instruction
messages that guide users through TestRail operations.
"""
from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp.prompts import UserMessage
else:
    try:
        from mcp.server.fastmcp.prompts import UserMessage
    except ImportError:
        # Fallback if import fails
        UserMessage = None  # type: ignore


def add_test_cases_prompt(
    section_id: int,
    title: str,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for adding test cases to TestRail.

    This prompt helps you create test cases with proper field formats
    and required field discovery. It follows the recommended workflow of
    discovering required fields first, then creating the case.

    Args:
        section_id: The ID of the section where the test case will be created.
        title: The title/name of the test case.
        type_id: Optional test type ID (1=Functional, 2=Performance, etc.).
        priority_id: Optional priority ID (1=Critical, 2=High, 3=Medium, etc.).
        estimate: Optional time estimate (e.g., "30m", "1h 30m").
        description: Optional description of the test case.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        # Fallback if UserMessage is not available
        return []

    instructions = f"""# Adding Test Cases to TestRail

## Overview
You are about to create a test case in TestRail. Follow this guided workflow to ensure
the case is created with all required fields in the correct format.

## Step 1: Discover Required Fields (IMPORTANT!)

Before creating the test case, you MUST discover which fields are required for this section.
This prevents errors and ensures correct field formats.

**Action:** Use the `testrail_cases` tool with action `get_required_case_fields`:
```json
{{
  "action": "get_required_case_fields",
  "params": {{
    "section_id": {section_id}
  }}
}}
```

This will return:
- All required custom fields with their types
- Format examples for each field type
- Field system names to use in the API call

## Step 2: Review Field Types

Pay special attention to:
- **Dropdown/Multi-select fields**: Must be arrays of STRING IDs (e.g., `["3", "5"]`) - NOT integers!
- **Separated steps fields**: Must be arrays of objects with `content` and `expected` keys
- **Checkbox fields**: Must be boolean values (true/false)
- **Text fields**: Must be string values

## Step 3: Get Field Options (if needed)

For dropdown/multi-select fields, you may need to get available options:
```json
{{
  "action": "get_field_options",
  "params": {{
    "field_name": "custom_interface_type"
  }}
}}
```

## Step 4: Create the Test Case

Now create the test case with all required fields:

**Action:** Use the `testrail_cases` tool with action `add_case`:
```json
{{
  "action": "add_case",
  "params": {{
    "section_id": {section_id},
    "title": "{title}"{f',\n    "type_id": {type_id}' if type_id else ''}{f',\n    "priority_id": {priority_id}' if priority_id else ''}{f',\n    "estimate": "{estimate}"' if estimate else ''}{f',\n    "description": "{description}"' if description else ''},
    "custom_fields": {{
      // Add all required custom fields here based on Step 1 results
      // Example formats:
      // "custom_interface_type": ["3", "5"],  // Array of STRING IDs
      // "custom_steps_separated": [
      //   {{"content": "Step 1", "expected": "Result 1"}},
      //   {{"content": "Step 2", "expected": "Result 2"}}
      // ],
      // "custom_case_test_data_required": true  // Boolean
    }}
  }}
}}
```

## Important Notes

1. **Custom fields must be nested** in the `custom_fields` parameter, not as top-level parameters
2. **Use STRING IDs** for dropdown/multi-select fields: `["3", "5"]` not `[3, 5]`
3. **Steps must be objects** with `content` and `expected` keys, both non-empty strings
4. **Always discover fields first** to avoid validation errors

## Related Prompts

- `testrail_update_test_case` - To update this case later
- `testrail_get_test_case_details` - To retrieve case information

## Related Tools

- `testrail_cases` - All test case operations
- `testrail_sections` - Section management
"""

    return [UserMessage(content=instructions)]


def retrieve_test_run_data_prompt(
    run_id: int
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test run data from TestRail.

    This prompt helps you get all relevant information about a test run,
    including run details, associated tests, and results.

    Args:
        run_id: The ID of the test run to retrieve data for.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Retrieving Test Run Data from TestRail

## Overview
You are retrieving comprehensive data about test run ID {run_id}. This workflow
will help you get all relevant information including run details, tests, and results.

## Step 1: Get Test Run Details

First, retrieve the basic test run information:

**Action:** Use the `testrail_runs` tool with action `get_run`:
```json
{{
  "action": "get_run",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns:
- Run name, description, and status
- Project and suite information
- Milestone and assigned user
- Created/updated timestamps
- Configuration details

## Step 2: Get Run Statistics

Get summary statistics for the test run:

**Action:** Use the `testrail_runs` tool with action `get_run_stats`:
```json
{{
  "action": "get_run_stats",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns:
- Total tests count
- Status breakdown (passed, failed, blocked, etc.)
- Progress percentage
- Status distribution

## Step 3: Get All Tests in the Run

Retrieve all test cases included in this run:

**Action:** Use the `testrail_tests` tool with action `get_tests`:
```json
{{
  "action": "get_tests",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns a list of all tests with:
- Test case information
- Current status
- Assigned user
- Test case details

## Step 4: Get Test Results

Retrieve all test results for this run:

**Action:** Use the `testrail_results` tool with action `get_results_for_run`:
```json
{{
  "action": "get_results_for_run",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns:
- All test results with status
- Comments and defects
- Execution time (elapsed)
- Version information
- Custom field values

## Step 5: Get Results for Specific Test (Optional)

To get results for a specific test case in the run:

**Action:** Use the `testrail_results` tool with action `get_results_for_case`:
```json
{{
  "action": "get_results_for_case",
  "params": {{
    "run_id": {run_id},
    "case_id": <case_id>
  }}
}}
```

## Complete Data Structure

After following these steps, you will have:
1. **Run metadata**: Name, description, status, dates
2. **Statistics**: Summary counts and percentages
3. **Test list**: All tests included in the run
4. **Results**: All execution results with details

## Related Prompts

- `testrail_get_run_results` - Focused on just results
- `testrail_create_test_run` - To create new runs

## Related Tools

- `testrail_runs` - Run management operations
- `testrail_tests` - Test operations
- `testrail_results` - Result operations
"""

    return [UserMessage(content=instructions)]


def create_test_run_prompt(
    project_id: int,
    name: str,
    suite_id: Optional[int] = None,
    milestone_id: Optional[int] = None,
    description: Optional[str] = None,
    assignedto_id: Optional[int] = None,
    include_all: bool = True,
    case_ids: Optional[List[int]] = None
) -> List['UserMessage']:
    """
    Guide for creating a new test run in TestRail.

    This prompt helps you create a test run with proper configuration,
    including suite selection and case inclusion options.

    Args:
        project_id: The ID of the project to create the run in.
        name: The name of the test run.
        suite_id: Optional ID of the test suite to base the run on.
        milestone_id: Optional ID of the milestone to associate with the run.
        description: Optional description of the test run.
        assignedto_id: Optional ID of the user to assign the run to.
        include_all: Whether to include all test cases from the suite (default: True).
        case_ids: Optional list of specific case IDs to include (if include_all is False).

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    case_ids_str = f"[{', '.join(map(str, case_ids))}]" if case_ids else None

    instructions = f"""# Creating a Test Run in TestRail

## Overview
You are creating a new test run in TestRail. Test runs are used to execute test cases
and track their results. Follow this guide to create a properly configured test run.

## Step 1: Prepare Run Parameters

Gather the following information:
- **Project ID**: {project_id}
- **Run Name**: {name}
{f'- **Suite ID**: {suite_id}' if suite_id else '- **Suite ID**: (optional - will use default suite)'}
{f'- **Milestone ID**: {milestone_id}' if milestone_id else '- **Milestone ID**: (optional)'}
{f'- **Description**: {description}' if description else '- **Description**: (optional)'}
{f'- **Assigned To**: User ID {assignedto_id}' if assignedto_id else '- **Assigned To**: (optional)'}
- **Include All Cases**: {str(include_all).lower()}
{f'- **Specific Case IDs**: {case_ids_str}' if case_ids else ''}

## Step 2: Create the Test Run

**Action:** Use the `testrail_runs` tool with action `add_run`:
```json
{{
  "action": "add_run",
  "params": {{
    "project_id": {project_id},
    "name": "{name}"{f',\n    "suite_id": {suite_id}' if suite_id else ''}{f',\n    "milestone_id": {milestone_id}' if milestone_id else ''}{f',\n    "description": "{description}"' if description else ''}{f',\n    "assignedto_id": {assignedto_id}' if assignedto_id else ''},
    "include_all": {str(include_all).lower()}{f',\n    "case_ids": {case_ids_str}' if case_ids and not include_all else ''}
  }}
}}
```

## Important Notes

1. **include_all vs case_ids**:
   - If `include_all` is `true`, all cases from the suite are included
   - If `include_all` is `false`, you must provide `case_ids` to specify which cases to include
   - You cannot use both `include_all: true` and `case_ids` together

2. **Suite Selection**:
   - If `suite_id` is not provided, TestRail will use the default suite for the project
   - Make sure the suite exists and contains test cases

3. **Run Status**:
   - New runs are created in "Active" status
   - Use `close_run` action to mark the run as completed later

## Step 3: Verify the Run (Optional)

After creation, retrieve the run to verify it was created correctly:

**Action:** Use the `testrail_runs` tool with action `get_run`:
```json
{{
  "action": "get_run",
  "params": {{
    "run_id": <run_id_from_step_2>
  }}
}}
```

## Related Prompts

- `testrail_retrieve_test_run_data` - To get comprehensive run data
- `testrail_add_test_results` - To add results to this run
- `testrail_get_run_results` - To retrieve results from this run

## Related Tools

- `testrail_runs` - All test run operations
- `testrail_projects` - Project information
- `testrail_suites` - Suite information
"""

    return [UserMessage(content=instructions)]


def create_test_plan_prompt(
    project_id: int,
    name: str,
    description: Optional[str] = None,
    milestone_id: Optional[int] = None,
    entries: Optional[List[Dict[str, Any]]] = None
) -> List['UserMessage']:
    """
    Guide for creating a test plan in TestRail.

    This prompt helps you create a test plan with optional test run entries.
    Test plans organize and schedule multiple test runs.

    Args:
        project_id: The ID of the project to create the plan in.
        name: The name of the test plan.
        description: Optional description of the test plan.
        milestone_id: Optional ID of the milestone to associate with the plan.
        entries: Optional list of test plan entries (runs) to include in the plan.
                 Each entry should contain: suite_id, name, and optional fields.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    entries_example = """[
    {
      "suite_id": 1,
      "name": "Regression Test Run 1",
      "description": "Full regression suite",
      "include_all": true
    },
    {
      "suite_id": 2,
      "name": "Smoke Test Run",
      "include_all": true,
      "case_ids": [1, 2, 3]
    }
  ]"""

    instructions = f"""# Creating a Test Plan in TestRail

## Overview
You are creating a new test plan in TestRail. Test plans organize and schedule
multiple test runs, making it easier to manage complex testing scenarios.

## Step 1: Prepare Plan Parameters

Gather the following information:
- **Project ID**: {project_id}
- **Plan Name**: {name}
{f'- **Description**: {description}' if description else '- **Description**: (optional)'}
{f'- **Milestone ID**: {milestone_id}' if milestone_id else '- **Milestone ID**: (optional)'}
{f'- **Entries**: {len(entries) if entries else 0} test run(s) to include' if entries else '- **Entries**: (optional - can add runs later)'}

## Step 2: Prepare Test Run Entries (Optional)

If you want to include test runs in the plan, prepare entry objects. Each entry
represents a test run that will be created as part of the plan:

**Entry Structure:**
```json
{{
  "suite_id": <suite_id>,           // Required: Suite to base run on
  "name": "<run_name>",              // Required: Name of the test run
  "description": "<description>",    // Optional: Run description
  "assignedto_id": <user_id>,        // Optional: Assign to user
  "include_all": true,               // Optional: Include all cases (default: true)
  "case_ids": [1, 2, 3]              // Optional: Specific cases (if include_all is false)
}}
```

{f'**Your Entries:**\n```json\n{entries_example if not entries else str(entries)}\n```' if entries else '**Note:** You can create the plan without entries and add runs later using `update_plan`.'}

## Step 3: Create the Test Plan

**Action:** Use the `testrail_plans` tool with action `add_plan`:
```json
{{
  "action": "add_plan",
  "params": {{
    "project_id": {project_id},
    "name": "{name}"{f',\n    "description": "{description}"' if description else ''}{f',\n    "milestone_id": {milestone_id}' if milestone_id else ''}{f',\n    "entries": {str(entries) if entries else "[]"}' if entries else ''}
  }}
}}
```

## Important Notes

1. **Plan vs Run**:
   - A plan can contain multiple test runs
   - Each entry in the plan creates a separate test run
   - Plans help organize related runs together

2. **Adding Entries Later**:
   - You can create a plan without entries
   - Use `update_plan` action to add entries later
   - Or create runs separately and associate them with the plan

3. **Entry Requirements**:
   - Each entry must have `suite_id` and `name`
   - `include_all` and `case_ids` work the same as in `add_run`
   - You cannot use both `include_all: true` and `case_ids` together

## Step 4: Verify the Plan (Optional)

After creation, retrieve the plan to verify:

**Action:** Use the `testrail_plans` tool with action `get_plan`:
```json
{{
  "action": "get_plan",
  "params": {{
    "plan_id": <plan_id_from_step_3>
  }}
}}
```

## Related Prompts

- `testrail_get_test_plan_details` - To retrieve comprehensive plan information
- `testrail_create_test_run` - To create individual runs (alternative to plan entries)

## Related Tools

- `testrail_plans` - All test plan operations
- `testrail_runs` - Individual run operations
- `testrail_suites` - Suite information for entries
"""

    return [UserMessage(content=instructions)]


def add_test_results_prompt(
    run_id: int,
    case_id: int,
    status_id: int,
    comment: Optional[str] = None,
    version: Optional[str] = None,
    elapsed: Optional[str] = None,
    defects: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for adding test execution results to TestRail.

    This prompt helps you record test results with proper status codes
    and optional metadata like comments, version, and execution time.

    Args:
        run_id: The ID of the test run.
        case_id: The ID of the test case.
        status_id: The status ID (1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed).
        comment: Optional comment describing the test result.
        version: Optional version of the software under test.
        elapsed: Optional time taken to execute (e.g., "30s", "2m 30s").
        defects: Optional comma-separated list of defect IDs or references.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    status_map = {
        1: "Passed",
        2: "Blocked",
        3: "Untested",
        4: "Retest",
        5: "Failed"
    }
    status_name = status_map.get(status_id, f"Status {status_id}")

    instructions = f"""# Adding Test Results to TestRail

## Overview
You are recording a test execution result in TestRail. This workflow helps you
add results with proper status codes and optional metadata.

## Step 1: Understand Status Codes

TestRail uses numeric status IDs:
- **1 = Passed**: Test executed successfully
- **2 = Blocked**: Test cannot be executed (blocked by another issue)
- **3 = Untested**: Test has not been executed yet
- **4 = Retest**: Test needs to be re-executed
- **5 = Failed**: Test execution failed

**Your Status**: {status_id} ({status_name})

## Step 2: Prepare Result Data

Gather the result information:
- **Run ID**: {run_id}
- **Case ID**: {case_id}
- **Status**: {status_id} ({status_name})
{f'- **Comment**: {comment}' if comment else '- **Comment**: (optional)'}
{f'- **Version**: {version}' if version else '- **Version**: (optional)'}
{f'- **Elapsed Time**: {elapsed}' if elapsed else '- **Elapsed Time**: (optional)'}
{f'- **Defects**: {defects}' if defects else '- **Defects**: (optional)'}

## Step 3: Add the Test Result

**Action:** Use the `testrail_results` tool with action `add_result`:
```json
{{
  "action": "add_result",
  "params": {{
    "run_id": {run_id},
    "case_id": {case_id},
    "status_id": {status_id}{f',\n    "comment": "{comment}"' if comment else ''}{f',\n    "version": "{version}"' if version else ''}{f',\n    "elapsed": "{elapsed}"' if elapsed else ''}{f',\n    "defects": "{defects}"' if defects else ''}
  }}
}}
```

## Important Notes

1. **Elapsed Time Format**:
   - Use formats like: "30s", "2m", "1h 30m", "2h 15m 30s"
   - TestRail will parse and store this as total seconds

2. **Defects Format**:
   - Comma-separated list: "BUG-123, BUG-456"
   - Or single defect: "BUG-123"
   - These are typically references to your issue tracking system

3. **Version**:
   - Version of the software/build being tested
   - Useful for tracking which version passed/failed

4. **Comments**:
   - Provide detailed information about the test execution
   - Include error messages for failed tests
   - Note any blocking conditions for blocked tests

## Step 4: Verify the Result (Optional)

Retrieve the result to verify it was recorded correctly:

**Action:** Use the `testrail_results` tool with action `get_results_for_case`:
```json
{{
  "action": "get_results_for_case",
  "params": {{
    "run_id": {run_id},
    "case_id": {case_id}
  }}
}}
```

## Bulk Results

To add results for multiple test cases at once, use `add_results_for_cases`:
```json
{{
  "action": "add_results_for_cases",
  "params": {{
    "run_id": {run_id},
    "results": [
      {{"case_id": 1, "status_id": 1, "comment": "Passed"}},
      {{"case_id": 2, "status_id": 5, "comment": "Failed", "defects": "BUG-123"}}
    ]
  }}
}}
```

## Related Prompts

- `testrail_get_run_results` - To retrieve all results for a run
- `testrail_retrieve_test_run_data` - To get comprehensive run information

## Related Tools

- `testrail_results` - All result operations
- `testrail_runs` - Run information
- `testrail_tests` - Test information
"""

    return [UserMessage(content=instructions)]


def get_test_case_details_prompt(
    case_id: int
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test case information from TestRail.

    This prompt helps you get all relevant information about a test case,
    including details, history, and related data.

    Args:
        case_id: The ID of the test case to retrieve.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Getting Test Case Details from TestRail

## Overview
You are retrieving comprehensive information about test case ID {case_id}.
This workflow will help you get all relevant details including case information,
history, and related data.

## Step 1: Get Test Case Information

Retrieve the basic test case details:

**Action:** Use the `testrail_cases` tool with action `get_case`:
```json
{{
  "action": "get_case",
  "params": {{
    "case_id": {case_id}
  }}
}}
```

This returns:
- Case title, description, and type
- Priority and estimate
- Section and suite information
- Custom field values
- Created/updated timestamps
- References and preconditions/postconditions

## Step 2: Get Case History (Optional)

Retrieve the change history for this test case:

**Action:** Use the `testrail_cases` tool with action `get_case_history`:
```json
{{
  "action": "get_case_history",
  "params": {{
    "case_id": {case_id}
  }}
}}
```

This returns:
- All changes made to the case
- Who made each change
- When changes were made
- What fields were changed

## Step 3: Get Case Fields (Optional)

To understand all available fields and their types:

**Action:** Use the `testrail_cases` tool with action `get_case_fields`:
```json
{{
  "action": "get_case_fields",
  "params": {{}}
}}
```

This helps you understand:
- All custom fields available
- Field types and formats
- Required vs optional fields

## Step 4: Get Related Information (Optional)

Depending on your needs, you may want to retrieve:

**Section Information:**
```json
{{
  "action": "get_section",
  "params": {{
    "section_id": <section_id_from_step_1>
  }}
}}
```

**Suite Information:**
```json
{{
  "action": "get_suite",
  "params": {{
    "suite_id": <suite_id_from_step_1>
  }}
}}
```

## Complete Data Structure

After following these steps, you will have:
1. **Case Details**: All case information and custom fields
2. **History**: Complete change history
3. **Field Definitions**: Understanding of available fields
4. **Related Data**: Section and suite information

## Related Prompts

- `testrail_add_test_cases` - To create new cases
- `testrail_update_test_case` - To modify this case
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_cases` - All test case operations
- `testrail_sections` - Section operations
- `testrail_suites` - Suite operations
"""

    return [UserMessage(content=instructions)]


def update_test_case_prompt(
    case_id: int,
    title: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for updating an existing test case in TestRail.

    This prompt helps you update test cases with proper field formats
    and required field validation.

    Args:
        case_id: The ID of the test case to update.
        title: Optional new title for the test case.
        type_id: Optional new type ID.
        priority_id: Optional new priority ID.
        estimate: Optional new time estimate.
        description: Optional new description.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Updating a Test Case in TestRail

## Overview
You are updating test case ID {case_id}. This workflow helps you modify
the case with proper field formats and ensures you understand what can be changed.

## Step 1: Get Current Case Information

First, retrieve the current case to see what fields exist:

**Action:** Use the `testrail_cases` tool with action `get_case`:
```json
{{
  "action": "get_case",
  "params": {{
    "case_id": {case_id}
  }}
}}
```

This shows you:
- Current field values
- Which fields are custom vs standard
- Field types and formats

## Step 2: Discover Required Fields (if updating custom fields)

If you're updating custom fields, discover which ones are required:

**Action:** Use the `testrail_cases` tool with action `get_required_case_fields`:
```json
{{
  "action": "get_required_case_fields",
  "params": {{
    "case_id": {case_id}
  }}
}}
```

**Note:** You can also use `section_id` from Step 1 instead of `case_id`.

## Step 3: Prepare Update Parameters

Gather the fields you want to update:
{f'- **Title**: {title}' if title else '- **Title**: (not updating)'}
{f'- **Type ID**: {type_id}' if type_id else '- **Type ID**: (not updating)'}
{f'- **Priority ID**: {priority_id}' if priority_id else '- **Priority ID**: (not updating)'}
{f'- **Estimate**: {estimate}' if estimate else '- **Estimate**: (not updating)'}
{f'- **Description**: {description}' if description else '- **Description**: (not updating)'}

## Step 4: Update the Test Case

**Action:** Use the `testrail_cases` tool with action `update_case`:
```json
{{
  "action": "update_case",
  "params": {{
    "case_id": {case_id}{f',\n    "title": "{title}"' if title else ''}{f',\n    "type_id": {type_id}' if type_id else ''}{f',\n    "priority_id": {priority_id}' if priority_id else ''}{f',\n    "estimate": "{estimate}"' if estimate else ''}{f',\n    "description": "{description}"' if description else ''},
    "custom_fields": {{
      // Add custom field updates here if needed
      // Follow the same format rules as add_case
      // Use STRING IDs for dropdowns: ["3", "5"]
      // Use objects for steps: [{{"content": "...", "expected": "..."}}]
    }}
  }}
}}
```

## Important Notes

1. **Partial Updates**:
   - You only need to include fields you want to change
   - Omitted fields remain unchanged
   - You cannot set a field to null/empty by omitting it

2. **Custom Fields**:
   - Custom fields must be nested in `custom_fields` parameter
   - Use the same format rules as `add_case`
   - Required custom fields must still be provided

3. **Field Formats**:
   - Dropdown/Multi-select: Arrays of STRING IDs `["3", "5"]`
   - Steps: Array of objects with `content` and `expected`
   - Checkboxes: Boolean values
   - Text: String values

## Step 5: Verify the Update (Optional)

Retrieve the case again to verify changes:

**Action:** Use the `testrail_cases` tool with action `get_case`:
```json
{{
  "action": "get_case",
  "params": {{
    "case_id": {case_id}
  }}
}}
```

## Related Prompts

- `testrail_get_test_case_details` - To view case information
- `testrail_add_test_cases` - To create new cases

## Related Tools

- `testrail_cases` - All test case operations
"""

    return [UserMessage(content=instructions)]


def get_test_plan_details_prompt(
    plan_id: int
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test plan information from TestRail.

    This prompt helps you get all relevant information about a test plan,
    including plan details, associated runs, and statistics.

    Args:
        plan_id: The ID of the test plan to retrieve.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Getting Test Plan Details from TestRail

## Overview
You are retrieving comprehensive information about test plan ID {plan_id}.
This workflow will help you get all relevant details including plan information,
associated runs, and statistics.

## Step 1: Get Test Plan Information

Retrieve the basic test plan details:

**Action:** Use the `testrail_plans` tool with action `get_plan`:
```json
{{
  "action": "get_plan",
  "params": {{
    "plan_id": {plan_id}
  }}
}}
```

This returns:
- Plan name, description, and milestone
- Project information
- Created/updated timestamps
- Plan entries (test runs) with their details
- Entry configurations and case selections

## Step 2: Get Plan Statistics

Get summary statistics for the test plan:

**Action:** Use the `testrail_plans` tool with action `get_plan_stats`:
```json
{{
  "action": "get_plan_stats",
  "params": {{
    "plan_id": {plan_id}
  }}
}}
```

This returns:
- Total runs count
- Status breakdown across all runs
- Progress percentage
- Status distribution

## Step 3: Get Individual Run Details (Optional)

For each run in the plan, you can get detailed information:

**Action:** Use the `testrail_runs` tool with action `get_run`:
```json
{{
  "action": "get_run",
  "params": {{
    "run_id": <run_id_from_step_1>
  }}
}}
```

## Step 4: Get Run Results (Optional)

For each run, retrieve test results:

**Action:** Use the `testrail_results` tool with action `get_results_for_run`:
```json
{{
  "action": "get_results_for_run",
  "params": {{
    "run_id": <run_id_from_step_1>
  }}
}}
```

## Complete Data Structure

After following these steps, you will have:
1. **Plan Details**: Name, description, milestone, entries
2. **Statistics**: Summary across all runs in the plan
3. **Run Details**: Individual run information for each entry
4. **Results**: Test results for each run

## Related Prompts

- `testrail_create_test_plan` - To create new plans
- `testrail_retrieve_test_run_data` - To get detailed run information
- `testrail_get_run_results` - To get results for specific runs

## Related Tools

- `testrail_plans` - All test plan operations
- `testrail_runs` - Run operations
- `testrail_results` - Result operations
"""

    return [UserMessage(content=instructions)]


def get_project_info_prompt(
    project_id: int
) -> List['UserMessage']:
    """
    Guide for exploring project structure in TestRail.

    This prompt helps you navigate a project's structure including
    project details, suites, sections, and cases.

    Args:
        project_id: The ID of the project to explore.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Getting Project Information from TestRail

## Overview
You are exploring project ID {project_id} in TestRail. This workflow helps you
navigate the project structure including project details, suites, sections, and cases.

## Step 1: Get Project Details

Retrieve basic project information:

**Action:** Use the `testrail_projects` tool with action `get_project`:
```json
{{
  "action": "get_project",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

This returns:
- Project name and description
- Project type (single vs multi-suite)
- Is completed status
- Created/updated timestamps

## Step 2: Get Project Statistics

Get summary statistics for the project:

**Action:** Use the `testrail_projects` tool with action `get_project_stats`:
```json
{{
  "action": "get_project_stats",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

This returns:
- Total cases count
- Total runs count
- Status breakdown
- Progress information

## Step 3: Get Test Suites

Retrieve all test suites in the project:

**Action:** Use the `testrail_suites` tool with action `get_suites`:
```json
{{
  "action": "get_suites",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

This returns:
- All suites with their names and descriptions
- Suite IDs for further navigation

## Step 4: Get Sections (for a specific suite)

For each suite, retrieve its sections:

**Action:** Use the `testrail_sections` tool with action `get_sections`:
```json
{{
  "action": "get_sections",
  "params": {{
    "project_id": {project_id},
    "suite_id": <suite_id_from_step_3>
  }}
}}
```

This returns:
- Section hierarchy (parent/child relationships)
- Section names and descriptions
- Section IDs for case retrieval

## Step 5: Get Test Cases

For each section, retrieve test cases:

**Action:** Use the `testrail_cases` tool with action `get_cases`:
```json
{{
  "action": "get_cases",
  "params": {{
    "project_id": {project_id},
    "suite_id": <suite_id>,
    "section_id": <section_id_from_step_4>
  }}
}}
```

This returns:
- All test cases in the section
- Case titles, types, priorities
- Case IDs for detailed retrieval

## Step 6: Get Additional Project Data (Optional)

**Test Plans:**
```json
{{
  "action": "get_plans",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

**Test Runs:**
```json
{{
  "action": "get_runs",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

**Milestones:**
```json
{{
  "action": "get_milestones",
  "params": {{
    "project_id": {project_id}
  }}
}}
```

## Navigation Hierarchy

The project structure follows this hierarchy:
1. **Project** (top level)
   - **Suites** (test organization)
     - **Sections** (case organization)
       - **Cases** (individual tests)
   - **Plans** (run organization)
     - **Runs** (execution instances)
   - **Milestones** (release tracking)

## Complete Data Structure

After following these steps, you will have:
1. **Project Info**: Basic project details and statistics
2. **Suite Structure**: All suites and their organization
3. **Section Hierarchy**: Section structure within suites
4. **Test Cases**: Cases organized by section
5. **Additional Data**: Plans, runs, milestones

## Related Prompts

- `testrail_add_test_cases` - To add cases to sections
- `testrail_create_test_run` - To create runs in this project
- `testrail_create_test_plan` - To create plans in this project

## Related Tools

- `testrail_projects` - Project operations
- `testrail_suites` - Suite operations
- `testrail_sections` - Section operations
- `testrail_cases` - Case operations
- `testrail_plans` - Plan operations
- `testrail_runs` - Run operations
"""

    return [UserMessage(content=instructions)]


def get_run_results_prompt(
    run_id: int
) -> List['UserMessage']:
    """
    Guide for retrieving all test results for a test run.

    This prompt helps you get comprehensive results data including
    all test results, statistics, and status breakdown.

    Args:
        run_id: The ID of the test run to get results for.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Getting Test Run Results from TestRail

## Overview
You are retrieving all test results for test run ID {run_id}. This workflow
helps you get comprehensive results data including individual results, statistics,
and status breakdown.

## Step 1: Get All Results for the Run

Retrieve all test results:

**Action:** Use the `testrail_results` tool with action `get_results_for_run`:
```json
{{
  "action": "get_results_for_run",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns:
- All test results with status IDs
- Comments and defect references
- Execution time (elapsed)
- Version information
- Custom field values
- Created timestamps

## Step 2: Get Run Statistics

Get summary statistics for the run:

**Action:** Use the `testrail_runs` tool with action `get_run_stats`:
```json
{{
  "action": "get_run_stats",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This returns:
- Total tests count
- Status breakdown:
  - Passed count
  - Failed count
  - Blocked count
  - Retest count
  - Untested count
- Progress percentage
- Status distribution

## Step 3: Get Individual Test Results (Optional)

For specific test cases, get detailed result history:

**Action:** Use the `testrail_results` tool with action `get_results_for_case`:
```json
{{
  "action": "get_results_for_case",
  "params": {{
    "run_id": {run_id},
    "case_id": <case_id>
  }}
}}
```

This returns:
- All results for this case in this run
- Result history (if multiple results exist)
- Latest result status

## Step 4: Get Test Information (Optional)

To see which tests are in the run:

**Action:** Use the `testrail_tests` tool with action `get_tests`:
```json
{{
  "action": "get_tests",
  "params": {{
    "run_id": {run_id}
  }}
}}
```

This helps you:
- See all tests included in the run
- Match test cases to their results
- Understand test organization

## Understanding Status Codes

Results use numeric status IDs:
- **1 = Passed**: Test executed successfully
- **2 = Blocked**: Test cannot be executed
- **3 = Untested**: Test has not been executed
- **4 = Retest**: Test needs re-execution
- **5 = Failed**: Test execution failed

## Complete Data Structure

After following these steps, you will have:
1. **All Results**: Complete list of all test results
2. **Statistics**: Summary counts and percentages
3. **Individual Results**: Detailed result information
4. **Test List**: Tests included in the run

## Related Prompts

- `testrail_add_test_results` - To add results to this run
- `testrail_retrieve_test_run_data` - To get comprehensive run information

## Related Tools

- `testrail_results` - All result operations
- `testrail_runs` - Run operations
- `testrail_tests` - Test operations
"""

    return [UserMessage(content=instructions)]
