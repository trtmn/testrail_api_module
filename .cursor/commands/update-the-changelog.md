# Update the Changelog

## Overview

This command helps you update the human-readable `CHANGELOG.md` file following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Process

### 1. Add Changes to Unreleased Section

For every code change, add a corresponding entry to the `[Unreleased]` section at the top of `CHANGELOG.md`.

**Location**: The `[Unreleased]` section is located at the top of the changelog, right after the header.

### 2. Categorize Your Changes

Use the appropriate category with emoji prefix:

- **✨ Added**: New features
- **🔧 Changed**: Changes in existing functionality
- **🔧 Fixed**: Bug fixes
- **🚨 Breaking Changes**: Breaking changes (use sparingly)
- **📚 Documentation**: Documentation updates
- **🔄 Maintenance**: Maintenance tasks, dependency updates, etc.

### 3. Write Clear Entries

Each entry should:

- **Be descriptive**: Clearly explain what changed
- **Include impact**: Describe how the change affects users or the system
- **Be specific**: Include relevant details like method names, file paths, or affected areas
- **Use bullet points**: Use `-` for list items
- **Use bold for emphasis**: Use `**bold**` for important terms like method names, file paths, or key concepts

### 4. Entry Format

```markdown
### ✨ Added

- **Feature Name**: Brief description of the feature
  - Additional details about the feature
  - Impact: How this affects users or the system
  - Example: `api.cases.new_method()`
```

### 5. Multiple Related Changes

Group related changes together under a single bullet point with sub-bullets:

```markdown
- **Feature Group**: Main description
  - Sub-feature 1 details
  - Sub-feature 2 details
  - Impact: Combined impact statement
```

### 6. When Releasing

When you're ready to release a new version:

1. **Create a new version section** with the date:
   ```markdown
   ## [0.5.2] - 2026-01-23
   ```

2. **Move entries** from `[Unreleased]` to the new version section

3. **Update the version number** in `pyproject.toml` to match

4. **Clear the Unreleased section** (keep the header):
   ```markdown
   ## [Unreleased]
   ```

## Examples

### Good Entry (Added Feature)
```markdown
- **New Validation Method**: Added `validate_case_fields()` method to pre-validate test case data
  - Checks required fields before submission to TestRail API
  - Returns detailed validation report with missing fields
  - Impact: Reduces API errors and improves user experience
  - Example: `result = api.cases.validate_case_fields(section_id=123, data={...})`
```

### Good Entry (Bug Fix)
```markdown
- **MCP Parameter Parsing**: Fixed JSON parsing errors when calling MCP tools
  - Changed `params` parameter type from `Union[Dict[str, Any], str, None]` to `Optional[Dict[str, Any]]`
  - Generates cleaner JSON schema that FastMCP can properly serialize
  - Resolves "Expected ',' or '}' after property value in JSON" errors
  - Impact: MCP tools can now be called successfully from Cursor and other MCP clients
```

### Good Entry (Breaking Change)
```markdown
- **Exception Handling**: Methods now raise specific exceptions instead of returning `None`
  - All API methods now raise `TestRailAPIError` or subclasses on failure
  - Previously returned `None` on errors, now raises exceptions
  - Impact: **BREAKING** - Code using `if result is None:` checks must be updated to use try/except
  - Migration: See MIGRATION_GUIDE.md for complete migration instructions
```

## Best Practices

1. **Update immediately**: Add changelog entries as you make changes, not at the end
2. **Be thorough**: Include all significant changes, not just user-facing ones
3. **Be consistent**: Use the same style and format throughout
4. **Include context**: Explain why the change was made when relevant
5. **Link to issues**: Reference issue numbers if applicable (e.g., `Fixes #123`)
6. **Group logically**: Group related changes together
7. **Use clear language**: Write for both technical and non-technical readers

## Quick Reference

- **File**: `CHANGELOG.md`
- **Unreleased section**: Top of file, after header
- **Format**: Keep a Changelog
- **Versioning**: Semantic Versioning (MAJOR.MINOR.PATCH)
- **Categories**: ✨ Added, 🔧 Changed, 🔧 Fixed, 🚨 Breaking Changes, 📚 Documentation, 🔄 Maintenance
