"""
Utility functions for MCP (Model Context Protocol) integration.

This module provides helper functions for discovering API methods and
creating MCP tools from TestRail API methods. These utilities are used
by the MCP server to automatically expose all TestRail API endpoints
as MCP tools.

The module includes functions for:
- Discovering public methods from API modules
- Generating consistent tool names
- Extracting method signatures and docstrings
- Creating TestRailAPI instances from environment variables
"""
import inspect
import logging
from typing import Dict, List, Callable, Any, Optional
from . import TestRailAPI

logger = logging.getLogger(__name__)


def discover_api_methods(api_instance: TestRailAPI) -> Dict[str, List[Callable]]:
    """
    Discover all public methods from all API modules.
    
    This function scans all API modules (cases, results, runs, etc.) and
    collects their public methods, excluding private methods and base API
    helper methods.
    
    Args:
        api_instance: The TestRailAPI instance to discover methods from.
        
    Returns:
        Dictionary mapping module names to lists of (method_name, method) tuples.
        Only includes public methods (not starting with '_') and excludes
        base API methods like '_get', '_post', '_api_request', etc.
        
    Example:
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> methods = discover_api_methods(api)
        >>> print(methods['cases'])  # List of (name, method) tuples
        [('get_case', <bound method ...>), ('get_cases', <bound method ...>), ...]
    """
    logger.debug("Starting API method discovery")
    methods_by_module: Dict[str, List[Callable]] = {}
    
    # List of all API module attributes
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
            methods = []
            
            logger.debug(f"Scanning module: {module_name}")
            
            # Get all methods from the module instance
            for name, method in inspect.getmembers(module_instance, 
                                                   predicate=inspect.ismethod):
                # Only include public methods that aren't in the exclusion list
                if not name.startswith('_') and name not in excluded_methods:
                    methods.append((name, method))
                    logger.debug(f"  Found method: {module_name}.{name}")
            
            if methods:
                methods_by_module[module_name] = methods
                logger.debug(f"Module {module_name} has {len(methods)} public methods")
        else:
            logger.debug(f"Module {module_name} not found on API instance")
    
    total_methods = sum(len(methods) for methods in methods_by_module.values())
    logger.debug(
        f"Discovery complete: {len(methods_by_module)} modules, "
        f"{total_methods} total methods"
    )
    
    return methods_by_module


def generate_tool_name(module_name: str, method_name: str) -> str:
    """
    Generate an MCP tool name from module and method names.
    
    Tool names follow a consistent format to make them easily identifiable
    and organized by module.
    
    Args:
        module_name: Name of the API module (e.g., 'cases', 'results').
        method_name: Name of the method (e.g., 'get_case', 'add_result').
        
    Returns:
        Tool name in format: testrail_{module}_{method}
        
    Example:
        >>> generate_tool_name('cases', 'get_case')
        'testrail_cases_get_case'
        >>> generate_tool_name('results', 'add_result')
        'testrail_results_add_result'
    """
    return f"testrail_{module_name}_{method_name}"


def get_method_signature(method: Callable) -> inspect.Signature:
    """
    Get the signature of a method, removing 'self' parameter.
    
    This function extracts the method signature and removes the 'self'
    parameter, which is needed when converting instance methods to
    standalone functions for MCP tools.
    
    Args:
        method: The method to get the signature for.
        
    Returns:
        Signature object with 'self' parameter removed. If the method
        doesn't have a 'self' parameter, returns the original signature.
        
    Example:
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> sig = get_method_signature(api.cases.get_case)
        >>> list(sig.parameters.keys())
        ['case_id']  # 'self' has been removed
    """
    sig = inspect.signature(method)
    
    # Remove 'self' parameter if present
    params = list(sig.parameters.values())
    if params and params[0].name == 'self':
        params = params[1:]
    
    # Create new signature without 'self'
    new_params = [
        param.replace(default=inspect.Parameter.empty) 
        if param.default == inspect.Parameter.empty 
        else param
        for param in params
    ]
    
    return sig.replace(parameters=new_params)


def extract_method_docstring(method: Callable) -> str:
    """
    Extract and format docstring from a method.
    
    Extracts the first line or paragraph of a method's docstring to use
    as a tool description. This provides a concise summary for MCP tools.
    
    Args:
        method: The method to extract docstring from.
        
    Returns:
        First line of the docstring (summary), stripped of whitespace.
        Returns empty string if the method has no docstring.
        
    Example:
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> doc = extract_method_docstring(api.cases.get_case)
        >>> print(doc)
        'Get a test case by ID.'
    """
    if method.__doc__:
        # Clean up the docstring
        doc = method.__doc__.strip()
        # Extract the summary (first line or paragraph)
        lines = doc.split('\n')
        summary = lines[0].strip()
        return summary
    return ""


def create_api_from_env() -> TestRailAPI:
    """
    Create TestRailAPI instance from environment variables.
    
    This function reads TestRail configuration from environment variables
    and creates a configured TestRailAPI instance. This is useful for
    command-line tools and automated deployments.
    
    Environment variables:
        TESTRAIL_BASE_URL: Base URL of TestRail instance (required)
        TESTRAIL_USERNAME: TestRail username (required)
        TESTRAIL_API_KEY: TestRail API key (optional, if password not provided)
        TESTRAIL_PASSWORD: TestRail password (optional, if api_key not provided)
        TESTRAIL_TIMEOUT: Request timeout in seconds (default: 30)
        
    Returns:
        Configured TestRailAPI instance ready for use.
        
    Raises:
        ValueError: If required environment variables (TESTRAIL_BASE_URL,
                    TESTRAIL_USERNAME) are missing, or if neither
                    TESTRAIL_API_KEY nor TESTRAIL_PASSWORD is provided.
        
    Example:
        >>> import os
        >>> os.environ['TESTRAIL_BASE_URL'] = 'https://test.testrail.io'
        >>> os.environ['TESTRAIL_USERNAME'] = 'user@example.com'
        >>> os.environ['TESTRAIL_API_KEY'] = 'api-key-123'
        >>> api = create_api_from_env()
        >>> print(api.base_url)
        'https://test.testrail.io'
    """
    import os
    
    logger.debug("Creating TestRailAPI instance from environment variables")
    
    base_url = os.getenv('TESTRAIL_BASE_URL')
    username = os.getenv('TESTRAIL_USERNAME')
    api_key = os.getenv('TESTRAIL_API_KEY')
    password = os.getenv('TESTRAIL_PASSWORD')
    timeout = int(os.getenv('TESTRAIL_TIMEOUT', '30'))
    
    # Log configuration (but mask sensitive data)
    logger.debug(f"Base URL: {base_url}")
    logger.debug(f"Username: {username}")
    logger.debug(f"API Key: {'***' if api_key else 'not set'}")
    logger.debug(f"Password: {'***' if password else 'not set'}")
    logger.debug(f"Timeout: {timeout}s")
    
    if not base_url or not username:
        logger.error("Missing required environment variables: TESTRAIL_BASE_URL and/or TESTRAIL_USERNAME")
        raise ValueError(
            "TESTRAIL_BASE_URL and TESTRAIL_USERNAME must be set as "
            "environment variables"
        )
    
    if not api_key and not password:
        logger.error("Missing authentication: Neither TESTRAIL_API_KEY nor TESTRAIL_PASSWORD is set")
        raise ValueError(
            "Either TESTRAIL_API_KEY or TESTRAIL_PASSWORD must be set as "
            "environment variables"
        )
    
    api = TestRailAPI(
        base_url=base_url,
        username=username,
        api_key=api_key,
        password=password,
        timeout=timeout
    )
    
    logger.debug("TestRailAPI instance created successfully")
    return api

