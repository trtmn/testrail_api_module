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

# Run with uvx using the module
uvx --package testrail-api-module -- python -m testrail_api_module
```

Or with command-line arguments:

```bash
uvx --package testrail-api-module -- python -m testrail_api_module \
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

## Logging

Enable verbose logging to see detailed information about tool registration and API calls:

```bash
testrail-mcp-server --verbose
```

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

To use the TestRail MCP server in Cursor, add it to your `mcp.json` configuration file (typically located at `~/.cursor/mcp.json` or `~/.config/cursor/mcp.json`):

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uvx",
      "args": [
        "--package",
        "testrail-api-module",
        "--",
        "python",
        "-m",
        "testrail_api_module"
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

**Using a Virtual Environment:**

If you're using a virtual environment, point to the Python executable in your venv:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "/path/to/your/.venv/bin/python",
      "args": [
        "-m",
        "testrail_api_module"
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

**Using the CLI Script Directly:**

Alternatively, you can use the installed CLI script directly:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "testrail-mcp-server",
      "env": {
        "TESTRAIL_BASE_URL": "https://your-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-username",
        "TESTRAIL_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Using uvx (No Installation Required):**

You can also use `uvx` to run the server without installing it:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uvx",
      "args": [
        "--package",
        "testrail-api-module",
        "--",
        "python",
        "-m",
        "testrail_api_module"
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

This is useful if you don't want to install the package globally or prefer to use `uvx` for package management. `uvx` will automatically download and cache the package on first use.

**Note**: The `--` separator is required to separate `uvx` arguments from the Python command arguments. The `--package` flag tells `uvx` which package to install, and everything after `--` is passed to Python.

**Using a .env File:**

If you prefer to use a `.env` file, you can reference it in the configuration:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "python",
      "args": [
        "-m",
        "testrail_api_module",
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
      "command": "python",
      "args": [
        "-m",
        "testrail_api_module"
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

### Finding Your Python Executable

To find the correct Python path for your configuration:

```bash
# For system Python
which python
# or
which python3

# For virtual environment
which python  # when venv is activated
# or check the venv path directly
echo $VIRTUAL_ENV/bin/python
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
