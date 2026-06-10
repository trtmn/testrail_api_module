"""
Tests for the SuitesAPI module.

This module contains comprehensive tests for all methods in the SuitesAPI class,
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
from testrail_api_module.suites import SuitesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestSuitesAPI:
    """Test suite for SuitesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def suites_api(self, mock_client: Mock) -> SuitesAPI:
        """Create a SuitesAPI instance with mocked client."""
        return SuitesAPI(mock_client)

    @pytest.fixture
    def sample_suite_data(self) -> dict:
        """Sample test suite data for testing."""
        return {
            "id": 1,
            "name": "Master Suite",
            "description": "The main test suite",
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test SuitesAPI initialization."""
        api = SuitesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_suite(self, suites_api: SuitesAPI) -> None:
        """Test get_suite method."""
        with patch.object(suites_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "Test Suite"}

            result = suites_api.get_suite(suite_id=1)

            mock_get.assert_called_once_with("get_suite/1")
            assert result == {"id": 1, "name": "Test Suite"}

    def test_get_suites(self, suites_api: SuitesAPI) -> None:
        """Test get_suites method."""
        with patch.object(suites_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Suite 1"},
                {"id": 2, "name": "Suite 2"},
            ]

            result = suites_api.get_suites(project_id=1)

            mock_get.assert_called_once_with("get_suites/1")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_add_suite_minimal(self, suites_api: SuitesAPI) -> None:
        """Test add_suite with minimal required parameters."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Suite"}

            result = suites_api.add_suite(project_id=1, name="New Suite")

            expected_data = {"name": "New Suite"}
            mock_post.assert_called_once_with(
                "add_suite/1", data=expected_data
            )
            assert result == {"id": 1, "name": "New Suite"}

    def test_add_suite_with_all_parameters(
        self,
        suites_api: SuitesAPI,
        sample_suite_data: dict,
    ) -> None:
        """Test add_suite with all optional parameters."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = sample_suite_data

            result = suites_api.add_suite(
                project_id=1,
                name="Master Suite",
                description="The main test suite",
            )

            expected_data = {
                "name": "Master Suite",
                "description": "The main test suite",
            }
            mock_post.assert_called_once_with(
                "add_suite/1", data=expected_data
            )
            assert result == sample_suite_data

    def test_add_suite_with_none_values(self, suites_api: SuitesAPI) -> None:
        """Test add_suite with None description excludes it from payload."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Suite"}

            suites_api.add_suite(
                project_id=1, name="New Suite", description=None
            )

            expected_data = {"name": "New Suite"}
            mock_post.assert_called_once_with(
                "add_suite/1", data=expected_data
            )

    def test_update_suite_minimal(self, suites_api: SuitesAPI) -> None:
        """Test update_suite with no optional fields."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Test Suite"}

            result = suites_api.update_suite(suite_id=1)

            mock_post.assert_called_once_with("update_suite/1", data={})
            assert result == {"id": 1, "name": "Test Suite"}

    def test_update_suite_with_all_parameters(
        self, suites_api: SuitesAPI
    ) -> None:
        """Test update_suite with all optional parameters."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Suite"}

            suites_api.update_suite(
                suite_id=1,
                name="Updated Suite",
                description="Updated description",
            )

            expected_data = {
                "name": "Updated Suite",
                "description": "Updated description",
            }
            mock_post.assert_called_once_with(
                "update_suite/1", data=expected_data
            )

    def test_update_suite_with_none_values(
        self, suites_api: SuitesAPI
    ) -> None:
        """Test update_suite with None values excludes them from payload."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Suite"}

            suites_api.update_suite(
                suite_id=1, name="Updated Suite", description=None
            )

            expected_data = {"name": "Updated Suite"}
            mock_post.assert_called_once_with(
                "update_suite/1", data=expected_data
            )

    def test_delete_suite(self, suites_api: SuitesAPI) -> None:
        """Test delete_suite method."""
        with patch.object(suites_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = suites_api.delete_suite(suite_id=1)

            mock_post.assert_called_once_with("delete_suite/1")
            assert result == {}

    def test_api_request_failure(self, suites_api: SuitesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(suites_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                suites_api.get_suite(suite_id=1)

    def test_authentication_error(self, suites_api: SuitesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(suites_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                suites_api.get_suite(suite_id=1)

    def test_rate_limit_error(self, suites_api: SuitesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(suites_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                suites_api.get_suite(suite_id=1)
