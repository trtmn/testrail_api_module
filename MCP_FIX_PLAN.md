# MCP Tool Fix Plan: Improving Context for LLM Case Creation

## Problem Summary

When using Claude to create test cases via the MCP tool, there are multiple issues causing trial-and-error:

1. **Confusing Error Messages**: TestRail API errors mix field type information with step validation text, making it unclear what's wrong
2. **Missing Field Discovery**: LLMs don't proactively discover required fields before attempting to create cases
3. **Incorrect Field Formatting**: Array fields (dropdowns/multi-select) are sometimes passed incorrectly
4. **Lack of Context**: Error messages don't provide enough actionable guidance

## Root Cause Analysis

### Issue 1: TestRail API Error Messages
The errors show that TestRail's API validation returns messages like:
```
Missing required field(s): 'custom_interface_type' (array of IDs from: {1=RecTrac, 2=WebTrac, ...}) (must include at least one step with non-empty 'content' and 'expected')
```

This is confusing because:
- The step validation text is incorrectly appended to dropdown fields
- The error doesn't clearly show the correct format
- Multiple errors occur in sequence instead of showing all issues at once

### Issue 2: No Proactive Field Discovery
The MCP tool description mentions `get_case_fields()` but doesn't strongly encourage using it first. LLMs attempt to create cases without knowing required fields.

### Issue 3: Array Field Formatting
Dropdown/multi-select fields require arrays of **string IDs** (e.g., `["3", "5"]`), but LLMs sometimes pass:
- Single values instead of arrays
- Integer IDs instead of string IDs
- Incorrect array structure

## Solution Plan

### Phase 1: Enhance MCP Tool Descriptions (High Priority)

**File**: `src/testrail_api_module/mcp_server.py`

**Changes**:
1. Add prominent guidance at the top of `testrail_cases` tool description recommending field discovery
2. Include a clear workflow example showing the recommended approach
3. Add explicit examples of correct field formats for common field types

**Implementation**:
```python
# In _create_module_tool, enhance the docstring for cases module:
if module_name == 'cases' and ('add_case' in method_names or 'update_case' in method_names):
    docstring_parts.insert(0, [
        "⚠️ IMPORTANT: Before creating test cases, discover required fields!",
        "",
        "RECOMMENDED WORKFLOW:",
        "  1. First, call get_required_case_fields to see what's required:",
        "     action='get_required_case_fields', params={'section_id': 123}",
        "  2. Review the field types and formats",
        "  3. Then create the case with all required fields",
        "",
        "This prevents trial-and-error and ensures correct field formats.",
        "",
    ])
```

### Phase 2: Improve Error Handling and Context (High Priority)

**File**: `src/testrail_api_module/mcp_server.py`

**Changes**:
1. Catch TestRail API errors and enhance them with better context
2. Parse TestRail error messages to extract field requirements
3. Provide actionable suggestions based on error content
4. Include examples of correct field formats in error messages

**Implementation**:
- Add error handler in `module_tool` function that:
  - Detects TestRail validation errors
  - Extracts field names and types from error messages
  - Suggests calling `get_required_case_fields` if not already called
  - Provides format examples for the missing fields

### Phase 3: Add Pre-Validation for Common Mistakes (Medium Priority)

**File**: `src/testrail_api_module/cases.py`

**Changes**:
1. Add validation to ensure array fields are properly formatted before sending to TestRail
2. Convert single values to arrays for multi-select fields when appropriate
3. Validate that array elements are strings (not integers) for ID fields
4. Provide clear error messages for format issues

**Implementation**:
- Add `_validate_and_normalize_custom_fields` method that:
  - Checks field types from `get_case_fields()`
  - Validates array fields are arrays
  - Converts integer IDs to string IDs for dropdown/multi-select fields
  - Provides helpful error messages with examples

### Phase 4: Enhance Field Discovery Tools (Medium Priority)

**File**: `src/testrail_api_module/cases.py`

**Changes**:
1. Make `get_required_case_fields` more discoverable by accepting `section_id` directly
2. Add a convenience method that returns field requirements in a format optimized for LLMs
3. Include complete examples in the response showing correct field formats

**Implementation**:
- Enhance `get_required_case_fields` to:
  - Accept `section_id` and automatically resolve context
  - Return field information with complete format examples
  - Include valid option IDs and labels for dropdown fields

### Phase 5: Update Documentation (Low Priority)

**Files**: 
- `docs/MCP_USAGE.md`
- Tool docstrings

**Changes**:
1. Add a "Best Practices" section emphasizing field discovery
2. Include complete examples showing the recommended workflow
2. Document common pitfalls and how to avoid them

## Implementation Priority

1. **Phase 1** (High): Enhance tool descriptions - Quick win, immediate impact
2. **Phase 2** (High): Improve error handling - Reduces confusion when errors occur
3. **Phase 3** (Medium): Pre-validation - Prevents common mistakes
4. **Phase 4** (Medium): Field discovery enhancements - Makes discovery easier
5. **Phase 5** (Low): Documentation - Supports all other improvements

## Expected Outcomes

After implementing these fixes:

1. **Reduced Trial-and-Error**: LLMs will proactively discover required fields before creating cases
2. **Clearer Error Messages**: Errors will include actionable guidance and examples
3. **Better Field Formatting**: Pre-validation will catch format issues before sending to TestRail
4. **Improved Context**: Tool descriptions will guide LLMs to use the right workflow

## Testing Strategy

1. Test with example LLM prompts that previously failed
2. Verify that enhanced tool descriptions guide LLMs to discover fields first
3. Confirm error messages are more actionable
4. Validate that pre-validation catches common mistakes
5. Test the complete workflow: discover → validate → create

## Success Metrics

- Reduction in number of error iterations before successful case creation
- LLMs successfully discover required fields before first creation attempt
- Error messages provide actionable guidance (not just field names)
- Pre-validation catches format issues before TestRail API calls
