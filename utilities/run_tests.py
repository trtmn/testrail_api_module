#!/usr/bin/env python3
"""
Test runner script for testrail_api_module.

This script provides an easy way to run tests with various options.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_tests(verbose: bool = False, coverage: bool = False, specific_test: str | None = None) -> subprocess.CompletedProcess[bytes]:
    """Run the test suite with the specified options."""
    # Get the project root directory (utilities/../)
    project_root = Path(__file__).parent.parent

    cmd = [sys.executable, "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=src/testrail_api_module", "--cov-report=term-missing"])

    if specific_test:
        cmd.append(specific_test)

    print(f"Running tests with command: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=project_root)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run tests for testrail_api_module")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Run tests in verbose mode"
    )
    parser.add_argument(
        "-c", "--coverage", action="store_true", help="Run tests with coverage report"
    )
    parser.add_argument(
        "-t", "--test", type=str, help="Run a specific test file or test function"
    )

    # If no arguments are provided, default to verbose mode
    if len(sys.argv) == 1:
        args = parser.parse_args(["-v"])
    else:
        args = parser.parse_args()

    result = run_tests(
        verbose=args.verbose, coverage=args.coverage, specific_test=args.test
    )

    sys.exit(result.returncode)
