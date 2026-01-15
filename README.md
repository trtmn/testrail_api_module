# testrail_api_module

[![PyPI - Version](https://img.shields.io/pypi/v/testrail-api-module?label=Latest%20Version)](https://pypi.org/project/testrail-api-module/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/testrail-api-module?color=purple)](https://pypi.org/project/testrail-api-module/) [![GitHub Source](https://img.shields.io/badge/github-source-blue?logo=github)](https://github.com/trtmn/testrail-api-module/) [![PyPI Stats](https://img.shields.io/badge/%20%F0%9F%94%97-blue?label="📈%20Stats")](https://pypistats.org/packages/testrail-api-module/) [![Docs](https://img.shields.io/pypi/v/testrail-api-module?label=📖%20Docs&color=blue)](https://trtmn.github.io/testrail_api_module/)

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=testrail-mcp&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJ0ZXN0cmFpbC1hcGktbW9kdWxlIiwidGVzdHJhaWwtbWNwLXNlcnZlciJdLCJlbnYiOnsiVEVTVFJBSUxfQkFTRV9VUkwiOiJodHRwczovL3lvdXJpbnN0YW5jZS50ZXN0cmFpbC5pbyIsIlRFU1RSQUlMX1VTRVJOQU1FIjoiWW91cnRlc3RyYWlsdXNlckB5b3VyY29tcGFueS5jb20iLCJURVNUUkFJTF9BUElfS0VZIjoiWW91ciBBUEkgS2V5IGdvZXMgaGVyZSJ9fQ%3D%3D)



A comprehensive Python wrapper for the TestRail API that provides easy access to all TestRail functionalities. Now featuring a built-in MCP (Model Context Protocol) server for seamless AI assistant integration.

## Features

- **NEW**: MCP (Model Context Protocol) server support for AI assistants
- **NEW**: Comprehensive exception handling with specific error types
- **NEW**: Connection pooling and automatic retry logic
- **NEW**: Rate limiting awareness and handling
- **NEW**: Configurable request timeouts
- Full coverage of TestRail API endpoints
- Type hints for better IDE support
- Easy-to-use interface
- Support for both API key and password authentication

## 🚨 Breaking Changes in v0.4.x

**This is a major version update with breaking changes.** Please read the [Migration Guide](MIGRATION_GUIDE.md) before upgrading from v0.3.x.

### Key Changes:
- **Enhanced Error Handling**: Methods now raise specific exceptions instead of returning `None`
- **Consistent Return Types**: No more `Optional` wrappers - methods return data directly
- **Better Type Safety**: Comprehensive type annotations throughout
- **Performance Improvements**: Connection pooling, retry logic, and efficient requests
- **Official Compliance**: Follows TestRail API best practices

## MCP (Model Context Protocol) Server

This package includes a built-in MCP server that enables AI assistants (like Cursor, Claude Desktop, etc.) to interact with TestRail through a standardized interface. All TestRail API methods are automatically exposed as MCP tools.

### ⚡ Quick Install for Cursor

**One-click install link for Cursor:**

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=testrail-mcp&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJ0ZXN0cmFpbC1hcGktbW9kdWxlIiwidGVzdHJhaWwtbWNwLXNlcnZlciJdLCJlbnYiOnsiVEVTVFJBSUxfQkFTRV9VUkwiOiJodHRwczovL3lvdXJpbnN0YW5jZS50ZXN0cmFpbC5pbyIsIlRFU1RSQUlMX1VTRVJOQU1FIjoiWW91cnRlc3RyYWlsdXNlckB5b3VyY29tcGFueS5jb20iLCJURVNUUkFJTF9BUElfS0VZIjoiWW91ciBBUEkgS2V5IGdvZXMgaGVyZSJ9fQ%3D%3D)

**After clicking the link:**
1. Cursor will prompt you to install the MCP server
2. You'll need to update the environment variables in the prompt / your `mcp.json` file:
   - Replace `https://yourinstance.testrail.io` with your TestRail instance URL
   - Replace `Yourtestrailuser@yourcompany.com` with your TestRail username/email
   - Replace `Your API Key goes here` with your TestRail API key (found in your TestRail profile settings)
3. Restart Cursor to activate the MCP server

**Text link (if button doesn't work):**
```
cursor://anysphere.cursor-deeplink/mcp/install?name=testrail-mcp&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJ0ZXN0cmFpbC1hcGktbW9kdWxlIiwidGVzdHJhaWwtbWNwLXNlcnZlciJdLCJlbnYiOnsiVEVTVFJBSUxfQkFTRV9VUkwiOiJodHRwczovL3lvdXJpbnN0YW5jZS50ZXN0cmFpbC5pbyIsIlRFU1RSQUlMX1VTRVJOQU1FIjoiWW91cnRlc3RyYWlsdXNlckB5b3VyY29tcGFueS5jb20iLCJURVNUUkFJTF9BUElfS0VZIjoiWW91ciBBUEkgS2V5IGdvZXMgaGVyZSJ9fQ==
```


> **⚠️ Important**: You must have [`uv`](https://github.com/astral-sh/uv) installed before running the MCP server. The MCP server uses `uvx` to run without requiring a global package installation.

#### Step 1: Install `uv` (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Step 2: Install MCP Server in Cursor

**📋 Click to Copy Configuration**

Open or create `~/.cursor/mcp.json` (or `~/.config/cursor/mcp.json` on Linux) and add this configuration:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uvx",
      "args": [
        "--from",
        "testrail-api-module",
        "testrail-mcp-server"
      ],
      "env": {
        "TESTRAIL_BASE_URL": "https://your-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-username",
        "TESTRAIL_API_KEY": "your-api-key"
      }
    }
  }
}
```

**After copying:**
1. Replace `https://your-instance.testrail.io` with your TestRail instance URL
2. Replace `your-username` with your TestRail username/email
3. Replace `your-api-key` with your TestRail API key (found in your TestRail profile settings)

#### Step 3: Restart Cursor

Restart Cursor to load the MCP server. The TestRail tools will be available in your AI assistant.

> **Note**: This configuration runs the `testrail-mcp-server` CLI using
> `uvx --from testrail-api-module`. `uvx` will automatically download and
> cache the package from PyPI if needed, so you don't need a global install
> or a pre-created virtual environment.

### Alternative Installation Methods

**Using uvx directly from GitHub** (no PyPI install required):

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/trtmn/testrail_api_module",
        "testrail-mcp-server"
      ],
      "env": {
        "TESTRAIL_BASE_URL": "https://your-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-username",
        "TESTRAIL_API_KEY": "your-api-key"
      }
    }
  }
}
```

### MCP Features

- **Automatic Tool Discovery**: All TestRail API methods are automatically exposed as MCP tools
- **Module-Based Organization**: Tools are organized by TestRail module (cases, runs, results, etc.)
- **Full API Coverage**: Access to all 22 TestRail API modules
- **Environment-Based Configuration**: Configure via environment variables or `.env` files
- **No Installation Required**: Use `uvx` to run without installing the package globally

### Available Tools

The MCP server exposes tools for all TestRail API modules:
- `attachments` - Managing attachments
- `cases` - Test cases
- `configurations` - Test configurations
- `milestones` - Milestones
- `plans` - Test plans
- `projects` - Projects
- `results` - Test results
- `runs` - Test runs
- `suites` - Test suites
- And many more...

### Documentation

For detailed MCP usage instructions, see the [MCP Usage Guide](docs/MCP_USAGE.md).

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
    
    # Add a test result
    result = api.results.add_result(
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
[docs](https://trtmn.github.io/testrail-api-module/).

## Dependency Management

This project uses modern Python packaging with `pyproject.toml` for dependency
management.

### Files

- `pyproject.toml` - Package configuration and dependency specifications

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
