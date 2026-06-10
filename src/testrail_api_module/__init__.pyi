from typing import Self

import requests

from . import attachments as attachments
from . import bdd as bdd
from . import cases as cases
from . import configurations as configurations
from . import datasets as datasets
from . import groups as groups
from . import labels as labels
from . import milestones as milestones
from . import plans as plans
from . import priorities as priorities
from . import projects as projects
from . import reports as reports
from . import result_fields as result_fields
from . import results as results
from . import roles as roles
from . import runs as runs
from . import sections as sections
from . import shared_steps as shared_steps
from . import statuses as statuses
from . import suites as suites
from . import templates as templates
from . import tests as tests
from . import users as users
from . import variables as variables
from .attachments import AttachmentsAPI
from .base import TestRailAPIError as TestRailAPIError
from .base import TestRailAPIException as TestRailAPIException
from .base import TestRailAuthenticationError as TestRailAuthenticationError
from .base import TestRailRateLimitError as TestRailRateLimitError
from .bdd import BDDAPI
from .cases import CasesAPI
from .configurations import ConfigurationsAPI
from .datasets import DatasetsAPI
from .groups import GroupsAPI
from .labels import LabelsAPI
from .milestones import MilestonesAPI
from .plans import PlansAPI
from .priorities import PrioritiesAPI
from .projects import ProjectsAPI
from .reports import ReportsAPI
from .result_fields import ResultFieldsAPI
from .results import ResultsAPI
from .roles import RolesAPI
from .runs import RunsAPI
from .sections import SectionsAPI
from .shared_steps import SharedStepsAPI
from .statuses import StatusesAPI
from .suites import SuitesAPI
from .templates import TemplatesAPI
from .tests import TestsAPI
from .users import UsersAPI
from .variables import VariablesAPI

__version__: str
__author__: str

__all__ = [
    "TestRailAPI",
    "TestRailAPIError",
    "TestRailAuthenticationError",
    "TestRailRateLimitError",
    "TestRailAPIException",
    "attachments",
    "bdd",
    "cases",
    "configurations",
    "datasets",
    "groups",
    "labels",
    "milestones",
    "plans",
    "priorities",
    "projects",
    "reports",
    "result_fields",
    "results",
    "roles",
    "runs",
    "sections",
    "shared_steps",
    "statuses",
    "suites",
    "templates",
    "tests",
    "users",
    "variables",
]

class TestRailAPI:
    """
    Main class for interacting with the TestRail API.
    This class serves as the entry point for all TestRail API functionality.
    """

    base_url: str
    username: str
    api_key: str | None
    password: str | None
    timeout: int
    session: requests.Session
    attachments: AttachmentsAPI
    bdd: BDDAPI
    cases: CasesAPI
    configurations: ConfigurationsAPI
    datasets: DatasetsAPI
    groups: GroupsAPI
    labels: LabelsAPI
    milestones: MilestonesAPI
    plans: PlansAPI
    priorities: PrioritiesAPI
    projects: ProjectsAPI
    reports: ReportsAPI
    result_fields: ResultFieldsAPI
    results: ResultsAPI
    roles: RolesAPI
    runs: RunsAPI
    sections: SectionsAPI
    shared_steps: SharedStepsAPI
    statuses: StatusesAPI
    suites: SuitesAPI
    templates: TemplatesAPI
    tests: TestsAPI
    users: UsersAPI
    variables: VariablesAPI
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
    def close(self) -> None:
        """Close the shared HTTP session and its connection pools."""
    def __enter__(self) -> Self: ...
    def __exit__(self, *exc_info: object) -> None: ...
