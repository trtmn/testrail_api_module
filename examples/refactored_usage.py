#!/usr/bin/env python3
"""
Example script demonstrating the refactored TestRail API module usage.

This script shows how to use the improved TestRail API module with proper
error handling, type safety, and following official TestRail API patterns.
"""

from typing import Any

from testrail_api_module import (
    TestRailAPI,
    TestRailAPIError,
    TestRailAuthenticationError,
)


def unwrap(response: Any, key: str) -> list[dict[str, Any]]:
    """Unwrap a TestRail pagination envelope into a plain list.

    Current TestRail versions return bulk GET results wrapped in a
    pagination envelope, e.g. ``{"offset": 0, "limit": 250, "size": 1,
    "_links": {...}, "projects": [...]}``. Older versions return a
    plain list. This handles both.
    """
    if isinstance(response, dict):
        return response.get(key, response)
    return response


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
            timeout=30,  # Request timeout in seconds
        )

        print("✅ TestRail API client initialized successfully")

        # Example 1: Get all projects
        print("\n📋 Getting all projects...")
        try:
            projects = unwrap(api.projects.get_projects(), "projects")
            print(f"Found {len(projects)} projects:")
            for project in projects:
                print(f"  - {project['name']} (ID: {project['id']})")
        except TestRailAPIError as e:
            print(f"❌ Error getting projects: {e}")
            return

        # Example 2: Get test cases for a project (if projects exist)
        if projects:
            project_id = projects[0]["id"]
            print(f"\n🧪 Getting test cases for project {project_id}...")
            try:
                cases = unwrap(
                    api.cases.get_cases(
                        project_id=project_id,
                        limit=10,  # Limit results for demo
                    ),
                    "cases",
                )
                print(f"Found {len(cases)} test cases:")
                for case in cases[:5]:  # Show first 5 cases
                    print(f"  - {case['title']} (ID: {case['id']})")
            except TestRailAPIError as e:
                print(f"❌ Error getting test cases: {e}")

        # Example 3: Create a test case (if we have a project and sections)
        if projects:
            project_id = projects[0]["id"]
            print(f"\n➕ Creating a test case in project {project_id}...")
            try:
                # First, get suites to find a section
                suites = unwrap(
                    api.suites.get_suites(project_id=project_id),
                    "suites",
                )
                if suites:
                    suite_id = suites[0]["id"]
                    sections = unwrap(
                        api.sections.get_sections(
                            project_id=project_id, suite_id=suite_id
                        ),
                        "sections",
                    )
                    if sections:
                        section_id = sections[0]["id"]

                        new_case = api.cases.add_case(
                            section_id=section_id,
                            title="API Test Case - Refactored Module Demo",
                            type_id=2,  # Functional test
                            priority_id=2,  # High priority
                            description="This test case was created using the refactored TestRail API module",
                            preconditions="TestRail API access is available",
                            postconditions="Test case is created and visible in TestRail",
                        )
                        case_title = new_case["title"]
                        case_id = new_case["id"]
                        print(
                            f"✅ Created test case: {case_title} "
                            f"(ID: {case_id})"
                        )
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
                api_key="invalid-key",
            )
            invalid_api.projects.get_projects()
        except TestRailAuthenticationError as e:
            print(f"✅ Authentication error handled correctly: {e}")
        except TestRailAPIError as e:
            print(f"✅ General API error handled correctly: {e}")

        # Example 5: Demonstrate bulk operations
        print("\n📦 Demonstrating bulk operations...")
        if projects:
            project_id = projects[0]["id"]
            try:
                # Create a test run
                test_run = api.runs.add_run(
                    project_id=project_id,
                    name="API Module Refactoring Demo Run",
                    description="Test run created by the refactored API module",
                    include_all=True,
                )
                run_name = test_run["name"]
                run_id = test_run["id"]
                print(f"✅ Created test run: {run_name} (ID: {run_id})")

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
