"""
MCP (Model Context Protocol) server for TestRail API.

This module provides a FastMCP server that exposes all TestRail API methods
as MCP tools, enabling LLMs to interact with TestRail through a standardized
interface.

The server automatically discovers all public methods from all API modules
and registers them as module-based MCP tools. Each module has one tool that
accepts an 'action' parameter to specify which method to call, reducing the
total number of tools while preserving all functionality.

This allows any MCP-compatible client (Claude Desktop, Cursor, etc.) to
interact with TestRail through the standardized MCP protocol.

Example:
    >>> from testrail_api_module import TestRailAPI
    >>> from testrail_api_module.mcp_server import create_mcp_server
    >>> 
    >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
    >>> mcp = create_mcp_server(api_instance=api)
    >>> mcp.run()  # Start the MCP server
"""
import inspect
import logging
import functools
from typing import Annotated, Any, Callable, Dict, List, Literal, Optional, TYPE_CHECKING

try:
    from pydantic import Field
except ImportError:
    # Pydantic should be available via fastmcp, but handle gracefully
    Field = None  # type: ignore

if TYPE_CHECKING:
    from fastmcp import FastMCP
    from . import TestRailAPI
else:
    try:
        from fastmcp import FastMCP
    except ImportError:
        FastMCP = None  # type: ignore

from .mcp_utils import (
    discover_api_methods,
    generate_tool_name,
    get_method_signature,
    extract_method_docstring
)

logger = logging.getLogger(__name__)


def create_mcp_server(
    api_instance: Optional['TestRailAPI'] = None,
    server_name: str = "TestRail API Server"
) -> 'FastMCP':
    """
    Create and configure a FastMCP server with module-based TestRail API tools.
    
    This function discovers all public methods from all TestRail API modules
    and registers them as module-based MCP tools. Each module has one tool that
    accepts an 'action' parameter to specify which method to call, reducing the
    total number of tools from ~132 to 22 while preserving all functionality.
    
    Tools are named using the format: `testrail_{module}` (e.g., `testrail_cases`).
    Each tool accepts an 'action' parameter (the method name) and 'params' (method parameters).
    
    Args:
        api_instance: Optional TestRailAPI instance. If not provided, will attempt
                     to create from environment variables using `create_api_from_env()`.
        server_name: Name for the MCP server (default: "TestRail API Server").
                     This name appears in MCP client interfaces.
        
    Returns:
        Configured FastMCP server instance with all tools registered and ready
        to run. Call `mcp.run()` to start the server.
        
    Raises:
        ImportError: If fastmcp is not installed. This should not occur as it's
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
        >>> os.environ['TESTRAIL_BASE_URL'] = 'https://test.testrail.io'
        >>> os.environ['TESTRAIL_USERNAME'] = 'user@example.com'
        >>> os.environ['TESTRAIL_API_KEY'] = 'api-key-123'
        >>> mcp = create_mcp_server()  # Creates API from env vars
        >>> mcp.run()
    """
    if FastMCP is None:
        raise ImportError(
            "fastmcp is not installed. This should be included in the base "
            "installation. Please reinstall: pip install testrail-api-module"
        )
    
    # Create or use provided API instance
    if api_instance is None:
        from .mcp_utils import create_api_from_env
        api_instance = create_api_from_env()
    
    # Create FastMCP server
    mcp = FastMCP(server_name)
    
    # Discover all API methods
    methods_by_module = discover_api_methods(api_instance)
    
    # Register one tool per module
    tool_count = 0
    for module_name, methods in methods_by_module.items():
        try:
            tool_wrapper = _create_module_tool(
                api_instance, module_name, methods
            )
            tool_name = f"testrail_{module_name}"
            
            # Register the module tool
            decorated_tool = mcp.tool(name=tool_name)(tool_wrapper)
            tool_count += 1
            # Only log in debug mode to avoid interfering with stdio
            if logger.isEnabledFor(logging.DEBUG):
                method_names = [name for name, _ in methods]
                logger.debug(
                    f"Registered module tool: {tool_name} "
                    f"with {len(methods)} actions: {', '.join(method_names)}"
                )
        except Exception as e:
            # Only log warnings in debug mode
            if logger.isEnabledFor(logging.DEBUG):
                logger.warning(
                    f"Failed to register module tool {module_name}: {e}"
                )
    
    # Only log info in debug mode
    if logger.isEnabledFor(logging.DEBUG):
        logger.info(f"Registered {tool_count} module-based MCP tools from TestRail API")
    
    return mcp


def _create_tool_wrapper(
    api_instance: 'TestRailAPI',
    module_name: str,
    method_name: str,
    method: Callable
) -> Callable:
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
    # Get the module instance
    module_instance = getattr(api_instance, module_name)
    method_func = getattr(module_instance, method_name)
    
    # Get method signature and docstring
    sig = get_method_signature(method)
    docstring = extract_method_docstring(method)
    
    # Create wrapper function
    @functools.wraps(method_func)
    def tool_wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        MCP tool wrapper for TestRail API method.
        
        This tool calls the TestRail API method and returns the result.
        """
        try:
            result = method_func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(
                f"Error calling {module_name}.{method_name}: {e}",
                exc_info=True
            )
            # Re-raise to let FastMCP handle error reporting
            raise
    
    # Set function metadata
    tool_wrapper.__name__ = generate_tool_name(module_name, method_name)
    tool_wrapper.__signature__ = sig
    tool_wrapper.__doc__ = docstring or f"Call {module_name}.{method_name} on TestRail API"
    
    # Copy annotations from method, handling cases where annotations might not exist
    if hasattr(method, '__annotations__'):
        tool_wrapper.__annotations__ = method.__annotations__.copy()
    else:
        tool_wrapper.__annotations__ = {}
    
    # Ensure return annotation is set from signature if not already present
    if 'return' not in tool_wrapper.__annotations__:
        if sig.return_annotation != inspect.Signature.empty:
            tool_wrapper.__annotations__['return'] = sig.return_annotation
    
    return tool_wrapper


def _create_module_tool(
    api_instance: 'TestRailAPI',
    module_name: str,
    methods: List[tuple[str, Callable]]
) -> Callable:
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
    # Get the module instance
    module_instance = getattr(api_instance, module_name)
    
    # Extract method names and create action list for Literal type
    method_names = [name for name, _ in methods]
    
    # Create a mapping of method names to method functions
    method_map = {name: getattr(module_instance, name) for name, _ in methods}
    
    # Build description with available actions
    action_descriptions = []
    for method_name, method in methods:
        docstring = extract_method_docstring(method)
        action_descriptions.append(f"- {method_name}: {docstring}")
    
    description = (
        f"TestRail {module_name} API operations. "
        f"Available actions: {', '.join(method_names)}. "
        f"Each action accepts parameters as specified in the TestRail API documentation."
    )
    
    # Create tool function with type hints - FastMCP will infer schema from types and docstring
    # Create a simple docstring that will be read by FastMCP
    simple_docstring = f"Execute a TestRail API action for the {module_name} module"
    
    def module_tool(
        action: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        if params is None:
            params = {}
        
        # Validate action
        if action not in method_map:
            available = ', '.join(method_names)
            raise ValueError(
                f"Invalid action '{action}' for {module_name} module. "
                f"Available actions: {available}"
            )
        
        # Get the method function
        method_func = method_map[action]
        
        try:
            # Call the method with the provided parameters
            result = method_func(**params)
            return result
        except TypeError as e:
            # If there's a type error, it might be due to missing required parameters
            # Try to extract required parameters from the method signature
            try:
                sig = inspect.signature(method_func)
                required_params = [
                    name for name, param in sig.parameters.items()
                    if param.default == inspect.Parameter.empty and name != 'self'
                ]
                if required_params:
                    error_msg = (
                        f"Invalid parameters for {module_name}.{action}. "
                        f"Missing required parameter(s): {', '.join(required_params)}. "
                        f"Error: {e}"
                    )
                else:
                    error_msg = (
                        f"Invalid parameters for {module_name}.{action}: {e}. "
                        f"Check the method signature for required parameters."
                    )
            except Exception:
                error_msg = (
                    f"Invalid parameters for {module_name}.{action}: {e}. "
                    f"Check the method signature for required parameters."
                )
            
            logger.error(
                f"Error calling {module_name}.{action} with params {params}: {e}",
                exc_info=True
            )
            raise ValueError(error_msg) from e
        except Exception as e:
            logger.error(
                f"Error calling {module_name}.{action}: {e}",
                exc_info=True
            )
            # Re-raise to let FastMCP handle error reporting
            raise
    
    # Set function metadata and docstring BEFORE FastMCP reads it
    # FastMCP reads the docstring when the decorator is applied, so set it now
    module_tool.__name__ = f"testrail_{module_name}"
    module_tool.__doc__ = simple_docstring
    
    # Ensure return annotation is set
    if not hasattr(module_tool, '__annotations__'):
        module_tool.__annotations__ = {}
    if 'return' not in module_tool.__annotations__:
        module_tool.__annotations__['return'] = Any
    
    return module_tool

