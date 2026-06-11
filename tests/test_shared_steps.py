"""
Tests for the SharedStepsAPI module.

This module contains comprehensive tests for all methods in the SharedStepsAPI class,
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
from testrail_api_module.shared_steps import SharedStepsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestSharedStepsAPI:
    """Test suite for SharedStepsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def shared_steps_api(self, mock_client: Mock) -> SharedStepsAPI:
        """Create a SharedStepsAPI instance with mocked client."""
        return SharedStepsAPI(mock_client)

    @pytest.fixture
    def sample_shared_step_data(self) -> dict:
        """Sample shared step data for testing."""
        return {
            "id": 1,
            "title": "Login Steps",
            "project_id": 1,
            "custom_steps_separated": [
                {
                    "content": "Navigate to login page",
                    "expected": "Login page is displayed",
                },
                {
                    "content": "Enter credentials",
                    "expected": "User is logged in",
                    "refs": "AUTH-001",
                },
            ],
        }

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def test_init(self, mock_client: Mock) -> None:
        """Test SharedStepsAPI initialization."""
        api = SharedStepsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    # ------------------------------------------------------------------
    # get_shared_step
    # ------------------------------------------------------------------

    def test_get_shared_step(self, shared_steps_api: SharedStepsAPI) -> None:
        """Test get_shared_step with a valid ID."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "title": "Shared Step 1"}

            result = shared_steps_api.get_shared_step(shared_step_id=1)

            mock_get.assert_called_once_with("get_shared_step/1")
            assert result == {"id": 1, "title": "Shared Step 1"}

    def test_get_shared_step_large_id(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_step with a large ID value."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {"id": 999999, "title": "Step"}

            result = shared_steps_api.get_shared_step(shared_step_id=999999)

            mock_get.assert_called_once_with("get_shared_step/999999")
            assert result["id"] == 999999

    def test_get_shared_step_api_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_step raises TestRailAPIError on failure."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.get_shared_step(shared_step_id=1)

    def test_get_shared_step_auth_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_step raises TestRailAuthenticationError."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                shared_steps_api.get_shared_step(shared_step_id=1)

    def test_get_shared_step_rate_limit_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_step raises TestRailRateLimitError."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                shared_steps_api.get_shared_step(shared_step_id=1)

    # ------------------------------------------------------------------
    # get_shared_steps
    # ------------------------------------------------------------------

    def test_get_shared_steps_minimal(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps with only the required project_id."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 0,
                "limit": 250,
                "size": 2,
                "_links": {"next": None, "prev": None},
                "shared_steps": [
                    {"id": 1, "title": "Shared Step 1"},
                    {"id": 2, "title": "Shared Step 2"},
                ],
            }

            result = shared_steps_api.get_shared_steps(project_id=1)

            mock_get.assert_called_once_with("get_shared_steps/1", params={})
            assert result["size"] == 2
            assert len(result["shared_steps"]) == 2

    def test_get_shared_steps_with_all_parameters(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps with all optional filter parameters."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 10,
                "limit": 50,
                "size": 1,
                "_links": {},
                "shared_steps": [{"id": 5, "title": "Step"}],
            }

            result = shared_steps_api.get_shared_steps(
                project_id=1,
                created_after=1609459200,
                created_before=1640995199,
                created_by=42,
                limit=50,
                offset=10,
                updated_after=1625000000,
                updated_before=1640000000,
            )

            mock_get.assert_called_once_with(
                "get_shared_steps/1",
                params={
                    "created_after": 1609459200,
                    "created_before": 1640995199,
                    "created_by": 42,
                    "limit": 50,
                    "offset": 10,
                    "updated_after": 1625000000,
                    "updated_before": 1640000000,
                },
            )
            assert result["size"] == 1

    def test_get_shared_steps_with_none_values(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps omits None filter values from params."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 0,
                "limit": 250,
                "size": 0,
                "_links": {},
                "shared_steps": [],
            }

            shared_steps_api.get_shared_steps(
                project_id=1,
                created_after=None,
                created_before=None,
                created_by=None,
                limit=None,
                offset=None,
                updated_after=None,
                updated_before=None,
            )

            mock_get.assert_called_once_with("get_shared_steps/1", params={})

    def test_get_shared_steps_created_by_list(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps with created_by as a list of user IDs."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 0,
                "limit": 250,
                "size": 0,
                "_links": {},
                "shared_steps": [],
            }

            shared_steps_api.get_shared_steps(
                project_id=5, created_by=[1, 2, 3]
            )

            mock_get.assert_called_once_with(
                "get_shared_steps/5",
                params={"created_by": [1, 2, 3]},
            )

    def test_get_shared_steps_pagination(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps with limit and offset for pagination."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 25,
                "limit": 25,
                "size": 25,
                "_links": {},
                "shared_steps": [],
            }

            shared_steps_api.get_shared_steps(
                project_id=1, limit=25, offset=25
            )

            mock_get.assert_called_once_with(
                "get_shared_steps/1",
                params={"limit": 25, "offset": 25},
            )

    def test_get_shared_steps_api_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps raises TestRailAPIError on failure."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.get_shared_steps(project_id=1)

    def test_get_shared_steps_auth_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps raises TestRailAuthenticationError."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                shared_steps_api.get_shared_steps(project_id=1)

    def test_get_shared_steps_rate_limit_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test get_shared_steps raises TestRailRateLimitError."""
        with patch.object(shared_steps_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                shared_steps_api.get_shared_steps(project_id=1)

    # ------------------------------------------------------------------
    # add_shared_step
    # ------------------------------------------------------------------

    def test_add_shared_step_minimal(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step with only required parameters."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Login Steps"}

            result = shared_steps_api.add_shared_step(
                project_id=1, title="Login Steps"
            )

            mock_post.assert_called_once_with(
                "add_shared_step/1",
                data={"title": "Login Steps"},
            )
            assert result == {"id": 1, "title": "Login Steps"}

    def test_add_shared_step_with_all_parameters(
        self,
        shared_steps_api: SharedStepsAPI,
        sample_shared_step_data: dict,
    ) -> None:
        """Test add_shared_step with all optional parameters."""
        steps = [
            {
                "content": "Navigate to login page",
                "expected": "Login page is displayed",
            },
            {
                "content": "Enter credentials",
                "expected": "User is logged in",
                "refs": "AUTH-001",
            },
        ]

        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = sample_shared_step_data

            result = shared_steps_api.add_shared_step(
                project_id=1,
                title="Login Steps",
                custom_steps_separated=steps,
            )

            mock_post.assert_called_once_with(
                "add_shared_step/1",
                data={
                    "title": "Login Steps",
                    "custom_steps_separated": steps,
                },
            )
            assert result == sample_shared_step_data

    def test_add_shared_step_with_none_values(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step omits None custom_steps_separated."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "My Steps"}

            result = shared_steps_api.add_shared_step(
                project_id=1,
                title="My Steps",
                custom_steps_separated=None,
            )

            mock_post.assert_called_once_with(
                "add_shared_step/1",
                data={"title": "My Steps"},
            )
            assert result == {"id": 1, "title": "My Steps"}

    def test_add_shared_step_with_empty_steps(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step with an empty list of steps."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 2, "title": "Empty Steps"}

            result = shared_steps_api.add_shared_step(
                project_id=2,
                title="Empty Steps",
                custom_steps_separated=[],
            )

            mock_post.assert_called_once_with(
                "add_shared_step/2",
                data={"title": "Empty Steps", "custom_steps_separated": []},
            )
            assert result["id"] == 2

    def test_add_shared_step_api_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step raises TestRailAPIError on failure."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.add_shared_step(project_id=1, title="Steps")

    def test_add_shared_step_auth_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step raises TestRailAuthenticationError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                shared_steps_api.add_shared_step(project_id=1, title="Steps")

    def test_add_shared_step_rate_limit_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test add_shared_step raises TestRailRateLimitError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                shared_steps_api.add_shared_step(project_id=1, title="Steps")

    # ------------------------------------------------------------------
    # update_shared_step
    # ------------------------------------------------------------------

    def test_update_shared_step_minimal(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step with no optional fields (empty body)."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Old Title"}

            result = shared_steps_api.update_shared_step(shared_step_id=1)

            mock_post.assert_called_once_with("update_shared_step/1", data={})
            assert result == {"id": 1, "title": "Old Title"}

    def test_update_shared_step_title_only(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step updating only the title."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "New Title"}

            result = shared_steps_api.update_shared_step(
                shared_step_id=1, title="New Title"
            )

            mock_post.assert_called_once_with(
                "update_shared_step/1",
                data={"title": "New Title"},
            )
            assert result["title"] == "New Title"

    def test_update_shared_step_with_all_parameters(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step with both title and steps."""
        steps = [{"content": "Updated step", "expected": "Updated result"}]

        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {
                "id": 3,
                "title": "Updated Title",
                "custom_steps_separated": steps,
            }

            result = shared_steps_api.update_shared_step(
                shared_step_id=3,
                title="Updated Title",
                custom_steps_separated=steps,
            )

            mock_post.assert_called_once_with(
                "update_shared_step/3",
                data={
                    "title": "Updated Title",
                    "custom_steps_separated": steps,
                },
            )
            assert result["title"] == "Updated Title"

    def test_update_shared_step_with_none_values(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step omits None values from the body."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Unchanged"}

            shared_steps_api.update_shared_step(
                shared_step_id=1,
                title=None,
                custom_steps_separated=None,
            )

            mock_post.assert_called_once_with("update_shared_step/1", data={})

    def test_update_shared_step_api_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step raises TestRailAPIError on failure."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.update_shared_step(
                    shared_step_id=1, title="New"
                )

    def test_update_shared_step_auth_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step raises TestRailAuthenticationError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                shared_steps_api.update_shared_step(
                    shared_step_id=1, title="New"
                )

    def test_update_shared_step_rate_limit_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test update_shared_step raises TestRailRateLimitError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                shared_steps_api.update_shared_step(
                    shared_step_id=1, title="New"
                )

    # ------------------------------------------------------------------
    # delete_shared_step
    # ------------------------------------------------------------------

    def test_delete_shared_step_minimal(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step with only the required ID."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = shared_steps_api.delete_shared_step(shared_step_id=1)

            mock_post.assert_called_once_with(
                "delete_shared_step/1", data=None
            )
            assert result == {}

    def test_delete_shared_step_keep_in_cases_true(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step with keep_in_cases=True."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = shared_steps_api.delete_shared_step(
                shared_step_id=1, keep_in_cases=True
            )

            mock_post.assert_called_once_with(
                "delete_shared_step/1",
                data={"keep_in_cases": True},
            )
            assert result == {}

    def test_delete_shared_step_keep_in_cases_false(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step with keep_in_cases=False."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {}

            shared_steps_api.delete_shared_step(
                shared_step_id=2, keep_in_cases=False
            )

            mock_post.assert_called_once_with(
                "delete_shared_step/2",
                data={"keep_in_cases": False},
            )

    def test_delete_shared_step_with_none_keep_in_cases(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step with keep_in_cases=None omits the field."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.return_value = {}

            shared_steps_api.delete_shared_step(
                shared_step_id=1, keep_in_cases=None
            )

            mock_post.assert_called_once_with(
                "delete_shared_step/1", data=None
            )

    def test_delete_shared_step_api_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step raises TestRailAPIError on failure."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.delete_shared_step(shared_step_id=1)

    def test_delete_shared_step_auth_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step raises TestRailAuthenticationError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                shared_steps_api.delete_shared_step(shared_step_id=1)

    def test_delete_shared_step_rate_limit_error(
        self, shared_steps_api: SharedStepsAPI
    ) -> None:
        """Test delete_shared_step raises TestRailRateLimitError."""
        with patch.object(shared_steps_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                shared_steps_api.delete_shared_step(shared_step_id=1)
