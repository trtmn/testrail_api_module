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
    project_name: str,
    section_name: str,
    title: str,
    suite_name: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for adding test cases to TestRail.

    This prompt helps you create test cases by first finding the right project
    and section, then discovering required fields, and finally creating the case.

    Args:
        project_name: The name of the project to add the test case to.
        section_name: The name of the section where the test case will be created.
        title: The title/name of the test case.
        suite_name: Optional name of the suite (if project uses multiple suites).
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
You want to create a test case titled "{title}" in the section "{section_name}" within the project "{project_name}". This guide will help you find the right location and create the case with all required fields.

## Step 1: Find the Project

First, search for the project by name to get its ID:

Use the `testrail_projects` tool with action `get_projects` to list all projects. Look through the results to find the project named "{project_name}" and note its ID.

## Step 2: Find the Section

Once you have the project ID, find the section where you want to add the test case:

1. If you know the suite name ("{suite_name if suite_name else 'or if the project uses suites'}"), first get the suites for the project using `testrail_suites` with action `get_suites`, passing the project_id.

2. Then use `testrail_sections` with action `get_sections`, passing the project_id (and suite_id if needed) to get all sections. Look through the results to find the section named "{section_name}" and note its ID.

## Step 3: Discover Required Fields

Before creating the test case, you MUST discover which fields are required for this section. This prevents errors and ensures correct field formats.

Use the `testrail_cases` tool with action `get_required_case_fields`, passing the section_id you found in Step 2.

This will return:
- All required custom fields with their types
- Format examples for each field type
- Field system names to use when creating the case

## Step 4: Review Field Types

Pay special attention to the field types returned:
- **Dropdown/Multi-select fields**: Must be arrays of STRING IDs (e.g., ["3", "5"]) - NOT integers!
- **Separated steps fields**: Must be arrays of objects with "content" and "expected" keys
- **Checkbox fields**: Must be boolean values (true/false)
- **Text fields**: Must be string values

## Step 5: Get Field Options (if needed)

For dropdown/multi-select fields, you may need to get available options. Use the `testrail_cases` tool with action `get_field_options`, passing the field_name to see what values are available.

## Step 6: Create the Test Case

Now create the test case with all required fields. Use the `testrail_cases` tool with action `add_case`, passing:
- section_id: The ID you found in Step 2
- title: "{title}"
{f'- type_id: {type_id}' if type_id else ''}
{f'- priority_id: {priority_id}' if priority_id else ''}
{f'- estimate: "{estimate}"' if estimate else ''}
{f'- description: "{description}"' if description else ''}
- custom_fields: A dictionary containing all required custom fields based on what you discovered in Step 3

Remember:
- Custom fields must be nested in the "custom_fields" parameter
- Use STRING IDs for dropdown/multi-select fields: ["3", "5"] not [3, 5]
- Steps must be objects with "content" and "expected" keys, both non-empty strings
- Always include all required fields from Step 3

## Related Prompts

- `testrail_update_test_case` - To update this case later
- `testrail_get_test_case_details` - To retrieve case information
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_suites` - Suite operations
- `testrail_sections` - Section operations
- `testrail_cases` - All test case operations
"""

    return [UserMessage(content=instructions)]


def retrieve_test_run_data_prompt(
    run_name: str,
    project_name: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test run data from TestRail.

    This prompt helps you find a test run by name and get all relevant
    information including run details, associated tests, and results.

    Args:
        run_name: The name of the test run to retrieve data for.
        project_name: Optional name of the project to search within.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Retrieving Test Run Data from TestRail

## Overview
You want to retrieve comprehensive data about the test run named "{run_name}"{project_help}. This guide will help you find the run and get all relevant information including run details, tests, and results.

## Step 1: Find the Test Run

First, you need to locate the test run by name:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_runs` with action `get_runs`, passing the project_id to get all runs for that project. Look through the results to find the run named "{run_name}" and note its run_id.

## Step 2: Get Test Run Details

Once you have the run_id, retrieve the basic test run information using `testrail_runs` with action `get_run`, passing the run_id.

This returns:
- Run name, description, and status
- Project and suite information
- Milestone and assigned user
- Created/updated timestamps
- Configuration details

## Step 3: Get Run Statistics

Get summary statistics for the test run using `testrail_runs` with action `get_run_stats`, passing the run_id.

This returns:
- Total tests count
- Status breakdown (passed, failed, blocked, etc.)
- Progress percentage
- Status distribution

## Step 4: Get All Tests in the Run

Retrieve all test cases included in this run using `testrail_tests` with action `get_tests`, passing the run_id.

This returns a list of all tests with:
- Test case information
- Current status
- Assigned user
- Test case details

## Step 5: Get Test Results

Retrieve all test results for this run using `testrail_results` with action `get_results_for_run`, passing the run_id.

This returns:
- All test results with status
- Comments and defects
- Execution time (elapsed)
- Version information
- Custom field values

## Step 6: Get Results for Specific Test (Optional)

To get results for a specific test case in the run, use `testrail_results` with action `get_results_for_case`, passing both the run_id and case_id.

## Complete Data Structure

After following these steps, you will have:
1. **Run metadata**: Name, description, status, dates
2. **Statistics**: Summary counts and percentages
3. **Test list**: All tests included in the run
4. **Results**: All execution results with details

## Related Prompts

- `testrail_get_run_results` - Focused on just results
- `testrail_create_test_run` - To create new runs
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_runs` - Run management operations
- `testrail_tests` - Test operations
- `testrail_results` - Result operations
"""

    return [UserMessage(content=instructions)]


def create_test_run_prompt(
    project_name: str,
    name: str,
    suite_name: Optional[str] = None,
    milestone_name: Optional[str] = None,
    description: Optional[str] = None,
    include_all: bool = True,
    case_titles: Optional[List[str]] = None
) -> List['UserMessage']:
    """
    Guide for creating a new test run in TestRail.

    This prompt helps you find the project and suite, then create a test run
    with proper configuration and case selection.

    Args:
        project_name: The name of the project to create the run in.
        name: The name of the test run.
        suite_name: Optional name of the test suite to base the run on.
        milestone_name: Optional name of the milestone to associate with the run.
        description: Optional description of the test run.
        include_all: Whether to include all test cases from the suite (default: True).
        case_titles: Optional list of specific case titles to include (if include_all is False).

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    case_titles_str = f'cases: {", ".join(case_titles)}' if case_titles else ''

    instructions = f"""# Creating a Test Run in TestRail

## Overview
You want to create a new test run named "{name}" in the project "{project_name}". This guide will help you find the project and suite, then create a properly configured test run.

## Step 1: Find the Project

First, search for the project by name. Use the `testrail_projects` tool with action `get_projects` to list all projects. Look through the results to find the project named "{project_name}" and note its ID.

## Step 2: Find the Suite (if specified)

{f'If you specified a suite name ("{suite_name}"), find it using `testrail_suites` with action `get_suites`, passing the project_id. Look through the results to find the suite and note its ID.' if suite_name else 'If the project uses multiple suites, you may want to find the suite first using `testrail_suites` with action `get_suites`, passing the project_id. Otherwise, TestRail will use the default suite.'}

## Step 3: Find Specific Cases (if not including all)

{f'If you want to include specific cases ({case_titles_str}), you\'ll need to find their IDs. Use `testrail_cases` with action `get_cases`, passing the project_id (and suite_id if needed). Look through the results to find the cases by title and note their IDs.' if case_titles else ''}

## Step 4: Find the Milestone (if specified)

{f'If you specified a milestone name ("{milestone_name}"), find it using `testrail_milestones` with action `get_milestones`, passing the project_id. Look through the results to find the milestone and note its ID.' if milestone_name else ''}

## Step 5: Create the Test Run

Now create the test run using `testrail_runs` with action `add_run`, passing:
- project_id: The ID you found in Step 1
- name: "{name}"
{f'- suite_id: The ID you found in Step 2' if suite_name else ''}
{f'- milestone_id: The ID you found in Step 4' if milestone_name else ''}
{f'- description: "{description}"' if description else ''}
- include_all: {str(include_all).lower()}
{f'- case_ids: The list of case IDs you found in Step 3' if case_titles and not include_all else ''}

## Important Notes

1. **include_all vs case_ids**:
   - If include_all is true, all cases from the suite are included
   - If include_all is false, you must provide case_ids to specify which cases to include
   - You cannot use both include_all: true and case_ids together

2. **Suite Selection**:
   - If suite_id is not provided, TestRail will use the default suite for the project
   - Make sure the suite exists and contains test cases

3. **Run Status**:
   - New runs are created in "Active" status
   - Use the close_run action to mark the run as completed later

## Step 6: Verify the Run (Optional)

After creation, retrieve the run to verify it was created correctly using `testrail_runs` with action `get_run`, passing the run_id returned from Step 5.

## Related Prompts

- `testrail_retrieve_test_run_data` - To get comprehensive run data
- `testrail_add_test_results` - To add results to this run
- `testrail_get_run_results` - To retrieve results from this run
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_suites` - Suite operations
- `testrail_cases` - Case operations
- `testrail_milestones` - Milestone operations
- `testrail_runs` - All test run operations
"""

    return [UserMessage(content=instructions)]


def create_test_plan_prompt(
    project_name: str,
    name: str,
    description: Optional[str] = None,
    milestone_name: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for creating a test plan in TestRail.

    This prompt helps you find the project and milestone, then create a test plan.
    Test plans organize and schedule multiple test runs.

    Args:
        project_name: The name of the project to create the plan in.
        name: The name of the test plan.
        description: Optional description of the test plan.
        milestone_name: Optional name of the milestone to associate with the plan.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Creating a Test Plan in TestRail

## Overview
You want to create a new test plan named "{name}" in the project "{project_name}". Test plans organize and schedule multiple test runs, making it easier to manage complex testing scenarios.

## Step 1: Find the Project

First, search for the project by name. Use the `testrail_projects` tool with action `get_projects` to list all projects. Look through the results to find the project named "{project_name}" and note its ID.

## Step 2: Find the Milestone (if specified)

{f'If you specified a milestone name ("{milestone_name}"), find it using `testrail_milestones` with action `get_milestones`, passing the project_id. Look through the results to find the milestone and note its ID.' if milestone_name else ''}

## Step 3: Create the Test Plan

Now create the test plan using `testrail_plans` with action `add_plan`, passing:
- project_id: The ID you found in Step 1
- name: "{name}"
{f'- description: "{description}"' if description else ''}
{f'- milestone_id: The ID you found in Step 2' if milestone_name else ''}

## Important Notes

1. **Plan vs Run**:
   - A plan can contain multiple test runs
   - You can add runs to the plan later using the update_plan action
   - Plans help organize related runs together

2. **Adding Entries Later**:
   - You can create a plan without entries (runs)
   - Use the update_plan action to add entries later
   - Or create runs separately and associate them with the plan

3. **Plan Entries**:
   - Each entry represents a test run that will be created as part of the plan
   - Entries require a suite_id and name
   - You can specify include_all or case_ids for each entry

## Step 4: Verify the Plan (Optional)

After creation, retrieve the plan to verify it was created correctly using `testrail_plans` with action `get_plan`, passing the plan_id returned from Step 3.

## Related Prompts

- `testrail_get_test_plan_details` - To retrieve comprehensive plan information
- `testrail_create_test_run` - To create individual runs
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_milestones` - Milestone operations
- `testrail_plans` - All test plan operations
- `testrail_runs` - Individual run operations
- `testrail_suites` - Suite information
"""

    return [UserMessage(content=instructions)]


def add_test_results_prompt(
    run_name: str,
    case_title: str,
    status_id: int,
    project_name: Optional[str] = None,
    comment: Optional[str] = None,
    version: Optional[str] = None,
    elapsed: Optional[str] = None,
    defects: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for adding test execution results to TestRail.

    This prompt helps you find the run and case, then record test results
    with proper status codes and optional metadata.

    Args:
        run_name: The name of the test run.
        case_title: The title of the test case.
        status_id: The status ID (1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed).
        project_name: Optional name of the project to search within.
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
    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Adding Test Results to TestRail

## Overview
You want to record a test execution result for the case "{case_title}" in the run "{run_name}"{project_help}. The status is {status_id} ({status_name}). This guide will help you find the run and case, then add the result.

## Step 1: Understand Status Codes

TestRail uses numeric status IDs:
- 1 = Passed: Test executed successfully
- 2 = Blocked: Test cannot be executed (blocked by another issue)
- 3 = Untested: Test has not been executed yet
- 4 = Retest: Test needs to be re-executed
- 5 = Failed: Test execution failed

Your Status: {status_id} ({status_name})

## Step 2: Find the Test Run

First, locate the test run by name:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_runs` with action `get_runs`, passing the project_id to get all runs for that project. Look through the results to find the run named "{run_name}" and note its run_id.

## Step 3: Find the Test Case

Now find the test case by title:

1. Use `testrail_tests` with action `get_tests`, passing the run_id you found in Step 2 to get all tests in that run.

2. Look through the results to find the test case with title "{case_title}" and note its case_id.

Alternatively, if you know the project and suite, you can search for the case using `testrail_cases` with action `get_cases`, passing the project_id (and suite_id if needed), then look for the case by title.

## Step 4: Add the Test Result

Now add the test result using `testrail_results` with action `add_result`, passing:
- run_id: The ID you found in Step 2
- case_id: The ID you found in Step 3
- status_id: {status_id}
{f'- comment: "{comment}"' if comment else ''}
{f'- version: "{version}"' if version else ''}
{f'- elapsed: "{elapsed}"' if elapsed else ''}
{f'- defects: "{defects}"' if defects else ''}

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

## Step 5: Verify the Result (Optional)

Retrieve the result to verify it was recorded correctly using `testrail_results` with action `get_results_for_case`, passing both the run_id and case_id.

## Bulk Results

To add results for multiple test cases at once, use `testrail_results` with action `add_results_for_cases`, passing the run_id and a list of result objects, each containing case_id, status_id, and optional fields like comment, version, elapsed, and defects.

## Related Prompts

- `testrail_get_run_results` - To retrieve all results for a run
- `testrail_retrieve_test_run_data` - To get comprehensive run information

## Related Tools

- `testrail_projects` - Project operations
- `testrail_runs` - Run operations
- `testrail_tests` - Test operations
- `testrail_cases` - Case operations
- `testrail_results` - All result operations
"""

    return [UserMessage(content=instructions)]


def get_test_case_details_prompt(
    case_title: str,
    project_name: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test case information from TestRail.

    This prompt helps you find a test case by title and get all relevant
    information including details, history, and related data.

    Args:
        case_title: The title of the test case to retrieve.
        project_name: Optional name of the project to search within.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Getting Test Case Details from TestRail

## Overview
You want to retrieve comprehensive information about the test case titled "{case_title}"{project_help}. This guide will help you find the case and get all relevant details including case information, history, and related data.

## Step 1: Find the Test Case

First, locate the test case by title:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_cases` with action `get_cases`, passing the project_id to get all cases for that project. Look through the results to find the case with title "{case_title}" and note its case_id.

## Step 2: Get Test Case Information

Once you have the case_id, retrieve the basic test case details using `testrail_cases` with action `get_case`, passing the case_id.

This returns:
- Case title, description, and type
- Priority and estimate
- Section and suite information
- Custom field values
- Created/updated timestamps
- References and preconditions/postconditions

## Step 3: Get Case History (Optional)

Retrieve the change history for this test case using `testrail_cases` with action `get_case_history`, passing the case_id.

This returns:
- All changes made to the case
- Who made each change
- When changes were made
- What fields were changed

## Step 4: Get Case Fields (Optional)

To understand all available fields and their types, use `testrail_cases` with action `get_case_fields` (no parameters needed).

This helps you understand:
- All custom fields available
- Field types and formats
- Required vs optional fields

## Step 5: Get Related Information (Optional)

Depending on your needs, you may want to retrieve:

- Section information: Use `testrail_sections` with action `get_section`, passing the section_id from Step 2
- Suite information: Use `testrail_suites` with action `get_suite`, passing the suite_id from Step 2

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

- `testrail_projects` - Project operations
- `testrail_cases` - All test case operations
- `testrail_sections` - Section operations
- `testrail_suites` - Suite operations
"""

    return [UserMessage(content=instructions)]


def update_test_case_prompt(
    case_title: str,
    project_name: Optional[str] = None,
    title: Optional[str] = None,
    type_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    estimate: Optional[str] = None,
    description: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for updating an existing test case in TestRail.

    This prompt helps you find the case and update it with proper field formats.

    Args:
        case_title: The title of the test case to update.
        project_name: Optional name of the project to search within.
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

    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Updating a Test Case in TestRail

## Overview
You want to update the test case titled "{case_title}"{project_help}. This guide will help you find the case and update it with proper field formats.

## Step 1: Find the Test Case

First, locate the test case by title:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_cases` with action `get_cases`, passing the project_id to get all cases for that project. Look through the results to find the case with title "{case_title}" and note its case_id.

## Step 2: Get Current Case Information

Retrieve the current case to see what fields exist using `testrail_cases` with action `get_case`, passing the case_id.

This shows you:
- Current field values
- Which fields are custom vs standard
- Field types and formats

## Step 3: Discover Required Fields (if updating custom fields)

If you're updating custom fields, discover which ones are required using `testrail_cases` with action `get_required_case_fields`, passing either the case_id or the section_id from Step 2.

## Step 4: Prepare Update Parameters

Gather the fields you want to update:
{f'- Title: "{title}"' if title else '- Title: (not updating)'}
{f'- Type ID: {type_id}' if type_id else '- Type ID: (not updating)'}
{f'- Priority ID: {priority_id}' if priority_id else '- Priority ID: (not updating)'}
{f'- Estimate: "{estimate}"' if estimate else '- Estimate: (not updating)'}
{f'- Description: "{description}"' if description else '- Description: (not updating)'}

## Step 5: Update the Test Case

Now update the test case using `testrail_cases` with action `update_case`, passing:
- case_id: The ID you found in Step 1
{f'- title: "{title}"' if title else ''}
{f'- type_id: {type_id}' if type_id else ''}
{f'- priority_id: {priority_id}' if priority_id else ''}
{f'- estimate: "{estimate}"' if estimate else ''}
{f'- description: "{description}"' if description else ''}
- custom_fields: A dictionary containing any custom field updates (if needed)

Remember:
- Custom fields must be nested in the "custom_fields" parameter
- Use STRING IDs for dropdown/multi-select fields: ["3", "5"]
- Steps must be objects with "content" and "expected" keys
- Required custom fields must still be provided

## Important Notes

1. **Partial Updates**:
   - You only need to include fields you want to change
   - Omitted fields remain unchanged
   - You cannot set a field to null/empty by omitting it

2. **Custom Fields**:
   - Custom fields must be nested in the "custom_fields" parameter
   - Use the same format rules as add_case
   - Required custom fields must still be provided

3. **Field Formats**:
   - Dropdown/Multi-select: Arrays of STRING IDs ["3", "5"]
   - Steps: Array of objects with "content" and "expected"
   - Checkboxes: Boolean values
   - Text: String values

## Step 6: Verify the Update (Optional)

Retrieve the case again to verify changes using `testrail_cases` with action `get_case`, passing the case_id.

## Related Prompts

- `testrail_get_test_case_details` - To view case information
- `testrail_add_test_cases` - To create new cases
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_cases` - All test case operations
"""

    return [UserMessage(content=instructions)]


def get_test_plan_details_prompt(
    plan_name: str,
    project_name: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for retrieving comprehensive test plan information from TestRail.

    This prompt helps you find a test plan by name and get all relevant
    information including plan details, associated runs, and statistics.

    Args:
        plan_name: The name of the test plan to retrieve.
        project_name: Optional name of the project to search within.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Getting Test Plan Details from TestRail

## Overview
You want to retrieve comprehensive information about the test plan named "{plan_name}"{project_help}. This guide will help you find the plan and get all relevant details including plan information, associated runs, and statistics.

## Step 1: Find the Test Plan

First, locate the test plan by name:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_plans` with action `get_plans`, passing the project_id to get all plans for that project. Look through the results to find the plan named "{plan_name}" and note its plan_id.

## Step 2: Get Test Plan Information

Once you have the plan_id, retrieve the basic test plan details using `testrail_plans` with action `get_plan`, passing the plan_id.

This returns:
- Plan name, description, and milestone
- Project information
- Created/updated timestamps
- Plan entries (test runs) with their details
- Entry configurations and case selections

## Step 3: Get Plan Statistics

Get summary statistics for the test plan using `testrail_plans` with action `get_plan_stats`, passing the plan_id.

This returns:
- Total runs count
- Status breakdown across all runs
- Progress percentage
- Status distribution

## Step 4: Get Individual Run Details (Optional)

For each run in the plan, you can get detailed information using `testrail_runs` with action `get_run`, passing the run_id from Step 2.

## Step 5: Get Run Results (Optional)

For each run, retrieve test results using `testrail_results` with action `get_results_for_run`, passing the run_id from Step 2.

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
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_plans` - All test plan operations
- `testrail_runs` - Run operations
- `testrail_results` - Result operations
"""

    return [UserMessage(content=instructions)]


def get_project_info_prompt(
    project_name: str
) -> List['UserMessage']:
    """
    Guide for exploring project structure in TestRail.

    This prompt helps you find a project by name and navigate its structure
    including project details, suites, sections, and cases.

    Args:
        project_name: The name of the project to explore.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    instructions = f"""# Getting Project Information from TestRail

## Overview
You want to explore the project named "{project_name}" in TestRail. This guide will help you find the project and navigate its structure including project details, suites, sections, and cases.

## Step 1: Find the Project

First, search for the project by name. Use the `testrail_projects` tool with action `get_projects` to list all projects. Look through the results to find the project named "{project_name}" and note its ID.

## Step 2: Get Project Details

Once you have the project_id, retrieve basic project information using `testrail_projects` with action `get_project`, passing the project_id.

This returns:
- Project name and description
- Project type (single vs multi-suite)
- Is completed status
- Created/updated timestamps

## Step 3: Get Project Statistics

Get summary statistics for the project using `testrail_projects` with action `get_project_stats`, passing the project_id.

This returns:
- Total cases count
- Total runs count
- Status breakdown
- Progress information

## Step 4: Get Test Suites

Retrieve all test suites in the project using `testrail_suites` with action `get_suites`, passing the project_id.

This returns:
- All suites with their names and descriptions
- Suite IDs for further navigation

## Step 5: Get Sections (for a specific suite)

For each suite, retrieve its sections using `testrail_sections` with action `get_sections`, passing the project_id and suite_id.

This returns:
- Section hierarchy (parent/child relationships)
- Section names and descriptions
- Section IDs for case retrieval

## Step 6: Get Test Cases

For each section, retrieve test cases using `testrail_cases` with action `get_cases`, passing the project_id, suite_id (if needed), and section_id.

This returns:
- All test cases in the section
- Case titles, types, priorities
- Case IDs for detailed retrieval

## Step 7: Get Additional Project Data (Optional)

You can also retrieve:
- Test Plans: Use `testrail_plans` with action `get_plans`, passing the project_id
- Test Runs: Use `testrail_runs` with action `get_runs`, passing the project_id
- Milestones: Use `testrail_milestones` with action `get_milestones`, passing the project_id

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
- `testrail_milestones` - Milestone operations
"""

    return [UserMessage(content=instructions)]


def get_run_results_prompt(
    run_name: str,
    project_name: Optional[str] = None
) -> List['UserMessage']:
    """
    Guide for retrieving all test results for a test run.

    This prompt helps you find a test run by name and get comprehensive
    results data including all test results, statistics, and status breakdown.

    Args:
        run_name: The name of the test run to get results for.
        project_name: Optional name of the project to search within.

    Returns:
        List of UserMessage objects containing the prompt instructions.
    """
    if UserMessage is None:
        return []

    project_help = f' within the project "{project_name}"' if project_name else ''

    instructions = f"""# Getting Test Run Results from TestRail

## Overview
You want to retrieve all test results for the test run named "{run_name}"{project_help}. This guide will help you find the run and get comprehensive results data including individual results, statistics, and status breakdown.

## Step 1: Find the Test Run

First, locate the test run by name:

1. If you know the project name ("{project_name if project_name else 'or need to find it'}"), start by getting all projects using `testrail_projects` with action `get_projects`. Look for the project and note its ID.

2. Then use `testrail_runs` with action `get_runs`, passing the project_id to get all runs for that project. Look through the results to find the run named "{run_name}" and note its run_id.

## Step 2: Get All Results for the Run

Once you have the run_id, retrieve all test results using `testrail_results` with action `get_results_for_run`, passing the run_id.

This returns:
- All test results with status IDs
- Comments and defect references
- Execution time (elapsed)
- Version information
- Custom field values
- Created timestamps

## Step 3: Get Run Statistics

Get summary statistics for the run using `testrail_runs` with action `get_run_stats`, passing the run_id.

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

## Step 4: Get Individual Test Results (Optional)

For specific test cases, get detailed result history using `testrail_results` with action `get_results_for_case`, passing both the run_id and case_id.

This returns:
- All results for this case in this run
- Result history (if multiple results exist)
- Latest result status

## Step 5: Get Test Information (Optional)

To see which tests are in the run, use `testrail_tests` with action `get_tests`, passing the run_id.

This helps you:
- See all tests included in the run
- Match test cases to their results
- Understand test organization

## Understanding Status Codes

Results use numeric status IDs:
- 1 = Passed: Test executed successfully
- 2 = Blocked: Test cannot be executed
- 3 = Untested: Test has not been executed
- 4 = Retest: Test needs re-execution
- 5 = Failed: Test execution failed

## Complete Data Structure

After following these steps, you will have:
1. **All Results**: Complete list of all test results
2. **Statistics**: Summary counts and percentages
3. **Individual Results**: Detailed result information
4. **Test List**: Tests included in the run

## Related Prompts

- `testrail_add_test_results` - To add results to this run
- `testrail_retrieve_test_run_data` - To get comprehensive run information
- `testrail_get_project_info` - To explore project structure

## Related Tools

- `testrail_projects` - Project operations
- `testrail_runs` - Run operations
- `testrail_tests` - Test operations
- `testrail_results` - All result operations
"""

    return [UserMessage(content=instructions)]
