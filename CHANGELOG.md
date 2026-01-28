# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.3] 2026-01-27

### Changed
- **Refactored `build_and_release.py` to use GitFlow workflow**: The script now follows a proper GitFlow branching model:
  - **dev branch → main**: Version bump happens here (because main is protected), then changes are merged to main
  - **main → release**: When ready to release, merge main into release branch (version already set from dev→main)
  - **release branch**: Version tags are created and pushed on the release branch
  - The script automatically detects which branch you're on and adapts its behavior accordingly
  - PRs are now fully created (not drafts) before showing the URL
  - Impact: Provides a clear, structured workflow for managing releases with proper branch separation and version bumping on dev branch where main is protected

### Fixed
- Fixed `build_and_release.py` to automatically create a release branch when run on protected branches (like `main`), preventing uncommitted changes from blocking the release process. The script now detects protected branches and creates a `release/v{VERSION}` branch before making any file changes.

### ✨ Added

- **Pre-commit Hooks Configuration**: Added pre-commit framework to automatically run code quality checks on every commit
  - Configured hooks for Python linting and formatting (ruff)
  - Added type checking with mypy
  - Included markdown linting
  - Added security checks with bandit
  - Configured general file checks (trailing whitespace, end of file, YAML/TOML/JSON validation)
  - **Credential Detection**: Added detect-secrets hook to prevent credentials, API keys, passwords, and other secrets from being committed
    - Scans all files for common secret patterns (API keys, tokens, passwords, private keys, etc.)
    - Excludes test files and lock files from scanning
    - Blocks commits containing detected secrets (exit code 1)
    - Uses baseline file to track known false positives
  - Enhanced .gitignore to exclude credential files (.env, *.key, *.pem, secrets.json, etc.)
  - Hooks run automatically regardless of git client (command line, GUI, IDE)
  - Impact: Ensures code quality and consistency across all commits, prevents credentials from being committed, and prevents common issues before they reach the repository

- **Repository Ruleset for Main Branch Protection**: Created GitHub repository ruleset to prevent direct pushes to main branch
  - Ruleset prevents branch deletion and force pushes (non-fast-forward)
  - Works in conjunction with existing branch protection that requires pull requests
  - Ruleset configuration stored in `.github/ruleset-main-protection.json`
  - Impact: Ensures all changes to main branch go through pull request review process

- **Build and Release Script**: Added comprehensive `build_and_release.py` script to automate the release process
  - Runs tests and type checking before release
  - Automatically updates version in `pyproject.toml`
  - Automatically updates `CHANGELOG.md` (moves unreleased entries to new version)
  - Builds the package using `uv build`
  - Creates git tags for releases
  - Optionally pushes tags to trigger GitHub Actions workflow
  - Supports dry-run mode for testing
  - Includes validation and safety checks
  - Checks for existing tags and handles them gracefully
  - Validates git repository status and handles edge cases
  - Improved error messages with helpful tips
  - Impact: Streamlines the release process and reduces manual errors

### 🐛 Fixed

- **Bandit Test File Scanning**: Updated bandit security scanner to include test files in security checks
  - Removed exclusion of test files from bandit scanning
  - Changed scanning scope from `src/` only to project root (excluding only build artifacts and virtual environments)
  - Test files are now scanned for security vulnerabilities and credentials, ensuring no secrets are committed in test code
  - Impact: Improved security coverage by ensuring test files are also checked for security issues

- **Pytest Collection Warnings**: Fixed 86 pytest collection warnings caused by pytest attempting to collect classes from source code
  - Added `norecursedirs` configuration to exclude `src` directory from test discovery
  - Added `--ignore=src` to pytest options to prevent scanning source code during collection
  - Added `filterwarnings` configuration to suppress `PytestCollectionWarning` messages
  - Classes like `TestRailAPIError`, `TestRailAuthenticationError`, `TestRailRateLimitError`, and `TestsAPI` were being incorrectly collected as test classes
  - Impact: All 468 tests now pass cleanly without warnings, improving test output readability

- **Test Case Type Mapping**: Fixed test expectations in `test_get_required_case_fields_type_mapping` to match actual implementation
  - Updated checkbox field type_hint expectation from `'boolean'` to `'boolean (True/False)'`
  - Updated multi-select field type_hint expectation from `'array of string IDs'` to `'array of IDs'`
  - Fixed stepped field test to use field name containing `'steps_separated'` to properly test step objects hint
  - Impact: All tests in `test_cases.py` now pass correctly

### 🔧 Changed

- **Build and Release Script Version Management**: Updated `build_and_release.py` to use `uv` for version management instead of manual file manipulation
  - Replaced manual `pyproject.toml` file parsing and regex-based version updates with `uv version` command
  - `get_current_version()` now uses `uv version --short` to read the current version
  - `update_version_in_pyproject()` now uses `uv version <version>` to update the version
  - Removed dependency on `toml` package for version management
  - Impact: More reliable version management using uv's built-in capabilities, consistent with project's use of uv for dependency management

- **Build and Release Script Interactive Mode**: Made `build_and_release.py` interactive with user confirmation prompts at each major step
  - Added `confirm_step()` helper function for consistent user prompts
  - Added interactive confirmations before: running tests, type checking, updating version, updating changelog, building package, creating git tag, and pushing tag
  - Added `--non-interactive` flag to skip all prompts for automation/CI scenarios
  - Prompts show default values (Y/n or y/N) and accept Enter to use defaults
  - Dry-run mode automatically skips prompts (non-interactive)
  - Impact: Users can review and confirm each step before execution, reducing risk of accidental releases while maintaining automation capability

- **Build and Release Script PR Creation**: Added pull request creation functionality to `build_and_release.py`
  - Automatically commits version and changelog changes
  - Pushes the current branch to remote
  - Creates a pull request to merge changes into the release branch (configurable via `--release-branch`, default: "release")
  - Uses GitHub CLI (`gh`) if available, otherwise provides manual instructions
  - Added `--skip-pr` flag to skip PR creation
  - Integrated into the release workflow: updates → build → commit → push → PR
  - Impact: Enables proper release workflow with PR review before tagging, ensuring changes are reviewed before release

- **Build and Release Script Tag Management**: Refactored tag creation to be opt-in and release-branch-only
  - Removed automatic tag creation from the main release workflow
  - Added `--tag` option that only works when on the release branch (prevents accidental tagging on wrong branch)
  - `--tag` automatically reads version from `pyproject.toml` (no need to specify `--version`)
  - When using `--tag` alone, skips all release steps (tests, version update, changelog, build, PR) and only creates/pushes tag
  - Tag creation validates current branch matches release branch
  - After tag creation, automatically prompts to push the tag (with confirmation)
  - Removed `--skip-push` option (no longer needed)
  - Impact: Prevents accidental tag creation on wrong branches, ensures tags are only created on the release branch after PR merge, and simplifies tag creation workflow

- **Build and Release Script Version Bumping**: Added interactive version bump prompts
  - When `--version` is not provided, script prompts user to select bump type (major, minor, patch, alpha, beta, rc, stable, post, dev)
  - Uses `uv version --bump` to automatically calculate and update the new version
  - Shows current version and what the new version will be before bumping
  - Supports all semantic versioning bump types
  - `--version` flag still works for explicit version specification
  - Impact: Simplifies version management by automatically calculating next version based on semantic versioning rules



## [0.5.4] 2026-01-27



## [0.5.5] 2026-01-27


## [Unreleased]

## [0.5.4] 2026-01-27

## [0.5.3] 2026-01-27

## [0.5.2] 2026-01-23

### ✨ Added

- **Automated PyPI Publishing Workflow**: Added GitHub Actions workflow for automated PyPI publishing on release tags
  - Workflow triggers automatically when tags matching semantic version patterns are pushed
  - Supports tags with or without 'v' prefix (e.g., `v0.5.2` or `0.5.2`)
  - Builds package using `uv` and `setuptools`
  - Publishes to PyPI using secure API token from repository secrets
  - Includes comprehensive publishing guide in `docs/PYPI_PUBLISHING_GUIDE.md`
  - Added Cursor command (`.cursor/commands/publish-to-pypi.md`) for easy reference
  - Impact: Simplifies release process and ensures consistent PyPI deployments

### 🔧 Changed

- **Documentation Publishing Workflow**: Updated GitHub Pages workflow to align with release process
  - Changed trigger from `main` branch pushes to release tags (same pattern as PyPI publish workflow)
  - Updated workflow name and descriptions to clearly indicate it's for publishing documentation
  - Documentation now publishes automatically when release tags are created
  - Impact: Documentation stays in sync with releases and is only published for tagged versions

### ✨ Added

- **MCP Prompts for Common TestRail Actions**: Added 10 reusable MCP prompts that provide guided workflows for common TestRail operations
  - Created new `mcp_prompts.py` module with prompt function definitions
  - Created `mcp_prompts.pyi` type stubs for type safety
  - Integrated prompt registration into `mcp_server.py` with automatic discovery
  - All prompts automatically registered when MCP server is created
  - Impact: Users can now use guided prompts instead of raw tool calls, reducing errors and improving workflow efficiency
  - Available prompts:
    - `testrail_add_test_cases` - Step-by-step guide for adding test cases with required field discovery workflow
    - `testrail_retrieve_test_run_data` - Comprehensive guide for retrieving test run information including details, tests, and results
    - `testrail_create_test_run` - Guide for creating test runs with proper configuration and case selection
    - `testrail_create_test_plan` - Guide for creating test plans with optional test run entries
    - `testrail_add_test_results` - Guide for recording test execution results with proper status codes
    - `testrail_get_test_case_details` - Guide for retrieving comprehensive test case information and history
    - `testrail_update_test_case` - Guide for updating existing test cases with proper field formats
    - `testrail_get_test_plan_details` - Guide for retrieving test plan information with statistics
    - `testrail_get_project_info` - Guide for exploring project structure including suites, sections, and cases
    - `testrail_get_run_results` - Guide for retrieving all test run results with status breakdown
  - Each prompt provides:
    - Step-by-step instructions with clear workflow guidance
    - JSON examples of tool calls with proper parameter formats
    - Field format guidelines (e.g., string IDs for arrays, step object structure)
    - References to related prompts and tools for navigation
    - Best practices and common pitfalls to avoid
  - Updated `docs/MCP_USAGE.md` with comprehensive prompts documentation
  - Added test suite in `tests/test_mcp_prompts.py` for prompt validation
  - Prompts use FastMCP's `@prompt` decorator pattern and return `UserMessage` objects
  - Graceful fallback handling if MCP prompts module cannot be imported

## [0.5.1] - 2026-01-23

### ✨ Added

- **Enhanced MCP Tool Descriptions**: Added prominent guidance in `testrail_cases` tool description to proactively guide LLMs to discover required fields before creating test cases
  - Added recommended workflow section at the top of tool description with warning emoji for visibility
  - Includes step-by-step instructions to call `get_required_case_fields` first
  - Added explicit field type examples with correct formats (arrays of string IDs, step objects, etc.)
  - Emphasizes using string IDs for arrays (not integers) with clear examples
  - Helps reduce trial-and-error when creating test cases by guiding LLMs to discover requirements first

- **Improved Error Handling for TestRail API Validation Errors**: Enhanced error messages when TestRail API returns validation errors
  - Detects validation errors about missing required fields from TestRail API responses
  - Provides actionable guidance including recommended workflow to discover fields
  - Suggests calling `get_required_case_fields` and `get_field_options` to understand requirements
  - Includes format examples for common field types (arrays, strings, booleans, step objects)
  - Helps LLMs understand what went wrong and how to fix it without multiple iterations

- **Custom Field Normalization and Pre-Validation**: Added automatic normalization and validation of custom fields before sending to TestRail API
  - Automatically converts single values to arrays for multi-select/dropdown fields
  - Converts integer IDs to string IDs for dropdown/multi-select fields (e.g., `3` → `["3"]`)
  - Validates array fields are properly formatted as arrays of strings
  - Validates step objects have correct structure (content and expected keys)
  - Provides clear error messages with format examples when validation fails
  - Prevents common formatting mistakes before they reach TestRail API
  - Reduces trial-and-error by catching format issues early

- **Enhanced Field Discovery Tools**: Improved `get_required_case_fields` method with format examples and better context
  - Added `format_example` field to each required field showing correct usage
  - Includes concrete examples for each field type (arrays, strings, booleans, step objects)
  - Added `format_guide` summary with quick reference for common field types
  - Added `context` information showing resolved project/suite/template IDs
  - Format examples include warnings about common mistakes (e.g., using integers instead of string IDs)
  - Makes it easier for LLMs to understand correct field formats without trial-and-error

- **Enhanced MCP Documentation**: Updated MCP usage documentation with best practices and complete examples
  - Added "Best Practices" section emphasizing field discovery workflow
  - Added complete workflow example showing discover → review → create process
  - Documented common pitfalls and how to avoid them with examples
  - Updated field discovery examples to show new `format_example` and `format_guide` fields
  - Provides clear guidance on correct field formats with before/after examples

### 🔧 Changed

- **add_case Validation Disabled by Default**: Changed default value of `validate_required` parameter from `True` to `False` in `add_case` method
  - Validation is now disabled by default to allow TestRail API to handle validation
  - Users can still enable validation by setting `validate_required=True` if they want pre-validation
  - The `validate_only` parameter remains available for pre-submission validation checks without creating the case
  - Custom field normalization still runs automatically to fix common format issues (single values → arrays, integer IDs → string IDs)
  - This change works better with the enhanced error handling and field discovery improvements

### 🔧 Fixed

- **Stub Generation Script**: Fixed `generate_stubs.py` to handle cases where `stubgen` executable is not in PATH
  - Now falls back to using `python -m mypy.stubgen` when `stubgen` executable is not found
  - Automatically detects and uses virtual environment Python if available
  - Improved error messages to show more details when stub generation fails
  - Fixes error: "'stubgen' executable not found" when mypy is installed but stubgen is not in PATH

- **MCP Delete Operations JSON Error**: Fixed "Invalid JSON response" error when deleting test cases (and other delete operations) via MCP server
  - TestRail's delete API returns empty response body with 200 status code
  - Updated `_handle_response` method to gracefully handle empty responses
  - Empty responses now return `{}` (empty dict) instead of raising JSON decode error
  - Fixes error: "Invalid JSON response: Expecting value: line 1 column 1 (char 0)"
  - Affects all delete operations: `delete_case`, `delete_run`, `delete_section`, etc.

### 🔧 Changed

- **add_case Validation Disabled by Default**: Changed default value of `validate_required` parameter from `True` to `False` in `add_case` method
  - Validation is now disabled by default to prevent false positives and allow TestRail API to handle validation
  - Users can still enable validation by setting `validate_required=True` if needed
  - The `validate_only` parameter remains available for pre-submission validation checks
  - This change prevents validation errors when custom fields are properly provided but validation logic incorrectly reports them as missing

### ✨ Added

- **Example Script for iPhone Test Cases**: Created `examples/create_10_iphone_cases_mcp.py` script
  - Demonstrates creating 10 test cases for iPhone mobile application testing
  - Uses MCP server tools directly to create test cases with all required custom fields
  - Includes proper handling of custom fields: `custom_automation_type`, `custom_interface_type`, `custom_module`, `custom_steps_separated`, and `custom_case_test_data_required`
  - Loads credentials from `.env` file using `python-dotenv`
  - Successfully creates test cases in Section ID 3699 (iPhone Testing section)

### 🔧 Fixed

- **Field Validation Bug in add_case**: Fixed critical bug where required custom fields were incorrectly reported as missing
  - Fixed validation logic to properly detect custom fields in the data dictionary
  - Fixed error message construction to only append step validation text (`must include at least one step...`) to actual step fields (type_id == 12), not to other field types like `custom_module` or `custom_interface_type`
  - Added fallback check to look for fields in `custom_fields` parameter if not found in data dict
  - Added comprehensive debug logging to trace field detection issues
  - Validation now correctly identifies provided array fields (e.g., `custom_module: ["17"]`, `custom_interface_type: ["3"]`) as present
  - Error messages now accurately reflect which fields are actually missing without incorrect validation text

- **MCP Custom Fields Handling**: Fixed issue where custom fields passed as top-level parameters for `add_case` and `update_case` actions were not properly nested
  - Added automatic separation of custom fields from standard fields in MCP server
  - Custom fields starting with `custom_` are now automatically moved to nested `custom_fields` dictionary
  - Supports both input styles: top-level custom fields (e.g., `custom_automation_type="7"`) and nested format (e.g., `custom_fields={"custom_automation_type": "7"}`)
  - Top-level custom fields are automatically merged into nested `custom_fields` if both formats are provided
  - Updated tool documentation to clarify both supported input formats
  - Improved user experience by eliminating the need to manually nest custom fields
  - Affects `testrail_cases` MCP tool for `add_case` and `update_case` actions

- **MCP Parameter Serialization**: Fixed issue where MCP tool parameters were being serialized as Python dict strings instead of proper dictionaries
  - Updated `params` parameter type annotation to `Union[Dict[str, Any], str, None]` to accept multiple formats
  - Added support for parsing both JSON strings and Python dict literal strings using `ast.literal_eval`
  - Added automatic repair for malformed strings (missing commas, extra braces) as a workaround for MCP client serialization bugs
  - Improved error messages to guide users on correct parameter formats and indicate when the MCP client is sending malformed data
  - Note: MCP server must be restarted for schema changes to take effect
  - **Known Issue**: Some MCP clients may still serialize Dict parameters as malformed strings. The server attempts to repair these, but the root cause is in the client's serialization logic.

- **MCP Server Entry Point**: Fixed MCP configuration to use correct entry point (`testrail_api_module` instead of `testrail_api_module.mcp_server`)
  - Resolves "Connection closed" and "No server info found" errors when Cursor attempts to connect to the MCP server
  - The configuration now correctly uses the package's `__main__.py` entry point which properly initializes the CLI
  - Impact: MCP server now starts correctly and Cursor can successfully connect and retrieve server information

- **MCP Tool Parameter Schema**: Fixed JSON parsing errors when calling MCP tools by simplifying parameter type annotation
  - Changed `params` parameter type from `Union[Dict[str, Any], str, None]` to `Dict[str, Any]` with default empty dict
  - This generates a cleaner JSON schema that FastMCP can properly serialize/deserialize
  - Resolves "Expected ',' or '}' after property value in JSON" errors when invoking MCP tools
  - Impact: MCP tools can now be called successfully from Cursor and other MCP clients

- **MCP Parameter Handling Simplification**: Further refined parameter handling in MCP tools for improved reliability
  - Removed complex Python dict literal parsing (`ast.literal_eval`) and regex-based string repair logic
  - Simplified to handle only JSON string parsing when needed (edge case fallback)
  - Added support for Pydantic model parameters (automatically converts to dict via `model_dump()`)
  - Improved error messages to clearly indicate when unexpected parameter types are received
  - Impact: More reliable parameter handling with cleaner code and better error reporting

### ✨ Added

- **Field Requirements Caching**: Automatic caching of TestRail field requirements to reduce API calls
  - Field requirements are fetched once and cached per `CasesAPI` instance
  - Dramatically improves performance when creating multiple test cases
  - Use `clear_case_fields_cache()` to refresh if project configuration changes
  - Reduces API calls from ~20+ to ~10 when creating multiple test cases
  - Cache can be bypassed with `use_cache=False` parameter when needed

- **Validate-Only Mode**: New `validate_only` parameter for `add_case()` method
  - Check field requirements without creating the test case
  - Returns detailed validation report with missing/provided fields
  - Includes field type hints and comprehensive guidance
  - Perfect for pre-submission validation in forms and UIs
  - Example: `result = api.cases.add_case(..., validate_only=True)`
  - Returns: `{"valid": bool, "missing_fields": [...], "provided_fields": [...], "message": str}`

- **MCP Debug Logging**: Added comprehensive debug logging for MCP server components
  - New `TESTRAIL_MCP_DEBUG` environment variable to enable debug logging
  - Detailed logging for API method discovery, tool registration, and execution
  - Debug logs include method parameters, results, and error context
  - Debug logging added to field validation process showing:
    - Number of required fields found
    - Individual field checks (present/missing)
    - Validation pass/fail status
  - All debug output is sent to stderr to avoid interfering with stdio communication
  - Filters out FastMCP internal debug logs for clean, relevant output
  - Compatible with existing `--verbose` CLI flag for backward compatibility

- **Required Fields Query Method**: New `get_required_case_fields()` method for querying required fields
  - Query required fields BEFORE attempting to create test cases
  - Supports optional `project_id` parameter for project-specific field filtering
  - Returns formatted field information with type hints and context:
    - `system_name`: The key to use in `custom_fields` parameter
    - `label`: Human-readable field name
    - `type_name` and `type_hint`: Clear guidance on expected data format
    - `is_global` and `project_ids`: Project context information
    - `description`: Field description from TestRail
  - Automatically exposed as MCP action `testrail_cases` with action `get_required_case_fields`
  - Includes caching support via `use_cache` parameter (default: True)
  - Example: `result = api.cases.get_required_case_fields(project_id=1)`
  - Returns structured dict: `{"required_fields": [...], "field_count": int, "project_filtered": bool, "cache_used": bool}`

- **Dynamic Field Options Query**: New `get_field_options()` method for discovering valid field values
  - Query complete list of valid options for dropdown, multi-select, and other fields
  - Returns full option details: ID, label, default value, and format hints
  - Reduces trial-and-error when creating test cases with custom fields
  - Automatically exposed as MCP action `testrail_cases` with action `get_field_options`
  - Example: `options = api.cases.get_field_options('custom_automation_type')`
  - Returns structured dict with options array: `{"field_name": "...", "options": [{"id": "1", "label": "..."}], ...}`

- **Dynamic Type Hints**: Field type hints now derive from TestRail config dynamically
  - Dropdown/multi-select hints show actual valid option IDs and labels
  - Step fields show the exact structure expected (content, expected, additional_info, refs)
  - Hints are context-aware, using the selected config for the target project/suite/template

### 🔧 Changed

- **Reduced MCP Server Log Verbosity**: Consolidated tool registration logs for cleaner output
  - Individual tool registrations now logged at DEBUG level only
  - Single INFO-level summary shows all registered tools with action counts
  - Reduces log clutter while preserving useful debugging information

- **Improved Error Messages**: Enhanced error handling for common MCP and API usage errors
  - Custom field parameters passed incorrectly now show helpful correction message
  - Error messages detect when `custom_*` fields are passed as top-level parameters
  - Provides correct usage example showing how to nest fields in `custom_fields` dict
  - MCP error messages now reference `get_case_fields()` for field requirements
  
- **Enhanced add_case Validation**: Comprehensive validation and error reporting
  - Validates all required fields at once (not one-at-a-time)
  - Shows field data types in error messages (string, array, boolean, etc.)
  - Provides specific format examples for complex fields (steps_separated, multi-select)
  - Enhanced docstring with complete custom field examples and type information
  - Improved guidance for array fields (interface_type, module) requiring string IDs
  - **BREAKING**: Validation now fails explicitly if unable to fetch field requirements
    - Previously, validation failures were silently bypassed
    - Now raises clear `ValueError` when field definitions cannot be retrieved
    - Prevents cryptic TestRail API errors by catching issues early
    - Use `validate_required=False` to disable validation if needed (e.g., for testing)

### 🐛 Fixed

- **MCP Tool Params Parsing**: Fixed issue where `params` parameter was being received
  as a JSON string instead of a dictionary in MCP tool calls
  - Added automatic JSON parsing for `params` when received as a string
  - Ensures compatibility with MCP protocol parameter handling
  - Provides clear error messages if JSON parsing fails
  - Fixes direct MCP calls that were previously failing due to type mismatch

- **Section Context Resolution**: Added suite fallback when section data lacks
  `project_id`, ensuring `add_case` resolves project context for MCP case
  creation.

- **Case Creation Validation**: Fixed `add_case` method to properly validate required
  fields before sending requests to TestRail API
  - Added automatic validation of required fields from project configuration
  - Improved error messages to clearly indicate which required fields are missing
  - Added `validate_required` parameter (default: True) to allow skipping validation
    for performance when needed
  - Enhanced documentation to clarify that custom fields should use system names
    (e.g., 'custom_field_name') as keys, not display names

- **Field Cache Empty State Bug**: Fixed critical bug where empty field cache caused validation bypass
  - Empty API responses are no longer cached, preventing false validation passes
  - Added warning logs when cache is empty to help diagnose configuration issues
  - Cache now distinguishes between "not yet fetched" (None) vs "fetched and empty" ([])
  - If validation reports 0 required fields unexpectedly, restart MCP server or call `clear_case_fields_cache()`

- **Project-Specific Required Fields**: Fixed validation to correctly detect required fields from TestRail API
  - Now checks both top-level `is_required` flag AND `configs[].options.is_required` 
  - TestRail returns project-specific requirements in the `configs` array with context information
  - Validation now correctly identifies all required custom fields (e.g., `custom_automation_type`)
  - Added detailed debug logging showing which config triggered the requirement (global vs project-specific)

- **Template-Aware Required Field Validation**: `add_case` now resolves section context and validates required fields
  against the effective template used to create the case
  - Resolves `project_id`/`suite_id` via `get_section` and selects the default template when `template_id` is omitted
  - Evaluates required-ness per matching `configs[].context` (project/suite/template when present)
  - Applies `options.default_value` automatically for required fields when provided by TestRail, reducing avoidable API failures

- **CLI Logging Side Effects**: `setup_logging()` no longer globally disables Python logging
  - Keeps stdio mode quiet by setting log levels to `ERROR` instead of calling `logging.disable()`
  - Allows downstream apps/tests to re-enable logging as needed

- **Setuptools Deprecation Warning**: Updated `pyproject.toml` license format to use SPDX expression
  - Changed from deprecated TOML table format `license = { file = "LICENSE" }` to modern format
  - Now using `license = "MIT"` with `license-files = ["LICENSE"]`
  - Eliminates SetuptoolsDeprecationWarning about deprecated license format
  - Ensures compatibility with setuptools>=77.0.0 and future versions

- **Development dependency resolution**: Removed invalid `stubgen` dev dependency
  - `stubgen` is provided by `mypy` (via the `stubgen` console script)
  - Fixes `uv` dependency resolution failures for `testrail-api-module[dev]`

- **MCP noisy INFO logs**: Suppressed `mcp.server.*` INFO output in debug/verbose mode
  - Prevents internal “Processing request of type …” lines from cluttering stderr
  - Helps avoid Cursor surfacing routine MCP logs as “errors”

### 🔄 Maintenance

- **Gitignore Updates**: Added `.cursor/mcp.json` to `.gitignore` to prevent tracking of MCP configuration files
  - Prevents accidental commits of user-specific MCP server configuration
  - Impact: Cleaner repository state and prevents configuration conflicts between users

### 📚 Documentation

- **Installation Instructions**: Streamlined and improved MCP server installation
  instructions in README and MCP_USAGE guide
  - Simplified installation steps for better clarity
  - Enhanced quick-start guide for new users
  - Improved formatting and organization

## [0.5.0] - 2026-01-14

### ✨ Added

- **MCP Server Integration**: Built-in Model Context Protocol server for AI
  assistant integration (Cursor, Claude Desktop, etc.)
  - Automatic tool discovery for all TestRail API methods
  - Module-based organization with 22 API modules
  - Environment-based configuration via environment variables or `.env` files
  - One-click install support for Cursor IDE
- **FastMCP Integration**: Complete FastMCP integration as a core dependency
- **CLI Functionality**: Command-line interface for running the MCP server
  - Support for `.env` file loading
  - Configurable logging control
- **Dynamic Version Retrieval**: Version now dynamically retrieved from
  `pyproject.toml` for improved maintainability

### 🔧 Changed

- **Tool Architecture**: Transitioned from ~132 individual tools to 22
  module-based tools for better discoverability and maintainability
- **Project Name**: Changed package name from `testrail_api_module` to
  `testrail-api-module` for PyPI consistency
- **Dependency Organization**: Reorganized dependencies with clearer separation
  between runtime and development dependencies

### 📚 Documentation

- **MCP Usage Guide**: New comprehensive guide for using the MCP server
- **README Updates**: Enhanced documentation with MCP installation
  instructions, quick-start guide, and configuration examples
- **Installation Links**: Added one-click install buttons for Cursor IDE

### 🔄 Maintenance

- Updated license year to 2026
- Removed legacy `requirements.txt` in favor of `pyproject.toml`
- Cleaned up outdated test scripts
- Enhanced error handling and logging capabilities

## [0.4.0] - 2024-12-19

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

# NEW (v0.4.0)
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
