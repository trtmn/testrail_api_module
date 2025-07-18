# Utilities

This directory contains utility scripts for development and deployment of the TestRail API Module.

## Scripts

### `deploy.py`
Interactive deployment script that automates the entire build and publish process.

**Features:**
- ✅ Git status checking
- ✅ Test suite execution
- ✅ Interactive version bumping
- ✅ Package building and verification
- ✅ Test PyPI publishing (optional)
- ✅ Production PyPI publishing (optional)
- ✅ Git push and tagging (optional)

**Usage:**
```bash
python utilities/deploy.py
```

### `test_deploy.py`
Test script to verify the deployment script functions work correctly without performing actual deployment actions.

**Usage:**
```bash
python utilities/test_deploy.py
```

### `generate_docs.py`
Script to generate documentation for the project.

**Usage:**
```bash
python utilities/generate_docs.py
```

### `run_tests.py`
Script to run tests with various options and configurations.

**Usage:**
```bash
python utilities/run_tests.py
```

## Quick Start

1. **Test the deployment script:**
   ```bash
   python utilities/test_deploy.py
   ```

2. **Run a full deployment:**
   ```bash
   python utilities/deploy.py
   ```

3. **Generate documentation:**
   ```bash
   python utilities/generate_docs.py
   ```

## Requirements

All scripts require the development environment to be set up as described in the main `dev-readme.md`.

## Troubleshooting

If you encounter issues with any script:

1. Ensure you're in the project root directory
2. Activate the virtual environment
3. Check that all dependencies are installed
4. Run the test script to verify functionality

For more detailed troubleshooting, see the main `dev-readme.md`. 