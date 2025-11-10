"""
Tests for the ResultFieldsAPI module.

This module contains comprehensive tests for all methods in the ResultFieldsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.result_fields import ResultFieldsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestResultFieldsAPI:
    """Test suite for ResultFieldsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def result_fields_api(self, mock_client: Mock) -> ResultFieldsAPI:
        """Create a ResultFieldsAPI instance with mocked client."""
        return ResultFieldsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test ResultFieldsAPI initialization."""
        api = ResultFieldsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_result_field(self, result_fields_api: ResultFieldsAPI) -> None:
        """Test get_result_field method."""
        with patch.object(result_fields_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Custom Field", "type": "string"}
            
            result = result_fields_api.get_result_field(field_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_result_field/1')
            assert result == {"id": 1, "name": "Custom Field", "type": "string"}

    def test_get_result_fields(self, result_fields_api: ResultFieldsAPI) -> None:
        """Test get_result_fields method."""
        with patch.object(result_fields_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Field 1"},
                {"id": 2, "name": "Field 2"}
            ]
            
            result = result_fields_api.get_result_fields()
            
            mock_request.assert_called_once_with('GET', 'get_result_fields')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_api_request_failure(self, result_fields_api: ResultFieldsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(result_fields_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                result_fields_api.get_result_field(field_id=1)

    def test_authentication_error(self, result_fields_api: ResultFieldsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(result_fields_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                result_fields_api.get_result_field(field_id=1)

    def test_rate_limit_error(self, result_fields_api: ResultFieldsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(result_fields_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                result_fields_api.get_result_field(field_id=1)




