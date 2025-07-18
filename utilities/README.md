# Utilities

This directory contains utility scripts for managing the TestRail API module.

## Scripts

### `generate_docs.py`

Generates documentation for the TestRail API module using pdoc.

**Features:**

- Automatically includes current version information
- Creates a temporary version file for documentation
- Cleans up temporary files after generation
- Uses pdoc configuration from `pdoc.yaml`

**Usage:**

```bash
python utilities/generate_docs.py
```

### `update_version.py`

Updates the version in the module's `__init__.py` file.

**Features:**

- Validates version format (x.y.z)
- Updates `__version__` in the main module
- Called automatically by bumpversion

**Usage:**

```bash
python utilities/update_version.py 0.3.0
```

### `run_tests.py`

Runs the test suite for the project.

**Usage:**

```bash
python utilities/run_tests.py
```

## Version Management

The project uses `bumpversion` for version management. When you bump the version:

1. `pyproject.toml` is updated
2. `src/testrail_api_module/__init__.py` is updated automatically
3. Documentation can be regenerated to show the new version

**To bump version:**

```bash
bumpversion patch  # for bug fixes
bumpversion minor  # for new features
bumpversion major  # for breaking changes
```

**To regenerate documentation with new version:**

```bash
python utilities/generate_docs.py
```
