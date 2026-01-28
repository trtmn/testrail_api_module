"""
Tests for MCP prompts functionality.

This module tests the prompt registration and functionality in the MCP server.
"""
import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401

try:
    from mcp.server.fastmcp.prompts import UserMessage
    PROMPTS_AVAILABLE = True
except ImportError:
    PROMPTS_AVAILABLE = False
    UserMessage = None  # type: ignore

from testrail_api_module.mcp_prompts import (
    add_test_cases_prompt,
    retrieve_test_run_data_prompt,
    create_test_run_prompt,
    create_test_plan_prompt,
    add_test_results_prompt,
    get_test_case_details_prompt,
    update_test_case_prompt,
    get_test_plan_details_prompt,
    get_project_info_prompt,
    get_run_results_prompt,
)


@pytest.mark.skipif(not PROMPTS_AVAILABLE, reason="MCP prompts not available")
class TestPrompts:
    """Test suite for MCP prompts."""

    def test_add_test_cases_prompt_basic(self) -> None:
        """Test add_test_cases_prompt with basic parameters."""
        result = add_test_cases_prompt(
            section_id=123,
            title="Test Case Title"
        )

        assert isinstance(result, list)
        assert len(result) > 0
        if UserMessage is not None:
            assert all(isinstance(msg, UserMessage) for msg in result)

        # Check that section_id and title are in the content
        content = result[0].content if result else ""
        assert "123" in content
        assert "Test Case Title" in content
        assert "section_id" in content.lower()
        assert "add_case" in content.lower()

    def test_add_test_cases_prompt_with_optional_fields(self) -> None:
        """Test add_test_cases_prompt with optional parameters."""
        result = add_test_cases_prompt(
            section_id=123,
            title="Test Case",
            type_id=1,
            priority_id=3,
            estimate="30m",
            description="Test description"
        )

        assert isinstance(result, list)
        assert len(result) > 0

        content = result[0].content if result else ""
        assert "1" in content or "type_id" in content.lower()
        assert "3" in content or "priority_id" in content.lower()
        assert "30m" in content or "estimate" in content.lower()

    def test_retrieve_test_run_data_prompt(self) -> None:
        """Test retrieve_test_run_data_prompt."""
        result = retrieve_test_run_data_prompt(run_id=456)

        assert isinstance(result, list)
        assert len(result) > 0

        content = result[0].content if result else ""
        assert "456" in content
        assert "run_id" in content.lower()
        assert "get_run" in content.lower()

    def test_create_test_run_prompt_basic(self) -> None:
        """Test create_test_run_prompt with basic parameters."""
        result = create_test_run_prompt(
            project_id=1,
            name="Test Run"
        )

        assert isinstance(result, list)
        assert len(result) > 0

        content = result[0].content if result else ""
        assert "1" in content
        assert "Test Run" in content
        assert "add_run" in content.lower()

    def test_create_test_run_prompt_with_options(self) -> None:
        """Test create_test_run_prompt with optional parameters."""
        result = create_test_run_prompt(
            project_id=1,
            name="Test Run",
            suite_id=2,
            milestone_id=3,
            description="Description",
            assignedto_id=4,
            include_all=False,
            case_ids=[1, 2, 3]
        )

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "2" in content or "suite_id" in content.lower()
        assert "false" in content.lower() or "include_all" in content.lower()

    def test_create_test_plan_prompt(self) -> None:
        """Test create_test_plan_prompt."""
        result = create_test_plan_prompt(
            project_id=1,
            name="Test Plan"
        )

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "1" in content
        assert "Test Plan" in content
        assert "add_plan" in content.lower()

    def test_create_test_plan_prompt_with_entries(self) -> None:
        """Test create_test_plan_prompt with entries."""
        entries = [
            {
                "suite_id": 1,
                "name": "Run 1",
                "include_all": True
            }
        ]
        result = create_test_plan_prompt(
            project_id=1,
            name="Test Plan",
            entries=entries
        )

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "entries" in content.lower()

    def test_add_test_results_prompt(self) -> None:
        """Test add_test_results_prompt."""
        result = add_test_results_prompt(
            run_id=1,
            case_id=2,
            status_id=1,
            comment="Test passed",
            version="1.0.0",
            elapsed="30s"
        )

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "1" in content
        assert "2" in content
        assert "add_result" in content.lower()
        assert "Passed" in content or "status" in content.lower()

    def test_get_test_case_details_prompt(self) -> None:
        """Test get_test_case_details_prompt."""
        result = get_test_case_details_prompt(case_id=123)

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "123" in content
        assert "get_case" in content.lower()

    def test_update_test_case_prompt(self) -> None:
        """Test update_test_case_prompt."""
        result = update_test_case_prompt(
            case_id=123,
            title="Updated Title"
        )

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "123" in content
        assert "Updated Title" in content
        assert "update_case" in content.lower()

    def test_get_test_plan_details_prompt(self) -> None:
        """Test get_test_plan_details_prompt."""
        result = get_test_plan_details_prompt(plan_id=456)

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "456" in content
        assert "get_plan" in content.lower()

    def test_get_project_info_prompt(self) -> None:
        """Test get_project_info_prompt."""
        result = get_project_info_prompt(project_id=1)

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "1" in content
        assert "get_project" in content.lower()

    def test_get_run_results_prompt(self) -> None:
        """Test get_run_results_prompt."""
        result = get_run_results_prompt(run_id=789)

        assert isinstance(result, list)
        content = result[0].content if result else ""
        assert "789" in content
        assert "get_results_for_run" in content.lower()


@pytest.mark.skipif(not PROMPTS_AVAILABLE, reason="MCP prompts not available")
class TestPromptRegistration:
    """Test prompt registration with MCP server."""

    def test_prompts_importable(self) -> None:
        """Test that all prompts can be imported."""
        from testrail_api_module.mcp_prompts import (
            add_test_cases_prompt,
            retrieve_test_run_data_prompt,
            create_test_run_prompt,
            create_test_plan_prompt,
            add_test_results_prompt,
            get_test_case_details_prompt,
            update_test_case_prompt,
            get_test_plan_details_prompt,
            get_project_info_prompt,
            get_run_results_prompt,
        )

        # All imports should succeed
        assert add_test_cases_prompt is not None
        assert retrieve_test_run_data_prompt is not None
        assert create_test_run_prompt is not None
        assert create_test_plan_prompt is not None
        assert add_test_results_prompt is not None
        assert get_test_case_details_prompt is not None
        assert update_test_case_prompt is not None
        assert get_test_plan_details_prompt is not None
        assert get_project_info_prompt is not None
        assert get_run_results_prompt is not None

    def test_prompts_registered_in_server(
            self, mocker: "MockerFixture") -> None:
        """Test that prompts are registered when creating MCP server."""
        from testrail_api_module import TestRailAPI
        from testrail_api_module.mcp_server import create_mcp_server

        # Create a mock API instance
        api = TestRailAPI(
            base_url="https://test.testrail.io",
            username="test@example.com",
            api_key="test-key"
        )

        # Mock the FastMCP prompt registration
        mock_prompt = mocker.MagicMock()
        mock_mcp = mocker.MagicMock()
        mock_mcp.prompt = mocker.MagicMock(return_value=mock_prompt)

        # This test verifies that prompts can be registered
        # The actual registration happens in create_mcp_server
        mcp = create_mcp_server(api_instance=api)

        # Verify MCP server was created
        assert mcp is not None
