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

# Bump version (1=patch, 2=minor, 3=major)
python utilities/update_version.py bump 1  # patch (0.3.0 -> 0.3.1)
python utilities/update_version.py bump 2  # minor (0.3.0 -> 0.4.0)
python utilities/update_version.py bump 3  # major (1.0.0 -> 2.0.0)

# Dry run to see what would change
python utilities/update_version.py bump 1 --dry-run
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

### `build.py`

Comprehensive build script that handles the entire build process with interactive prompts.

**Features:**

- Interactive prompts for version updates, tests, documentation, and stubs
- **Automatic doc/stub regeneration when version is updated**
- Pretty output using Rich library
- Progress indicators for long-running tasks
- Automatic dependency checking
- Build artifact cleaning
- Package building with build
- Build summary with artifact details

**Usage:**

```bash
# Interactive mode (default)
python utilities/build.py

# Non-interactive mode (for CI/CD)
python utilities/build.py --non-interactive

# Skip specific steps
python utilities/build.py --skip-tests --skip-docs --skip-stubs

# Show help
python utilities/build.py --help
```

**Command-line options:**

- `--non-interactive`: Run without prompts (useful for CI/CD)
- `--skip-tests`: Skip running tests
- `--skip-docs`: Skip generating documentation
- `--skip-stubs`: Skip generating type stubs
- `--skip-version`: Skip version update prompts

**What it does:**

1. Checks all required dependencies
2. Prompts for version updates (using update_version.py)
3. **Automatically regenerates docs and stubs if version was updated**
4. Optionally runs tests
5. Optionally generates documentation (if not already done due to version update)
6. Optionally generates type stubs (if not already done due to version update)
7. Cleans previous build artifacts
8. Builds the package
9. Shows a summary of generated artifacts

## Dependencies

This project uses a clean separation of dependencies:

### Runtime Dependencies (for consumers)
- `requests>=2.32.0` - HTTP client for API calls

### Development Dependencies (for developers)
- `pdoc>=14.0.0` - Documentation generation
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-mock>=3.10.0` - Mocking for tests
- `mypy>=1.0.0` - Type checking and stub generation (includes `stubgen`)
- `bump-my-version>=1.0.0` - Version management
- `rich>=13.0.0` - Rich terminal output
- `click>=8.0.0` - CLI framework
- `wheel>=0.40.0` - Package building
- `build>=1.0.0` - Package building
- `toml>=0.10.0` - TOML file handling
- `python-dotenv>=1.0.0` - Environment variable management

**Installation:**
```bash
# For consumers (runtime only)
pip install testrail-api-module

# For developers (with all dev tools)
pip install -e .[dev]
```

## Version Management

The project uses `bump-my-version` for version management. When you bump the version:

1. `pyproject.toml` is updated
2. `src/testrail_api_module/__init__.py` is updated automatically
3. Documentation can be regenerated to show the new version

**To bump version:**

```bash
# Using the utility script (recommended)
python utilities/update_version.py bump 1  # for bug fixes (patch)
python utilities/update_version.py bump 2  # for new features (minor)
python utilities/update_version.py bump 3  # for breaking changes (major)

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
