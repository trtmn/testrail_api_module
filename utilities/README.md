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

Updates the version using bump-my-version for both pyproject.toml and __init__.py files.

**Features:**

- Uses bump-my-version for consistent version management
- Updates both pyproject.toml and __init__.py files
- Supports patch, minor, and major version bumps
- Includes dry-run mode for testing changes
- Auto-installs bump-my-version if not present

**Usage:**

```bash
# Show current version
python utilities/update_version.py show

# Bump patch version (0.3.0 -> 0.3.1)
python utilities/update_version.py patch

# Bump minor version (0.3.0 -> 0.4.0)
python utilities/update_version.py minor

# Bump major version (1.0.0 -> 2.0.0)
python utilities/update_version.py major

# Dry run to see what would change
python utilities/update_version.py patch --dry-run
```

### `generate_stubs.py`

Generates library stubs (.pyi files) for the TestRail API module using stubgen.

**Features:**

- Automatically generates type stubs for all modules
- Improves generated stubs with better type annotations
- Creates py.typed file for typing support
- Updates pyproject.toml with mypy configuration
- Adds stubgen to development dependencies

**Usage:**

```bash
python utilities/generate_stubs.py
```

### `run_tests.py`

Runs the test suite for the project.

**Usage:**

```bash
python utilities/run_tests.py
```

## Version Management

The project uses `bump-my-version` for version management. When you bump the version:

1. `pyproject.toml` is updated
2. `src/testrail_api_module/__init__.py` is updated automatically
3. Documentation can be regenerated to show the new version

**To bump version:**

```bash
# Using the utility script (recommended)
python utilities/update_version.py patch   # for bug fixes
python utilities/update_version.py minor   # for new features
python utilities/update_version.py major   # for breaking changes

# Or using bump-my-version directly
bump-my-version bump patch
bump-my-version bump minor
bump-my-version bump major
```

**To show current version:**

```bash
python utilities/update_version.py show
```

**To regenerate documentation with new version:**

```bash
python utilities/generate_docs.py
```

## Type Checking and Stubs

The project includes library stubs (.pyi files) for better IDE support and static type checking.

**To generate/regenerate stubs:**

```bash
python utilities/generate_stubs.py
```

**To check types with mypy:**

```bash
mypy src/testrail_api_module
```

**Stub files included:**

- All `.pyi` files in `src/testrail_api_module/` (inline stubs)
- `py.typed` file for typing support
- Mypy configuration in `pyproject.toml`
