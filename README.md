# testrail_api_module

[![PyPI - Version](https://img.shields.io/pypi/v/testrail-api-module?label=Latest%20Version)](https://pypi.org/project/testrail-api-module/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/testrail-api-module?color=purple)](https://pypi.org/project/testrail-api-module/) [![GitHub Source](https://img.shields.io/badge/github-source-blue?logo=github)](https://github.com/trtmn/testrail_api_module/) [![PyPI Stats](https://img.shields.io/badge/%20%F0%9F%94%97-blue?label="📈%20Stats")](https://pypistats.org/packages/testrail-api-module/) [![Docs](https://img.shields.io/pypi/v/testrail-api-module?label=📖%20Docs&color=blue)](https://trtmn.github.io/testrail_api_module/)

A comprehensive Python wrapper for the TestRail API that provides easy access to all TestRail functionalities.

## Features

- **NEW**: Comprehensive exception handling with specific error types
- **NEW**: Connection pooling and automatic retry logic
- **NEW**: Rate limiting awareness and handling
- **NEW**: Configurable request timeouts
- Full coverage of TestRail API endpoints
- Type hints for better IDE support
- Easy-to-use interface
- Support for both API key and password authentication

## 🚨 Breaking Changes in v0.6.3

**API parity audit.** All endpoints were audited against the [official TestRail API reference](https://support.testrail.com/hc/en-us/sections/7077196685204-Reference). Several methods were renamed, restructured, or removed to match the real API. See details below.

### Configurations API (rewritten)

The old single-level API has been replaced with the correct two-level group/config structure:

| Removed | Replacement |
|---|---|
| `get_configuration(config_id)` | `get_configs(project_id)` |
| `get_configurations(project_id)` | `get_configs(project_id)` |
| `add_configuration(project_id, ...)` | `add_config_group(project_id, name)` / `add_config(config_group_id, name)` |
| `update_configuration(config_id, ...)` | `update_config_group(config_group_id, name)` / `update_config(config_id, name)` |
| `delete_configuration(config_id)` | `delete_config_group(config_group_id)` / `delete_config(config_id)` |

### Results API (restructured)

| Change | Old | New |
|---|---|---|
| Renamed | `add_result(run_id, case_id, ...)` | `add_result_for_case(run_id, case_id, ...)` |
| New | — | `add_result(test_id, ...)` (adds result by test ID) |
| New | — | `get_results(test_id, ...)` (gets results by test ID) |
| Fixed | `add_results(...)` called `add_results_for_cases` endpoint | `add_results(...)` now correctly calls `add_results/{run_id}` |
| Removed | `add_result_for_run(...)` | (not a real TestRail endpoint) |

### Cases API

| Change | Old | New |
|---|---|---|
| Renamed | `get_case_history(case_id)` | `get_history_for_case(case_id)` |
| New | — | `add_case_field(...)`, `update_cases(...)`, `delete_cases(...)` |

### Plans API

| Change | Old | New |
|---|---|---|
| Removed | `get_plan_stats(plan_id)` | (not a real TestRail endpoint) |
| New | — | `add_plan_entry(...)`, `update_plan_entry(...)`, `delete_plan_entry(...)` |

### New modules and methods

- **Labels API** (new module): `get_label`, `get_labels`, `add_label`, `update_label`, `delete_label`
- **Sections**: `move_section(section_id, ...)`
- **Users**: `get_current_user()`
- **Statuses**: `get_case_statuses()`
- **Datasets**: `add_dataset(...)`, `update_dataset(...)`, `delete_dataset(...)`

## 🚨 Breaking Changes in v0.4.x

**This is a major version update with breaking changes.** Please read the [Migration Guide](MIGRATION_GUIDE.md) before upgrading from v0.3.x.

### Key Changes

- **Enhanced Error Handling**: Methods now raise specific exceptions instead of returning `None`
- **Consistent Return Types**: No more `Optional` wrappers - methods return data directly
- **Better Type Safety**: Comprehensive type annotations throughout
- **Performance Improvements**: Connection pooling, retry logic, and efficient requests
- **Official Compliance**: Follows TestRail API best practices

## Installation

### For Consumers

```bash
# Install the package with runtime dependencies only
pip install testrail-api-module
```

### For Developers

```bash
# Clone the repository
git clone https://github.com/trtmn/testrail-api-module.git
cd testrail-api-module

# Create virtual environment and install dependencies using uv
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies (includes all dev tools like pytest, mypy, etc.)
uv sync --extra dev

# Or install all optional dependencies
uv sync --all-extras
```

## Testing

```bash
# Run tests with the current Python version
uv run pytest

# Run tests across all supported Python versions (3.11, 3.12, 3.13)
tox
```

## Quick Start

```python
from testrail_api_module import TestRailAPI, TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

# Initialize the API client
api = TestRailAPI(
    base_url='https://your-instance.testrail.io',
    username='your-username',
    api_key='your-api-key',  # or use password='your-password'
    timeout=30  # Optional: request timeout in seconds
)

try:
    # Get a list of projects
    projects = api.projects.get_projects()
    print(f"Found {len(projects)} projects")

    # Create a new test case
    new_case = api.cases.add_case(
        section_id=123,
        title='Test Login Functionality',
        type_id=1,  # Functional test
        priority_id=3,  # Medium priority
        estimate='30m',  # 30 minutes
        refs='JIRA-123'
    )
    print(f"Created case: {new_case['title']}")

    # Add a test result for a case in a run
    result = api.results.add_result_for_case(
        run_id=456,
        case_id=789,
        status_id=1,  # Passed
        comment='Test executed successfully',
        elapsed='15m',  # Actual time taken
        version='1.0.0'
    )
    print(f"Added result: {result['id']}")

except TestRailAuthenticationError as e:
    print(f"Authentication failed: {e}")
except TestRailRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except TestRailAPIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Use Cases

### Managing Test Cases

```python
try:
    # Get all test cases in a project
    cases = api.cases.get_cases(project_id=1)
    print(f"Found {len(cases)} cases")

    # Update a test case
    updated_case = api.cases.update_case(
        case_id=123,
        title='Updated Test Case Title',
        type_id=2,  # Performance test
        priority_id=1  # Critical priority
    )
    print(f"Updated case: {updated_case['title']}")

    # Delete a test case
    result = api.cases.delete_case(case_id=123)
    print("Case deleted successfully")

except TestRailAPIError as e:
    print(f"Error managing test cases: {e}")
```

### Working with Test Runs

```python
# Create a new test run
new_run = api.runs.add_run(
    project_id=1,
    name='Sprint 1 Regression',
    description='Full regression test suite',
    suite_id=2,
    milestone_id=3,
    include_all=True
)

# Get test run results
results = api.runs.get_run_stats(run_id=new_run['id'])

# Close a test run
api.runs.close_run(run_id=new_run['id'])
```

### Managing Attachments

```python
# Add an attachment to a test case
api.attachments.add_attachment(
    entity_type='case',
    entity_id=123,
    file_path='path/to/screenshot.png',
    description='Screenshot of the error'
)

# Get attachments for a test case
attachments = api.attachments.get_attachments(
    entity_type='case',
    entity_id=123
)
```

### Working with BDD Scenarios

```python
# Import a BDD scenario
api.bdd.add_bdd(
    section_id=123,
    feature_file='path/to/feature/file.feature',
    description='Login feature tests'
)

# Export a BDD scenario
scenario = api.bdd.get_bdd(case_id=456)
```

## Error Handling

The module includes comprehensive error handling with specific exception types:

```python
from testrail_api_module import TestRailAPI, TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

try:
    result = api.cases.get_case(case_id=999999)
    print(f"Case: {result['title']}")
except TestRailAuthenticationError as e:
    print(f"Authentication failed: {e}")
except TestRailRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except TestRailAPIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Exception Types

- **`TestRailAPIError`**: Base exception for all API-related errors
- **`TestRailAuthenticationError`**: Authentication failures (401 errors)
- **`TestRailRateLimitError`**: Rate limit exceeded (429 errors)
- **`TestRailAPIException`**: General API errors with status codes and response details

## Migration Guide

**Upgrading from v0.3.x?** Please read our comprehensive [Migration Guide](MIGRATION_GUIDE.md) for detailed instructions on updating your code to work with v0.4.0.

### Quick Migration Summary

1. **Update error handling**: Wrap API calls in try/except blocks
2. **Remove None checks**: Methods now return data directly or raise exceptions
3. **Import exception classes**: Add `TestRailAPIError`, `TestRailAuthenticationError`, `TestRailRateLimitError` to your imports
4. **Update method calls**: Use explicit parameters instead of `**kwargs` where applicable

## Documentation

For complete documentation, visit our
[docs](https://trtmn.github.io/testrail_api_module/).

## Dependency Management

This project uses modern Python packaging with `pyproject.toml` for dependency
management.

### Files

- `pyproject.toml` - Package configuration and dependency specifications

## 🔒 Security & Credential Protection

This project includes automated credential detection to prevent secrets from being committed to the repository.

### Pre-commit Hooks

The repository uses [pre-commit](https://pre-commit.com/) hooks that automatically:

- **Detect secrets**: Scans for API keys, passwords, tokens, private keys, and other credentials using detect-secrets
- **Block commits**: Prevents commits containing detected secrets
- **Run on all git clients**: Works with command line, GUI clients, and IDEs

### Setting Up Pre-commit Hooks

1. **Install dependencies**:

   ```bash
   uv sync --extra dev
   ```

2. **Install git hooks**:

   ```bash
   pre-commit install
   ```

3. **Run hooks manually** (optional):

   ```bash
   pre-commit run --all-files
   ```

### Credential Management Best Practices

**✅ DO:**

- Use environment variables for credentials (`TESTRAIL_API_KEY`, `TESTRAIL_PASSWORD`)
- Store credentials in `.env` files (already in `.gitignore`)
- Use GitHub Secrets for CI/CD pipelines
- Use test credentials in test files (they're excluded from secret detection)

**❌ DON'T:**

- Commit `.env` files or any files containing real credentials
- Hardcode API keys or passwords in source code
- Commit files with `.key`, `.pem`, or other credential file extensions
- Bypass pre-commit hooks with `--no-verify` when committing credentials

### What Gets Detected

The secret detection scans for:

- API keys and tokens (TestRail, GitHub, AWS, etc.)
- Passwords and authentication credentials
- Private keys (SSH, SSL certificates)
- High-entropy strings (likely to be secrets)
- Common credential patterns

### If You Accidentally Commit Credentials

If credentials are accidentally committed:

1. **Immediately rotate/revoke** the exposed credentials
2. **Remove from git history** using `git filter-branch` or BFG Repo-Cleaner
3. **Force push** to update the remote repository (coordinate with team)
4. **Notify team members** to update their local repositories

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.

## Authors

- Matt Troutman
- Christian Thompson
- Andrew Tipper

## Support

If you encounter any issues or have questions, please
[open an issue](https://github.com/trtmn/testrail_api_module/issues/new) on
GitHub.
