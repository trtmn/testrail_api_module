from . import TestRailAPI as TestRailAPI
from .mcp_utils import discover_api_methods as discover_api_methods, extract_method_docstring as extract_method_docstring, generate_tool_name as generate_tool_name, get_method_signature as get_method_signature
from typing import Any, Optional, Dict, List
from fastmcp import FastMCP
from pydantic_core import core_schema as core_schema
from typing import Any, Callable

logger: Any

def _create_literal_type(values: tuple[str, ...]) -> Any:
    """
    Create a Literal type dynamically from a tuple of string values.
    
    This helper function constructs a Literal type annotation that can be used
    for type hints, which helps FastMCP/Pydantic generate proper JSON schemas
    with enum constraints.
    
    Args:
        values: Tuple of string values to create Literal type from.
        
    Returns:
        Literal type annotation that can be used in __annotations__.
    """
def create_mcp_server(api_instance: TestRailAPI | None = None, server_name: str = 'TestRail API Server') -> FastMCP:
    '''
    Create and configure a FastMCP server with module-based TestRail API tools.
    
    This function discovers all public methods from all TestRail API modules
    and registers them as module-based MCP tools. Each module has one tool that
    accepts an \'action\' parameter to specify which method to call, reducing the
    total number of tools from ~132 to 22 while preserving all functionality.
    
    Tools are named using the format: `testrail_{module}` (e.g., `testrail_cases`).
    Each tool accepts an \'action\' parameter (the method name) and \'params\' (method parameters).
    
    Args:
        api_instance: Optional TestRailAPI instance. If not provided, will attempt
                     to create from environment variables using `create_api_from_env()`.
        server_name: Name for the MCP server (default: "TestRail API Server").
                     This name appears in MCP client interfaces.
        
    Returns:
        Configured FastMCP server instance with all tools registered and ready
        to run. Call `mcp.run()` to start the server.
        
    Raises:
        ImportError: If fastmcp is not installed. This should not occur as it\'s
                    included in the base installation. Reinstall with:
                    `pip install testrail-api-module`
        ValueError: If api_instance is not provided and cannot be created from
                    environment variables (missing required env vars).
        
    Example:
        >>> from testrail_api_module import TestRailAPI
        >>> from testrail_api_module.mcp_server import create_mcp_server
        >>> 
        >>> # Using provided API instance
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> mcp = create_mcp_server(api_instance=api)
        >>> mcp.run()
        >>> 
        >>> # Using environment variables
        >>> import os
        >>> os.environ[\'TESTRAIL_BASE_URL\'] = \'https://test.testrail.io\'
        >>> os.environ[\'TESTRAIL_USERNAME\'] = \'user@example.com\'
        >>> os.environ[\'TESTRAIL_API_KEY\'] = \'api-key-123\'
        >>> mcp = create_mcp_server()  # Creates API from env vars
        >>> mcp.run()
    '''
def _create_tool_wrapper(api_instance: TestRailAPI, module_name: str, method_name: str, method: Callable) -> Callable:
    """
    Create an MCP tool wrapper for an API method.
    
    This internal function creates a wrapper function that can be registered
    as an MCP tool. The wrapper preserves the original method's signature
    (without 'self'), docstring, and type annotations, while handling errors
    appropriately for MCP.
    
    Args:
        api_instance: The TestRailAPI instance containing the method.
        module_name: Name of the API module (e.g., 'cases', 'results').
        method_name: Name of the method (e.g., 'get_case', 'add_result').
        method: The method object to wrap (bound method from API module).
        
    Returns:
        Wrapper function that can be registered as an MCP tool. The function:
        - Has the name `testrail_{module_name}_{method_name}`
        - Preserves the original method's signature (without 'self')
        - Uses the original method's docstring as description
        - Calls the original method and returns its result
        - Logs and re-raises exceptions for proper error handling
        
    Note:
        This is an internal function used by `create_mcp_server()`. Users
        should not need to call this directly.
    """
def _separate_custom_fields_for_case_action(action: str, params: dict[str, Any]) -> dict[str, Any]:
    '''
    Separate custom fields from standard fields for add_case and update_case actions.
    
    This function supports both input styles:
    1. Custom fields as top-level: custom_automation_type="7"
    2. Custom fields nested: custom_fields={"custom_automation_type": "7"}
    
    Args:
        action: The action name (\'add_case\' or \'update_case\').
        params: Dictionary of parameters that may contain custom fields at top level.
        
    Returns:
        Dictionary with custom fields properly nested under \'custom_fields\' key.
    '''
def _create_module_tool(api_instance: TestRailAPI, module_name: str, methods: list[tuple[str, Callable]]) -> Callable:
    """
    Create a module-based MCP tool that routes actions to appropriate methods.
    
    This function creates a single tool per module that accepts an 'action' parameter
    to specify which method to call, and a 'params' parameter for method arguments.
    This reduces the total number of tools while preserving all functionality.
    
    Args:
        api_instance: The TestRailAPI instance containing the methods.
        module_name: Name of the API module (e.g., 'cases', 'results').
        methods: List of (method_name, method) tuples for this module.
        
    Returns:
        Tool function that can be registered as an MCP tool. The function:
        - Has the name `testrail_{module_name}`
        - Accepts 'action' (method name) and 'params' (method parameters)
        - Routes to the appropriate method and returns its result
        - Logs and re-raises exceptions for proper error handling
    """
