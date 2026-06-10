"""
Tests for the DatasetsAPI module.

This module contains comprehensive tests for all methods in the
DatasetsAPI class, including edge cases, error handling, and proper
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
from testrail_api_module.datasets import DatasetsAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestDatasetsAPI:
    """Test suite for DatasetsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def datasets_api(self, mock_client: Mock) -> DatasetsAPI:
        """Create a DatasetsAPI instance with mocked client."""
        return DatasetsAPI(mock_client)

    @pytest.fixture
    def sample_dataset_data(self) -> dict:
        """Sample dataset data for testing."""
        return {
            "id": 1,
            "name": "Test Dataset",
            "variables": [
                {"id": 1, "name": "username", "value": "testuser"},
                {"id": 2, "name": "password", "value": "testpass"},
            ],
        }

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    def test_init(self, mock_client: Mock) -> None:
        """Test DatasetsAPI initialization."""
        api = DatasetsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    # -------------------------------------------------------------------------
    # get_dataset
    # -------------------------------------------------------------------------

    def test_get_dataset_minimal(
        self,
        datasets_api: DatasetsAPI,
        sample_dataset_data: dict,
    ) -> None:
        """Test get_dataset with minimal required parameters."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = sample_dataset_data

            result = datasets_api.get_dataset(dataset_id=1)

            mock_get.assert_called_once_with("get_dataset/1")
            assert result == sample_dataset_data

    def test_get_dataset_with_variables(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_dataset returns dataset with variables array."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = {
                "id": 5,
                "name": "Complex Dataset",
                "variables": [
                    {"id": 10, "name": "username", "value": "testuser"},
                    {"id": 11, "name": "password", "value": "testpass"},
                    {"id": 12, "name": "environment", "value": "staging"},
                ],
            }

            result = datasets_api.get_dataset(dataset_id=5)

            mock_get.assert_called_once_with("get_dataset/5")
            assert len(result["variables"]) == 3
            assert result["variables"][0]["name"] == "username"

    def test_get_dataset_different_ids(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_dataset with different dataset IDs."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "Dataset"}

            datasets_api.get_dataset(dataset_id=1)
            datasets_api.get_dataset(dataset_id=100)

            assert mock_get.call_count == 2
            mock_get.assert_any_call("get_dataset/1")
            mock_get.assert_any_call("get_dataset/100")

    def test_get_dataset_api_error(self, datasets_api: DatasetsAPI) -> None:
        """Test get_dataset raises TestRailAPIError on API failure."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.get_dataset(dataset_id=1)

    def test_get_dataset_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_dataset raises TestRailAuthenticationError."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.get_dataset(dataset_id=1)

    def test_get_dataset_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_dataset raises TestRailRateLimitError."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.get_dataset(dataset_id=1)

    # -------------------------------------------------------------------------
    # get_datasets
    # -------------------------------------------------------------------------

    def test_get_datasets_minimal(self, datasets_api: DatasetsAPI) -> None:
        """Test get_datasets with minimal required parameters."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Dataset 1"},
                {"id": 2, "name": "Dataset 2"},
            ]

            result = datasets_api.get_datasets(project_id=1)

            mock_get.assert_called_once_with("get_datasets/1")
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2

    def test_get_datasets_empty_list(self, datasets_api: DatasetsAPI) -> None:
        """Test get_datasets returns empty list when no datasets exist."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = []

            result = datasets_api.get_datasets(project_id=1)

            mock_get.assert_called_once_with("get_datasets/1")
            assert result == []

    def test_get_datasets_different_project_ids(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets with different project IDs."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "name": "Dataset 1"}]

            datasets_api.get_datasets(project_id=1)
            datasets_api.get_datasets(project_id=2)

            assert mock_get.call_count == 2
            mock_get.assert_any_call("get_datasets/1")
            mock_get.assert_any_call("get_datasets/2")

    def test_get_datasets_api_error(self, datasets_api: DatasetsAPI) -> None:
        """Test get_datasets raises TestRailAPIError on API failure."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.get_datasets(project_id=1)

    def test_get_datasets_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets raises TestRailAuthenticationError."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.get_datasets(project_id=1)

    def test_get_datasets_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets raises TestRailRateLimitError."""
        with patch.object(datasets_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.get_datasets(project_id=1)

    # -------------------------------------------------------------------------
    # add_dataset
    # -------------------------------------------------------------------------

    def test_add_dataset_minimal(self, datasets_api: DatasetsAPI) -> None:
        """Test add_dataset with only required parameters."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "My Dataset"}

            result = datasets_api.add_dataset(project_id=1, name="My Dataset")

            expected_data = {"name": "My Dataset"}
            mock_post.assert_called_once_with(
                "add_dataset/1", data=expected_data
            )
            assert result == {"id": 1, "name": "My Dataset"}

    def test_add_dataset_with_variables(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test add_dataset with variables list."""
        with patch.object(datasets_api, "_post") as mock_post:
            variables = [
                {"id": 1, "value": "user1"},
                {"id": 2, "value": "pass1"},
            ]
            mock_post.return_value = {
                "id": 1,
                "name": "My Dataset",
                "variables": variables,
            }

            result = datasets_api.add_dataset(
                project_id=1,
                name="My Dataset",
                variables=variables,
            )

            expected_data = {"name": "My Dataset", "variables": variables}
            mock_post.assert_called_once_with(
                "add_dataset/1", data=expected_data
            )
            assert result["variables"] == variables

    def test_add_dataset_with_none_variables(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test add_dataset with variables=None omits variables from payload."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "My Dataset"}

            datasets_api.add_dataset(
                project_id=1, name="My Dataset", variables=None
            )

            expected_data = {"name": "My Dataset"}
            mock_post.assert_called_once_with(
                "add_dataset/1", data=expected_data
            )

    def test_add_dataset_api_error(self, datasets_api: DatasetsAPI) -> None:
        """Test add_dataset raises TestRailAPIError on API failure."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.add_dataset(project_id=1, name="My Dataset")

    def test_add_dataset_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test add_dataset raises TestRailAuthenticationError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.add_dataset(project_id=1, name="My Dataset")

    def test_add_dataset_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test add_dataset raises TestRailRateLimitError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.add_dataset(project_id=1, name="My Dataset")

    # -------------------------------------------------------------------------
    # update_dataset
    # -------------------------------------------------------------------------

    def test_update_dataset_minimal(self, datasets_api: DatasetsAPI) -> None:
        """Test update_dataset with no optional parameters sends empty body."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Original"}

            result = datasets_api.update_dataset(dataset_id=1)

            mock_post.assert_called_once_with("update_dataset/1", data={})
            assert result == {"id": 1, "name": "Original"}

    def test_update_dataset_with_name(self, datasets_api: DatasetsAPI) -> None:
        """Test update_dataset with name parameter."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Dataset"}

            result = datasets_api.update_dataset(
                dataset_id=1, name="Updated Dataset"
            )

            expected_data = {"name": "Updated Dataset"}
            mock_post.assert_called_once_with(
                "update_dataset/1", data=expected_data
            )
            assert result["name"] == "Updated Dataset"

    def test_update_dataset_with_variables(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test update_dataset with variables parameter."""
        with patch.object(datasets_api, "_post") as mock_post:
            variables = [{"id": 1, "value": "new_value"}]
            mock_post.return_value = {"id": 1, "variables": variables}

            result = datasets_api.update_dataset(
                dataset_id=1, variables=variables
            )

            expected_data = {"variables": variables}
            mock_post.assert_called_once_with(
                "update_dataset/1", data=expected_data
            )
            assert result["variables"] == variables

    def test_update_dataset_with_all_parameters(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test update_dataset with all optional parameters."""
        with patch.object(datasets_api, "_post") as mock_post:
            variables = [{"id": 1, "value": "value1"}]
            mock_post.return_value = {
                "id": 1,
                "name": "New Name",
                "variables": variables,
            }

            result = datasets_api.update_dataset(
                dataset_id=1,
                name="New Name",
                variables=variables,
            )

            expected_data = {"name": "New Name", "variables": variables}
            mock_post.assert_called_once_with(
                "update_dataset/1", data=expected_data
            )
            assert result["name"] == "New Name"

    def test_update_dataset_with_none_values(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test update_dataset with None values excludes them from payload."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1}

            datasets_api.update_dataset(
                dataset_id=1, name=None, variables=None
            )

            mock_post.assert_called_once_with("update_dataset/1", data={})

    def test_update_dataset_api_error(self, datasets_api: DatasetsAPI) -> None:
        """Test update_dataset raises TestRailAPIError on API failure."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.update_dataset(dataset_id=1, name="New Name")

    def test_update_dataset_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test update_dataset raises TestRailAuthenticationError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.update_dataset(dataset_id=1, name="New Name")

    def test_update_dataset_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test update_dataset raises TestRailRateLimitError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.update_dataset(dataset_id=1, name="New Name")

    # -------------------------------------------------------------------------
    # delete_dataset
    # -------------------------------------------------------------------------

    def test_delete_dataset_minimal(self, datasets_api: DatasetsAPI) -> None:
        """Test delete_dataset with required parameters."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = datasets_api.delete_dataset(dataset_id=1)

            mock_post.assert_called_once_with("delete_dataset/1")
            assert result == {}

    def test_delete_dataset_different_ids(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test delete_dataset with different dataset IDs."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {}

            datasets_api.delete_dataset(dataset_id=1)
            datasets_api.delete_dataset(dataset_id=99)

            assert mock_post.call_count == 2
            mock_post.assert_any_call("delete_dataset/1")
            mock_post.assert_any_call("delete_dataset/99")

    def test_delete_dataset_large_id(self, datasets_api: DatasetsAPI) -> None:
        """Test delete_dataset with a large dataset_id value."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.return_value = {}

            datasets_api.delete_dataset(dataset_id=999999)

            mock_post.assert_called_once_with("delete_dataset/999999")

    def test_delete_dataset_api_error(self, datasets_api: DatasetsAPI) -> None:
        """Test delete_dataset raises TestRailAPIError on API failure."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.delete_dataset(dataset_id=1)

    def test_delete_dataset_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test delete_dataset raises TestRailAuthenticationError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.delete_dataset(dataset_id=1)

    def test_delete_dataset_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test delete_dataset raises TestRailRateLimitError."""
        with patch.object(datasets_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.delete_dataset(dataset_id=1)
