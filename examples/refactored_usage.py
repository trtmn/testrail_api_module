#!/usr/bin/env python3
"""
Example script demonstrating the refactored TestRail API module usage.

This script shows how to use the improved TestRail API module with proper
error handling, type safety, and following official TestRail API patterns.
"""

from testrail_api_module import (
    TestRailAPI,
    TestRailAPIError,
    TestRailAuthenticationError,
)
import os
import sys

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def main() -> None:
    """Main function demonstrating the refactored TestRail API usage."""

    # Configuration - replace with your actual TestRail instance details
    BASE_URL = "https://your-instance.testrail.io"
    USERNAME = "your-email@example.com"
    API_KEY = "your-api-key"  # Or use password instead

    try:
        # Initialize the TestRail API client with improved error handling
        api = TestRailAPI(
            base_url=BASE_URL,
            username=USERNAME,
            api_key=API_KEY,
            timeout=30  # Request timeout in seconds
        )

        print("✅ TestRail API client initialized successfully")

        # Example 1: Get all projects
        print("\n📋 Getting all projects...")
        try:
            projects = api.projects.get_projects()
            print(f"Found {len(projects)} projects:")
            for project in projects:
                print(f"  - {project['name']} (ID: {project['id']})")
        except TestRailAPIError as e:
            print(f"❌ Error getting projects: {e}")
            return

        # Example 2: Get test cases for a project (if projects exist)
        if projects:
            project_id = projects[0]['id']
            print(f"\n🧪 Getting test cases for project {project_id}...")
            try:
                cases = api.cases.get_cases(
                    project_id=project_id,
                    limit=10  # Limit results for demo
                )
                print(f"Found {len(cases)} test cases:")
                for case in cases[:5]:  # Show first 5 cases
                    print(f"  - {case['title']} (ID: {case['id']})")
            except TestRailAPIError as e:
                print(f"❌ Error getting test cases: {e}")

        # Example 3: Create a test case (if we have a project and sections)
        if projects:
            project_id = projects[0]['id']
            print(f"\n➕ Creating a test case in project {project_id}...")
            try:
                # First, get suites to find a section
                suites = api.suites.get_suites(project_id=project_id)
                if suites:
                    suite_id = suites[0]['id']
                    sections = api.sections.get_sections(
                        project_id=project_id, suite_id=suite_id)
                    if sections:
                        section_id = sections[0]['id']

                        new_case = api.cases.add_case(
                            section_id=section_id,
                            title="API Test Case - Refactored Module Demo",
                            type_id=2,  # Functional test
                            priority_id=2,  # High priority
                            description="This test case was created using the refactored TestRail API module",
                            preconditions="TestRail API access is available",
                            postconditions="Test case is created and visible in TestRail"
                        )
                        print(
                            f"✅ Created test case: {
                                new_case['title']} (ID: {
                                new_case['id']})")
                    else:
                        print("⚠️  No sections found in the first suite")
                else:
                    print("⚠️  No suites found in the project")
            except TestRailAPIError as e:
                print(f"❌ Error creating test case: {e}")

        # Example 4: Demonstrate error handling
        print("\n🛡️  Demonstrating error handling...")

        # Test with invalid credentials
        try:
            invalid_api = TestRailAPI(
                base_url=BASE_URL,
                username="invalid@example.com",
                api_key="invalid-key"
            )
            invalid_api.projects.get_projects()
        except TestRailAuthenticationError as e:
            print(f"✅ Authentication error handled correctly: {e}")
        except TestRailAPIError as e:
            print(f"✅ General API error handled correctly: {e}")

        # Example 5: Demonstrate bulk operations
        print("\n📦 Demonstrating bulk operations...")
        if projects:
            project_id = projects[0]['id']
            try:
                # Create a test run
                test_run = api.runs.add_run(
                    project_id=project_id,
                    name="API Module Refactoring Demo Run",
                    description="Test run created by the refactored API module",
                    include_all=True)
                print(
                    f"✅ Created test run: {
                        test_run['name']} (ID: {
                        test_run['id']})")

                # Add multiple results at once
                # Note: This will only work if there are actual test cases in the run
                # results_data = [
                #     {
                #         "case_id": 1,
                #         "status_id": 1,  # Passed
                #         "comment": "Test passed using refactored API",
                #         "elapsed": "30s"
                #     },
                #     {
                #         "case_id": 2,
                #         "status_id": 5,  # Failed
                #         "comment": "Test failed - demo result",
                #         "elapsed": "45s"
                #     }
                # ]
                # results = api.results.add_results_for_cases(
                #     run_id=test_run['id'],
                #     results=results_data
                # )
                # print(f"✅ Added {len(results_data)} test results")

            except TestRailAPIError as e:
                print(f"❌ Error with bulk operations: {e}")

        print("\n🎉 Demo completed successfully!")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
