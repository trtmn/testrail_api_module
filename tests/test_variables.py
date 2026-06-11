"""
Tests for the VariablesAPI module.

This module contains comprehensive tests for all methods in the VariablesAPI class,
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
from testrail_api_module.variables import VariablesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestVariablesAPI:
    """Test suite for VariablesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def variables_api(self, mock_client: Mock) -> VariablesAPI:
        """Create a VariablesAPI instance with mocked client."""
        return VariablesAPI(mock_client)

    @pytest.fixture
    def sample_variable_data(self) -> dict:
        """Sample variable data for testing."""
        return {"id": 1, "name": "browser_type"}

    def test_init(self, mock_client: Mock) -> None:
        """Test VariablesAPI initialization."""
        api = VariablesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_variable(self, variables_api: VariablesAPI) -> None:
        """Test get_variable method."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "name": "browser_type"}

            result = variables_api.get_variable(variable_id=1)

            mock_get.assert_called_once_with("get_variable/1")
            assert result == {"id": 1, "name": "browser_type"}

    def test_get_variables_minimal(self, variables_api: VariablesAPI) -> None:
        """Test get_variables with only required project_id."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "var1"},
                {"id": 2, "name": "var2"},
            ]

            result = variables_api.get_variables(project_id=1)

            mock_get.assert_called_once_with("get_variables/1", params={})
            assert len(result) == 2

    def test_get_variables_with_limit(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test get_variables with limit pagination parameter."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "name": "var1"}]

            variables_api.get_variables(project_id=1, limit=10)

            mock_get.assert_called_once_with(
                "get_variables/1", params={"limit": 10}
            )

    def test_get_variables_with_offset(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test get_variables with offset pagination parameter."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = []

            variables_api.get_variables(project_id=1, offset=20)

            mock_get.assert_called_once_with(
                "get_variables/1", params={"offset": 20}
            )

    def test_get_variables_with_all_pagination(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test get_variables with both limit and offset."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = []

            variables_api.get_variables(project_id=1, limit=10, offset=20)

            mock_get.assert_called_once_with(
                "get_variables/1", params={"limit": 10, "offset": 20}
            )

    def test_get_variables_with_none_pagination(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test get_variables with None pagination omits params."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.return_value = []

            variables_api.get_variables(project_id=1, limit=None, offset=None)

            mock_get.assert_called_once_with("get_variables/1", params={})

    def test_add_variable_minimal(
        self,
        variables_api: VariablesAPI,
        sample_variable_data: dict,
    ) -> None:
        """Test add_variable with required name parameter."""
        with patch.object(variables_api, "_post") as mock_post:
            mock_post.return_value = sample_variable_data

            result = variables_api.add_variable(
                project_id=1, name="browser_type"
            )

            expected_data = {"name": "browser_type"}
            mock_post.assert_called_once_with(
                "add_variable/1", data=expected_data
            )
            assert result == sample_variable_data

    def test_update_variable(self, variables_api: VariablesAPI) -> None:
        """Test update_variable method."""
        with patch.object(variables_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "name": "updated_var"}

            result = variables_api.update_variable(
                variable_id=1, name="updated_var"
            )

            expected_data = {"name": "updated_var"}
            mock_post.assert_called_once_with(
                "update_variable/1", data=expected_data
            )
            assert result == {"id": 1, "name": "updated_var"}

    def test_delete_variable(self, variables_api: VariablesAPI) -> None:
        """Test delete_variable method."""
        with patch.object(variables_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = variables_api.delete_variable(variable_id=1)

            mock_post.assert_called_once_with("delete_variable/1")
            assert result == {}

    def test_api_request_failure(self, variables_api: VariablesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                variables_api.get_variables(project_id=1)

    def test_authentication_error(self, variables_api: VariablesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                variables_api.get_variables(project_id=1)

    def test_rate_limit_error(self, variables_api: VariablesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(variables_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                variables_api.get_variables(project_id=1)
