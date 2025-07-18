# Test Suite for testrail_api_module

This directory contains comprehensive tests for the `testrail_api_module` package.

## Test Structure

- `test_results.py` - Tests for the `ResultsAPI` class
- `__init__.py` - Makes tests a Python package

## Running Tests

### Prerequisites

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

### Running All Tests

```bash
# Using pytest directly
pytest

# Using the test runner script
python run_tests.py

# With verbose output
python run_tests.py -v

# With coverage report
python run_tests.py -c
```

### Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_results.py

# Run a specific test class
pytest tests/test_results.py::TestResultsAPI

# Run a specific test method
pytest tests/test_results.py::TestResultsAPI::test_add_result_minimal

# Using the test runner
python run_tests.py -t tests/test_results.py
```

## Test Coverage

The test suite covers:

- All public methods in the `ResultsAPI` class
- Edge cases and error conditions
- Different parameter combinations
- API request formatting
- Mock interactions

## Test Patterns

- **Fixtures**: Used for common test data and mock objects
- **Mocking**: API requests are mocked to avoid external dependencies
- **Parametrized Tests**: Used for testing multiple similar scenarios
- **Edge Cases**: Tests include None values, empty strings, and boundary conditions

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention: `test_<method_name>_<scenario>`
2. Use appropriate fixtures for common setup
3. Mock external dependencies
4. Include both positive and negative test cases
5. Test edge cases and error conditions 