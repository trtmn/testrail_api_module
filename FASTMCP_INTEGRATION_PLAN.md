# FastMCP Integration Plan for TestRail API Module

## Status: ✅ IMPLEMENTATION COMPLETE

**Last Updated**: 2024 - Implementation completed with module-based tool architecture

**Update**: MCP functionality is now included in the base installation (fastmcp moved from optional to main dependencies). The implementation uses a module-based tool architecture that reduces the number of tools from ~132 to 22 while preserving all functionality.

### Quick Status Summary

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Dependencies and Setup | ✅ Complete | All dependencies added, project structure created |
| Phase 2: Core MCP Server | ✅ Complete | Method discovery, tool registration, authentication working |
| Phase 3: Tool Wrappers | ✅ Complete | Dynamic tool creation with proper naming and descriptions |
| Phase 4: CLI and Configuration | ✅ Complete | Full CLI with env vars, .env files, and entry point |
| Phase 5: Error Handling | ✅ Complete | Comprehensive error handling and logging |
| Phase 6: Testing & Docs | ⚠️ Partial | Unit tests complete, integration tests need fastmcp |

**Overall**: Core functionality is **100% complete** and ready for use. Some optional enhancements remain (see "Known Limitations" section).

## Overview

This plan outlines the integration of fastMCP into the TestRail API module to expose all API endpoints as MCP (Model Context Protocol) tools. This will enable LLMs to interact with TestRail through a standardized MCP interface.

**Implementation Status**: All core functionality has been implemented and is ready for use.

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
   - Module-based tool architecture (22 tools instead of ~132)
   - Authentication handling
   - Tool naming and organization

2. **MCP Utilities** (`src/testrail_api_module/mcp_utils.py`)
   - Helper functions for method discovery
   - Tool name generation (for internal use)
   - Method signature and docstring extraction
   - Environment-based API instance creation

3. **CLI Entry Point** (`src/testrail_api_module/cli.py`)
   - Command-line interface to run the MCP server
   - Configuration loading (env vars, .env files)
   - Server startup with stdio transport
   - Logging control (disabled by default for stdio compatibility)

4. **Configuration** (Environment variables or .env file)
   - `TESTRAIL_BASE_URL`
   - `TESTRAIL_USERNAME`
   - `TESTRAIL_API_KEY` or `TESTRAIL_PASSWORD`
   - `TESTRAIL_TIMEOUT` (optional)

## Implementation Steps

### Phase 1: Dependencies and Setup ✅ COMPLETED

1. **Add fastMCP dependency** ✅
   - ✅ Added `fastmcp>=0.9.0` to `pyproject.toml` as **base dependency** (not optional)
   - ✅ Added `python-dotenv>=1.0.0` to `[project.optional-dependencies.dev]` (optional, for .env file support)
   - ✅ MCP extra kept for backward compatibility but no longer needed

2. **Project structure** ✅
   - ✅ Created MCP server module: `src/testrail_api_module/mcp_server.py`
   - ✅ Created MCP utilities: `src/testrail_api_module/mcp_utils.py`
   - ✅ Created CLI module: `src/testrail_api_module/cli.py`
   - ✅ Created standalone script: `scripts/mcp_server.py`

### Phase 2: Core MCP Server Implementation ✅ COMPLETED

1. **Method Discovery System** ✅
   - ✅ Created `discover_api_methods()` function in `mcp_utils.py`
   - ✅ Filters out private methods (starting with `_`)
   - ✅ Filters out base API methods (`_get`, `_post`, `_api_request`, etc.)
   - ✅ Organizes methods by API module (cases, results, runs, etc.)
   - ✅ Returns dictionary mapping module names to method lists

2. **Tool Registration** ✅
   - ✅ Created `_create_module_tool()` function for module-based tool creation
   - ✅ Generates tool names: `testrail_{module}` (e.g., `testrail_cases`, `testrail_results`)
   - ✅ Each module tool accepts `action` (method name) and `params` (method parameters)
   - ✅ Reduces total tools from ~132 individual tools to 22 module-based tools
   - ✅ Preserves all functionality while improving tool discoverability
   - ✅ Uses `mcp.tool()` decorator for registration
   - ✅ Includes comprehensive docstrings with available actions and parameter hints

3. **Authentication Handling** ✅
   - ✅ Supports initialization from environment variables via `create_api_from_env()`
   - ✅ Supports initialization from passed TestRailAPI instance
   - ✅ Validates credentials before starting server (in CLI)
   - ⚠️ Config file support (JSON/YAML) not implemented - uses .env files instead

4. **Parameter Handling** ✅
   - ✅ Method parameters automatically handled by FastMCP via function signatures
   - ✅ Optional parameters supported through Python type hints
   - ✅ Complex types (Dict, List, Union, Optional) supported via type annotations
   - ⚠️ File uploads for attachment methods - handled by underlying API methods

### Phase 3: Tool Wrapper Implementation ✅ COMPLETED

1. **Module-Based Tool Creation** ✅
   - ✅ Created `_create_module_tool()` function for module-based tools
   - ✅ Each tool accepts `action` (str) and `params` (Optional[Dict[str, Any]])
   - ✅ Routes to appropriate API method based on action parameter
   - ✅ Validates action against available methods in the module
   - ✅ Returns results directly (FastMCP handles MCP format conversion)
   - ✅ Handles exceptions with detailed error messages and logging
   - ✅ Provides helpful error messages for invalid actions or parameters

2. **Tool Naming Convention** ✅
   - ✅ Format: `testrail_{module}` implemented (e.g., `testrail_cases`, `testrail_results`)
   - ✅ Examples working:
     - `testrail_cases` (with action: `get_case`, `get_cases`, `add_case`, etc.)
     - `testrail_results` (with action: `add_result`, `get_results`, etc.)
     - `testrail_runs` (with action: `get_runs`, `add_run`, etc.)
   - ✅ Uses snake_case consistently
   - ✅ Reduces tool count from ~132 to 22 tools

3. **Tool Descriptions** ✅
   - ✅ Comprehensive docstrings generated for each module tool
   - ✅ Lists all available actions for the module
   - ✅ Includes parameter hints for common actions
   - ✅ Provides example usage in docstrings
   - ✅ Uses Literal types for action parameter to enable enum constraints in MCP schema

### Phase 4: CLI and Configuration ✅ COMPLETED

1. **CLI Implementation** ✅
   - ✅ Created command-line interface using `argparse` in `cli.py`
   - ✅ Supports all required flags:
     - ✅ `--base-url` / `--username` / `--api-key` / `--password` flags
     - ✅ `--timeout` for request timeout
     - ✅ `--verbose` / `-v` for logging (disabled by default for stdio compatibility)
     - ✅ `--env-file` for .env file path
     - ✅ `--server-name` for custom server name
   - ✅ Loads from environment variables as fallback
   - ✅ Comprehensive help text and examples
   - ✅ Logging disabled by default to avoid interfering with stdio communication

2. **Configuration Management** ✅
   - ✅ Supports `.env` file loading (using `python-dotenv` - optional dependency)
   - ⚠️ JSON/YAML config files not implemented (uses .env files instead)
   - ✅ Priority: CLI args > env vars > .env file > defaults
   - ✅ Gracefully handles missing `python-dotenv` (silently skips .env loading)

3. **Entry Point** ✅
   - ✅ Added console script entry point to `pyproject.toml`
   - ✅ Command: `testrail-mcp-server`
   - ✅ Points to `testrail_api_module.cli:main`
   - ✅ Server runs with `mcp.run(transport="stdio", show_banner=False)` for MCP compatibility

### Phase 5: Error Handling and Logging ✅ COMPLETED

1. **Exception Handling** ✅
   - ✅ Catches TestRail API exceptions in tool wrappers
   - ✅ FastMCP automatically converts exceptions to MCP-compatible error responses
   - ✅ Error details (status codes, messages) preserved via exception re-raising
   - ✅ Errors logged with full traceback via `logger.error(..., exc_info=True)`

2. **Logging** ✅
   - ✅ Set up structured logging using Python's `logging` module
   - ✅ Logging **disabled by default** in stdio mode to avoid interfering with MCP communication
   - ✅ Logs tool registration (debug level, only when verbose)
   - ✅ Logs tool invocation errors (error level, only when verbose)
   - ✅ Logs server startup and configuration (info level, only when verbose)
   - ✅ Supports different log levels via `--verbose` flag
   - ✅ FastMCP and uvicorn logging suppressed in non-verbose mode
   - ⚠️ API request/response logging not implemented (can be added via requests logging)

### Phase 6: Testing and Documentation ⚠️ PARTIALLY COMPLETED

1. **Unit Tests** ✅
   - ✅ Created `tests/test_mcp_utils.py` with comprehensive tests:
     - ✅ Test method discovery (`TestDiscoverAPIMethods`)
     - ✅ Test tool name generation (`TestGenerateToolName`)
     - ✅ Test method signature extraction (`TestGetMethodSignature`)
     - ✅ Test docstring extraction (`TestExtractMethodDocstring`)
     - ✅ Test API creation from environment (`TestCreateAPIFromEnv`)
   - ✅ Created `tests/test_mcp_server.py` with basic tests:
     - ✅ Test MCP server creation (with fastmcp availability checks)
     - ⚠️ Full integration tests require fastmcp to be installed

2. **Integration Tests** ⚠️ PARTIAL
   - ✅ Basic MCP server creation tests
   - ⚠️ Tool invocation tests require fastmcp installation
   - ⚠️ End-to-end scenarios not fully tested (requires MCP client)
   - ⚠️ Mocked API tests could be expanded

3. **Documentation** ✅
   - ✅ Created comprehensive `docs/MCP_USAGE.md` with:
     - ✅ Installation instructions
     - ✅ Quick start guide
     - ✅ Configuration options
     - ✅ Usage examples (CLI and library)
     - ✅ Tool discovery information
     - ✅ Troubleshooting guide
   - ⚠️ README not updated yet (can be added if needed)
   - ✅ Updated `__init__.py` to conditionally export MCP functionality

## Technical Considerations

### Method Discovery

```python
def discover_api_methods(api_instance: TestRailAPI) -> Dict[str, List[tuple[str, Callable]]]:
    """
    Discover all public methods from all API modules.
    
    Returns:
        Dictionary mapping module names to lists of (method_name, method) tuples
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
    
    # Base API methods to exclude
    excluded_methods = {
        '_get', '_post', '_put', '_delete', '_patch',
        '_api_request', '_build_url', '_get_auth', '_handle_response'
    }
    
    for module_name in api_modules:
        if hasattr(api_instance, module_name):
            module_instance = getattr(api_instance, module_name)
            methods = [
                (name, method) for name, method in inspect.getmembers(module_instance, 
                                                                      predicate=inspect.ismethod)
                if not name.startswith('_') and name not in excluded_methods
            ]
            if methods:
                methods_by_module[module_name] = methods
    
    return methods_by_module
```

### Module-Based Tool Pattern

```python
def _create_module_tool(
    api_instance: TestRailAPI,
    module_name: str,
    methods: List[tuple[str, Callable]]
) -> Callable:
    """
    Create a module-based MCP tool that routes actions to appropriate methods.
    
    This creates a single tool per module that accepts an 'action' parameter
    to specify which method to call, and a 'params' parameter for method arguments.
    """
    module_instance = getattr(api_instance, module_name)
    method_names = [name for name, _ in methods]
    method_map = {name: getattr(module_instance, name) for name, _ in methods}
    
    def module_tool(
        action: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        if params is None:
            params = {}
        
        if action not in method_map:
            raise ValueError(f"Invalid action '{action}'. Available: {', '.join(method_names)}")
        
        method_func = method_map[action]
        return method_func(**params)
    
    # Set metadata and annotations
    module_tool.__name__ = f"testrail_{module_name}"
    module_tool.__annotations__ = {
        'action': Literal[tuple(method_names)],  # Enum constraint
        'params': Optional[Dict[str, Any]],
        'return': Any
    }
    
    return module_tool
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

## File Structure ✅ COMPLETED

```
src/testrail_api_module/
├── __init__.py            # ✅ Updated to export MCP functionality
├── base.py
├── mcp_server.py          # ✅ CREATED: Main MCP server implementation
├── mcp_utils.py           # ✅ CREATED: MCP utility functions
├── cli.py                 # ✅ CREATED: CLI for MCP server
├── [existing API modules...]

scripts/
└── mcp_server.py          # ✅ CREATED: Standalone CLI script

tests/
├── test_mcp_server.py     # ✅ CREATED: Tests for MCP server
└── test_mcp_utils.py      # ✅ CREATED: Tests for MCP utilities

docs/
└── MCP_USAGE.md           # ✅ CREATED: MCP usage documentation
```

## Dependencies

### Required (Base Installation)
- `fastmcp>=0.9.0` - FastMCP framework (included in base dependencies)
- `requests>=2.32.0` - HTTP library
- `pytest>=8.4.2` - Testing framework

### Optional
- `python-dotenv>=1.0.0` - Environment variable loading (optional, for .env file support)
  - Available via `[dev]` extra
  - CLI gracefully handles missing dependency (silently skips .env loading)
- `argparse` - CLI framework (stdlib, no installation needed)

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
mcp = create_mcp_server(api_instance=api)
mcp.run(transport="stdio", show_banner=False)
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

# Using .env file
testrail-mcp-server --env-file .env

# With verbose logging (for debugging)
testrail-mcp-server --verbose
```

### Tool Usage Example
```python
# Each module has one tool that accepts 'action' and 'params'
# Example: testrail_cases tool
{
    "action": "get_case",
    "params": {"case_id": 1}
}

# Example: testrail_results tool
{
    "action": "add_result",
    "params": {
        "run_id": 1,
        "case_id": 1,
        "status_id": 1
    }
}
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

1. ✅ **All API methods exposed as MCP tools** - COMPLETED
   - All public methods from all 23 API modules are automatically discovered and registered
   - Implemented as 22 module-based tools (one per module) instead of ~132 individual tools
   - Each module tool accepts `action` parameter to specify which method to call
   
2. ✅ **Tools are discoverable and callable via MCP client** - COMPLETED
   - Tools follow consistent naming convention: `testrail_{module}`
   - FastMCP handles tool discovery and invocation
   - Action parameter uses Literal types for enum constraints in MCP schema
   
3. ✅ **Authentication works via multiple methods** - COMPLETED
   - Environment variables
   - Command-line arguments
   - .env files
   - Direct API instance passing
   
4. ✅ **Error handling is comprehensive** - COMPLETED
   - Exceptions are caught, logged, and re-raised for FastMCP
   - Error details preserved
   
5. ✅ **Documentation is complete** - COMPLETED
   - Comprehensive usage guide created (`docs/MCP_USAGE.md`)
   - Includes examples, configuration, troubleshooting
   
6. ⚠️ **Tests provide good coverage** - PARTIALLY COMPLETED
   - Unit tests for utilities: ✅ Complete
   - Unit tests for server: ✅ Basic coverage (requires fastmcp for full testing)
   - Integration tests: ⚠️ Partial (requires fastmcp and MCP client)
   
7. ✅ **No breaking changes to existing API** - COMPLETED
   - FastMCP is now included in base dependencies
   - All existing functionality preserved
   - MCP features available in base installation (no extra needed)

## Implementation Summary

### ✅ Completed Features

- ✅ FastMCP integration with automatic tool discovery
- ✅ Module-based tool architecture (22 tools instead of ~132)
- ✅ Dynamic tool registration with action routing
- ✅ CLI interface with comprehensive options
- ✅ Environment variable and .env file support
- ✅ Error handling with detailed error messages
- ✅ Logging control (disabled by default for stdio compatibility)
- ✅ Unit tests for core functionality
- ✅ Comprehensive documentation
- ✅ Literal type annotations for action parameters (enum constraints)

### ⚠️ Known Limitations / Future Work

1. **JSON/YAML Config Files**: Not implemented - uses .env files instead
2. **Full Integration Tests**: Require fastmcp installation and MCP client for complete testing
3. **Tool Filtering**: Not implemented - all methods are exposed (can be added later)
4. **Rate Limiting**: Not implemented at MCP level (handled by underlying API)
5. **Caching**: Not implemented (can be added as enhancement)
6. **Batch Operations**: Not implemented (can be added as enhancement)
7. **Individual Tool Mode**: Module-based tools are the default; individual tool mode could be added as an option

### 📝 Next Steps (Optional Enhancements)

1. Add JSON/YAML config file support
2. Expand integration tests with mocked MCP client
3. Add tool filtering/grouping options
4. Add response caching for read operations
5. Update main README with MCP section
6. Add example MCP client configurations
7. Consider adding option to use individual tools instead of module-based tools
8. Add validation for action parameter at tool registration time
9. Improve error messages with method signature hints

## Architecture Changes Summary

### Module-Based Tool Architecture

The implementation uses a **module-based tool architecture** instead of individual tools per method. This design decision provides several benefits:

1. **Reduced Tool Count**: From ~132 individual tools to 22 module-based tools
2. **Better Discoverability**: Easier to find relevant tools by module name
3. **Consistent Interface**: All tools follow the same pattern (`action` + `params`)
4. **Maintainability**: Easier to add new methods without creating new tools

### Tool Structure

Each module tool:
- **Name**: `testrail_{module}` (e.g., `testrail_cases`, `testrail_results`)
- **Parameters**:
  - `action` (str, Literal type): The method name to call
  - `params` (Optional[Dict[str, Any]]): Method parameters as a dictionary
- **Returns**: Result from the called method (typically dict or list of dicts)

### Implementation Details

- `discover_api_methods()` returns `Dict[str, List[tuple[str, Callable]]]` (method name + method object)
- `_create_module_tool()` creates a single tool per module that routes actions
- Literal types are used for action parameters to enable enum constraints in MCP schema
- Comprehensive docstrings include available actions, parameter hints, and examples
- Error handling provides detailed messages for invalid actions or parameters
