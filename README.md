# testrail_api_module

[![PyPI - Version](https://img.shields.io/pypi/v/testrail-api-module?label=Latest%20Version)](https://pypi.org/project/testrail-api-module/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/testrail-api-module?color=purple)](https://pypi.org/project/testrail-api-module/) [![GitHub Source](https://img.shields.io/badge/github-source-blue?logo=github)](https://github.com/trtmn/testrail-api-module/) [![PyPI Stats](https://img.shields.io/badge/%20%F0%9F%94%97-blue?label="📈%20Stats")](https://pypistats.org/packages/testrail-api-module/) [![Docs](https://img.shields.io/pypi/v/testrail-api-module?label=📖%20Docs&color=blue)](https://trtmn.github.io/testrail_api_module/)


A comprehensive Python wrapper for the TestRail API that provides easy access to all
TestRail functionalities.

## Features

- Full coverage of TestRail API endpoints
- Type hints for better IDE support
- Easy-to-use interface
- Comprehensive error handling
- Support for both API key and password authentication

## Installation

### For Consumers

```bash
# Install the package with runtime dependencies only
pip install testrail-api-module
```

### For Developers

```bash
# Clone the repository
git clone https://github.com/trtmn/testrail-api-module.git
cd testrail-api-module

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies using pip-tools
pip-compile --extra dev | pip-sync

```

## Quick Start

```python
from testrail_api_module import TestRailAPI

# Initialize the API client
api = TestRailAPI(
    base_url='https://your-instance.testrail.io',
    username='your-username',
    api_key='your-api-key'  # or use password='your-password'
)

# Get a list of projects
projects = api.projects.get_projects()

# Create a new test case
new_case = api.cases.add_case(
    section_id=123,
    title='Test Login Functionality',
    type_id=1,  # Functional test
    priority_id=3,  # Medium priority
    estimate='30m',  # 30 minutes
    refs='JIRA-123'
)

# Add a test result
api.results.add_result(
    run_id=456,
    case_id=789,
    status_id=1,  # Passed
    comment='Test executed successfully',
    elapsed='15m',  # Actual time taken
    version='1.0.0'
)
```

## Common Use Cases

### Managing Test Cases

```python
# Get all test cases in a project
cases = api.cases.get_cases(project_id=1)

# Update a test case
api.cases.update_case(
    case_id=123,
    title='Updated Test Case Title',
    type_id=2,  # Performance test
    priority_id=1  # Critical priority
)

# Delete a test case
api.cases.delete_case(case_id=123)
```

### Working with Test Runs

```python
# Create a new test run
new_run = api.runs.add_run(
    project_id=1,
    name='Sprint 1 Regression',
    description='Full regression test suite',
    suite_id=2,
    milestone_id=3,
    include_all=True
)

# Get test run results
results = api.runs.get_run_stats(run_id=new_run['id'])

# Close a test run
api.runs.close_run(run_id=new_run['id'])
```

### Managing Attachments

```python
# Add an attachment to a test case
api.attachments.add_attachment(
    entity_type='case',
    entity_id=123,
    file_path='path/to/screenshot.png',
    description='Screenshot of the error'
)

# Get attachments for a test case
attachments = api.attachments.get_attachments(
    entity_type='case',
    entity_id=123
)
```

### Working with BDD Scenarios

```python
# Import a BDD scenario
api.bdd.add_bdd(
    section_id=123,
    feature_file='path/to/feature/file.feature',
    description='Login feature tests'
)

# Export a BDD scenario
scenario = api.bdd.get_bdd(case_id=456)
```

## Error Handling

The module includes comprehensive error handling. Here's an example:

```python
try:
    result = api.cases.get_case(case_id=999999)
except Exception as e:
    print(f"Error accessing test case: {e}")
```

## Documentation

For complete documentation, visit our
[docs](https://trtmn.github.io/testrail-api-module/).

## Dependency Management

This project uses modern Python packaging with `pyproject.toml` for dependency
management.

### Files

- `pyproject.toml` - Package configuration and dependency specifications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.

## Authors

- Matt Troutman
- Christian Thompson
- Andrew Tipper

## Support

If you encounter any issues or have questions, please
[open an issue](https://github.com/trtmn/testrail_api_module/issues/new) on
GitHub.
