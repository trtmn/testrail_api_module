# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Entries for **0.7.4 and earlier** are hand-written. From **0.7.5
> onward**, this file is maintained by
> [release-please](https://github.com/googleapis/release-please), which
> prepends new blocks above the most recent release based on
> Conventional Commits.

## [Unreleased]

### 🔄 Maintenance

- Automate GitHub release creation in the release workflow. New
  releases ship with a GitHub release containing notes extracted from
  the matching `CHANGELOG.md` section and an install snippet, with no
  manual step required. (#122, #123)
- Migrate the release flow to
  [release-please](https://github.com/googleapis/release-please).
  Version bumps and `CHANGELOG.md` entries are now machine-generated
  from Conventional Commits PR titles; the old manual prep-branch dance
  is gone. The maintainer's only release action is merging the
  `chore(main): release X.Y.Z` PR that release-please keeps open
  against `development`, then merging the sync PR `development → main`
  that the workflow opens after publish. The legacy `tag-release.yml`
  is replaced by `release-please.yml`. Dependabot is reconfigured to
  emit `deps:` and `ci:` commit prefixes so its PRs flow through the
  same pipeline. (#124, #125)

## [0.7.4] - 2026-05-22

### 🔄 Maintenance

- Bump GitHub Actions to drop Node.js 20 deprecation warnings on CI runs
  (#116):
  - `actions/checkout` 4 → 6
  - `astral-sh/setup-uv` 4 → 7
  - `actions/setup-python` 5 → 6
  - `actions/configure-pages` 5 → 6
  - `actions/upload-pages-artifact` 3 → 5
  - `actions/deploy-pages` 4 → 5
- Bump Python dependencies via Dependabot's uv group (#117). The
  `requests` bump is to the runtime dep (the HTTP library that powers
  `BaseAPI`); the rest are dev-only:
  - `requests` 2.33.0 → 2.34.2 (runtime)
  - `pytest-cov` 7.0.0 → 7.1.0
  - `mypy` 1.19.1 → 2.1.0
  - `pre-commit` 4.5.1 → 4.6.0
  - `ruff` 0.14.11 → 0.15.14
  - `bandit` 1.9.3 → 1.9.4

## [0.7.3] - 2026-05-22

### 🔄 Maintenance

- Bump transitive `Pygments` from 2.19.2 to 2.20.0 to resolve a low-severity
  ReDoS advisory (CVE-2026-4539 / GHSA-5239-wwwm-4pmq). Pygments is
  dev-only — pulled in by `pdoc`, `pytest`, and `rich` — so this does
  not affect published-wheel users (#114, #115).
- Commit `.github/dependabot.yml` codifying the previously UI-only
  Dependabot configuration: weekly updates for both the `uv` ecosystem
  and `github-actions`, with both ecosystems grouped into a single PR
  each (#114, #115).
- Document the new release workflow in `.claude/skills/release/SKILL.md`:
  pre-release drift check, local `tox` run, two-PR flow
  (release-branch → development → main), PyPI verification, and
  GitHub release creation (#113).

## [0.7.2] - 2026-05-22

### 🐛 Fixed

- `ResultsAPI.add_results_for_cases` return type annotation corrected from
  `dict[str, Any]` to `list[dict[str, Any]]` to match the TestRail API, which
  returns an unpaginated list of result objects. Both `results.py` and
  `results.pyi` updated; regression test pins the annotation via
  `typing.get_type_hints` (#100, #102).
- TRAM logo on the PyPI project page (was rendering as a broken-image
  placeholder). README now references the logo by absolute
  `raw.githubusercontent.com` URL so PyPI's renderer can resolve it
  (#109, #110).

### 🔄 Maintenance

- Gitignore `.claude/agent-memory/`, `.claude/agents/`, and `.1password/`
  to prevent accidental commits of agent state and local tooling config
  containing absolute `/Users/<name>/` paths (#105, #106).
- Back-merge `main` into `development` to reconverge branches after the
  0.7.1 release work landed directly on `main`. Adds `enforce_admins`
  branch protection on `main` and a required Tests status check
  (Python 3.11/3.12/3.13/3.14) to prevent future drift (#107, #108).

## [0.7.1] - 2026-04-14

### 🔧 Changed

- Rebrand project title to **TRAM — TestRail API Module** in README
- Add TRAM logo to README
- Remove `| None` return types from 14 older submodules — methods raise on failure, never return `None`
- Improve class docstrings across all submodules with descriptive summaries
- Standardize docstring format (Args/Returns/Raises sections, remove old-style type annotations)
- Add `**kwargs: Any` type annotations to all `update_*()` methods and `base.py` helpers

### ✨ Added

- Add `__all__` exports to 18 submodules that were missing them

### 🔄 Maintenance

- Remove `mypy[dev]` from runtime dependencies (was only needed in dev)
- Remove redundant `autopep8` and `flake8` from `dependency-groups` (ruff handles both)
- Bump version to 0.7.1
- Fix release skill post-merge sync step to fetch `main` and merge back into `development`
- Add `.venv-*/` and `.1password/` patterns to `.gitignore`
- Enable parallel test execution in `tox.ini` (`parallel = auto`)
- Add Python 3.14 to supported versions (`tox.ini`, CI matrix, docs)

## [0.7.0] - 2026-02-19

### 🚨 Breaking Changes

- Removed 63 fabricated API methods across 18 submodules that do not exist in the official TestRail API:
  - **attachments**: removed `get_attachment_content`
  - **groups**: removed `add_group_to_suite`, `remove_group_from_suite`, `get_group_cases`, `get_group_suites`
  - **milestones**: removed `get_milestone_stats`
  - **priorities**: removed `get_priority`, `add_priority`, `update_priority`, `delete_priority`, `get_priority_counts`, `get_priority_stats`
  - **projects**: removed `get_project_stats`, `get_project_activity`, `get_project_attachments`, `add_project_attachment`
  - **reports**: removed `get_report`, `add_report`, `update_report`, `delete_report`, `get_report_results`
  - **result_fields**: removed `get_result_field`
  - **roles**: removed `get_role`, `add_role`, `update_role`, `delete_role`
  - **runs**: removed `get_run_stats`
  - **sections**: removed `get_section_cases`, `get_section_stats`
  - **statuses**: removed `get_status`, `add_status`, `update_status`, `delete_status`, `get_status_counts`, `get_status_history`
  - **suites**: removed `get_suite_cases`, `get_suite_stats`, `get_suite_runs`
  - **templates**: removed `get_template`, `add_template`, `update_template`, `delete_template`, `get_template_fields`, `add_template_field`, `update_template_field`, `delete_template_field`
  - **tests**: removed `get_test_results`, `add_test_result`, `add_test_results`
  - **users**: removed `add_user`, `update_user`, `delete_user`, `get_user_activity`, `get_user_projects`, `get_user_roles`
  - **variables**: removed `get_variable`, `get_variable_groups`, `add_variable_group`, `update_variable_group`, `delete_variable_group`

### 🔄 Maintenance

- Adopted git-flow branching strategy: `development` as integration branch, `main` for releases only
- Added `development` branch to CI test triggers
- Updated release skill to follow dev→main PR workflow
- Require GitHub issue before starting work; branch names must include issue number (e.g., `81-description`)
- Require updating GitHub issues with progress comments throughout work
- Close issues when PR merges to `development` with passing CI
- Changed default branch to `development` so `Closes #N` auto-closes issues

### 🐛 Fixed

- Fixed PyPI Stats badge broken link in README (trailing slash)

## [0.6.6] - 2026-02-19

### 🐛 Fixed

- Fixed 29 mypy strict-mode type errors in `cases.py`: return-type mismatches, missing annotations, unreachable code, and None-safety issues

## [0.6.5] - 2026-02-19

### 🐛 Fixed

- Fixed GitHub Source badge and docs link in README using hyphens instead of underscores for repo name

## [0.6.4] - 2026-02-19

### 🔄 Maintenance

- Automated release workflow: version tags are now created automatically by GitHub Actions when a PR is merged to `main`, which then triggers docs deployment and PyPI publishing in a single pipeline
- Added `tag-release.yml` workflow; `publish.yml` is now manual-only

## [0.6.3] - 2026-02-19

### 🐛 Fixed

- Fixed incorrect version number in README breaking changes heading (was v0.7.0, should be v0.6.2)

## [0.6.2] - 2026-02-19

### 🚨 Breaking Changes

- **Configurations API rewritten** to match the official two-level group/config structure:
  - Removed: `get_configuration`, `get_configurations`, `add_configuration`, `update_configuration`, `delete_configuration`
  - Added: `get_configs`, `add_config_group`, `add_config`, `update_config_group`, `update_config`, `delete_config_group`, `delete_config`
- **Results API restructured** to match official endpoint names:
  - Renamed: `add_result(run_id, case_id, ...)` → `add_result_for_case(run_id, case_id, ...)`
  - Changed: `add_result(test_id, ...)` now adds a result by test ID (new signature)
  - Changed: `get_results(test_id, ...)` now gets results by test ID (was an alias for `get_results_for_run`)
  - Fixed: `add_results(run_id, ...)` now calls `add_results/{run_id}` (was incorrectly calling `add_results_for_cases`)
  - Removed: `add_result_for_run` (not a real TestRail endpoint)
- **Cases API**: Renamed `get_case_history` → `get_history_for_case` to match official endpoint
- **Plans API**: Removed `get_plan_stats` (not a real TestRail endpoint)

### ✨ Added

- **Labels API** (new module): `get_label`, `get_labels`, `add_label`, `update_label`, `delete_label`
- **Plans**: `add_plan_entry`, `update_plan_entry`, `delete_plan_entry`
- **Cases**: `add_case_field`, `update_cases` (bulk), `delete_cases` (bulk)
- **Sections**: `move_section` (requires TestRail 6.5.2+)
- **Users**: `get_current_user` (requires TestRail 6.6+)
- **Statuses**: `get_case_statuses` (requires TestRail Enterprise 7.3+)
- **Datasets**: `add_dataset`, `update_dataset`, `delete_dataset` (requires TestRail Enterprise 7.6+)

### 🔧 Changed

- Updated all `.pyi` type stubs to match new method signatures
- Updated `__init__.py` to wire the new Labels module
- Rewrote test suites for Configurations, Results, Plans, and Cases to match updated APIs
- Added test suite for new Labels module

## [0.6.1] - 2026-02-19

### ✨ Added

- **CI test workflow**: Added GitHub Actions workflow to run tests across Python 3.11, 3.12, 3.13
- **PyPI publish gating**: PyPI publish workflow now depends on docs build and test workflows passing

### 🔧 Changed

- Removed mypy and ruff from CI test workflow (handled by pre-commit)
- Removed lint env from `tox.ini`
- Excluded orphaned `__main__.pyi` from mypy checks

## [0.6.0] - 2026-02-19

### 🚨 Breaking Changes

- **MCP Server removed**: Removed all MCP (Model Context Protocol) server functionality
  - Removed `mcp_server.py`, `mcp_tools.py`, `mcp_utils.py`, `mcp_prompts.py` and type stubs
  - Removed `cli.py` and `__main__.py` entry points
  - Removed `testrail-mcp-server` CLI script
  - Removed `fastmcp` dependency
  - Removed MCP-related tests and documentation
  - Impact: The package is now a pure Python API wrapper without MCP server capabilities

### ✨ Added

- `CLAUDE.md` and `AGENTS.md` for AI-assisted development guidance
- Claude Code skill for TestRail Python API integration

### 🐛 Fixed

- Fixed multi-line f-string syntax in `cases.py` and `base.py` for Python 3.11 compatibility (f-strings with `{` at end of line require Python 3.12+)

### 🔄 Maintenance

- Added `.claude/settings.local.json` to `.gitignore`
- Added pre-commit hook to block direct commits to main
- Untracked `.claude/settings.local.json` from git history

## [0.5.6] - 2026-01-27

## [0.5.5] - 2026-01-27

## [0.5.4] - 2026-01-27

## [0.5.3] - 2026-01-27

### 🔧 Changed

- **Refactored `build_and_release.py` to use GitFlow workflow**: The script now follows a proper GitFlow branching model:
  - **dev branch → main**: Version bump happens here (because main is protected), then changes are merged to main
  - **main → release**: When ready to release, merge main into release branch (version already set from dev→main)
  - **release branch**: Version tags are created and pushed on the release branch
  - The script automatically detects which branch you're on and adapts its behavior accordingly
  - PRs are now fully created (not drafts) before showing the URL
  - Impact: Provides a clear, structured workflow for managing releases with proper branch separation and version bumping on dev branch where main is protected
- **Build and Release Script Version Management**: Updated `build_and_release.py` to use `uv` for version management instead of manual file manipulation
  - Replaced manual `pyproject.toml` file parsing and regex-based version updates with `uv version` command
  - `get_current_version()` now uses `uv version --short` to read the current version
  - `update_version_in_pyproject()` now uses `uv version <version>` to update the version
  - Removed dependency on `toml` package for version management
- **Build and Release Script Interactive Mode**: Made `build_and_release.py` interactive with user confirmation prompts at each major step
  - Added `confirm_step()` helper function for consistent user prompts
  - Added `--non-interactive` flag to skip all prompts for automation/CI scenarios
- **Build and Release Script PR Creation**: Added pull request creation functionality to `build_and_release.py`
  - Automatically commits version and changelog changes
  - Creates a pull request to merge changes into the release branch
  - Uses GitHub CLI (`gh`) if available, otherwise provides manual instructions
- **Build and Release Script Tag Management**: Refactored tag creation to be opt-in and release-branch-only
  - Added `--tag` option that only works when on the release branch
  - Tag creation validates current branch matches release branch
- **Build and Release Script Version Bumping**: Added interactive version bump prompts
  - When `--version` is not provided, script prompts user to select bump type
  - Uses `uv version --bump` to automatically calculate and update the new version

### 🐛 Fixed

- Fixed `build_and_release.py` to automatically create a release branch when run on protected branches
- **Bandit Test File Scanning**: Updated bandit security scanner to include test files in security checks
- **Pytest Collection Warnings**: Fixed 86 pytest collection warnings caused by pytest attempting to collect classes from source code
- **Test Case Type Mapping**: Fixed test expectations in `test_get_required_case_fields_type_mapping` to match actual implementation

### ✨ Added

- **Pre-commit Hooks Configuration**: Added pre-commit framework to automatically run code quality checks on every commit
  - Configured hooks for Python linting and formatting (ruff)
  - Added type checking with mypy
  - Included markdown linting
  - Added security checks with bandit
  - **Credential Detection**: Added detect-secrets hook to prevent credentials from being committed
- **Repository Ruleset for Main Branch Protection**: Created GitHub repository ruleset to prevent direct pushes to main branch
- **Build and Release Script**: Added comprehensive `build_and_release.py` script to automate the release process

## [0.5.2] - 2026-01-23

### ✨ Added

- **Automated PyPI Publishing Workflow**: Added GitHub Actions workflow for automated PyPI publishing on release tags
- **MCP Prompts for Common TestRail Actions**: Added 10 reusable MCP prompts that provide guided workflows for common TestRail operations

### 🔧 Changed

- **Documentation Publishing Workflow**: Updated GitHub Pages workflow to trigger on release tags instead of main branch pushes

## [0.5.1] - 2026-01-23

### ✨ Added

- **Enhanced MCP Tool Descriptions**: Added prominent guidance in `testrail_cases` tool description to proactively guide LLMs to discover required fields before creating test cases
- **Improved Error Handling for TestRail API Validation Errors**: Enhanced error messages when TestRail API returns validation errors
- **Custom Field Normalization and Pre-Validation**: Added automatic normalization and validation of custom fields before sending to TestRail API
- **Enhanced Field Discovery Tools**: Improved `get_required_case_fields` method with format examples and better context
- **Field Requirements Caching**: Automatic caching of TestRail field requirements to reduce API calls
- **Validate-Only Mode**: New `validate_only` parameter for `add_case()` method
- **MCP Debug Logging**: Added comprehensive debug logging for MCP server components
- **Required Fields Query Method**: New `get_required_case_fields()` method for querying required fields
- **Dynamic Field Options Query**: New `get_field_options()` method for discovering valid field values
- **Dynamic Type Hints**: Field type hints now derive from TestRail config dynamically
- **Example Script for iPhone Test Cases**: Created `examples/create_10_iphone_cases_mcp.py` script

### 🔧 Changed

- **add_case Validation Disabled by Default**: Changed default value of `validate_required` parameter from `True` to `False`
- **Reduced MCP Server Log Verbosity**: Consolidated tool registration logs for cleaner output
- **Improved Error Messages**: Enhanced error handling for common MCP and API usage errors
- **Enhanced add_case Validation**: Comprehensive validation and error reporting

### 🐛 Fixed

- **Stub Generation Script**: Fixed `generate_stubs.py` to handle cases where `stubgen` executable is not in PATH
- **MCP Delete Operations JSON Error**: Fixed "Invalid JSON response" error when deleting test cases via MCP server
- **Field Validation Bug in add_case**: Fixed critical bug where required custom fields were incorrectly reported as missing
- **MCP Custom Fields Handling**: Fixed issue where custom fields passed as top-level parameters were not properly nested
- **MCP Parameter Serialization**: Fixed issue where MCP tool parameters were being serialized as Python dict strings
- **MCP Server Entry Point**: Fixed MCP configuration to use correct entry point
- **MCP Tool Parameter Schema**: Fixed JSON parsing errors when calling MCP tools
- **MCP Parameter Handling Simplification**: Further refined parameter handling in MCP tools
- **MCP Tool Params Parsing**: Fixed issue where `params` parameter was being received as a JSON string
- **Section Context Resolution**: Added suite fallback when section data lacks `project_id`
- **Case Creation Validation**: Fixed `add_case` method to properly validate required fields
- **Field Cache Empty State Bug**: Fixed critical bug where empty field cache caused validation bypass
- **Project-Specific Required Fields**: Fixed validation to correctly detect required fields from TestRail API
- **Template-Aware Required Field Validation**: `add_case` now resolves section context and validates required fields against the effective template
- **CLI Logging Side Effects**: `setup_logging()` no longer globally disables Python logging
- **Setuptools Deprecation Warning**: Updated `pyproject.toml` license format to use SPDX expression
- **Development dependency resolution**: Removed invalid `stubgen` dev dependency
- **MCP noisy INFO logs**: Suppressed `mcp.server.*` INFO output in debug/verbose mode

### 🔄 Maintenance

- **Gitignore Updates**: Added `.cursor/mcp.json` to `.gitignore`

### 📚 Documentation

- **Installation Instructions**: Streamlined and improved MCP server installation instructions

## [0.5.0] - 2026-01-14

### ✨ Added

- **MCP Server Integration**: Built-in Model Context Protocol server for AI assistant integration (Cursor, Claude Desktop, etc.)
- **FastMCP Integration**: Complete FastMCP integration as a core dependency
- **CLI Functionality**: Command-line interface for running the MCP server
- **Dynamic Version Retrieval**: Version now dynamically retrieved from `pyproject.toml`

### 🔧 Changed

- **Tool Architecture**: Transitioned from ~132 individual tools to 22 module-based tools
- **Project Name**: Changed package name from `testrail_api_module` to `testrail-api-module` for PyPI consistency
- **Dependency Organization**: Reorganized dependencies with clearer separation between runtime and development dependencies

### 📚 Documentation

- **MCP Usage Guide**: New comprehensive guide for using the MCP server
- **README Updates**: Enhanced documentation with MCP installation instructions

### 🔄 Maintenance

- Updated license year to 2026
- Removed legacy `requirements.txt` in favor of `pyproject.toml`
- Cleaned up outdated test scripts

## [0.4.0] - 2024-12-19

### 🚨 Breaking Changes

- **Exception Handling**: Methods now raise specific exceptions instead of returning `None`
- **Return Types**: Consistent return types - no more `Optional` wrappers
- **Method Signatures**: Updated parameter handling for better type safety

### ✨ Added

- **Enhanced Error Handling**: Comprehensive exception hierarchy (`TestRailAPIError`, `TestRailAuthenticationError`, `TestRailRateLimitError`, `TestRailAPIException`)
- **Performance Improvements**: HTTP session with connection pooling, automatic retry logic, configurable request timeouts
- **Better Type Safety**: Comprehensive type annotations throughout
- **Migration Guide**: Complete migration guide for upgrading from v0.3.x

### 🔧 Changed

- **Base API Client**: Complete rewrite with modern patterns
- **Authentication**: Streamlined authentication with proper validation
- **Parameter Handling**: Consistent parameter handling across all modules

### 🐛 Fixed

- **URL Construction**: Proper URL encoding and parameter handling
- **Session Management**: Proper HTTP session management with connection pooling

### 🔄 Migration Required

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
