"""
Tests for the ConfigurationsAPI module.

This module contains comprehensive tests for all methods in the
ConfigurationsAPI class, including error handling and proper API
request formatting.
"""

from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.configurations import ConfigurationsAPI


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
        assert hasattr(api, "logger")

    # --- get_configs ---

    def test_get_configs(self, configurations_api: ConfigurationsAPI) -> None:
        """Test get_configs returns configuration groups for a project."""
        with patch.object(configurations_api, "_get") as mock_get:
            mock_get.return_value = [
                {
                    "id": 1,
                    "name": "Browsers",
                    "configs": [
                        {"id": 10, "name": "Chrome"},
                        {"id": 11, "name": "Firefox"},
                    ],
                }
            ]

            result = configurations_api.get_configs(project_id=1)

            mock_get.assert_called_once_with("get_configs/1")
            assert result == [
                {
                    "id": 1,
                    "name": "Browsers",
                    "configs": [
                        {"id": 10, "name": "Chrome"},
                        {"id": 11, "name": "Firefox"},
                    ],
                }
            ]

    def test_get_configs_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test get_configs raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.get_configs(project_id=1)

    def test_get_configs_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test get_configs raises TestRailAuthenticationError on 401."""
        with patch.object(configurations_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.get_configs(project_id=1)

    def test_get_configs_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test get_configs raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.get_configs(project_id=1)

    # --- add_config_group ---

    def test_add_config_group(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config_group creates a new configuration group."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {"id": 5, "name": "Operating Systems"}

            result = configurations_api.add_config_group(
                project_id=1, name="Operating Systems"
            )

            mock_post.assert_called_once_with(
                "add_config_group/1", data={"name": "Operating Systems"}
            )
            assert result == {"id": 5, "name": "Operating Systems"}

    def test_add_config_group_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config_group raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.add_config_group(
                    project_id=1, name="Browsers"
                )

    def test_add_config_group_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config_group raises TestRailAuthenticationError on 401."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.add_config_group(
                    project_id=1, name="Browsers"
                )

    def test_add_config_group_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config_group raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.add_config_group(
                    project_id=1, name="Browsers"
                )

    # --- add_config ---

    def test_add_config(self, configurations_api: ConfigurationsAPI) -> None:
        """Test add_config creates a new configuration in a group."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {
                "id": 20,
                "name": "Chrome",
                "group_id": 5,
            }

            result = configurations_api.add_config(
                config_group_id=5, name="Chrome"
            )

            mock_post.assert_called_once_with(
                "add_config/5", data={"name": "Chrome"}
            )
            assert result == {"id": 20, "name": "Chrome", "group_id": 5}

    def test_add_config_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.add_config(config_group_id=5, name="Chrome")

    def test_add_config_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config raises TestRailAuthenticationError on 401."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.add_config(config_group_id=5, name="Chrome")

    def test_add_config_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test add_config raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.add_config(config_group_id=5, name="Chrome")

    # --- update_config_group ---

    def test_update_config_group(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config_group renames a configuration group."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {"id": 5, "name": "Web Browsers"}

            result = configurations_api.update_config_group(
                config_group_id=5, name="Web Browsers"
            )

            mock_post.assert_called_once_with(
                "update_config_group/5", data={"name": "Web Browsers"}
            )
            assert result == {"id": 5, "name": "Web Browsers"}

    def test_update_config_group_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config_group raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.update_config_group(
                    config_group_id=5, name="Web Browsers"
                )

    def test_update_config_group_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config_group raises TestRailAuthenticationError."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.update_config_group(
                    config_group_id=5, name="Web Browsers"
                )

    def test_update_config_group_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config_group raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.update_config_group(
                    config_group_id=5, name="Web Browsers"
                )

    # --- update_config ---

    def test_update_config(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config renames an individual configuration."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {"id": 20, "name": "Chromium"}

            result = configurations_api.update_config(
                config_id=20, name="Chromium"
            )

            mock_post.assert_called_once_with(
                "update_config/20", data={"name": "Chromium"}
            )
            assert result == {"id": 20, "name": "Chromium"}

    def test_update_config_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.update_config(config_id=20, name="Chromium")

    def test_update_config_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config raises TestRailAuthenticationError on 401."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.update_config(config_id=20, name="Chromium")

    def test_update_config_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test update_config raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.update_config(config_id=20, name="Chromium")

    # --- delete_config_group ---

    def test_delete_config_group(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config_group removes a configuration group."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = configurations_api.delete_config_group(config_group_id=5)

            mock_post.assert_called_once_with("delete_config_group/5")
            assert result == {}

    def test_delete_config_group_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config_group raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.delete_config_group(config_group_id=5)

    def test_delete_config_group_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config_group raises TestRailAuthenticationError."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.delete_config_group(config_group_id=5)

    def test_delete_config_group_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config_group raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.delete_config_group(config_group_id=5)

    # --- delete_config ---

    def test_delete_config(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config removes an individual configuration."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = configurations_api.delete_config(config_id=20)

            mock_post.assert_called_once_with("delete_config/20")
            assert result == {}

    def test_delete_config_api_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config raises TestRailAPIError on failure."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAPIError("API error")

            with pytest.raises(TestRailAPIError, match="API error"):
                configurations_api.delete_config(config_id=20)

    def test_delete_config_auth_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config raises TestRailAuthenticationError on 401."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                configurations_api.delete_config(config_id=20)

    def test_delete_config_rate_limit_error(
        self, configurations_api: ConfigurationsAPI
    ) -> None:
        """Test delete_config raises TestRailRateLimitError on 429."""
        with patch.object(configurations_api, "_post") as mock_post:
            mock_post.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                configurations_api.delete_config(config_id=20)
