"""
Tests for the RolesAPI module.

This module contains comprehensive tests for all methods in the RolesAPI class,
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
from testrail_api_module.roles import RolesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestRolesAPI:
    """Test suite for RolesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def roles_api(self, mock_client: Mock) -> RolesAPI:
        """Create a RolesAPI instance with mocked client."""
        return RolesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test RolesAPI initialization."""
        api = RolesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_roles(self, roles_api: RolesAPI) -> None:
        """Test get_roles method."""
        with patch.object(roles_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Admin"},
                {"id": 2, "name": "User"},
            ]

            result = roles_api.get_roles()

            mock_request.assert_called_once_with("GET", "get_roles")
            assert len(result) == 2

    def test_api_request_failure(self, roles_api: RolesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(roles_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                roles_api.get_roles()

    def test_authentication_error(self, roles_api: RolesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(roles_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                roles_api.get_roles()

    def test_rate_limit_error(self, roles_api: RolesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(roles_api, "_api_request") as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                roles_api.get_roles()
