# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python wrapper for the TestRail REST API (`testrail-api-module` on PyPI). Requires Python 3.11+. Uses `uv` as the package/venv manager.

## Branching Strategy

This project uses a git-flow workflow with issue-linked branches.

### Before starting work

Every piece of work must have an associated GitHub issue. If one doesn't exist, create it first with `gh issue create`. This ensures all changes are tracked and linked.

### Branches

- **`main`** — production releases only, protected branch
- **`development`** — integration branch, all feature work merges here
- **Feature/fix branches** — branch from `development`, PR back to `development`
- **Releases** — PR from `development` → `main` (merge triggers automatic tagging + PyPI publish)

Branch names must include the issue number so GitHub auto-links them:

```
<issue-number>-short-description
```

Examples: `81-require-issue-branch-naming`, `42-fix-auth-bug`, `15-add-milestones-api`

Always work on `development` or a feature branch. Never commit directly to `main`.

## Commands

```bash
# Install dev dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run tests across all supported Python versions (3.11, 3.12, 3.13)
tox

# Run a single test file or test
uv run pytest tests/test_cases.py
uv run pytest tests/test_cases.py::TestCasesAPI::test_get_case

# Type check
uv run mypy src/

# Lint and format
uv run ruff check . --fix
uv run ruff format .

# Run pre-commit hooks
pre-commit run --all-files

# Generate docs
uv run python utilities/generate_docs.py
```

## Architecture

### API Wrapper Pattern

`TestRailAPI` (in `__init__.py`) is the entry point. It instantiates 23 submodule APIs as attributes, passing `self` as the client:

```
api = TestRailAPI(base_url=..., username=..., api_key=...)
api.cases.get_case(123)        # CasesAPI
api.runs.add_run(...)          # RunsAPI
api.results.add_result(...)    # ResultsAPI
```

### BaseAPI (`base.py`)

All 23 submodules inherit from `BaseAPI`, which provides:

- `_get(endpoint, params)` / `_post(endpoint, data)` — HTTP helpers with Basic Auth
- `requests.Session` with connection pooling and retry on 429/5xx (3 retries, backoff=1)
- URL construction: `<base_url>/index.php?/api/v2/<endpoint>`
- Response handling that maps HTTP status codes to the exception hierarchy

DELETE operations in TestRail use POST and return empty bodies — `_handle_response` returns `{}` for these.

### Exception Hierarchy

```
TestRailAPIError                    # base
├── TestRailAuthenticationError     # 401
├── TestRailRateLimitError          # 429
└── TestRailAPIException            # other 4xx/5xx (has .status_code, .response_text)
```

Methods never return `None` — they raise on failure.

### Submodule Pattern

Every submodule follows this structure:

- Class inherits `BaseAPI`, accepts client in `__init__`
- GET methods call `self._get(endpoint, params={})`
- POST methods build a `data` dict (excluding `None` values) and call `self._post(endpoint, data=data)`
- Each file declares `__all__ = ['<ClassName>API']`

### Type Stubs

Every `.py` has a matching `.pyi` stub. The package ships `py.typed` (PEP 561). Stubs are included via `pyproject.toml` package-data config.

### CasesAPI — Most Complex Module

`cases.py` adds field caching, required field discovery (`get_required_case_fields`), custom field normalization/validation, and context resolution from section IDs. Custom fields use `system_name` keys (e.g., `custom_automation_type`) and are passed via `custom_fields={}` parameter.

## Test Conventions

Tests live in `tests/` with one file per module. The authoritative reference is `tests/test-writing-standards.mdc`. Key rules:

- **Mocking**: Always `patch.object(api_instance, '_get'/'_post')`. Never make real HTTP calls.
- **Assertions**: Always assert both the mock call args AND the return value.
- **Required tests per method**: init, minimal params, all params, None values, error handling (APIError, AuthError, RateLimitError).
- **Type annotations**: All test methods must have `-> None` and docstrings.
- **Fixtures**: Every class needs `mock_client`, `<module>_api`, and optionally `sample_<entity>_data`.

## Versioning

Use `uv version` for all version operations:

```bash
# Check current version
uv version --short

# Bump version (patch, minor, major)
uv version --bump patch   # 0.6.1 → 0.6.2
uv version --bump minor   # 0.6.1 → 0.7.0
uv version --bump major   # 0.6.1 → 1.0.0

# Set explicit version
uv version 0.7.0
```

## Changelog

`CHANGELOG.md` must be updated whenever code changes are made. Add entries under `## [Unreleased]` at the top of the file. Use [Keep a Changelog](https://keepachangelog.com/) categories: `### ✨ Added`, `### 🔧 Changed`, `### 🐛 Fixed`, `### 🚨 Breaking Changes`, `### 🔄 Maintenance`. Entries are ordered newest version first. When releasing, the `[Unreleased]` section gets renamed to the version number.

## Code Style

- **Line length**: 79 chars (ruff)
- **Quotes**: Double quotes
- **Target**: Python 3.11
- **Linter rules**: E, W, F, I (isort), B (bugbear), C4, UP (pyupgrade)
