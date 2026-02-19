from typing import Any

from .base import TestRailAPIError as TestRailAPIError
from .base import TestRailAPIException as TestRailAPIException
from .base import TestRailAuthenticationError as TestRailAuthenticationError
from .base import TestRailRateLimitError as TestRailRateLimitError

__all__ = [
    "TestRailAPI",
    "TestRailAPIError",
    "TestRailAuthenticationError",
    "TestRailRateLimitError",
    "TestRailAPIException",
]

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
    labels: Any
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
    def __init__(
        self,
        base_url: str,
        username: str,
        api_key: str | None = None,
        password: str | None = None,
        timeout: int = 30,
    ) -> None:
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
