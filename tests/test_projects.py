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

    @pytest.fixture
    def sample_project_data(self) -> dict:
        """Sample project data for testing."""
        return {
            "id": 1,
            "name": "Test Project",
            "announcement": "Project announcement",
            "show_announcement": True,
            "is_completed": False,
            "suite_mode": 1,
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test ProjectsAPI initialization."""
        api = ProjectsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_project(self, projects_api: ProjectsAPI) -> None:
        """Test get_project method."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "Test Project"}

            result = projects_api.get_project(project_id=1)

            mock_get.assert_called_once_with("get_project/1")
            assert result == {"id": 1, "name": "Test Project"}

    def test_get_projects_minimal(self, projects_api: ProjectsAPI) -> None:
        """Test get_projects with no filters."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Project 1"},
                {"id": 2, "name": "Project 2"},
            ]

            result = projects_api.get_projects()

            mock_get.assert_called_once_with("get_projects", params={})
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_projects_with_is_completed_filter(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test get_projects with is_completed filter."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 2, "name": "Done Project"}]

            result = projects_api.get_projects(is_completed=True)

            mock_get.assert_called_once_with(
                "get_projects", params={"is_completed": True}
            )
            assert len(result) == 1

    def test_get_projects_with_none_filter(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test get_projects with None is_completed omits param."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.return_value = []

            projects_api.get_projects(is_completed=None)

            mock_get.assert_called_once_with("get_projects", params={})

    def test_add_project_minimal(self, projects_api: ProjectsAPI) -> None:
        """Test add_project with minimal required parameters."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Project"}

            result = projects_api.add_project(name="New Project")

            expected_data = {"name": "New Project"}
            mock_post.assert_called_once_with(
                "add_project", data=expected_data
            )
            assert result == {"id": 1, "name": "New Project"}

    def test_add_project_with_all_parameters(
        self,
        projects_api: ProjectsAPI,
        sample_project_data: dict,
    ) -> None:
        """Test add_project with all optional parameters."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = sample_project_data

            result = projects_api.add_project(
                name="New Project",
                announcement="Project announcement",
                show_announcement=True,
                suite_mode=1,
            )

            expected_data = {
                "name": "New Project",
                "announcement": "Project announcement",
                "show_announcement": True,
                "suite_mode": 1,
            }
            mock_post.assert_called_once_with(
                "add_project", data=expected_data
            )
            assert result == sample_project_data

    def test_add_project_with_none_values(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test add_project with None values excludes them from payload."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Project"}

            projects_api.add_project(
                name="New Project",
                announcement=None,
                show_announcement=None,
                suite_mode=None,
            )

            expected_data = {"name": "New Project"}
            mock_post.assert_called_once_with(
                "add_project", data=expected_data
            )

    def test_update_project_minimal(self, projects_api: ProjectsAPI) -> None:
        """Test update_project with no optional fields."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Project"}

            result = projects_api.update_project(project_id=1)

            mock_post.assert_called_once_with("update_project/1", data={})
            assert result == {"id": 1, "name": "Test Project"}

    def test_update_project_with_all_parameters(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test update_project with all optional parameters."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Project"}

            projects_api.update_project(
                project_id=1,
                name="Updated Project",
                announcement="New announcement",
                show_announcement=True,
                is_completed=True,
                suite_mode=3,
            )

            expected_data = {
                "name": "Updated Project",
                "announcement": "New announcement",
                "show_announcement": True,
                "is_completed": True,
                "suite_mode": 3,
            }
            mock_post.assert_called_once_with(
                "update_project/1", data=expected_data
            )

    def test_update_project_with_none_values(
        self, projects_api: ProjectsAPI
    ) -> None:
        """Test update_project with None values excludes them from payload."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Project"}

            projects_api.update_project(
                project_id=1,
                name="Updated Project",
                announcement=None,
                show_announcement=None,
                is_completed=None,
                suite_mode=None,
            )

            expected_data = {"name": "Updated Project"}
            mock_post.assert_called_once_with(
                "update_project/1", data=expected_data
            )

    def test_delete_project(self, projects_api: ProjectsAPI) -> None:
        """Test delete_project method."""
        with patch.object(projects_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = projects_api.delete_project(project_id=1)

            mock_post.assert_called_once_with("delete_project/1")
            assert result == {}

    def test_api_request_failure(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                projects_api.get_project(project_id=1)

    def test_authentication_error(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                projects_api.get_project(project_id=1)

    def test_rate_limit_error(self, projects_api: ProjectsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(projects_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                projects_api.get_project(project_id=1)
