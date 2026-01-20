# TestRail API Module - MCP (Model Context Protocol) Usage

This document describes how to use the TestRail API module as an MCP server, enabling LLMs to interact with TestRail through a standardized interface.

## Installation

MCP functionality is included in the base installation. Simply install the package:

```bash
# Using pip
pip install testrail-api-module

# Using uv
uv sync
```

**Note**: For `.env` file support, you may optionally install `python-dotenv`:
```bash
pip install python-dotenv
# or
pip install testrail-api-module[mcp]  # Includes python-dotenv
```

## Quick Start

### As a Command-Line Tool

The easiest way to run the MCP server is using the command-line tool:

```bash
# Set environment variables
export TESTRAIL_BASE_URL="https://your-instance.testrail.io"
export TESTRAIL_USERNAME="your-username"
export TESTRAIL_API_KEY="your-api-key"

# Start the server
testrail-mcp-server
```

Or use command-line arguments:

```bash
testrail-mcp-server \
  --base-url "https://your-instance.testrail.io" \
  --username "your-username" \
  --api-key "your-api-key" \
  --verbose
```

### Using uvx (No Installation Required)

You can also run the MCP server directly with `uvx` without installing the package:

```bash
# Set environment variables
export TESTRAIL_BASE_URL="https://your-instance.testrail.io"
export TESTRAIL_USERNAME="your-username"
export TESTRAIL_API_KEY="your-api-key"

# Run with uvx from PyPI
uvx --from testrail-api-module testrail-mcp-server

# Or run directly from GitHub (no PyPI required)
uvx --from git+https://github.com/trtmn/testrail_api_module testrail-mcp-server
```

Or with command-line arguments:

```bash
uvx --from testrail-api-module testrail-mcp-server \
  --base-url "https://your-instance.testrail.io" \
  --username "your-username" \
  --api-key "your-api-key" \
  --verbose
```

**Note**: `uvx` will automatically download and cache the package if it's not already available, making it convenient for one-off runs or when you don't want to install the package globally.

### As a Python Library

You can also create and run the MCP server programmatically:

```python
from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_server import create_mcp_server

# Create API instance
api = TestRailAPI(
    base_url="https://your-instance.testrail.io",
    username="your-username",
    api_key="your-api-key"
)

# Create and run MCP server
mcp = create_mcp_server(api_instance=api)
mcp.run()
```

## Configuration

### Environment Variables

The MCP server can be configured using environment variables:

- `TESTRAIL_BASE_URL` - Base URL of your TestRail instance (required)
- `TESTRAIL_USERNAME` - Your TestRail username (required)
- `TESTRAIL_API_KEY` - Your TestRail API key (required if password not set)
- `TESTRAIL_PASSWORD` - Your TestRail password (required if API key not set)
- `TESTRAIL_TIMEOUT` - Request timeout in seconds (default: 30)
- `TESTRAIL_MCP_DEBUG` - Enable debug logging (set to `1`, `true`, `yes`, or `on`)

### Command-Line Options

```bash
testrail-mcp-server --help
```

Available options:
- `--base-url` - TestRail base URL
- `--username` - TestRail username
- `--api-key` - TestRail API key
- `--password` - TestRail password
- `--timeout` - Request timeout (default: 30)
- `--env-file` - Path to .env file
- `--server-name` - Name for the MCP server (default: "TestRail API Server")
- `--verbose`, `-v` - Enable verbose logging

### .env File

You can also use a `.env` file:

```bash
# .env
TESTRAIL_BASE_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-username
TESTRAIL_API_KEY=your-api-key
TESTRAIL_TIMEOUT=30
```

Then run:

```bash
testrail-mcp-server --env-file .env
```

## Available Tools

All TestRail API methods are automatically exposed as MCP tools with the naming convention:

`testrail_{module}_{method}`

For example:
- `testrail_cases_get_case` - Get a test case by ID
- `testrail_cases_get_cases` - Get all test cases for a project
- `testrail_results_add_result` - Add a test result
- `testrail_runs_get_runs` - Get all test runs for a project

### Tool Discovery

The MCP server automatically discovers and registers all public methods from all API modules:

- `attachments` - Managing attachments
- `bdd` - BDD features
- `cases` - Test cases
- `configurations` - Test configurations
- `datasets` - Test datasets
- `groups` - User groups
- `milestones` - Milestones
- `plans` - Test plans
- `priorities` - Test priorities
- `projects` - Projects
- `reports` - Reports
- `result_fields` - Result fields
- `results` - Test results
- `roles` - User roles
- `runs` - Test runs
- `sections` - Test sections
- `shared_steps` - Shared steps
- `statuses` - Test statuses
- `suites` - Test suites
- `templates` - Test templates
- `tests` - Tests
- `users` - Users
- `variables` - Variables

## Error Handling

The MCP server handles errors from the TestRail API and converts them to appropriate MCP error responses. All TestRail API exceptions are preserved with their original error messages and status codes.

### Common Errors

#### Custom Fields Must Be Nested

When adding or updating test cases, custom fields must be passed in a `custom_fields` dictionary, not as top-level parameters.

**Incorrect:**
```json
{
  "action": "add_case",
  "params": {
    "section_id": 123,
    "title": "Test Case Title",
    "custom_steps": "1. Do this\n2. Do that",
    "custom_expected": "Expected result"
  }
}
```

**Correct:**
```json
{
  "action": "add_case",
  "params": {
    "section_id": 123,
    "title": "Test Case Title",
    "custom_fields": {
      "custom_steps": "1. Do this\n2. Do that",
      "custom_expected": "Expected result"
    }
  }
}
```

The error message will detect this mistake and provide a helpful correction with the correct format.

#### Understanding Custom Field Data Types

Different custom fields require different data types. The validation will show all missing fields with their types:

**Text fields** - String values:
```json
{
  "custom_automation_type": "Automated"
}
```

**Dropdown/Multi-select fields** - Arrays of STRING IDs (not integers):
```json
{
  "custom_interface_type": ["3", "5"],  // Strings, not integers!
  "custom_module": ["7"]
}
```

**Checkbox fields** - Boolean values:
```json
{
  "custom_case_test_data_required": true
}
```

**Separated steps** - Array of objects with `content` and `expected` keys:
```json
{
  "custom_steps_separated": [
    {
      "content": "Navigate to login page",
      "expected": "Login form is displayed"
    },
    {
      "content": "Enter credentials and submit",
      "expected": "User is logged in successfully"
    }
  ]
}
```

#### Comprehensive Validation

The improved validation shows ALL missing required fields at once, not one at a time:

**Error message example:**
```
Missing required field(s): 
  'custom_automation_type' (string), 
  'custom_steps_separated' (array of step objects: [{'content': '...', 'expected': '...'}]),
  'custom_case_test_data_required' (boolean),
  'custom_interface_type' (array of string IDs: ['3', '5']),
  'custom_module' (array of string IDs: ['3', '5'])

Field type guide:
  - Text fields: String values
  - Dropdown/Multi-select: Arrays of string IDs (e.g., ['3', '5'])
  - Checkboxes: Boolean values (True/False)
  - Separated steps: Array of step objects with 'content' and 'expected' keys
    Example: [{'content': 'Step 1', 'expected': 'Result 1'}]

Use get_case_fields() to see complete field requirements and types for your project.
```

#### Checking Required Fields

Before creating test cases, you can query which fields are required:

**Option 1: Get only required fields (recommended)**

Use the `get_required_case_fields` action to get a filtered list of only required fields with formatted type hints:

```json
{
  "action": "get_required_case_fields",
  "params": {
    "project_id": 1,  // Optional: filter by project
    "use_cache": true  // Optional: use cached data (default: true)
  }
}
```

This returns detailed information about each required field:

```json
{
  "required_fields": [
    {
      "system_name": "custom_automation_type",
      "label": "Automation Type",
      "type_id": 1,
      "type_name": "String",
      "type_hint": "string",
      "is_global": true,
      "project_ids": null,
      "description": "The automation type for the test case"
    },
    {
      "system_name": "custom_steps_separated",
      "label": "Steps",
      "type_id": 12,
      "type_name": "Stepped",
      "type_hint": "array of step objects: [{'content': '...', 'expected': '...'}]",
      "is_global": false,
      "project_ids": [1, 2, 3],
      "description": "Test steps"
    }
  ],
  "field_count": 2,
  "project_filtered": true,
  "cache_used": true
}
```

Benefits:
- System name (to use as key in `custom_fields`)
- Display label and description
- Field type with helpful hints
- Project context (global vs project-specific)
- Pre-filtered to only required fields

**Option 2: Get all fields**

Use the `get_case_fields` action to see ALL fields (required and optional):

```json
{
  "action": "get_case_fields",
  "params": {}
}
```

This will return all field definitions including:
- `system_name`: The field name to use in API calls
- `label`: The display name shown in TestRail UI
- `type_id`: The field type (1=String, 5=Checkbox, 6=Dropdown, 11=Multi-select, 12=Steps)
- `is_required`: Whether the field is required
- `configs`: Project-specific configurations

## Logging

### Debug Logging

Enable debug logging to see detailed information about MCP server operations, including:
- API method discovery
- Tool registration details
- Method calls with parameters
- API response types and sizes
- Error stack traces

You can enable debug logging in two ways:

**Option 1: Using the `--verbose` flag:**

```bash
testrail-mcp-server --verbose
```

**Option 2: Using the `TESTRAIL_MCP_DEBUG` environment variable:**

```bash
export TESTRAIL_MCP_DEBUG=1
testrail-mcp-server
```

Or in your `.env` file:

```bash
# .env
TESTRAIL_BASE_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-username
TESTRAIL_API_KEY=your-api-key
TESTRAIL_MCP_DEBUG=1
```

**Note**: Debug logs are written to `stderr` to avoid interfering with the MCP protocol's `stdio` communication. This is important for MCP clients like Cursor and Claude Desktop that communicate via standard input/output.

Debug logging is configured to show only TestRail API module messages, not FastMCP's internal debug logs, keeping the output clean and relevant.

## Examples

### Example: Get a Test Case

```python
# Tool: testrail_cases_get_case
# Parameters:
#   case_id: int - The ID of the test case
# Returns: Dict containing test case data
```

### Example: Add a Test Result

```python
# Tool: testrail_results_add_result
# Parameters:
#   run_id: int - The ID of the test run
#   case_id: int - The ID of the test case
#   status_id: int - The status ID (1: Passed, 2: Blocked, 3: Untested, 4: Retest, 5: Failed)
#   comment: Optional[str] - Comment for the result
#   version: Optional[str] - Version of the software under test
#   elapsed: Optional[str] - Time taken (e.g., "30s", "2m 30s")
# Returns: Dict containing the created result data
```

## Integration with MCP Clients

The MCP server can be used with any MCP-compatible client. The server exposes all tools through the standard MCP protocol, making it compatible with:

- Claude Desktop
- Cursor
- Other MCP-compatible tools

### Configuring for Cursor

To use the TestRail MCP server in Cursor, add it to your `mcp.json` configuration file (typically located at `~/.cursor/mcp.json` or `~/.config/cursor/mcp.json`).

**Using uvx from PyPI (recommended):**

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

**Installing directly from GitHub (without PyPI):**

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

`uvx` will automatically download and cache the package on first use. The `--from` flag specifies the package source, and `testrail-mcp-server` is the entry point script to run.

**Using a .env File:**

If you prefer to use a `.env` file, you can reference it in the configuration:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uvx",
      "args": [
        "--from",
        "testrail-api-module",
        "testrail-mcp-server",
        "--env-file",
        "/path/to/your/.env"
      ]
    }
  }
}
```

### Configuring for Claude Desktop

For Claude Desktop, add the server configuration to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent location on your system:

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

Or install directly from GitHub:

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

### Security Note

**Important**: Never commit your `mcp.json` file with API keys to version control. Consider using environment variables or a `.env` file that's excluded from git.

## Troubleshooting

### ImportError: fastmcp is not installed

This should not occur as `fastmcp` is included in the base installation. If you see this error:

1. Make sure you've installed the package:
   ```bash
   pip install testrail-api-module
   ```

2. If the error persists, try reinstalling:
   ```bash
   pip uninstall testrail-api-module
   pip install testrail-api-module
   ```

### Authentication Errors

Verify your credentials are correct:
- Check that `TESTRAIL_BASE_URL` is correct
- Verify `TESTRAIL_USERNAME` is your email address
- Ensure `TESTRAIL_API_KEY` or `TESTRAIL_PASSWORD` is valid

### Tool Registration Warnings

If you see warnings about tool registration failures, check the logs with `--verbose` to see the specific error. Most issues are related to method signatures or missing dependencies.

## Additional Resources

- [TestRail API Documentation](https://www.gurock.com/testrail/docs/api)
- [FastMCP Documentation](https://gofastmcp.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
