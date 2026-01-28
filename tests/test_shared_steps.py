"""
Tests for the SharedStepsAPI module.

This module contains comprehensive tests for all methods in the SharedStepsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.shared_steps import SharedStepsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

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

    def test_init(self, mock_client: Mock) -> None:
        """Test SharedStepsAPI initialization."""
        api = SharedStepsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_shared_step(self, shared_steps_api: SharedStepsAPI) -> None:
        """Test get_shared_step method."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "title": "Shared Step 1"}

            result = shared_steps_api.get_shared_step(shared_step_id=1)
            mock_request.assert_called_once_with('GET', 'get_shared_step/1')
            assert result == {"id": 1, "title": "Shared Step 1"}

    def test_get_shared_steps(self, shared_steps_api: SharedStepsAPI) -> None:
        """Test get_shared_steps method."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "title": "Shared Step 1"},
                {"id": 2, "title": "Shared Step 2"}
            ]

            result = shared_steps_api.get_shared_steps(project_id=1)

            mock_request.assert_called_once_with('GET', 'get_shared_steps/1')
            assert len(result) == 2

    def test_add_shared_step_minimal(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test add_shared_step with minimal required parameters."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "title": "New Shared Step"}

            steps = [
                {"content": "Step 1", "expected": "Result 1"},
                {"content": "Step 2", "expected": "Result 2"}
            ]

            result = shared_steps_api.add_shared_step(
                project_id=1,
                title="New Shared Step",
                steps=steps
            )

            expected_data = {
                "title": "New Shared Step",
                "steps": steps
            }
            mock_request.assert_called_once_with(
                'POST', 'add_shared_step/1', data=expected_data)
            assert result == {"id": 1, "title": "New Shared Step"}

    def test_add_shared_step_with_description(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test add_shared_step with description."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "title": "New Shared Step"}

            steps = [{"content": "Step 1", "expected": "Result 1"}]

            shared_steps_api.add_shared_step(
                project_id=1,
                title="New Shared Step",
                steps=steps,
                description="Shared step description"
            )

            expected_data = {
                "title": "New Shared Step",
                "steps": steps,
                "description": "Shared step description"
            }
            mock_request.assert_called_once_with(
                'POST', 'add_shared_step/1', data=expected_data)

    def test_update_shared_step(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test update_shared_step method."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "id": 1, "title": "Updated Shared Step"}

            shared_steps_api.update_shared_step(
                shared_step_id=1,
                title="Updated Shared Step",
                description="Updated description"
            )

            expected_data = {
                "title": "Updated Shared Step",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with(
                'POST', 'update_shared_step/1', data=expected_data)

    def test_delete_shared_step(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test delete_shared_step method."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.return_value = {}

            result = shared_steps_api.delete_shared_step(shared_step_id=1)

            mock_request.assert_called_once_with(
                'POST', 'delete_shared_step/1')
            assert result == {}

    def test_api_request_failure(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                shared_steps_api.get_shared_step(shared_step_id=1)

    def test_authentication_error(
            self, shared_steps_api: SharedStepsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed")

            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                shared_steps_api.get_shared_step(shared_step_id=1)

    def test_rate_limit_error(self, shared_steps_api: SharedStepsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(shared_steps_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded")

            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                shared_steps_api.get_shared_step(shared_step_id=1)
