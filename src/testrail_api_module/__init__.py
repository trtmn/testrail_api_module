# src/testrail_api_module/__init__.py
"""
This package provides functionalities to interact with the TestRail API, including managing attachments, cases, tests, and results.

Attributes:
    __version__ (str): The version of the package.
    __author__ (str): The authors of the package.
    __all__ (list): A list of modules to be imported when `from testrail_api_module import *` is used.
"""
import os
__version__ = '0.1.0'
__author__ = 'Matt Troutman / Christian Thompson'
package_version = __version__
"""The version of the package, used for compatibility checks and logging."""

authors = __author__
"""authors of the package, used for documentation and attribution."""

# Import all modules in the package
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


