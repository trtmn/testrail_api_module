"""
Tests for the LabelsAPI module.

This module contains comprehensive tests for all methods in the
LabelsAPI class, including edge cases, error handling, and proper
API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.labels import LabelsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestLabelsAPI:
    """Test suite for LabelsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def labels_api(self, mock_client: Mock) -> LabelsAPI:
        """Create a LabelsAPI instance with mocked client."""
        return LabelsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test LabelsAPI initialization."""
        api = LabelsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_label(self, labels_api: LabelsAPI) -> None:
        """Test get_label method."""
        with patch.object(labels_api, "_get") as mock_get:
            mock_get.return_value = {
                "id": 1,
                "name": "Smoke",
            }

            result = labels_api.get_label(label_id=1)

            mock_get.assert_called_once_with("get_label/1")
            assert result == {"id": 1, "name": "Smoke"}

    def test_get_labels(self, labels_api: LabelsAPI) -> None:
        """Test get_labels method."""
        with patch.object(labels_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Smoke"},
                {"id": 2, "name": "Regression"},
            ]

            result = labels_api.get_labels(project_id=1)

            mock_get.assert_called_once_with("get_labels/1")
            assert len(result) == 2
            assert result[0]["name"] == "Smoke"

    def test_add_label_minimal(self, labels_api: LabelsAPI) -> None:
        """Test add_label with minimal required parameters."""
        with patch.object(labels_api, "_post") as mock_post:
            mock_post.return_value = {
                "id": 1,
                "name": "New Label",
            }

            result = labels_api.add_label(project_id=1, name="New Label")

            expected_data = {"name": "New Label"}
            mock_post.assert_called_once_with(
                "add_label/1", data=expected_data
            )
            assert result == {"id": 1, "name": "New Label"}

    def test_add_label_with_color(self, labels_api: LabelsAPI) -> None:
        """Test add_label with color parameter."""
        with patch.object(labels_api, "_post") as mock_post:
            mock_post.return_value = {
                "id": 1,
                "name": "New Label",
                "color": "FF0000",
            }

            result = labels_api.add_label(
                project_id=1, name="New Label", color="FF0000"
            )

            expected_data = {
                "name": "New Label",
                "color": "FF0000",
            }
            mock_post.assert_called_once_with(
                "add_label/1", data=expected_data
            )
            assert result["color"] == "FF0000"

    def test_add_label_with_none_color(self, labels_api: LabelsAPI) -> None:
        """Test add_label with None color is excluded."""
        with patch.object(labels_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Label"}

            labels_api.add_label(project_id=1, name="Label", color=None)

            expected_data = {"name": "Label"}
            mock_post.assert_called_once_with(
                "add_label/1", data=expected_data
            )

    def test_update_label(self, labels_api: LabelsAPI) -> None:
        """Test update_label method."""
        with patch.object(labels_api, "_post") as mock_post:
            mock_post.return_value = {
                "id": 1,
                "name": "Updated",
            }

            result = labels_api.update_label(
                label_id=1, name="Updated", color="00FF00"
            )

            expected_data = {
                "name": "Updated",
                "color": "00FF00",
            }
            mock_post.assert_called_once_with(
                "update_label/1", data=expected_data
            )
            assert result["name"] == "Updated"

    def test_delete_label(self, labels_api: LabelsAPI) -> None:
        """Test delete_label method."""
        with patch.object(labels_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = labels_api.delete_label(label_id=1)

            mock_post.assert_called_once_with("delete_label/1")
            assert result == {}

    def test_api_request_failure(self, labels_api: LabelsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(labels_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                labels_api.get_label(label_id=1)

    def test_authentication_error(self, labels_api: LabelsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(labels_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError,
                match="Authentication failed",
            ):
                labels_api.get_label(label_id=1)

    def test_rate_limit_error(self, labels_api: LabelsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(labels_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError,
                match="Rate limit exceeded",
            ):
                labels_api.get_label(label_id=1)
