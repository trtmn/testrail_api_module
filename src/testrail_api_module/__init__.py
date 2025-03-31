# src/testrail_api_module/__init__.py
"""
This module provides functionalities to interact with the TestRail API, including managing attachments, cases, tests, and results, etc.

Attributes:
    __version__ (str): The version of the module.
    __author__ (str): The authors of the module.
    __all__ (list): A list of modules to be imported when `from testrail_api_module import *` is used.
"""
import os
__version__ = '0.1.2'
"""The version of the module, used for compatibility checks and logging."""
__author__ = 'Matt Troutman and Christian Thompson'

authors = __author__
"""authors of the module, used for documentation and attribution."""

# Import all submodules in the module
__all__ = [
    '_common',
    'attachments',
    'bdd',
    'case_fields',
    'case_types',
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
    'variables'
]

def __import_all_modules__():
    for _x in __all__:
        _local_name = f".{_x}"
        exec(f"from {_local_name} import *", globals())

__import_all_modules__()
del __import_all_modules__


