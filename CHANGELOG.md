# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2024-12-19

### 🚨 Breaking Changes

- **Exception Handling**: Methods now raise specific exceptions instead of returning `None`
- **Return Types**: Consistent return types - no more `Optional` wrappers
- **Method Signatures**: Updated parameter handling for better type safety
- **URL Construction**: Internal changes to parameter handling

### ✨ Added

- **Enhanced Error Handling**: Comprehensive exception hierarchy
  - `TestRailAPIError`: Base exception for all API-related errors
  - `TestRailAuthenticationError`: Authentication failures (401 errors)
  - `TestRailRateLimitError`: Rate limit exceeded (429 errors)
  - `TestRailAPIException`: General API errors with status codes and response details
- **Performance Improvements**:
  - HTTP session with connection pooling
  - Automatic retry logic for transient failures (429, 5xx errors)
  - Configurable request timeouts
- **Better Type Safety**: Comprehensive type annotations throughout
- **Rate Limiting Awareness**: Built-in rate limit detection and handling
- **Enhanced Filtering**: Additional filtering options for API calls
- **Comprehensive Documentation**: Detailed docstrings with examples and error handling
- **Migration Guide**: Complete migration guide for upgrading from v0.3.x

### 🔧 Changed

- **Base API Client**: Complete rewrite with modern patterns
- **Authentication**: Streamlined authentication with proper validation
- **Parameter Handling**: Consistent parameter handling across all modules
- **Error Messages**: Detailed error messages with context and status codes
- **Method Documentation**: Enhanced docstrings with examples and usage patterns

### 🐛 Fixed

- **URL Construction**: Proper URL encoding and parameter handling
- **Error Context**: Better error context and debugging information
- **Type Consistency**: Consistent return types across all methods
- **Session Management**: Proper HTTP session management with connection pooling

### 📚 Documentation

- **Migration Guide**: Comprehensive guide for upgrading from v0.3.x
- **API Reference**: Updated documentation with new patterns
- **Examples**: Enhanced examples showing new error handling patterns
- **README**: Updated with breaking changes notice and new features

### 🔄 Migration Required

This is a **major version update** requiring code changes:

```python
# OLD (v0.3.x)
result = api.cases.get_case(123)
if result is None:
    print("Error occurred")

# NEW (v0.5.0)
try:
    result = api.cases.get_case(123)
    print(f"Case: {result['title']}")
except TestRailAPIError as e:
    print(f"Error: {e}")
```

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for complete migration instructions.

## [0.3.3] - Previous Version

### Features
- Basic TestRail API wrapper
- Support for all TestRail API endpoints
- Type hints for better IDE support
- Support for both API key and password authentication

### Limitations
- Methods returned `None` on errors
- No specific exception types
- Basic error handling
- No connection pooling
- Manual URL construction
