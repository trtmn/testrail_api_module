# Test Cases and Custom Fields

## Table of Contents

- [The Required Fields Problem](#the-required-fields-problem)
- [Field Discovery Workflow](#field-discovery-workflow)
- [Custom Field Type Reference](#custom-field-type-reference)
- [Format Examples](#format-examples)
- [Creating a Test Case -- Complete Example](#creating-a-test-case----complete-example)
- [Updating a Test Case](#updating-a-test-case)
- [Common Pitfalls](#common-pitfalls)
- [Copy, Move, and Cache Operations](#copy-move-and-cache-operations)

## The Required Fields Problem

TestRail instances often have custom required fields configured per-project or per-template.
Attempting to create a test case without supplying all required custom fields produces validation
errors. The only reliable approach is to discover requirements before creating cases.

## Field Discovery Workflow

### Step 1: Discover Required Fields

Use `section_id` for automatic context resolution (recommended):

```python
fields = api.cases.get_required_case_fields(section_id=123)
```

Or specify context explicitly:

```python
fields = api.cases.get_required_case_fields(
    project_id=1, suite_id=2, template_id=3
)
```

The response includes:
- `required_fields`: List of field definitions with `system_name`, `type_id`, `type_name`, `format_example`
- `format_guide`: Quick reference for each field type format
- `context`: The resolved `project_id`, `suite_id`, `template_id`

### Step 2: Get Field Options

For dropdown and multi-select fields, get available option values:

```python
options = api.cases.get_field_options(field_name="custom_interface_type")
# Returns dict mapping option IDs to display names
```

### Step 3: Get All Fields (Optional)

To see all fields (required and optional) with full definitions:

```python
fields = api.cases.get_case_fields()
for field in fields:
    print(f"{field['system_name']}: type={field['type_id']}, required={field.get('is_required', False)}")
```

## Custom Field Type Reference

| type_id | Type Name    | Python Format                          |
|---------|-------------|----------------------------------------|
| 1       | String      | `"plain text string"`                  |
| 2       | Integer     | `42`                                   |
| 3       | Text        | `"multi-line\ntext"`                   |
| 4       | URL         | `"https://example.com"`                |
| 5       | Checkbox    | `True` or `False`                      |
| 6       | Dropdown    | `"3"` (single string ID)              |
| 7       | User        | `5` (user ID, integer)                |
| 8       | Date        | `"2026-01-15"` (date string)          |
| 9       | Milestone   | `10` (milestone ID, integer)          |
| 10      | Steps       | `"Step 1\nStep 2"` (text-based)       |
| 11      | Multi-select| `["3", "5"]` (array of STRING IDs)    |
| 12      | Stepped     | `[{"content": "...", "expected": "..."}]` |

## Format Examples

**Dropdown (type 6):**
```python
custom_fields={"custom_priority_level": "3"}
```

**Multi-select (type 11) -- MUST use string IDs, not integers:**
```python
custom_fields={
    "custom_interface_type": ["3", "5"],
    "custom_module": ["1"]
}
```

**Checkbox (type 5):**
```python
custom_fields={"custom_case_test_data_required": True}
```

**Separated steps (type 12):**
```python
custom_fields={
    "custom_steps_separated": [
        {"content": "Navigate to login page", "expected": "Login form is displayed"},
        {"content": "Enter valid credentials", "expected": "Dashboard loads"},
        {"content": "Click logout", "expected": "Redirected to login page"}
    ]
}
```

Each step object requires both `content` and `expected` keys with non-empty string values.

**Text/String (types 1, 3):**
```python
custom_fields={"custom_automation_type": "Automated"}
```

## Creating a Test Case -- Complete Example

```python
case = api.cases.add_case(
    section_id=123,
    title="Verify login with valid credentials",
    type_id=1,           # Functional
    priority_id=3,       # Medium
    estimate="15m",
    refs="JIRA-456",
    description="Verify that a user can log in with valid credentials",
    custom_fields={
        "custom_automation_type": "Manual",
        "custom_interface_type": ["3"],
        "custom_module": ["1", "2"],
        "custom_steps_separated": [
            {"content": "Open the login page", "expected": "Login form displayed"},
            {"content": "Enter username and password", "expected": "Fields populated"},
            {"content": "Click Sign In", "expected": "User dashboard loads"}
        ],
        "custom_case_test_data_required": False
    }
)
print(f"Created case ID: {case['id']}")
```

Standard `add_case` parameters:
- `section_id` (required)
- `title` (required)
- `type_id`, `priority_id`, `estimate`, `milestone_id`, `refs`
- `description`, `preconditions`, `postconditions`
- `template_id`
- `custom_fields` (dict of custom field values)
- `validate_required` (bool, default True) -- set to False to skip validation
- `validate_only` (bool) -- validate without creating

## Updating a Test Case

Only include fields to change. Omitted fields remain unchanged.

```python
updated = api.cases.update_case(
    case_id=789,
    title="Updated title",
    priority_id=1,
    custom_fields={
        "custom_priority_level": "2"
    }
)
```

## Common Pitfalls

### 1. Integer IDs instead of String IDs
```python
# WRONG -- will cause errors
custom_fields={"custom_interface_type": [3, 5]}

# CORRECT
custom_fields={"custom_interface_type": ["3", "5"]}
```

### 2. Missing custom_fields Nesting
```python
# WRONG -- custom fields at top level
api.cases.add_case(
    section_id=123,
    title="Test",
    custom_automation_type="Manual"  # Wrong placement!
)

# CORRECT -- nested under custom_fields
api.cases.add_case(
    section_id=123,
    title="Test",
    custom_fields={"custom_automation_type": "Manual"}
)
```

### 3. Wrong Step Object Keys
```python
# WRONG
[{"step": "Do X", "result": "Y happens"}]

# CORRECT
[{"content": "Do X", "expected": "Y happens"}]
```

### 4. Skipping Field Discovery
Always call `get_required_case_fields()` before `add_case()` to avoid repeated validation errors.

### 5. Empty Step Values
Both `content` and `expected` must be non-empty strings.

## Copy, Move, and Cache Operations

**Copy cases to another section:**
```python
api.cases.copy_cases_to_section(case_ids=[1, 2, 3], section_id=456)
```

**Move cases to another section:**
```python
api.cases.move_cases_to_section(case_ids=[1, 2, 3], section_id=456)
```

**Clear field cache** (if field definitions changed on the server):
```python
api.cases.clear_case_fields_cache()
```
