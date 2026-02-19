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

    def test_init(self, mock_client: Mock) -> None:
        """Test VariablesAPI initialization."""
        api = VariablesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_variable(self, variables_api: VariablesAPI) -> None:
        """Test get_variable method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 1,
                "name": "var1",
                "value": "value1",
            }

            result = result = variables_api.get_variable(variable_id=1)
            mock_request.assert_called_once_with("GET", "get_variable/1")
            assert result == {"id": 1, "name": "var1", "value": "value1"}

    def test_get_variables(self, variables_api: VariablesAPI) -> None:
        """Test get_variables method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "var1"},
                {"id": 2, "name": "var2"},
            ]

            result = variables_api.get_variables(project_id=1)
            mock_request.assert_called_once_with("GET", "get_variables/1")
            assert len(result) == 2

    def test_add_variable_minimal(self, variables_api: VariablesAPI) -> None:
        """Test add_variable with minimal required parameters."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 1,
                "name": "var1",
                "value": "value1",
            }

            result = variables_api.add_variable(
                project_id=1, name="var1", value="value1"
            )

            expected_data = {"name": "var1", "value": "value1"}
            mock_request.assert_called_once_with(
                "POST", "add_variable/1", data=expected_data
            )
            assert result == {"id": 1, "name": "var1", "value": "value1"}

    def test_add_variable_with_description(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test add_variable with description."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "var1"}

            variables_api.add_variable(
                project_id=1,
                name="var1",
                value="value1",
                description="Variable description",
            )

            expected_data = {
                "name": "var1",
                "value": "value1",
                "description": "Variable description",
            }
            mock_request.assert_called_once_with(
                "POST", "add_variable/1", data=expected_data
            )

    def test_update_variable(self, variables_api: VariablesAPI) -> None:
        """Test update_variable method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {
                "id": 1,
                "name": "updated_var",
                "value": "updated_value",
            }

            variables_api.update_variable(
                variable_id=1, name="updated_var", value="updated_value"
            )

            expected_data = {"name": "updated_var", "value": "updated_value"}
            mock_request.assert_called_once_with(
                "POST", "update_variable/1", data=expected_data
            )

    def test_delete_variable(self, variables_api: VariablesAPI) -> None:
        """Test delete_variable method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = result = variables_api.delete_variable(variable_id=1)
            mock_request.assert_called_once_with("POST", "delete_variable/1")
            assert result == {}

    def test_get_variable_groups(self, variables_api: VariablesAPI) -> None:
        """Test get_variable_groups method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Group 1"},
                {"id": 2, "name": "Group 2"},
            ]

            result = variables_api.get_variable_groups(project_id=1)

            mock_request.assert_called_once_with(
                "GET", "get_variable_groups/1"
            )
            assert len(result) == 2

    def test_add_variable_group_minimal(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test add_variable_group with minimal required parameters."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Group"}

            result = variables_api.add_variable_group(
                project_id=1, name="New Group"
            )

            expected_data = {"name": "New Group"}
            mock_request.assert_called_once_with(
                "POST", "add_variable_group/1", data=expected_data
            )
            assert result == {"id": 1, "name": "New Group"}

    def test_add_variable_group_with_description(
        self, variables_api: VariablesAPI
    ) -> None:
        """Test add_variable_group with description."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Group"}

            variables_api.add_variable_group(
                project_id=1, name="New Group", description="Group description"
            )

            expected_data = {
                "name": "New Group",
                "description": "Group description",
            }
            mock_request.assert_called_once_with(
                "POST", "add_variable_group/1", data=expected_data
            )

    def test_update_variable_group(self, variables_api: VariablesAPI) -> None:
        """Test update_variable_group method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Group"}

            variables_api.update_variable_group(
                group_id=1, name="Updated Group"
            )

            expected_data = {"name": "Updated Group"}
            mock_request.assert_called_once_with(
                "POST", "update_variable_group/1", data=expected_data
            )

    def test_delete_variable_group(self, variables_api: VariablesAPI) -> None:
        """Test delete_variable_group method."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.return_value = {}

            result = variables_api.delete_variable_group(group_id=1)

            mock_request.assert_called_once_with(
                "POST", "delete_variable_group/1"
            )
            assert result == {}

    def test_api_request_failure(self, variables_api: VariablesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                variables_api.get_variable(variable_id=1)

    def test_authentication_error(self, variables_api: VariablesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                variables_api.get_variable(variable_id=1)

    def test_rate_limit_error(self, variables_api: VariablesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(variables_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                variables_api.get_variable(variable_id=1)
