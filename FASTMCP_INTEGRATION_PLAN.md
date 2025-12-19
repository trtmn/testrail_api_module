# FastMCP Integration Plan for TestRail API Module

## Overview

This plan outlines the integration of fastMCP into the TestRail API module to expose all API endpoints as MCP (Model Context Protocol) tools. This will enable LLMs to interact with TestRail through a standardized MCP interface.

## Goals

1. Expose all TestRail API methods as MCP tools
2. Maintain backward compatibility with existing API usage
3. Provide easy configuration for authentication
4. Support both standalone MCP server and library usage
5. Follow project coding standards and best practices

## Architecture

### Components

1. **MCP Server Module** (`src/testrail_api_module/mcp_server.py`)
   - FastMCP server instance
   - Dynamic method discovery and registration
   - Authentication handling
   - Tool naming and organization

2. **MCP Utilities** (`src/testrail_api_module/mcp_utils.py`)
   - Helper functions for method discovery
   - Tool name generation
   - Parameter transformation utilities

3. **CLI Entry Point** (`src/testrail_api_module/cli.py` or `scripts/mcp_server.py`)
   - Command-line interface to run the MCP server
   - Configuration loading (env vars, config files)
   - Server startup and management

4. **Configuration** (Environment variables or config file)
   - `TESTRAIL_BASE_URL`
   - `TESTRAIL_USERNAME`
   - `TESTRAIL_API_KEY` or `TESTRAIL_PASSWORD`
   - `TESTRAIL_TIMEOUT` (optional)

## Implementation Steps

### Phase 1: Dependencies and Setup

1. **Add fastMCP dependency**
   - Add `fastmcp` to `pyproject.toml` dependencies
   - Consider making it an optional dependency (e.g., `[project.optional-dependencies]` with `mcp` extra)
   - Update `uv.lock` after adding dependency

2. **Project structure**
   - Create MCP server module: `src/testrail_api_module/mcp_server.py`
   - Create MCP utilities: `src/testrail_api_module/mcp_utils.py`
   - Create CLI script: `scripts/mcp_server.py` or add to existing CLI

### Phase 2: Core MCP Server Implementation

1. **Method Discovery System**
   - Create utility function to discover all public methods from API modules
   - Filter out private methods (starting with `_`)
   - Filter out base API methods (`_get`, `_post`, `_api_request`, etc.)
   - Organize methods by API module (cases, results, runs, etc.)

2. **Tool Registration**
   - For each discovered method, create an MCP tool wrapper
   - Generate tool names: `testrail_{module}_{method}` (e.g., `testrail_cases_get_case`)
   - Preserve method signatures and type hints
   - Extract docstrings for tool descriptions
   - Handle `self` parameter removal (methods become functions)

3. **Authentication Handling**
   - Support initialization from environment variables
   - Support initialization from passed TestRailAPI instance
   - Support initialization from config file
   - Validate credentials before starting server

4. **Parameter Handling**
   - Convert method parameters to MCP tool parameters
   - Handle optional parameters correctly
   - Support complex types (Dict, List, Union, Optional)
   - Handle file uploads for attachment methods

### Phase 3: Tool Wrapper Implementation

1. **Dynamic Tool Creation**
   - Create wrapper functions that:
     - Accept the same parameters as the original method
     - Call the appropriate API method on the TestRailAPI instance
     - Return results in MCP-compatible format
     - Handle exceptions and convert to appropriate error responses

2. **Tool Naming Convention**
   - Format: `testrail_{module}_{method}`
   - Examples:
     - `testrail_cases_get_case`
     - `testrail_results_add_result`
     - `testrail_runs_get_runs`
   - Use snake_case consistently

3. **Tool Descriptions**
   - Extract from method docstrings
   - Include parameter descriptions
   - Include return value descriptions
   - Include example usage if available

### Phase 4: CLI and Configuration

1. **CLI Implementation**
   - Create command-line interface using `argparse` or `click`
   - Support:
     - `--base-url` / `--username` / `--api-key` / `--password` flags
     - `--config` for config file path
     - `--timeout` for request timeout
     - `--verbose` for logging
   - Load from environment variables as fallback

2. **Configuration Management**
   - Support `.env` file loading (using `python-dotenv`)
   - Support JSON/YAML config files
   - Priority: CLI args > env vars > config file > defaults

3. **Entry Point**
   - Add console script entry point to `pyproject.toml`
   - Example: `testrail-mcp-server` command

### Phase 5: Error Handling and Logging

1. **Exception Handling**
   - Catch TestRail API exceptions
   - Convert to MCP-compatible error responses
   - Preserve error details (status codes, messages)
   - Log errors appropriately

2. **Logging**
   - Set up structured logging
   - Log tool invocations
   - Log API requests/responses (optional, configurable)
   - Support different log levels

### Phase 6: Testing and Documentation

1. **Unit Tests**
   - Test method discovery
   - Test tool registration
   - Test parameter handling
   - Test error handling
   - Test authentication

2. **Integration Tests**
   - Test MCP server startup
   - Test tool invocation (with mocked API)
   - Test end-to-end scenarios

3. **Documentation**
   - Update README with MCP usage instructions
   - Add MCP-specific documentation
   - Document configuration options
   - Provide examples

## Technical Considerations

### Method Discovery

```python
def discover_api_methods(api_instance: TestRailAPI) -> Dict[str, List[Callable]]:
    """
    Discover all public methods from all API modules.
    
    Returns:
        Dictionary mapping module names to lists of method objects
    """
    methods_by_module = {}
    
    # Get all API module attributes
    api_modules = [
        'attachments', 'bdd', 'cases', 'configurations', 'datasets',
        'groups', 'milestones', 'plans', 'priorities', 'projects',
        'reports', 'result_fields', 'results', 'roles', 'runs',
        'sections', 'shared_steps', 'statuses', 'suites', 'templates',
        'tests', 'users', 'variables'
    ]
    
    for module_name in api_modules:
        if hasattr(api_instance, module_name):
            module_instance = getattr(api_instance, module_name)
            methods = [
                method for name, method in inspect.getmembers(module_instance)
                if inspect.ismethod(method) and not name.startswith('_')
            ]
            methods_by_module[module_name] = methods
    
    return methods_by_module
```

### Tool Wrapper Pattern

```python
def create_tool_wrapper(api_instance: TestRailAPI, module_name: str, method_name: str, method: Callable):
    """
    Create an MCP tool wrapper for an API method.
    """
    @mcp.tool
    def tool_wrapper(*args, **kwargs):
        """Tool description from method docstring"""
        module = getattr(api_instance, module_name)
        method_func = getattr(module, method_name)
        return method_func(*args, **kwargs)
    
    # Set proper name and signature
    tool_wrapper.__name__ = f"testrail_{module_name}_{method_name}"
    tool_wrapper.__signature__ = inspect.signature(method)
    tool_wrapper.__doc__ = method.__doc__
    
    return tool_wrapper
```

### Authentication from Environment

```python
def create_api_from_env() -> TestRailAPI:
    """Create TestRailAPI instance from environment variables."""
    import os
    
    base_url = os.getenv('TESTRAIL_BASE_URL')
    username = os.getenv('TESTRAIL_USERNAME')
    api_key = os.getenv('TESTRAIL_API_KEY')
    password = os.getenv('TESTRAIL_PASSWORD')
    timeout = int(os.getenv('TESTRAIL_TIMEOUT', '30'))
    
    if not base_url or not username:
        raise ValueError("TESTRAIL_BASE_URL and TESTRAIL_USERNAME must be set")
    
    if not api_key and not password:
        raise ValueError("Either TESTRAIL_API_KEY or TESTRAIL_PASSWORD must be set")
    
    return TestRailAPI(
        base_url=base_url,
        username=username,
        api_key=api_key,
        password=password,
        timeout=timeout
    )
```

## File Structure

```
src/testrail_api_module/
├── __init__.py
├── base.py
├── mcp_server.py          # NEW: Main MCP server implementation
├── mcp_utils.py           # NEW: MCP utility functions
├── cli.py                 # NEW (optional): CLI for MCP server
├── [existing API modules...]

scripts/
└── mcp_server.py          # NEW (alternative): Standalone CLI script

tests/
├── test_mcp_server.py     # NEW: Tests for MCP server
└── test_mcp_utils.py      # NEW: Tests for MCP utilities

docs/
└── mcp_usage.md           # NEW: MCP usage documentation
```

## Dependencies

### Required
- `fastmcp` - FastMCP framework

### Optional (for CLI)
- `python-dotenv` - Environment variable loading (already in dev dependencies)
- `click` or `argparse` - CLI framework (argparse is stdlib)

## Configuration Example

### Environment Variables
```bash
export TESTRAIL_BASE_URL="https://your-instance.testrail.io"
export TESTRAIL_USERNAME="your-username"
export TESTRAIL_API_KEY="your-api-key"
export TESTRAIL_TIMEOUT="30"
```

### Config File (JSON)
```json
{
  "base_url": "https://your-instance.testrail.io",
  "username": "your-username",
  "api_key": "your-api-key",
  "timeout": 30
}
```

## Usage Examples

### As a Library
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
mcp = create_mcp_server(api)
mcp.run()
```

### As CLI
```bash
# Using environment variables
testrail-mcp-server

# Using command-line arguments
testrail-mcp-server \
  --base-url "https://your-instance.testrail.io" \
  --username "your-username" \
  --api-key "your-api-key"

# Using config file
testrail-mcp-server --config config.json
```

## Testing Strategy

1. **Unit Tests**
   - Test method discovery with mock API instances
   - Test tool wrapper creation
   - Test parameter transformation
   - Test error handling

2. **Integration Tests**
   - Test MCP server startup
   - Test tool registration
   - Test tool invocation with mocked API responses
   - Test authentication handling

3. **Manual Testing**
   - Test with actual MCP client
   - Verify all tools are accessible
   - Test error scenarios
   - Test with different authentication methods

## Migration and Compatibility

- **Backward Compatibility**: Existing API usage remains unchanged
- **Optional Dependency**: FastMCP can be an optional dependency
- **No Breaking Changes**: All existing functionality preserved

## Future Enhancements

1. **Tool Filtering**: Allow filtering which tools to expose
2. **Tool Grouping**: Organize tools by category
3. **Rate Limiting**: Add rate limiting awareness at MCP level
4. **Caching**: Add response caching for read operations
5. **Batch Operations**: Support batch tool invocations
6. **Webhook Support**: Add webhook endpoints for TestRail events

## Timeline Estimate

- **Phase 1**: 1-2 hours (dependencies, structure)
- **Phase 2**: 4-6 hours (core implementation)
- **Phase 3**: 3-4 hours (tool wrappers)
- **Phase 4**: 2-3 hours (CLI, config)
- **Phase 5**: 2-3 hours (error handling, logging)
- **Phase 6**: 4-6 hours (testing, documentation)

**Total**: ~18-24 hours of development time

## Success Criteria

1. ✅ All API methods exposed as MCP tools
2. ✅ Tools are discoverable and callable via MCP client
3. ✅ Authentication works via multiple methods
4. ✅ Error handling is comprehensive
5. ✅ Documentation is complete
6. ✅ Tests provide good coverage
7. ✅ No breaking changes to existing API
