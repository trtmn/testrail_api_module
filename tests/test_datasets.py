"""
Tests for the DatasetsAPI module.

This module contains comprehensive tests for all methods in the
DatasetsAPI class, including edge cases, error handling, and proper
API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.datasets import DatasetsAPI
from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError
)

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


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

    def test_init(self, mock_client: Mock) -> None:
        """Test DatasetsAPI initialization."""
        api = DatasetsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_dataset(self, datasets_api: DatasetsAPI) -> None:
        """Test get_dataset method."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "id": 1,
                "name": "Test Dataset",
                "variables": [
                    {"id": 1, "name": "var1", "value": "value1"},
                    {"id": 2, "name": "var2", "value": "value2"}
                ]
            }

            result = datasets_api.get_dataset(dataset_id=1)

            mock_request.assert_called_once_with('GET', 'get_dataset/1')
            assert result is not None
            assert result["id"] == 1
            assert result["name"] == "Test Dataset"
            assert len(result["variables"]) == 2
            assert result["variables"][0]["name"] == "var1"

    def test_get_datasets(self, datasets_api: DatasetsAPI) -> None:
        """Test get_datasets method."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {
                    "id": 1,
                    "name": "Dataset 1",
                    "variables": [
                        {"id": 1, "name": "var1", "value": "value1"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Dataset 2",
                    "variables": [
                        {"id": 2, "name": "var2", "value": "value2"}
                    ]
                }
            ]

            result = datasets_api.get_datasets(project_id=1)

            mock_request.assert_called_once_with('GET', 'get_datasets/1')
            assert result is not None
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["name"] == "Dataset 1"
            assert result[1]["id"] == 2
            assert result[1]["name"] == "Dataset 2"

    def test_get_datasets_empty_list(self, datasets_api: DatasetsAPI) -> None:
        """Test get_datasets with empty result."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = []

            result = datasets_api.get_datasets(project_id=1)

            mock_request.assert_called_once_with('GET', 'get_datasets/1')
            assert result == []

    def test_get_dataset_with_variables(self, datasets_api: DatasetsAPI) -> None:
        """Test get_dataset with multiple variables."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "id": 5,
                "name": "Complex Dataset",
                "variables": [
                    {"id": 10, "name": "username", "value": "testuser"},
                    {"id": 11, "name": "password", "value": "testpass"},
                    {"id": 12, "name": "environment", "value": "staging"}
                ]
            }

            result = datasets_api.get_dataset(dataset_id=5)

            mock_request.assert_called_once_with('GET', 'get_dataset/5')
            assert result is not None
            assert len(result["variables"]) == 3
            assert result["variables"][0]["name"] == "username"
            assert result["variables"][1]["name"] == "password"
            assert result["variables"][2]["name"] == "environment"

    def test_get_datasets_different_project_ids(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets with different project IDs."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = [{"id": 1, "name": "Dataset 1"}]

            result1 = datasets_api.get_datasets(project_id=1)
            result2 = datasets_api.get_datasets(project_id=2)

            assert mock_request.call_count == 2
            mock_request.assert_any_call('GET', 'get_datasets/1')
            mock_request.assert_any_call('GET', 'get_datasets/2')
            assert result1 is not None
            assert result2 is not None

    def test_get_dataset_different_ids(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_dataset with different dataset IDs."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Dataset"}

            result1 = datasets_api.get_dataset(dataset_id=1)
            result2 = datasets_api.get_dataset(dataset_id=100)

            assert mock_request.call_count == 2
            mock_request.assert_any_call('GET', 'get_dataset/1')
            mock_request.assert_any_call('GET', 'get_dataset/100')
            assert result1 is not None
            assert result2 is not None

    def test_api_request_failure(self, datasets_api: DatasetsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                datasets_api.get_dataset(dataset_id=1)

    def test_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test behavior when authentication fails."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.get_dataset(dataset_id=1)

    def test_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.get_dataset(dataset_id=1)

    def test_get_datasets_api_request_failure(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets behavior when API request fails."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError(
                "API request failed"
            )

            with pytest.raises(
                TestRailAPIError, match="API request failed"
            ):
                datasets_api.get_datasets(project_id=1)

    def test_get_datasets_authentication_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets behavior when authentication fails."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                datasets_api.get_datasets(project_id=1)

    def test_get_datasets_rate_limit_error(
        self, datasets_api: DatasetsAPI
    ) -> None:
        """Test get_datasets behavior when rate limit is exceeded."""
        with patch.object(datasets_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                datasets_api.get_datasets(project_id=1)

