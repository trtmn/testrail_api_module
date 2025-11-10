"""
Tests for the ConfigurationsAPI module.

This module contains comprehensive tests for all methods in the ConfigurationsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.configurations import ConfigurationsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestConfigurationsAPI:
    """Test suite for ConfigurationsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def configurations_api(self, mock_client: Mock) -> ConfigurationsAPI:
        """Create a ConfigurationsAPI instance with mocked client."""
        return ConfigurationsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test ConfigurationsAPI initialization."""
        api = ConfigurationsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_configuration(self, configurations_api: ConfigurationsAPI) -> None:
        """Test get_configuration method."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Config 1"}
            
            result = configurations_api.get_configuration(config_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_configuration/1')
            assert result == {"id": 1, "name": "Config 1"}

    def test_get_configurations(self, configurations_api: ConfigurationsAPI) -> None:
        """Test get_configurations method."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Config 1"},
                {"id": 2, "name": "Config 2"}
            ]
            
            result = configurations_api.get_configurations(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_configurations/1')
            assert len(result) == 2

    def test_add_configuration_minimal(self, configurations_api: ConfigurationsAPI) -> None:
        """Test add_configuration with minimal required parameters."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Config"}
            
            result = configurations_api.add_configuration(project_id=1, name="New Config")
            
            expected_data = {"name": "New Config"}
            mock_request.assert_called_once_with('POST', 'add_configuration/1', data=expected_data)
            assert result == {"id": 1, "name": "New Config"}

    def test_add_configuration_with_all_parameters(self, configurations_api: ConfigurationsAPI) -> None:
        """Test add_configuration with all optional parameters."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Config"}
            
            result = configurations_api.add_configuration(
                project_id=1,
                name="New Config",
                description="Config description",
                group_id=2
            )
            
            expected_data = {
                "name": "New Config",
                "description": "Config description",
                "group_id": 2
            }
            mock_request.assert_called_once_with('POST', 'add_configuration/1', data=expected_data)

    def test_update_configuration(self, configurations_api: ConfigurationsAPI) -> None:
        """Test update_configuration method."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Config"}
            
            result = configurations_api.update_configuration(
                config_id=1,
                name="Updated Config",
                description="Updated description"
            )
            
            expected_data = {
                "name": "Updated Config",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with('POST', 'update_configuration/1', data=expected_data)

    def test_delete_configuration(self, configurations_api: ConfigurationsAPI) -> None:
        """Test delete_configuration method."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = configurations_api.delete_configuration(config_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_configuration/1')
            assert result == {}

    def test_api_request_failure(self, configurations_api: ConfigurationsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                configurations_api.get_configuration(config_id=1)

    def test_authentication_error(self, configurations_api: ConfigurationsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                configurations_api.get_configuration(config_id=1)

    def test_rate_limit_error(self, configurations_api: ConfigurationsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(configurations_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                configurations_api.get_configuration(config_id=1)





