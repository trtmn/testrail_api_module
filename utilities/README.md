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
