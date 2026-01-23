import inspect
from . import TestRailAPI as TestRailAPI
from typing import Any, Optional, Dict, List
from typing import Callable

logger: Any

def discover_api_methods(api_instance: TestRailAPI) -> dict[str, list[Callable]]:
    '''
    Discover all public methods from all API modules.
    
    This function scans all API modules (cases, results, runs, etc.) and
    collects their public methods, excluding private methods and base API
    helper methods.
    
    Args:
        api_instance: The TestRailAPI instance to discover methods from.
        
    Returns:
        Dictionary mapping module names to lists of (method_name, method) tuples.
        Only includes public methods (not starting with \'_\') and excludes
        base API methods like \'_get\', \'_post\', \'_api_request\', etc.
        
    Example:
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> methods = discover_api_methods(api)
        >>> print(methods[\'cases\'])  # List of (name, method) tuples
        [(\'get_case\', <bound method ...>), (\'get_cases\', <bound method ...>), ...]
    '''
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
def get_method_signature(method: Callable) -> inspect.Signature:
    '''
    Get the signature of a method, removing \'self\' parameter.
    
    This function extracts the method signature and removes the \'self\'
    parameter, which is needed when converting instance methods to
    standalone functions for MCP tools.
    
    Args:
        method: The method to get the signature for.
        
    Returns:
        Signature object with \'self\' parameter removed. If the method
        doesn\'t have a \'self\' parameter, returns the original signature.
        
    Example:
        >>> api = TestRailAPI(base_url="...", username="...", api_key="...")
        >>> sig = get_method_signature(api.cases.get_case)
        >>> list(sig.parameters.keys())
        [\'case_id\']  # \'self\' has been removed
    '''
def extract_method_docstring(method: Callable) -> str:
    '''
    Extract and format docstring from a method.
    
    Extracts the first line or paragraph of a method\'s docstring to use
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
        \'Get a test case by ID.\'
    '''
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
