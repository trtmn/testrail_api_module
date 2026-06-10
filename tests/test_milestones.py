"""
Tests for the MilestonesAPI module.

This module contains comprehensive tests for all methods in the MilestonesAPI class,
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
from testrail_api_module.milestones import MilestonesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestMilestonesAPI:
    """Test suite for MilestonesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def milestones_api(self, mock_client: Mock) -> MilestonesAPI:
        """Create a MilestonesAPI instance with mocked client."""
        return MilestonesAPI(mock_client)

    @pytest.fixture
    def sample_milestone_data(self) -> dict:
        """Sample milestone data for testing."""
        return {
            "id": 1,
            "name": "Sprint 1",
            "description": "First sprint",
            "due_on": 1735689600,
            "parent_id": None,
            "refs": "JIRA-123",
            "start_on": 1704067200,
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test MilestonesAPI initialization."""
        api = MilestonesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_milestone(self, milestones_api: MilestonesAPI) -> None:
        """Test get_milestone method."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "Milestone 1"}

            result = milestones_api.get_milestone(milestone_id=1)

            mock_get.assert_called_once_with("get_milestone/1")
            assert result == {"id": 1, "name": "Milestone 1"}

    def test_get_milestones_minimal(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test get_milestones with only required project_id."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Milestone 1"},
                {"id": 2, "name": "Milestone 2"},
            ]

            result = milestones_api.get_milestones(project_id=1)

            mock_get.assert_called_once_with("get_milestones/1", params={})
            assert len(result) == 2

    def test_get_milestones_with_is_completed(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test get_milestones with is_completed filter."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = []

            milestones_api.get_milestones(project_id=1, is_completed=True)

            mock_get.assert_called_once_with(
                "get_milestones/1", params={"is_completed": True}
            )

    def test_get_milestones_with_is_started(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test get_milestones with is_started filter."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = []

            milestones_api.get_milestones(project_id=1, is_started=False)

            mock_get.assert_called_once_with(
                "get_milestones/1", params={"is_started": False}
            )

    def test_get_milestones_with_all_filters(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test get_milestones with all optional filters."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = []

            milestones_api.get_milestones(
                project_id=1, is_completed=False, is_started=True
            )

            mock_get.assert_called_once_with(
                "get_milestones/1",
                params={"is_completed": False, "is_started": True},
            )

    def test_get_milestones_with_none_filters(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test get_milestones with None filters omits them from params."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.return_value = []

            milestones_api.get_milestones(
                project_id=1, is_completed=None, is_started=None
            )

            mock_get.assert_called_once_with("get_milestones/1", params={})

    def test_add_milestone_minimal(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test add_milestone with minimal required parameters."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Milestone"}

            result = milestones_api.add_milestone(
                project_id=1, name="New Milestone"
            )

            expected_data = {"name": "New Milestone"}
            mock_post.assert_called_once_with(
                "add_milestone/1", data=expected_data
            )
            assert result == {"id": 1, "name": "New Milestone"}

    def test_add_milestone_with_all_parameters(
        self,
        milestones_api: MilestonesAPI,
        sample_milestone_data: dict,
    ) -> None:
        """Test add_milestone with all optional parameters."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = sample_milestone_data

            result = milestones_api.add_milestone(
                project_id=1,
                name="Sprint 1",
                description="First sprint",
                due_on=1735689600,
                parent_id=2,
                refs="JIRA-123",
                start_on=1704067200,
            )

            expected_data = {
                "name": "Sprint 1",
                "description": "First sprint",
                "due_on": 1735689600,
                "parent_id": 2,
                "refs": "JIRA-123",
                "start_on": 1704067200,
            }
            mock_post.assert_called_once_with(
                "add_milestone/1", data=expected_data
            )
            assert result == sample_milestone_data

    def test_add_milestone_with_none_values(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test add_milestone with None values excludes them from payload."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Milestone"}

            milestones_api.add_milestone(
                project_id=1,
                name="New Milestone",
                description=None,
                due_on=None,
                parent_id=None,
                refs=None,
                start_on=None,
            )

            expected_data = {"name": "New Milestone"}
            mock_post.assert_called_once_with(
                "add_milestone/1", data=expected_data
            )

    def test_update_milestone_minimal(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test update_milestone with no optional fields."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Milestone 1"}

            result = milestones_api.update_milestone(milestone_id=1)

            mock_post.assert_called_once_with("update_milestone/1", data={})
            assert result == {"id": 1, "name": "Milestone 1"}

    def test_update_milestone_with_all_parameters(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test update_milestone with all optional parameters."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Milestone"}

            milestones_api.update_milestone(
                milestone_id=1,
                name="Updated Milestone",
                description="Updated desc",
                due_on=1735689600,
                is_completed=True,
                is_started=True,
                parent_id=2,
                refs="JIRA-456",
                start_on=1704067200,
            )

            expected_data = {
                "name": "Updated Milestone",
                "description": "Updated desc",
                "due_on": 1735689600,
                "is_completed": True,
                "is_started": True,
                "parent_id": 2,
                "refs": "JIRA-456",
                "start_on": 1704067200,
            }
            mock_post.assert_called_once_with(
                "update_milestone/1", data=expected_data
            )

    def test_update_milestone_with_none_values(
        self, milestones_api: MilestonesAPI
    ) -> None:
        """Test update_milestone with None values excludes them."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Milestone"}

            milestones_api.update_milestone(
                milestone_id=1,
                name="Updated Milestone",
                description=None,
                due_on=None,
                is_completed=None,
                is_started=None,
                parent_id=None,
                refs=None,
                start_on=None,
            )

            expected_data = {"name": "Updated Milestone"}
            mock_post.assert_called_once_with(
                "update_milestone/1", data=expected_data
            )

    def test_delete_milestone(self, milestones_api: MilestonesAPI) -> None:
        """Test delete_milestone method."""
        with patch.object(milestones_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = milestones_api.delete_milestone(milestone_id=1)

            mock_post.assert_called_once_with("delete_milestone/1")
            assert result == {}

    def test_api_request_failure(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                milestones_api.get_milestone(milestone_id=1)

    def test_authentication_error(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                milestones_api.get_milestone(milestone_id=1)

    def test_rate_limit_error(self, milestones_api: MilestonesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(milestones_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                milestones_api.get_milestone(milestone_id=1)
