"""
Tests for the RunsAPI module.

This module contains comprehensive tests for all methods in the RunsAPI class,
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
from testrail_api_module.runs import RunsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestRunsAPI:
    """Test suite for RunsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def runs_api(self, mock_client: Mock) -> RunsAPI:
        """Create a RunsAPI instance with mocked client."""
        return RunsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test RunsAPI initialization."""
        api = RunsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_run(self, runs_api: RunsAPI) -> None:
        """Test get_run method."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "Test Run"}

            result = result = runs_api.get_run(run_id=1)
            mock_get.assert_called_once_with("get_run/1")
            assert result == {"id": 1, "name": "Test Run"}

    def test_get_runs_minimal(self, runs_api: RunsAPI) -> None:
        """Test get_runs with minimal required parameters."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Run 1"},
                {"id": 2, "name": "Run 2"},
            ]

            result = runs_api.get_runs(project_id=1)

            mock_get.assert_called_once_with("get_runs/1", params={})
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_runs_with_all_parameters(self, runs_api: RunsAPI) -> None:
        """Test get_runs with all optional parameters."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "name": "Run 1"}]

            runs_api.get_runs(
                project_id=1,
                suite_id=2,
                created_after=1000000,
                created_before=2000000,
                created_by=1,
                is_completed=True,
                limit=10,
                offset=0,
            )

            expected_params = {
                "suite_id": 2,
                "created_after": 1000000,
                "created_before": 2000000,
                "created_by": 1,
                "is_completed": True,
                "limit": 10,
                "offset": 0,
            }
            mock_get.assert_called_once_with(
                "get_runs/1", params=expected_params
            )

    def test_get_runs_with_none_values(self, runs_api: RunsAPI) -> None:
        """Test get_runs with None values for optional parameters."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            runs_api.get_runs(
                project_id=1,
                suite_id=None,
                created_after=None,
                created_before=None,
                created_by=None,
                is_completed=None,
                limit=None,
                offset=None,
            )

            mock_get.assert_called_once_with("get_runs/1", params={})

    def test_add_run_minimal(self, runs_api: RunsAPI) -> None:
        """Test add_run with minimal required parameters."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Run"}

            result = runs_api.add_run(project_id=1, name="Test Run")

            expected_data = {"name": "Test Run", "include_all": True}
            mock_post.assert_called_once_with("add_run/1", data=expected_data)
            assert result == {"id": 1, "name": "Test Run"}

    def test_add_run_with_all_parameters(self, runs_api: RunsAPI) -> None:
        """Test add_run with all optional parameters."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Run"}

            runs_api.add_run(
                project_id=1,
                name="Test Run",
                description="Test description",
                suite_id=2,
                milestone_id=3,
                assignedto_id=4,
                include_all=False,
                case_ids=[1, 2, 3],
            )

            expected_data = {
                "name": "Test Run",
                "include_all": False,
                "description": "Test description",
                "suite_id": 2,
                "milestone_id": 3,
                "assignedto_id": 4,
                "case_ids": [1, 2, 3],
            }
            mock_post.assert_called_once_with("add_run/1", data=expected_data)

    def test_add_run_with_none_values(self, runs_api: RunsAPI) -> None:
        """Test add_run with None values for optional parameters."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Run"}

            runs_api.add_run(
                project_id=1,
                name="Test Run",
                description=None,
                suite_id=None,
                milestone_id=None,
                assignedto_id=None,
                case_ids=None,
            )

            expected_data = {"name": "Test Run", "include_all": True}
            mock_post.assert_called_once_with("add_run/1", data=expected_data)

    def test_update_run_minimal(self, runs_api: RunsAPI) -> None:
        """Test update_run with minimal parameters (only run_id)."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1}

            result = runs_api.update_run(run_id=1)

            expected_data = {}
            mock_post.assert_called_once_with(
                "update_run/1", data=expected_data
            )
            assert result == {"id": 1}

    def test_update_run_with_all_parameters(self, runs_api: RunsAPI) -> None:
        """Test update_run with all optional parameters."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Run"}

            runs_api.update_run(
                run_id=1,
                name="Updated Run",
                description="Updated description",
                milestone_id=2,
                assignedto_id=3,
            )

            expected_data = {
                "name": "Updated Run",
                "description": "Updated description",
                "milestone_id": 2,
                "assignedto_id": 3,
            }
            mock_post.assert_called_once_with(
                "update_run/1", data=expected_data
            )

    def test_update_run_with_none_values(self, runs_api: RunsAPI) -> None:
        """Test update_run with None values for optional parameters."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1}

            runs_api.update_run(
                run_id=1,
                name=None,
                description=None,
                milestone_id=None,
                assignedto_id=None,
            )

            expected_data = {}
            mock_post.assert_called_once_with(
                "update_run/1", data=expected_data
            )

    def test_close_run(self, runs_api: RunsAPI) -> None:
        """Test close_run method."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = runs_api.close_run(run_id=1)
            mock_post.assert_called_once_with("close_run/1")
            assert result == {}

    def test_delete_run(self, runs_api: RunsAPI) -> None:
        """Test delete_run method."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = runs_api.delete_run(run_id=1)
            mock_post.assert_called_once_with("delete_run/1")
            assert result == {}

    def test_get_run_stats(self, runs_api: RunsAPI) -> None:
        """Test get_run_stats method."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = {
                "passed": 10,
                "failed": 2,
                "blocked": 1,
                "untested": 5,
            }

            result = runs_api.get_run_stats(run_id=1)
            mock_get.assert_called_once_with("get_run_stats/1")
            assert result["passed"] == 10

    def test_api_request_failure(self, runs_api: RunsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                runs_api.get_run(run_id=1)

    def test_authentication_error(self, runs_api: RunsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                runs_api.get_run(run_id=1)

    def test_rate_limit_error(self, runs_api: RunsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                runs_api.get_run(run_id=1)

    def test_get_runs_with_boolean_filters(self, runs_api: RunsAPI) -> None:
        """Test get_runs with boolean is_completed filter."""
        with patch.object(runs_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            runs_api.get_runs(project_id=1, is_completed=False)

            expected_params = {"is_completed": False}
            mock_get.assert_called_once_with(
                "get_runs/1", params=expected_params
            )

    def test_add_run_with_empty_case_ids(self, runs_api: RunsAPI) -> None:
        """Test add_run with empty case_ids list."""
        with patch.object(runs_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Run"}

            runs_api.add_run(
                project_id=1, name="Test Run", include_all=False, case_ids=[]
            )

            expected_data = {
                "name": "Test Run",
                "include_all": False,
                "case_ids": [],
            }
            mock_post.assert_called_once_with("add_run/1", data=expected_data)
