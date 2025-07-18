# Developer Guide - TestRail API Module

This guide explains how to set up the development environment, build, test, and deploy the `testrail_api_module` package.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Building](#building)
- [Deployment](#deployment)
- [Version Management](#version-management)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.11 or higher
- Git
- pip (latest version)
- Access to PyPI (for deployment)

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/trtmn/testrail_api_module.git
cd testrail_api_module
```

### 2. Create Virtual Environment

```bash
# Create virtual environment in project root
python3.11 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

**Note:** This project uses `.venv` as the virtual environment directory. If you see other virtual environments (like `.venv311` or `.venv38`), you can use those instead:

```bash
# If .venv311 exists (Python 3.11 environment)
source .venv311/bin/activate

# If .venv38 exists (Python 3.8 environment)
source .venv38/bin/activate
```

### 3. Install Development Dependencies

```bash
# Install build tools and development dependencies
pip install -r requirements.txt

# Or install directly from pyproject.toml
pip install -e ".[dev]"
```

### 4. Verify Setup

```bash
# Check that all tools are available
python -c "import pytest; print('pytest:', pytest.__version__)"
python -c "import build; print('build:', build.__version__)"
python -c "import twine; print('twine:', twine.__version__)"
```

## Testing

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=testrail_api_module --cov-report=term-missing

# Run tests for specific module
pytest tests/test_base.py -v
```

**Note:** Some test files may be missing if they were deleted. The current test suite includes:
- `tests/test_results.py` - Tests for the ResultsAPI module
- Additional test files can be created following the same patterns

### Test Coverage

```bash
# Generate coverage report
pytest tests/ --cov=testrail_api_module --cov-report=html

# View coverage report (opens in browser)
open htmlcov/index.html
```

### Linting and Type Checking

```bash
# Run mypy for type checking
mypy src/testrail_api_module/

# Run flake8 for linting (if installed)
flake8 src/ tests/
```

## Building

### 1. Clean Previous Builds

```bash
# Remove previous build artifacts
rm -rf dist/ build/ src/*.egg-info/
```

### 2. Build Package

```bash
# Build source distribution and wheel
python -m build

# Verify the build artifacts
ls -la dist/
```

This will create:
- `dist/testrail_api_module-{version}.tar.gz` - Source distribution
- `dist/testrail_api_module-{version}-py3-none-any.whl` - Wheel distribution

### 3. Verify Build

```bash
# Check the built package
twine check dist/*

# Install the built package in a test environment
pip install dist/testrail_api_module-{version}-py3-none-any.whl
```

## Deployment

### 1. Test PyPI (Recommended First Step)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ testrail-api-module
```

### 2. Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

**Note:** You'll need PyPI credentials. You can either:
- Use username/password when prompted
- Set up API tokens in `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

### 3. Verify Deployment

```bash
# Check that the package is available
pip install testrail-api-module --upgrade

# Test import
python -c "from testrail_api_module import TestRailAPI; print('Package installed successfully!')"
```

## Version Management

### Using bump-my-version

The project uses `bump-my-version` for version management:

```bash
# Bump patch version (0.2.0 -> 0.2.1)
bump-my-version bump patch

# Bump minor version (0.2.0 -> 0.3.0)
bump-my-version bump minor

# Bump major version (0.2.0 -> 1.0.0)
bump-my-version bump major

# Show current version
bump-my-version show
```

This will:
- Update version in `pyproject.toml`
- Update version in `src/testrail_api_module/__init__.py`
- Create a git commit with the version change
- Create a git tag for the new version

### Manual Version Update

If you need to update version manually:

1. Update `pyproject.toml`:
   ```toml
   [project]
   version = "0.2.1"
   ```

2. Update `src/testrail_api_module/__init__.py`:
   ```python
   __version__ = "0.2.1"
   ```

3. Commit and tag:
   ```bash
   git add .
   git commit -m "Bump version: 0.2.0 → 0.2.1"
   git tag v0.2.1
   ```

## Documentation

### Generate Documentation

```bash
# Generate HTML documentation
pdoc --html src/testrail_api_module --output-dir docs

# Generate documentation for specific module
pdoc --html src/testrail_api_module/base.py --output-dir docs
```

### View Documentation

```bash
# Open documentation in browser
open docs/testrail_api_module.html
```

## Interactive Deployment Script

For convenience, we've created an interactive deployment script that automates the entire process:

```bash
# Run the interactive deployment script
python utilities/deploy.py
```

This script will:
1. ✅ Check git status (ensures clean repository)
2. ✅ Run all tests
3. ✅ Interactive version bump (patch/minor/major)
4. ✅ Build the package
5. ✅ Test package installation
6. ✅ Optionally publish to Test PyPI
7. ✅ Optionally publish to production PyPI
8. ✅ Optionally push changes to git

### Testing the Deployment Script

You can test the deployment script without actually deploying:

```bash
python utilities/test_deploy.py
```

## Manual Build and Deploy Workflow

If you prefer to do it manually, here's the complete workflow:

```bash
# 1. Ensure you're on main branch and up to date
git checkout main
git pull origin main

# 2. Run tests to ensure everything works
pytest tests/ -v

# 3. Bump version
bump-my-version bump patch  # or minor/major

# 4. Clean previous builds
rm -rf dist/ build/ src/*.egg-info/

# 5. Build package
python -m build

# 6. Check build artifacts
twine check dist/*

# 7. Test on Test PyPI (optional but recommended)
twine upload --repository testpypi dist/*

# 8. Deploy to production PyPI
twine upload dist/*

# 9. Push changes and tags
git push origin main
git push --tags
```

## Troubleshooting

### Common Issues

#### Build Errors

```bash
# If you get build errors, ensure you have the latest build tools
pip install --upgrade build wheel setuptools

# Clean and rebuild
rm -rf dist/ build/ src/*.egg-info/
python -m build
```

#### License Deprecation Warning

You may see a deprecation warning about `project.license` as a TOML table. This is expected and will be fixed in a future update. The warning doesn't affect the build process.

To fix this warning, update `pyproject.toml`:
```toml
# Change from:
license = { file = "LICENSE" }

# To:
license = "MIT"
license-files = { paths = ["LICENSE"] }
```

#### Upload Errors

```bash
# If upload fails, check your credentials
twine check dist/*

# Verify you have the right permissions on PyPI
# Make sure you're using the correct repository URL
```

#### Import Errors After Installation

```bash
# If the package doesn't import correctly after installation
pip uninstall testrail-api-module
pip install testrail-api-module --no-cache-dir

# Check the installed package
pip show testrail-api-module
```

#### Version Conflicts

```bash
# If you have version conflicts, check installed packages
pip list | grep testrail

# Remove conflicting packages
pip uninstall testrail-api-module
```

### Environment Variables

You can set these environment variables for automation:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-pypi-token
export TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/
```

### CI/CD Integration

For GitHub Actions or other CI systems, you can use this workflow:

```yaml
# Example GitHub Actions workflow
- name: Build and Deploy
  run: |
    python -m build
    twine check dist/*
    twine upload dist/*
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

### Deployment Script Issues

If the interactive deployment script fails:

```bash
# Test the script components
python utilities/test_deploy.py

# Check if all required tools are installed
python -c "import subprocess, shutil; print('All dependencies available')"

# Run with verbose output
python utilities/deploy.py 2>&1 | tee deploy.log
```

## Development Best Practices

1. **Always run tests before building**
2. **Use Test PyPI for testing deployments**
3. **Keep version numbers consistent across all files**
4. **Tag releases in git**
5. **Update documentation after significant changes**
6. **Use virtual environments for development**

## Support

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/trtmn/testrail_api_module/issues)
2. Review the [PyPI documentation](https://packaging.python.org/)
3. Check the [twine documentation](https://twine.readthedocs.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 