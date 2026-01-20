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
import ast
import inspect
import json
import logging
import functools
from typing import Annotated, Any, Callable, Dict, List, Literal, Optional, Union, TYPE_CHECKING

try:
    from pydantic import Field, field_validator, Json
    from pydantic_core import core_schema
except ImportError:
    # Pydantic should be available via fastmcp, but handle gracefully
    Field = None  # type: ignore
    field_validator = None  # type: ignore
    Json = None  # type: ignore

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
    if not values:
        return str
    
    if len(values) == 1:
        return Literal[values[0]]  # type: ignore
    
    # For multiple values, Literal needs each value as a separate argument
    # We construct it by building the type annotation string and evaluating it
    # This is safe because we control the input (method names from our API)
    try:
        # Build the Literal type annotation: Literal['val1', 'val2', ...]
        literal_args = ', '.join(repr(v) for v in values)
        # Use eval in a controlled context - only Literal is available
        # This is safe because values come from our own API method names
        namespace = {'Literal': Literal}
        return eval(f'Literal[{literal_args}]', namespace)  # type: ignore
    except (TypeError, AttributeError, SyntaxError):
        # Fallback: use str type - FastMCP will still work, just without enum constraint
        return str


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
    
    logger.debug(f"Creating MCP server: {server_name}")
    
    # Create or use provided API instance
    if api_instance is None:
        logger.debug("No API instance provided, creating from environment")
        from .mcp_utils import create_api_from_env
        api_instance = create_api_from_env()
    else:
        logger.debug("Using provided API instance")
    
    # Create FastMCP server
    logger.debug(f"Initializing FastMCP server: {server_name}")
    mcp = FastMCP(server_name)
    
    # Discover all API methods
    logger.debug("Discovering API methods")
    methods_by_module = discover_api_methods(api_instance)
    logger.debug(f"Found {len(methods_by_module)} modules to register")
    
    # Register one tool per module
    tool_count = 0
    registered_tools = []
    failed_tools = []
    
    for module_name, methods in methods_by_module.items():
        try:
            tool_wrapper = _create_module_tool(
                api_instance, module_name, methods
            )
            tool_name = f"testrail_{module_name}"
            
            # Register the module tool
            decorated_tool = mcp.tool(name=tool_name)(tool_wrapper)
            tool_count += 1
            
            method_names = [name for name, _ in methods]
            registered_tools.append(f"{tool_name} ({len(methods)} actions)")
            
            # Only log individual tool registration at DEBUG level
            logger.debug(
                f"Registered tool: {tool_name} with {len(methods)} actions: "
                f"{', '.join(method_names)}"
            )
        except Exception as e:
            failed_tools.append(module_name)
            logger.warning(
                f"Failed to register module tool {module_name}: {e}",
                exc_info=True
            )
    
    # Log summary at INFO level
    if registered_tools:
        logger.info(
            f"Registered {tool_count} module-based MCP tools: "
            f"{', '.join(registered_tools)}"
        )
    if failed_tools:
        logger.warning(
            f"Failed to register {len(failed_tools)} tools: "
            f"{', '.join(failed_tools)}"
        )
    
    logger.debug("MCP server creation complete")
    
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


def _separate_custom_fields_for_case_action(
    action: str,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Separate custom fields from standard fields for add_case and update_case actions.
    
    This function supports both input styles:
    1. Custom fields as top-level: custom_automation_type="7"
    2. Custom fields nested: custom_fields={"custom_automation_type": "7"}
    
    Args:
        action: The action name ('add_case' or 'update_case').
        params: Dictionary of parameters that may contain custom fields at top level.
        
    Returns:
        Dictionary with custom fields properly nested under 'custom_fields' key.
    """
    # Define which parameters are standard (non-custom) fields
    if action == 'add_case':
        STANDARD_FIELDS = {
            'section_id', 'title', 'template_id', 'type_id',
            'priority_id', 'estimate', 'milestone_id', 'refs',
            'description', 'preconditions', 'postconditions',
            'validate_required', 'validate_only'
        }
    elif action == 'update_case':
        STANDARD_FIELDS = {
            'case_id', 'title', 'template_id', 'type_id',
            'priority_id', 'estimate', 'milestone_id', 'refs',
            'description', 'preconditions', 'postconditions'
        }
    else:
        # Should not happen, but return params as-is
        return params
    
    # Check if user already provided custom_fields as nested dict
    if 'custom_fields' in params:
        custom_fields_value = params.get('custom_fields')
        if isinstance(custom_fields_value, dict):
            # User already structured it correctly, but check for top-level custom fields too
            # Merge any top-level custom fields into the nested dict
            top_level_custom = {
                k: v for k, v in params.items()
                if k.startswith('custom_') and k != 'custom_fields' and k not in STANDARD_FIELDS
            }
            if top_level_custom:
                # Merge top-level custom fields into nested custom_fields
                params['custom_fields'].update(top_level_custom)
                # Remove top-level custom fields
                for key in top_level_custom:
                    params.pop(key)
                logger.debug(
                    f"Merged top-level custom fields into nested custom_fields: {list(top_level_custom.keys())}"
                )
            return params
        elif custom_fields_value is None:
            # custom_fields is explicitly set to None - treat as if it doesn't exist
            # and process top-level custom fields normally
            pass
        else:
            # custom_fields has an unexpected type - log and process normally
            logger.warning(
                f"custom_fields parameter has unexpected type {type(custom_fields_value)}, "
                f"processing as if it doesn't exist"
            )
    
    # Otherwise, restructure top-level custom fields
    standard_params = {}
    custom_fields = {}
    
    for key, value in params.items():
        if key in STANDARD_FIELDS:
            standard_params[key] = value
        elif key.startswith('custom_') and key != 'custom_fields':
            # This is a top-level custom field - move it to custom_fields dict
            custom_fields[key] = value
        elif key == 'custom_fields':
            # Should not happen here (checked above), but handle gracefully
            if isinstance(value, dict):
                custom_fields.update(value)
        else:
            # Unknown parameter - pass through (might be a new standard field)
            standard_params[key] = value
            logger.debug(f"Unknown parameter '{key}' passed through as standard field")
    
    # Add custom_fields to standard params if any exist
    if custom_fields:
        standard_params['custom_fields'] = custom_fields
        logger.debug(
            f"Separated {len(custom_fields)} custom field(s) into nested custom_fields: "
            f"{list(custom_fields.keys())}"
        )
    
    return standard_params


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
    # Build a comprehensive docstring with available actions and parameter info
    actions_list = ', '.join(method_names)
    
    # Build parameter hints for common action patterns
    param_hints = []
    for name in method_names:
        method = method_map.get(name)
        if method:
            try:
                sig = inspect.signature(method)
                required_params = [
                    pname for pname, param in sig.parameters.items()
                    if param.default == inspect.Parameter.empty and pname != 'self'
                ]
                if required_params:
                    # Create a hint for this action
                    hint = f"{name}: requires {', '.join(required_params)}"
                    param_hints.append(hint)
            except:
                pass
    
    docstring_parts = [
        f"Execute a TestRail API action for the {module_name} module.",
        "",
        "Args:",
        f"    action: The method name to call. Available actions: {actions_list}",
        "    params: Dictionary of parameters to pass to the method. Can be a dict, "
        "JSON string, or Python dict literal. Required and optional parameters "
        "depend on the action.",
        "",
    ]
    
    # Add special documentation for cases module about custom fields
    if module_name == 'cases' and ('add_case' in method_names or 'update_case' in method_names):
        docstring_parts.extend([
            "IMPORTANT - Custom Fields Usage:",
            "    For add_case and update_case actions, custom fields can be provided in two ways:",
            "",
            "    1. Nested format (RECOMMENDED):",
            "       {",
            '           "section_id": 123,',
            '           "title": "My Test",',
            '           "custom_fields": {',
            '               "custom_automation_type": "7",',
            '               "custom_steps": "Step 1..."',
            "           }",
            "       }",
            "",
            "    2. Top-level format (also supported):",
            "       {",
            '           "section_id": 123,',
            '           "title": "My Test",',
            '           "custom_automation_type": "7",',
            '           "custom_steps": "Step 1..."',
            "       }",
            "",
            "    Both formats are automatically converted to the nested format. Use",
            "    get_case_fields() action to see required fields and their data types.",
            "",
        ])
    
    # Add parameter hints if we have any
    if param_hints:
        docstring_parts.extend([
            "Common parameter requirements:",
        ])
        # Show first 5 to keep it concise
        for hint in param_hints[:5]:
            docstring_parts.append(f"    - {hint}")
        if len(param_hints) > 5:
            docstring_parts.append(f"    - ... and {len(param_hints) - 5} more")
        docstring_parts.append("")
    
    docstring_parts.extend([
        "Returns:",
        "    The result from the called method, typically a dict or list of dicts.",
    ])
    
    # Add example for a common get_* action
    example_action = None
    for name in method_names:
        if name.startswith('get_') and name not in ['get_case_fields', 'get_result_fields']:
            example_action = name
            break
    
    if example_action:
        example_method = method_map.get(example_action)
        if example_method:
            try:
                sig = inspect.signature(example_method)
                required_params = [
                    name for name, param in sig.parameters.items()
                    if param.default == inspect.Parameter.empty and name != 'self'
                ]
                if required_params:
                    example_value = 1 if 'id' in required_params[0] else 'example'
                    example_params = {required_params[0]: example_value}
                    docstring_parts.extend([
                        "",
                        "Example:",
                        f'    action="{example_action}", params={example_params}',
                    ])
            except:
                pass
    
    enhanced_docstring = '\n'.join(docstring_parts)
    
    def module_tool(
        action: str,
        params: Union[Dict[str, Any], str, None] = None
    ) -> Any:
        if params is None:
            params = {}
        
        # Handle case where params is received as a string (JSON or Python dict syntax)
        # This can happen when FastMCP receives parameters from MCP protocol
        # NOTE: The MCP client should send Dict parameters as JSON objects, not strings.
        # If we receive a string, it's likely a serialization issue on the client side.
        if isinstance(params, str):
            # Log the raw string for debugging
            logger.debug(f"Received params as string (first 200 chars): {params[:200]}")
            
            # Try to clean up common serialization issues
            cleaned_params = params.strip()
            
            # Try to fix malformed Python dict strings (missing commas, etc.)
            # This is a workaround for MCP client serialization bugs
            if cleaned_params.startswith('{') and not cleaned_params.startswith('{'):
                # Might have extra characters at the start
                pass
            
            # Try to fix missing commas in Python dict syntax
            # Pattern: 'key': value 'key2' should be 'key': value, 'key2'
            import re
            # Fix missing commas between dictionary items
            # Match pattern like: 'key': value 'key2' (missing comma)
            fixed_params = re.sub(r"('[\w_]+'):\s*([^,}]+)\s+('[\w_]+')", r"\1: \2, \3", cleaned_params)
            if fixed_params != cleaned_params:
                logger.debug(f"Fixed missing commas in params string")
                cleaned_params = fixed_params
            
            try:
                # First try JSON parsing (standard format)
                params = json.loads(cleaned_params)
                logger.debug(f"Parsed params from JSON string: {params}")
            except (json.JSONDecodeError, TypeError):
                # Fallback to Python literal evaluation (handles Python dict syntax)
                try:
                    params = ast.literal_eval(cleaned_params)
                    logger.debug(f"Parsed params from Python literal: {params}")
                except (ValueError, SyntaxError) as e:
                    # Try to fix common issues: remove leading/trailing braces if malformed
                    if cleaned_params.startswith('{}') and not cleaned_params.startswith('{}"'):
                        # Remove the leading {}
                        cleaned_params = cleaned_params[2:].strip()
                        try:
                            params = ast.literal_eval(cleaned_params)
                            logger.debug(f"Parsed params after removing leading braces: {params}")
                        except (ValueError, SyntaxError):
                            pass
                    
                    if not isinstance(params, dict):
                        error_msg = (
                            f"Invalid params format for {module_name}.{action}. "
                            f"Expected a dictionary object, not a string. "
                            f"The MCP client should send Dict parameters as JSON objects, not strings. "
                            f"Received malformed string (first 200 chars): {params[:200] if isinstance(params, str) else str(params)[:200]}. "
                            f"Error: {e}"
                        )
                        logger.error(error_msg)
                        raise ValueError(error_msg) from e
        
        # Ensure params is a dictionary after parsing
        if not isinstance(params, dict):
            error_msg = (
                f"Invalid params type for {module_name}.{action}. "
                f"Expected a dictionary, got: {type(params).__name__}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.debug(f"MCP tool called: {module_name}.{action}")
        logger.debug(f"Parameters: {params}")
        
        # Validate action
        if action not in method_map:
            available = ', '.join(method_names)
            error_msg = (
                f"Invalid action '{action}' for {module_name} module. "
                f"Available actions: {available}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Get the method function
        method_func = method_map[action]
        logger.debug(f"Calling method: {module_name}.{action}")
        
        # Handle custom fields separation for cases module add_case and update_case actions
        # Custom fields must be nested under 'custom_fields' parameter for TestRail API
        if module_name == 'cases' and action in ('add_case', 'update_case'):
            params = _separate_custom_fields_for_case_action(action, params)
        
        try:
            # Call the method with the provided parameters
            result = method_func(**params)
            logger.debug(f"Method {module_name}.{action} completed successfully")
            logger.debug(f"Result type: {type(result).__name__}")
            if isinstance(result, (list, dict)):
                logger.debug(f"Result size: {len(result)} items")
            return result
        except TypeError as e:
            # Check if custom fields are being passed incorrectly as top-level parameters
            custom_field_params = {
                k: v for k, v in params.items() 
                if k.startswith('custom_') and k != 'custom_fields'
            }
            
            if custom_field_params and 'unexpected keyword argument' in str(e):
                # User is passing custom fields as top-level parameters
                error_msg = (
                    f"Custom fields must be nested in 'custom_fields' parameter. "
                    f"Found custom field(s) as top-level parameters: {', '.join(custom_field_params.keys())}. "
                    f"\n\nCorrect usage: {module_name}.{action}("
                    f"section_id=..., title=..., "
                    f"custom_fields={{{', '.join(f'{k!r}: ...' for k in custom_field_params.keys())}}})"
                    f"\n\nNote: Use get_case_fields() action to see required fields and their data types."
                    f"\n      Common required fields may include: custom_automation_type, "
                    f"custom_steps_separated (array of step objects), custom_case_test_data_required, "
                    f"custom_interface_type (array), custom_module (array)."
                    f"\n\nOriginal error: {e}"
                )
                logger.error(
                    f"Custom fields passed incorrectly for {module_name}.{action}: {custom_field_params}",
                    exc_info=True
                )
                raise ValueError(error_msg) from e
            
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
                f"TypeError calling {module_name}.{action} with params {params}: {e}",
                exc_info=True
            )
            raise ValueError(error_msg) from e
        except Exception as e:
            logger.error(
                f"Error calling {module_name}.{action} with params {params}: {e}",
                exc_info=True
            )
            # Re-raise to let FastMCP handle error reporting
            raise
    
    # Set function metadata and docstring BEFORE FastMCP reads it
    # FastMCP reads the docstring when the decorator is applied, so set it now
    module_tool.__name__ = f"testrail_{module_name}"
    module_tool.__doc__ = enhanced_docstring
    
    # Set up annotations properly for FastMCP
    # Create Literal type for action parameter to help FastMCP generate proper schema
    if not hasattr(module_tool, '__annotations__'):
        module_tool.__annotations__ = {}
    
    # Set action parameter annotation with Literal type if we have method names
    # FastMCP uses Pydantic which understands Literal types for enum generation
    if method_names and len(method_names) > 0:
        try:
            # Create Literal type using helper function
            action_literal_type = _create_literal_type(tuple(method_names))
            module_tool.__annotations__['action'] = action_literal_type
        except Exception:
            # Fallback to str if Literal creation fails
            module_tool.__annotations__['action'] = str
    else:
        module_tool.__annotations__['action'] = str
    
    # Set params annotation to explicitly define it as a JSON object
    # The key is to ensure FastMCP generates a schema with type: "object"
    # Using Dict[str, Any] should already do this, but we'll be explicit
    module_tool.__annotations__['params'] = Union[Dict[str, Any], str, None]
    
    # If Field is available, try to add schema metadata to ensure it's treated as JSON object
    # Note: FastMCP should automatically infer "object" type from Dict[str, Any],
    # but the MCP client might be serializing it incorrectly
    # The real fix might need to be in how the MCP client handles Dict parameters
    
    # Ensure return annotation is set
    if 'return' not in module_tool.__annotations__:
        module_tool.__annotations__['return'] = Any
    
    return module_tool

