#!/usr/bin/env python3
"""
Test script for the deployment script.

This script tests the individual functions without performing actual deployment.
"""

import sys
import os

# Add the utilities directory to the path so we can import deploy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deploy import (
    get_current_version,
    check_git_status,
    Colors,
    print_header,
    print_success,
    print_info,
)


def test_version_parsing():
    """Test version parsing functionality."""
    print_header("Testing Version Parsing")

    try:
        version = get_current_version()
        print_success(f"Current version: {version}")
        return True
    except Exception as e:
        print(f"❌ Version parsing failed: {e}")
        return False


def test_git_status():
    """Test git status checking."""
    print_header("Testing Git Status")

    try:
        is_clean = check_git_status()
        if is_clean:
            print_success("Git repository is clean")
        else:
            print_info(
                "Git repository has uncommitted changes (expected in development)"
            )
        return True
    except Exception as e:
        print(f"❌ Git status check failed: {e}")
        return False


def main():
    """Run all tests."""
    print_header("Deployment Script Tests")

    tests = [
        test_version_parsing,
        test_git_status,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print_header("Test Results")
    print_success(f"Passed: {passed}/{total}")

    if passed == total:
        print_success("All tests passed! Deployment script is ready to use.")
    else:
        print("Some tests failed. Please check the deployment script.")


if __name__ == "__main__":
    main()
