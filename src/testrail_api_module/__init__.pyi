from typing import Any, Optional, Dict, List

__all__ = ['TestRailAPI', 'attachments', 'bdd', 'cases', 'configurations', 'datasets', 'groups', 'milestones', 'plans', 'priorities', 'projects', 'reports', 'result_fields', 'results', 'roles', 'runs', 'sections', 'shared_steps', 'statuses', 'suites', 'templates', 'tests', 'users', 'variables']

class TestRailAPI:
    """
    Main class for interacting with the TestRail API.
    This class serves as the entry point for all TestRail API functionality.
    """
    base_url: Any
    username: Any
    api_key: Any
    password: Any
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
    def __init__(self, base_url: str, username: str, api_key: str | None = None, password: str | None = None) -> None:
        """
        Initialize the TestRail API client.
        
        Args:
            base_url (str): The base URL of your TestRail instance (e.g., 'https://your-instance.testrail.io')
            username (str): Your TestRail username
            api_key (str, optional): Your TestRail API key. Either api_key or password must be provided.
            password (str, optional): Your TestRail password. Either api_key or password must be provided.
            
        Raises:
            ValueError: If neither api_key nor password is provided.
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
