"""
Tests for the PlansAPI module.

This module contains comprehensive tests for all methods in the PlansAPI class,
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
from testrail_api_module.plans import PlansAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestPlansAPI:
    """Test suite for PlansAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def plans_api(self, mock_client: Mock) -> PlansAPI:
        """Create a PlansAPI instance with mocked client."""
        return PlansAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test PlansAPI initialization."""
        api = PlansAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_plan(self, plans_api: PlansAPI) -> None:
        """Test get_plan method."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Test Plan"}

            result = plans_api.get_plan(plan_id=1)

            mock_request.assert_called_once_with("GET", "get_plan/1")
            assert result == {"id": 1, "name": "Test Plan"}

    def test_get_plans(self, plans_api: PlansAPI) -> None:
        """Test get_plans method."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Plan 1"},
                {"id": 2, "name": "Plan 2"},
            ]

            result = plans_api.get_plans(project_id=1)

            mock_request.assert_called_once_with("GET", "get_plans/1")
            assert len(result) == 2

    def test_add_plan_minimal(self, plans_api: PlansAPI) -> None:
        """Test add_plan with minimal required parameters."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Plan"}

            result = plans_api.add_plan(project_id=1, name="New Plan")

            expected_data = {"name": "New Plan"}
            mock_request.assert_called_once_with(
                "POST", "add_plan/1", data=expected_data
            )
            assert result == {"id": 1, "name": "New Plan"}

    def test_add_plan_with_all_parameters(self, plans_api: PlansAPI) -> None:
        """Test add_plan with all optional parameters."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Plan"}

            entries = [
                {"suite_id": 1, "name": "Test Run", "include_all": True}
            ]

            plans_api.add_plan(
                project_id=1,
                name="New Plan",
                description="Plan description",
                milestone_id=2,
                entries=entries,
            )

            expected_data = {
                "name": "New Plan",
                "description": "Plan description",
                "milestone_id": 2,
                "entries": entries,
            }
            mock_request.assert_called_once_with(
                "POST", "add_plan/1", data=expected_data
            )

    def test_add_plan_with_none_values(self, plans_api: PlansAPI) -> None:
        """Test add_plan with None values."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Plan"}

            plans_api.add_plan(
                project_id=1,
                name="New Plan",
                description=None,
                milestone_id=None,
                entries=None,
            )

            expected_data = {"name": "New Plan"}
            mock_request.assert_called_once_with(
                "POST", "add_plan/1", data=expected_data
            )

    def test_update_plan(self, plans_api: PlansAPI) -> None:
        """Test update_plan method."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Plan"}

            plans_api.update_plan(
                plan_id=1,
                name="Updated Plan",
                description="Updated description",
            )

            expected_data = {
                "name": "Updated Plan",
                "description": "Updated description",
            }
            mock_request.assert_called_once_with(
                "POST", "update_plan/1", data=expected_data
            )

    def test_close_plan(self, plans_api: PlansAPI) -> None:
        """Test close_plan method."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = plans_api.close_plan(plan_id=1)

            mock_request.assert_called_once_with("POST", "close_plan/1")
            assert result == {}

    def test_delete_plan(self, plans_api: PlansAPI) -> None:
        """Test delete_plan method."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = plans_api.delete_plan(plan_id=1)

            mock_request.assert_called_once_with("POST", "delete_plan/1")
            assert result == {}

    def test_add_plan_entry_minimal(self, plans_api: PlansAPI) -> None:
        """Test add_plan_entry with minimal required parameters."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 10, "suite_id": 5}

            result = plans_api.add_plan_entry(plan_id=1, suite_id=5)

            expected_data = {"suite_id": 5}
            mock_request.assert_called_once_with(
                "POST", "add_plan_entry/1", data=expected_data
            )
            assert result == {"id": 10, "suite_id": 5}

    def test_add_plan_entry_with_all_parameters(
        self, plans_api: PlansAPI
    ) -> None:
        """Test add_plan_entry with all optional parameters."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 10, "suite_id": 5}

            runs = [{"config_ids": [1, 2], "include_all": True}]

            result = plans_api.add_plan_entry(
                plan_id=1,
                suite_id=5,
                name="Entry Name",
                description="Entry description",
                assignedto_id=3,
                include_all=False,
                case_ids=[101, 102],
                config_ids=[1, 2],
                runs=runs,
            )

            expected_data = {
                "suite_id": 5,
                "name": "Entry Name",
                "description": "Entry description",
                "assignedto_id": 3,
                "include_all": False,
                "case_ids": [101, 102],
                "config_ids": [1, 2],
                "runs": runs,
            }
            mock_request.assert_called_once_with(
                "POST", "add_plan_entry/1", data=expected_data
            )
            assert result == {"id": 10, "suite_id": 5}

    def test_add_plan_entry_with_none_values(
        self, plans_api: PlansAPI
    ) -> None:
        """Test add_plan_entry excludes None optional fields from data."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 10, "suite_id": 5}

            plans_api.add_plan_entry(
                plan_id=1,
                suite_id=5,
                name=None,
                description=None,
                assignedto_id=None,
                case_ids=None,
                config_ids=None,
                runs=None,
            )

            expected_data = {"suite_id": 5}
            mock_request.assert_called_once_with(
                "POST", "add_plan_entry/1", data=expected_data
            )

    def test_add_plan_entry_include_all_true_not_sent(
        self, plans_api: PlansAPI
    ) -> None:
        """Test add_plan_entry omits include_all when it is True (default)."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 10, "suite_id": 5}

            plans_api.add_plan_entry(plan_id=1, suite_id=5, include_all=True)

            call_args = mock_request.call_args
            data_sent = call_args[1]["data"]
            assert "include_all" not in data_sent

    def test_update_plan_entry(self, plans_api: PlansAPI) -> None:
        """Test update_plan_entry with keyword arguments."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 10,
                "name": "Updated Entry",
            }

            result = plans_api.update_plan_entry(
                plan_id=1,
                entry_id="abc-123",
                name="Updated Entry",
                include_all=False,
                case_ids=[201, 202],
            )

            expected_data = {
                "name": "Updated Entry",
                "include_all": False,
                "case_ids": [201, 202],
            }
            mock_request.assert_called_once_with(
                "POST",
                "update_plan_entry/1/abc-123",
                data=expected_data,
            )
            assert result == {"id": 10, "name": "Updated Entry"}

    def test_update_plan_entry_no_kwargs(self, plans_api: PlansAPI) -> None:
        """Test update_plan_entry with no keyword arguments sends empty data."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = plans_api.update_plan_entry(
                plan_id=2, entry_id="entry-99"
            )

            mock_request.assert_called_once_with(
                "POST", "update_plan_entry/2/entry-99", data={}
            )
            assert result == {}

    def test_delete_plan_entry(self, plans_api: PlansAPI) -> None:
        """Test delete_plan_entry sends POST with correct endpoint."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = plans_api.delete_plan_entry(plan_id=1, entry_id="abc-123")

            mock_request.assert_called_once_with(
                "POST", "delete_plan_entry/1/abc-123"
            )
            assert result == {}

    def test_api_request_failure(self, plans_api: PlansAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                plans_api.get_plan(plan_id=1)

    def test_authentication_error(self, plans_api: PlansAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                plans_api.get_plan(plan_id=1)

    def test_rate_limit_error(self, plans_api: PlansAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(plans_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                plans_api.get_plan(plan_id=1)
