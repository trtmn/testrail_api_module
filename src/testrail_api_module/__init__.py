# src/testrail_api_module/__init__.py
"""
This module provides functionalities to interact with the TestRail API, including managing attachments, cases, tests, and results, etc.

Attributes:
    __version__ (str): The version of the module.
    __author__ (str): The authors of the module.
"""
import os
from typing import Optional

__version__ = '0.1.5'
"""The version of the module, used for compatibility checks and logging."""
__author__ = 'Matt Troutman and Christian Thompson'

class TestRailAPI:
    """
    Main class for interacting with the TestRail API.
    This class serves as the entry point for all TestRail API functionality.
    """
    def __init__(self, base_url: str, username: str, api_key: Optional[str] = None, password: Optional[str] = None):
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
        if not api_key and not password:
            raise ValueError("Either api_key or password must be provided for authentication")
            
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self.password = password
        
        # Initialize all submodules
        from . import attachments
        from . import bdd
        from . import case_fields
        from . import case_types
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
        self.bdd = bdd.BDDAPI(self)
        self.case_fields = case_fields.CaseFieldsAPI(self)
        self.case_types = case_types.CaseTypesAPI(self)
        self.cases = cases.CasesAPI(self)
        self.configurations = configurations.ConfigurationsAPI(self)
        self.datasets = datasets.DatasetsAPI(self)
        self.groups = groups.GroupsAPI(self)
        self.milestones = milestones.MilestonesAPI(self)
        self.plans = plans.PlansAPI(self)
        self.priorities = priorities.PrioritiesAPI(self)
        self.projects = projects.ProjectsAPI(self)
        self.reports = reports.ReportsAPI(self)
        self.result_fields = result_fields.ResultFieldsAPI(self)
        self.results = results.ResultsAPI(self)
        self.roles = roles.RolesAPI(self)
        self.runs = runs.RunsAPI(self)
        self.sections = sections.SectionsAPI(self)
        self.shared_steps = shared_steps.SharedStepsAPI(self)
        self.statuses = statuses.StatusesAPI(self)
        self.suites = suites.SuitesAPI(self)
        self.templates = templates.TemplatesAPI(self)
        self.tests = tests.TestsAPI(self)
        self.users = users.UsersAPI(self)
        self.variables = variables.VariablesAPI(self)

# Export the main class
__all__ = ['TestRailAPI']


