# src/testrail_api_module/__init__.py
"""
TestRail API Module
==================

A comprehensive Python wrapper for the TestRail API that provides easy-to-use
interfaces for managing test cases, runs, results, and all other TestRail resources.

**Version:** {version}

This module provides functionalities to interact with the TestRail API, including 
managing attachments, cases, tests, and results, etc.

Attributes:
    __version__ (str): The version of the module.
    __author__ (str): The authors of the module.
"""
import os
from typing import Optional

def _get_version() -> str:
    """
    Return the package version.

    First tries importlib.metadata (works for installed packages),
    then falls back to reading pyproject.toml (for development).

    Returns:
        str: The version of the module.

    Raises:
        RuntimeError: If the version cannot be determined.
    """
    # Try importlib.metadata first (works for installed packages)
    try:
        from importlib.metadata import version
        return version("testrail-api-module")
    except Exception:
        pass

    # Fallback: read from pyproject.toml (for development/editable installs)
    import re

    # Go up 3 levels: __init__.py -> testrail_api_module -> src -> project_root
    pyproject_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "pyproject.toml"
    )
    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(
                r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE
            )
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass

    # Last resort fallback
    return "0.0.0"

__version__ = _get_version()
"""The version of the module, used for compatibility checks and logging."""
__author__ = 'Matt Troutman, Christian Thompson, Andrew Tipper'

# Update the docstring with the current version
__doc__ = __doc__.format(version=__version__)

class TestRailAPI:
    """
    Main class for interacting with the TestRail API.
    This class serves as the entry point for all TestRail API functionality.
    """
    def __init__(self, base_url: str, username: str, api_key: Optional[str] = None, 
                 password: Optional[str] = None, timeout: int = 30):
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
        if not api_key and not password:
            raise ValueError("Either api_key or password must be provided for authentication")
        
        if not base_url or not base_url.startswith(('http://', 'https://')):
            raise ValueError("base_url must be a valid HTTP/HTTPS URL")
            
        # Normalize base_url (remove trailing slash)
        self.base_url = base_url.rstrip('/')
        """The base URL of your TestRail instance."""
        
        self.username = username
        """Your TestRail username. Required for authentication."""
        
        self.api_key = api_key
        """Your TestRail API key. Either api_key or password must be provided for authentication."""
        
        self.password = password
        """Your TestRail password. Either api_key or password must be provided for authentication."""
        
        self.timeout = timeout
        """Request timeout in seconds."""
        
        # Initialize all submodules
        from . import attachments
        from . import bdd
        from . import cases
        from . import configurations
        from . import datasets
        from . import groups
        from . import milestones
        from . import plans
        from . import priorities
        from . import projects
        from . import reports
        from . import result_fields
        from . import results
        from . import roles
        from . import runs
        from . import sections
        from . import shared_steps
        from . import statuses
        from . import suites
        from . import templates
        from . import tests
        from . import users
        from . import variables
        
        # Create instances of each submodule
        self.attachments = attachments.AttachmentsAPI(self)
        """API for managing attachments in TestRail. See [AttachmentsAPI](testrail_api_module/attachments.html) for details."""
        
        self.bdd = bdd.BDDAPI(self)
        """API for managing BDD features in TestRail. See [BDDAPI](testrail_api_module/bdd.html) for details."""
        
        self.cases = cases.CasesAPI(self)
        """API for managing test cases in TestRail. See [CasesAPI](testrail_api_module/cases.html) for details."""
        
        self.configurations = configurations.ConfigurationsAPI(self)
        """API for managing configurations in TestRail. See [ConfigurationsAPI](testrail_api_module/configurations.html) for details."""
        
        self.datasets = datasets.DatasetsAPI(self)
        """API for managing datasets in TestRail. See [DatasetsAPI](testrail_api_module/datasets.html) for details."""
        
        self.groups = groups.GroupsAPI(self)
        """API for managing user groups in TestRail. See [GroupsAPI](testrail_api_module/groups.html) for details."""
        
        self.milestones = milestones.MilestonesAPI(self)
        """API for managing milestones in TestRail. See [MilestonesAPI](testrail_api_module/milestones.html) for details."""
        
        self.plans = plans.PlansAPI(self)
        """API for managing test plans in TestRail. See [PlansAPI](testrail_api_module/plans.html) for details."""
        
        self.priorities = priorities.PrioritiesAPI(self)
        """API for managing test priorities in TestRail. See [PrioritiesAPI](testrail_api_module/priorities.html) for details."""
        
        self.projects = projects.ProjectsAPI(self)
        """API for managing projects in TestRail. See [ProjectsAPI](testrail_api_module/projects.html) for details."""
        
        self.reports = reports.ReportsAPI(self)
        """API for managing reports in TestRail. See [ReportsAPI](testrail_api_module/reports.html) for details."""
        
        self.result_fields = result_fields.ResultFieldsAPI(self)
        """API for managing result fields in TestRail. See [ResultFieldsAPI](testrail_api_module/result_fields.html) for details."""
        
        self.results = results.ResultsAPI(self)
        """API for managing test results in TestRail. See [ResultsAPI](testrail_api_module/results.html) for details."""
        
        self.roles = roles.RolesAPI(self)
        """API for managing user roles in TestRail. See [RolesAPI](testrail_api_module/roles.html) for details."""
        
        self.runs = runs.RunsAPI(self)
        """API for managing test runs in TestRail. See [RunsAPI](testrail_api_module/runs.html) for details."""
        
        self.sections = sections.SectionsAPI(self)
        """API for managing test sections in TestRail. See [SectionsAPI](testrail_api_module/sections.html) for details."""
        
        self.shared_steps = shared_steps.SharedStepsAPI(self)
        """API for managing shared steps in TestRail. See [SharedStepsAPI](testrail_api_module/shared_steps.html) for details."""
        
        self.statuses = statuses.StatusesAPI(self)
        """API for managing test statuses in TestRail. See [StatusesAPI](testrail_api_module/statuses.html) for details."""
        
        self.suites = suites.SuitesAPI(self)
        """API for managing test suites in TestRail. See [SuitesAPI](testrail_api_module/suites.html) for details."""
        
        self.templates = templates.TemplatesAPI(self)
        """API for managing test templates in TestRail. See [TemplatesAPI](testrail_api_module/templates.html) for details."""
        
        self.tests = tests.TestsAPI(self)
        """API for managing tests in TestRail. See [TestsAPI](testrail_api_module/tests.html) for details."""
        
        self.users = users.UsersAPI(self)
        """API for managing users in TestRail. See [UsersAPI](testrail_api_module/users.html) for details."""
        
        self.variables = variables.VariablesAPI(self)
        """API for managing variables in TestRail. See [VariablesAPI](testrail_api_module/variables.html) for details."""

# Import exception classes for easy access
from .base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError, TestRailAPIException

# Export the main class, exception classes, and all submodules
__all__ = [
    'TestRailAPI',
    'TestRailAPIError',
    'TestRailAuthenticationError', 
    'TestRailRateLimitError',
    'TestRailAPIException',
    'attachments',
    'bdd',
    'cases',
    'configurations',
    'datasets',
    'groups',
    'milestones',
    'plans',
    'priorities',
    'projects',
    'reports',
    'result_fields',
    'results',
    'roles',
    'runs',
    'sections',
    'shared_steps',
    'statuses',
    'suites',
    'templates',
    'tests',
    'users',
    'variables',
]

# Optional MCP exports (only if fastmcp is available)
try:
    from .mcp_server import create_mcp_server
    from .mcp_utils import create_api_from_env
    __all__.extend(['create_mcp_server', 'create_api_from_env'])
except ImportError:
    # fastmcp not installed, MCP functionality not available
    pass


