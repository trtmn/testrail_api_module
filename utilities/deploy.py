#!/usr/bin/env python3
"""
Interactive deployment script for testrail_api_module.

This script automates the process of:
1. Bumping version (patch/minor/major)
2. Building the package
3. Optionally publishing to PyPI

Usage:
    python utilities/deploy.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(text: str) -> None:
    """Print a header with color."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print("=" * len(text))


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")


def run_command(
    command: str, check: bool = True, capture_output: bool = False
) -> Tuple[int, str, str]:
    """Run a shell command and return the result."""
    print(f"{Colors.OKCYAN}Running: {command}{Colors.ENDC}")

    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=capture_output, text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout or "", e.stderr or ""


def get_current_version() -> str:
    """Get the current version from bump-my-version."""
    returncode, stdout, stderr = run_command(
        "bump-my-version show", capture_output=True
    )
    if returncode != 0:
        print_error(f"Failed to get current version: {stderr}")
        sys.exit(1)

    # Parse the output to extract version
    for line in stdout.split("\n"):
        if "'current_version':" in line:
            version = line.split("'")[-2]
            return version

    print_error("Could not parse current version")
    sys.exit(1)


def check_git_status() -> bool:
    """Check if git repository is clean."""
    returncode, stdout, stderr = run_command(
        "git status --porcelain", capture_output=True
    )
    if returncode != 0:
        print_error(f"Failed to check git status: {stderr}")
        return False

    if stdout.strip():
        print_warning("Git repository has uncommitted changes:")
        print(stdout)
        return False

    return True


def run_tests() -> bool:
    """Run the test suite."""
    print_header("Running Tests")

    returncode, stdout, stderr = run_command("python -m pytest tests/ -v")
    if returncode != 0:
        print_error("Tests failed!")
        print(stderr)
        return False

    print_success("All tests passed!")
    return True


def bump_version() -> str:
    """Bump the version and return the new version."""
    print_header("Version Bump")

    print("Select version bump type:")
    print("1. Patch (0.2.0 → 0.2.1) - Bug fixes")
    print("2. Minor (0.2.0 → 0.3.0) - New features")
    print("3. Major (0.2.0 → 1.0.0) - Breaking changes")

    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == "1":
            bump_type = "patch"
            break
        elif choice == "2":
            bump_type = "minor"
            break
        elif choice == "3":
            bump_type = "major"
            break
        else:
            print_error("Invalid choice. Please enter 1, 2, or 3.")

    current_version = get_current_version()
    print_info(f"Current version: {current_version}")

    # Confirm the bump
    confirm = input(f"\nBump version to {bump_type}? (y/N): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print_info("Version bump cancelled.")
        sys.exit(0)

    # Run the bump command
    returncode, stdout, stderr = run_command(f"bump-my-version bump {bump_type}")
    if returncode != 0:
        print_error(f"Failed to bump version: {stderr}")
        sys.exit(1)

    # Get the new version
    new_version = get_current_version()
    print_success(f"Version bumped to {new_version}")

    return new_version


def build_package() -> bool:
    """Build the package."""
    print_header("Building Package")

    # Clean previous builds
    print_info("Cleaning previous builds...")
    for path in ["dist", "build", "src/*.egg-info"]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    # Build the package
    returncode, stdout, stderr = run_command("python -m build")
    if returncode != 0:
        print_error("Build failed!")
        print(stderr)
        return False

    print_success("Package built successfully!")

    # Check the build artifacts
    print_info("Checking build artifacts...")
    returncode, stdout, stderr = run_command("twine check dist/*")
    if returncode != 0:
        print_error("Build artifacts check failed!")
        print(stderr)
        return False

    print_success("Build artifacts verified!")

    # Show the built files
    dist_files = list(Path("dist").glob("*"))
    print_info("Built files:")
    for file in dist_files:
        print(f"  - {file.name}")

    return True


def test_install() -> bool:
    """Test installing the built package."""
    print_header("Testing Package Installation")

    # Find the wheel file
    wheel_files = list(Path("dist").glob("*.whl"))
    if not wheel_files:
        print_error("No wheel file found!")
        return False

    wheel_file = wheel_files[0]
    print_info(f"Testing installation of {wheel_file.name}")

    # Test install
    returncode, stdout, stderr = run_command(f"pip install {wheel_file}")
    if returncode != 0:
        print_error("Test installation failed!")
        print(stderr)
        return False

    # Test import
    returncode, stdout, stderr = run_command(
        "python -c \"from testrail_api_module import TestRailAPI; print('✅ Package imports successfully!')\""
    )
    if returncode != 0:
        print_error("Test import failed!")
        print(stderr)
        return False

    print_success("Package installation and import test passed!")

    # Uninstall test installation
    returncode, stdout, stderr = run_command("pip uninstall testrail-api-module -y")

    return True


def publish_to_testpypi() -> bool:
    """Publish to Test PyPI."""
    print_header("Publishing to Test PyPI")

    confirm = input("Publish to Test PyPI? (y/N): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print_info("Test PyPI publishing skipped.")
        return True

    returncode, stdout, stderr = run_command(
        "twine upload --repository testpypi dist/*"
    )
    if returncode != 0:
        print_error("Failed to publish to Test PyPI!")
        print(stderr)
        return False

    print_success("Published to Test PyPI successfully!")

    # Test installation from Test PyPI
    test_install = input("Test installation from Test PyPI? (y/N): ").strip().lower()
    if test_install in ["y", "yes"]:
        print_info("Testing installation from Test PyPI...")
        returncode, stdout, stderr = run_command(
            "pip install --index-url https://test.pypi.org/simple/ testrail-api-module"
        )
        if returncode != 0:
            print_warning("Test PyPI installation failed, but continuing...")
        else:
            print_success("Test PyPI installation successful!")
            # Clean up
            run_command("pip uninstall testrail-api-module -y")

    return True


def publish_to_pypi() -> bool:
    """Publish to production PyPI."""
    print_header("Publishing to Production PyPI")

    print_warning("This will publish to the production PyPI repository!")
    print_warning("Make sure you have the correct credentials configured.")

    confirm = input("Publish to production PyPI? (y/N): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print_info("Production PyPI publishing skipped.")
        return True

    returncode, stdout, stderr = run_command("twine upload dist/*")
    if returncode != 0:
        print_error("Failed to publish to production PyPI!")
        print(stderr)
        return False

    print_success("Published to production PyPI successfully!")

    return True


def push_to_git() -> bool:
    """Push changes and tags to git."""
    print_header("Pushing to Git")

    confirm = input("Push changes and tags to git? (y/N): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print_info("Git push skipped.")
        return True

    # Push changes
    returncode, stdout, stderr = run_command("git push origin main")
    if returncode != 0:
        print_error("Failed to push changes!")
        print(stderr)
        return False

    # Push tags
    returncode, stdout, stderr = run_command("git push --tags")
    if returncode != 0:
        print_error("Failed to push tags!")
        print(stderr)
        return False

    print_success("Changes and tags pushed to git successfully!")
    return True


def main():
    """Main deployment function."""
    print_header("TestRail API Module Deployment")

    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print_error(
            "pyproject.toml not found. Please run this script from the project root."
        )
        sys.exit(1)

    # Check git status
    if not check_git_status():
        print_warning("Please commit or stash your changes before deploying.")
        sys.exit(1)

    # Run tests
    if not run_tests():
        print_error("Deployment aborted due to test failures.")
        sys.exit(1)

    # Bump version
    new_version = bump_version()

    # Build package
    if not build_package():
        print_error("Deployment aborted due to build failures.")
        sys.exit(1)

    # Test installation
    if not test_install():
        print_error("Deployment aborted due to installation test failures.")
        sys.exit(1)

    # Publish to Test PyPI
    if not publish_to_testpypi():
        print_error("Deployment aborted due to Test PyPI publishing failures.")
        sys.exit(1)

    # Publish to production PyPI
    if not publish_to_pypi():
        print_error("Deployment aborted due to production PyPI publishing failures.")
        sys.exit(1)

    # Push to git
    if not push_to_git():
        print_error("Deployment aborted due to git push failures.")
        sys.exit(1)

    print_header("Deployment Complete!")
    print_success(f"Version {new_version} has been successfully deployed!")
    print_info("Package is now available on PyPI.")
    print_info("Documentation will be updated automatically.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
