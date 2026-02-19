"""
Tests for the ProjectsAPI module.

This module contains comprehensive tests for all methods in the ProjectsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.projects import ProjectsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestProjectsAPI:
    """Test suite for ProjectsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def projects_api(self, mock_client: Mock) -> ProjectsAPI:
        """Create a ProjectsAPI instance with mocked client."""
        return ProjectsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test ProjectsAPI initialization."""
        api = ProjectsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_project(self, projects_api: ProjectsAPI) -> None:
        """Test get_project method."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test Project"}

            result = projects_api.get_project(project_id=1)

            mock_request.assert_called_once_with("GET", "get_project/1")
            assert result == {"id": 1, "name": "Test Project"}

    def test_get_projects(self, projects_api: ProjectsAPI) -> None:
        """Test get_projects method."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Project 1"},
                {"id": 2, "name": "Project 2"},
            ]

            result = projects_api.get_projects()

            mock_request.assert_called_once_with("GET", "get_projects")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_add_project_minimal(self, projects_api: ProjectsAPI) -> None:
        """Test add_project with minimal required parameters."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Project"}

            result = projects_api.add_project(name="New Project")

            expected_data = {
                "name": "New Project",
                "show_announcement": False,
                "is_completed": False,
            }
            mock_request.assert_called_once_with(
                "POST", "add_project", data=expected_data
            )
            assert result == {"id": 1, "name": "New Project"}

    def test_add_project_with_all_parameters(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test add_project with all optional parameters."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Project"}

            projects_api.add_project(
                name="New Project",
                announcement="Project announcement",
                show_announcement=True,
                is_completed=False,
            )

            expected_data = {
                "name": "New Project",
                "announcement": "Project announcement",
                "show_announcement": True,
                "is_completed": False,
            }
            mock_request.assert_called_once_with(
                "POST", "add_project", data=expected_data
            )

    def test_add_project_without_announcement(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test add_project without announcement parameter."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Project"}

            projects_api.add_project(
                name="New Project", announcement=None, show_announcement=True
            )

            expected_data = {
                "name": "New Project",
                "show_announcement": True,
                "is_completed": False,
            }
            mock_request.assert_called_once_with(
                "POST", "add_project", data=expected_data
            )

    def test_update_project(self, projects_api: ProjectsAPI) -> None:
        """Test update_project method."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Project"}

            projects_api.update_project(
                project_id=1, name="Updated Project", is_completed=True
            )

            expected_data = {"name": "Updated Project", "is_completed": True}
            mock_request.assert_called_once_with(
                "POST", "update_project/1", data=expected_data
            )

    def test_delete_project(self, projects_api: ProjectsAPI) -> None:
        """Test delete_project method."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = projects_api.delete_project(project_id=1)

            mock_request.assert_called_once_with("POST", "delete_project/1")
            assert result == {}

    def test_api_request_failure(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                projects_api.get_project(project_id=1)

    def test_authentication_error(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                projects_api.get_project(project_id=1)

    def test_rate_limit_error(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(projects_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                projects_api.get_project(project_id=1)
