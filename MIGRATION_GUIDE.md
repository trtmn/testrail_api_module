# Migration Guide: TestRail API Module v0.3.x → v0.4.0

## 🚨 Breaking Changes

This is a **major version update** with significant improvements and breaking changes. Please read this guide carefully before upgrading.

## 📋 Summary of Changes

### ✅ **Improvements**
- **Enhanced Error Handling**: Proper exception hierarchy with detailed error messages
- **Better Type Safety**: Consistent return types and comprehensive type annotations
- **Performance Improvements**: Connection pooling, retry logic, and efficient requests
- **Official Compliance**: Follows TestRail API best practices and patterns
- **Comprehensive Documentation**: Detailed docstrings with examples
- **Rate Limiting Awareness**: Built-in rate limit detection and handling

### ⚠️ **Breaking Changes**
- **Exception Handling**: Methods now raise exceptions instead of returning `None`
- **Return Types**: Consistent return types (no more `Optional` wrappers)
- **Method Signatures**: Some methods have updated parameter handling
- **URL Construction**: Internal changes to parameter handling

## 🔄 Migration Steps

### 1. **Update Error Handling**

**Before (v0.3.x):**
```python
from testrail_api_module import TestRailAPI

api = TestRailAPI(
    base_url="https://your-instance.testrail.io",
    username="your-email@example.com",
    api_key="your-api-key"
)

# Old error handling
result = api.cases.get_case(123)
if result is None:
    print("Error occurred")
else:
    print(f"Case: {result['title']}")
```

**After (v0.4.0):**
```python
from testrail_api_module import TestRailAPI, TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

api = TestRailAPI(
    base_url="https://your-instance.testrail.io",
    username="your-email@example.com",
    api_key="your-api-key",
    timeout=30  # New: configurable timeout
)

# New error handling
try:
    result = api.cases.get_case(123)
    print(f"Case: {result['title']}")
except TestRailAPIError as e:
    print(f"API Error: {e}")
except TestRailAuthenticationError as e:
    print(f"Authentication Error: {e}")
except TestRailRateLimitError as e:
    print(f"Rate Limit Error: {e}")
```

### 2. **Update Return Type Handling**

**Before (v0.3.x):**
```python
# Methods returned Optional[Dict] or Optional[List]
cases = api.cases.get_cases(project_id=1)
if cases is None:
    print("No cases found")
else:
    for case in cases:
        print(case['title'])
```

**After (v0.4.0):**
```python
# Methods now return Dict or List directly
try:
    cases = api.cases.get_cases(project_id=1)
    for case in cases:
        print(case['title'])
except TestRailAPIError as e:
    print(f"Error getting cases: {e}")
```

### 3. **Update Method Calls**

**Before (v0.3.x):**
```python
# Old parameter handling
api.cases.update_case(123, title="New Title", priority_id=1)

# Old URL construction
runs = api.runs.get_runs(project_id=1, suite_id=2)
```

**After (v0.4.0):**
```python
# New explicit parameter handling
try:
    api.cases.update_case(
        case_id=123,
        title="New Title",
        priority_id=1
    )
except TestRailAPIError as e:
    print(f"Error updating case: {e}")

# New parameter handling
try:
    runs = api.runs.get_runs(
        project_id=1,
        suite_id=2,
        limit=50,
        offset=0
    )
except TestRailAPIError as e:
    print(f"Error getting runs: {e}")
```

### 4. **Update Bulk Operations**

**Before (v0.3.x):**
```python
# Old bulk operations
results_data = [
    {"case_id": 1, "status_id": 1, "comment": "Passed"},
    {"case_id": 2, "status_id": 5, "comment": "Failed"}
]
result = api.results.add_results_for_cases(run_id=1, results=results_data)
if result is None:
    print("Error adding results")
```

**After (v0.4.0):**
```python
# New bulk operations with error handling
try:
    results_data = [
        {"case_id": 1, "status_id": 1, "comment": "Passed"},
        {"case_id": 2, "status_id": 5, "comment": "Failed"}
    ]
    result = api.results.add_results_for_cases(run_id=1, results=results_data)
    print(f"Added {len(result['results'])} results")
except TestRailAPIError as e:
    print(f"Error adding results: {e}")
```

## 🆕 **New Features**

### 1. **Enhanced Filtering**
```python
# New filtering options
cases = api.cases.get_cases(
    project_id=1,
    created_after=1640995200,  # Timestamp
    priority_id=[1, 2],  # Multiple priorities
    type_id=2,  # Functional tests only
    limit=100,
    offset=0
)
```

### 2. **Rate Limiting Handling**
```python
try:
    result = api.cases.get_case(123)
except TestRailRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Handle rate limiting appropriately
```

### 3. **Timeout Configuration**
```python
# New timeout configuration
api = TestRailAPI(
    base_url="https://your-instance.testrail.io",
    username="your-email@example.com",
    api_key="your-api-key",
    timeout=60  # 60 second timeout
)
```

### 4. **Better Authentication**
```python
# More robust authentication
try:
    api = TestRailAPI(
        base_url="https://your-instance.testrail.io",
        username="your-email@example.com",
        api_key="your-api-key"
    )
    projects = api.projects.get_projects()
except TestRailAuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## 📝 **Complete Migration Example**

**Before (v0.3.x):**
```python
from testrail_api_module import TestRailAPI

def test_case_workflow():
    api = TestRailAPI(
        base_url="https://your-instance.testrail.io",
        username="your-email@example.com",
        api_key="your-api-key"
    )
    
    # Get projects
    projects = api.projects.get_projects()
    if projects is None:
        print("Error getting projects")
        return
    
    # Get cases
    cases = api.cases.get_cases(project_id=projects[0]['id'])
    if cases is None:
        print("Error getting cases")
        return
    
    # Add result
    result = api.results.add_result(
        run_id=1,
        case_id=cases[0]['id'],
        status_id=1,
        comment="Test passed"
    )
    if result is None:
        print("Error adding result")
        return
    
    print("Success!")
```

**After (v0.4.0):**
```python
from testrail_api_module import TestRailAPI, TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

def test_case_workflow():
    try:
        api = TestRailAPI(
            base_url="https://your-instance.testrail.io",
            username="your-email@example.com",
            api_key="your-api-key",
            timeout=30
        )
        
        # Get projects
        projects = api.projects.get_projects()
        print(f"Found {len(projects)} projects")
        
        # Get cases
        cases = api.cases.get_cases(project_id=projects[0]['id'])
        print(f"Found {len(cases)} cases")
        
        # Add result
        result = api.results.add_result(
            run_id=1,
            case_id=cases[0]['id'],
            status_id=1,
            comment="Test passed"
        )
        print(f"Added result: {result['id']}")
        
    except TestRailAuthenticationError as e:
        print(f"Authentication failed: {e}")
    except TestRailRateLimitError as e:
        print(f"Rate limit exceeded: {e}")
    except TestRailAPIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_case_workflow()
```

## 🔧 **Installation**

```bash
# Uninstall old version
pip uninstall testrail-api-module

# Install new version
pip install testrail-api-module==0.4.0

# Or using uv
uv add testrail-api-module==0.4.0
```

## 📚 **Additional Resources**

- **API Reference**: See the updated documentation for all available methods
- **Examples**: Check `examples/refactored_usage.py` for comprehensive usage examples
- **Error Handling**: Review the exception hierarchy in `base.py`
- **Type Hints**: All methods now have comprehensive type annotations

## 🆘 **Need Help?**

If you encounter issues during migration:

1. **Check the examples** in `examples/refactored_usage.py`
2. **Review the API reference** documentation
3. **Test with a small script** before migrating large codebases
4. **Use the new error handling** to get detailed error messages

## 🎯 **Benefits of Upgrading**

- **Better Error Messages**: Clear, specific error information
- **Improved Performance**: Connection pooling and retry logic
- **Type Safety**: Comprehensive type annotations
- **Official Compliance**: Follows TestRail API best practices
- **Future-Proof**: Easier to maintain and extend
- **Better Documentation**: Detailed examples and usage patterns

The migration requires updating your error handling code, but the benefits significantly outweigh the effort required.
