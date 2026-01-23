from .base import TestRailAPIError as TestRailAPIError, TestRailAPIException as TestRailAPIException, TestRailAuthenticationError as TestRailAuthenticationError, TestRailRateLimitError as TestRailRateLimitError
from .mcp_server import create_mcp_server as create_mcp_server
from .mcp_utils import create_api_from_env as create_api_from_env
from typing import Any, Optional, Dict, List

__all__ = ['TestRailAPI', 'TestRailAPIError', 'TestRailAuthenticationError', 'TestRailRateLimitError', 'TestRailAPIException', 'attachments', 'bdd', 'cases', 'configurations', 'datasets', 'groups', 'milestones', 'plans', 'priorities', 'projects', 'reports', 'result_fields', 'results', 'roles', 'runs', 'sections', 'shared_steps', 'statuses', 'suites', 'templates', 'tests', 'users', 'variables', 'create_mcp_server', 'create_api_from_env']

class TestRailAPI:
    """
    Main class for interacting with the TestRail API.
    This class serves as the entry point for all TestRail API functionality.
    """
    base_url: Any
    username: Any
    api_key: Any
    password: Any
    timeout: Any
    attachments: Any
    bdd: Any
    cases: Any
    configurations: Any
    datasets: Any
    groups: Any
    milestones: Any
    plans: Any
    priorities: Any
    projects: Any
    reports: Any
    result_fields: Any
    results: Any
    roles: Any
    runs: Any
    sections: Any
    shared_steps: Any
    statuses: Any
    suites: Any
    templates: Any
    tests: Any
    users: Any
    variables: Any
    def __init__(self, base_url: str, username: str, api_key: str | None = None, password: str | None = None, timeout: int = 30) -> None:
        """
        Initialize the TestRail API client.
        
        Args:
            base_url: The base URL of your TestRail instance (e.g., 'https://your-instance.testrail.io')
            username: Your TestRail username (typically your email address)
            api_key: Your TestRail API key. Either api_key or password must be provided.
            password: Your TestRail password. Either api_key or password must be provided.
            timeout: Request timeout in seconds (default: 30)
            
        Raises:
            ValueError: If neither api_key nor password is provided.
            ValueError: If base_url is not a valid URL format.
        """

# Names in __all__ with no definition:
#   attachments
#   bdd
#   cases
#   configurations
#   datasets
#   groups
#   milestones
#   plans
#   priorities
#   projects
#   reports
#   result_fields
#   results
#   roles
#   runs
#   sections
#   shared_steps
#   statuses
#   suites
#   templates
#   tests
#   users
#   variables
