"""
Tests for the BaseAPI module.

This module contains comprehensive tests for the BaseAPI class,
including authentication methods, API request handling, error scenarios,
and edge cases.
"""

import pytest
import json
import logging
from unittest.mock import Mock, patch, MagicMock

from testrail_api_module.base import BaseAPI


class TestBaseAPI:
    """Test suite for BaseAPI class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        client.password = "test_password"
        return client

    @pytest.fixture
    def base_api(self, mock_client):
        """Create a BaseAPI instance with mocked client."""
        return BaseAPI(mock_client)

    def test_init(self, mock_client):
        """Test BaseAPI initialization."""
        api = BaseAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")
        assert isinstance(api.logger, logging.Logger)
        assert api.logger.name == "testrail_api_module.base"

    def test_api_request_success_with_api_key(self, base_api):
        """Test successful API request using API key authentication."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True, "data": "test"}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Verify request was made with API key auth
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert (
                call_args[0][1]
                == "https://testrail.example.com/index.php?/api/v2/test/endpoint"
            )
            assert call_args[1]["auth"] == ("testuser", "test_api_key")
            assert call_args[1]["headers"] == {"Content-Type": "application/json"}
            assert result == {"success": True, "data": "test"}

    def test_api_request_success_with_password_fallback(self, base_api):
        """Test API request falling back to password authentication when API key fails."""
        with patch("requests.request") as mock_request:
            # First call fails with 401 (API key auth failed)
            mock_response_401 = Mock()
            mock_response_401.status_code = 401

            # Second call succeeds with password auth
            mock_response_200 = Mock()
            mock_response_200.status_code = 200
            mock_response_200.json.return_value = {"success": True, "data": "test"}

            mock_request.side_effect = [mock_response_401, mock_response_200]

            result = base_api._api_request("POST", "test/endpoint", {"key": "value"})

            # Verify two requests were made
            assert mock_request.call_count == 2

            # First call with API key
            first_call = mock_request.call_args_list[0]
            assert first_call[1]["auth"] == ("testuser", "test_api_key")

            # Second call with password
            second_call = mock_request.call_args_list[1]
            assert second_call[1]["auth"] == ("testuser", "test_password")
            assert second_call[1]["data"] == '{"key": "value"}'

            assert result == {"success": True, "data": "test"}

    def test_api_request_with_custom_headers(self, base_api):
        """Test API request with custom headers."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            custom_headers = {"X-Custom-Header": "custom_value"}
            result = base_api._api_request(
                "GET", "test/endpoint", headers=custom_headers
            )

            call_args = mock_request.call_args
            expected_headers = {
                "Content-Type": "application/json",
                "X-Custom-Header": "custom_value",
            }
            assert call_args[1]["headers"] == expected_headers
            assert result == {"success": True}

    def test_api_request_with_data(self, base_api):
        """Test API request with data payload."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            test_data = {"name": "test", "description": "test description"}
            result = base_api._api_request("POST", "test/endpoint", data=test_data)

            call_args = mock_request.call_args
            assert call_args[1]["data"] == json.dumps(test_data)
            assert result == {"success": True}

    def test_api_request_with_none_data(self, base_api):
        """Test API request with None data."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint", data=None)

            call_args = mock_request.call_args
            assert call_args[1]["data"] is None
            assert result == {"success": True}

    def test_api_request_with_additional_kwargs(self, base_api):
        """Test API request with additional kwargs."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request(
                "GET", "test/endpoint", timeout=30, verify=False
            )

            call_args = mock_request.call_args
            assert call_args[1]["timeout"] == 30
            assert call_args[1]["verify"] is False
            assert result == {"success": True}

    def test_api_request_api_key_failure_no_password(self, base_api):
        """Test API request when API key fails and no password is available."""
        # Remove password from client
        base_api.client.password = None

        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Should only make one request with API key
            mock_request.assert_called_once()
            assert result is None

    def test_api_request_both_auth_methods_fail(self, base_api):
        """Test API request when both API key and password authentication fail."""
        with patch("requests.request") as mock_request:
            # API key fails with 401, password fails with 500
            mock_response_401 = Mock()
            mock_response_401.status_code = 401

            mock_response_500 = Mock()
            mock_response_500.status_code = 500
            mock_response_500.text = "Internal Server Error"

            mock_request.side_effect = [mock_response_401, mock_response_500]

            result = base_api._api_request("GET", "test/endpoint")

            # Should make two requests (API key then password)
            assert mock_request.call_count == 2
            assert result is None

    def test_api_request_no_auth_methods_available(self, base_api):
        """Test API request when no authentication methods are available."""
        # Remove both auth methods
        base_api.client.api_key = None
        base_api.client.password = None

        result = base_api._api_request("GET", "test/endpoint")

        # Should return None without making any requests
        assert result is None

    def test_api_request_client_without_api_key_attr(self, base_api):
        """Test API request when client doesn't have api_key attribute."""
        # Remove api_key attribute entirely
        delattr(base_api.client, "api_key")

        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Should use password auth directly
            call_args = mock_request.call_args
            assert call_args[1]["auth"] == ("testuser", "test_password")
            assert result == {"success": True}

    def test_api_request_client_without_password_attr(self, base_api):
        """Test API request when client doesn't have password attribute."""
        # Remove password attribute entirely
        delattr(base_api.client, "password")

        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Should use API key auth
            call_args = mock_request.call_args
            assert call_args[1]["auth"] == ("testuser", "test_api_key")
            assert result == {"success": True}

    def test_api_request_different_http_methods(self, base_api):
        """Test API request with different HTTP methods."""
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

        for method in methods:
            with patch("requests.request") as mock_request:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"method": method}
                mock_request.return_value = mock_response

                result = base_api._api_request(method, "test/endpoint")

                call_args = mock_request.call_args
                assert call_args[0][0] == method
                assert result == {"method": method}

    def test_api_request_complex_data_serialization(self, base_api):
        """Test API request with complex data that needs JSON serialization."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            complex_data = {
                "nested": {
                    "list": [1, 2, 3],
                    "dict": {"key": "value"},
                    "null": None,
                    "boolean": True,
                },
                "unicode": "café",
                "special_chars": "!@#$%^&*()",
            }

            result = base_api._api_request("POST", "test/endpoint", data=complex_data)

            call_args = mock_request.call_args
            expected_json = json.dumps(complex_data)
            assert call_args[1]["data"] == expected_json
            assert result == {"success": True}

    def test_api_request_empty_data_dict(self, base_api):
        """Test API request with empty data dictionary."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("POST", "test/endpoint", data={})

            call_args = mock_request.call_args
            # Empty dict {} is falsy in Python, so it becomes None
            assert call_args[1]["data"] is None
            assert result == {"success": True}

    def test_api_request_url_construction(self, base_api):
        """Test that API request constructs URLs correctly."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            base_api._api_request("GET", "projects/get/123")

            call_args = mock_request.call_args
            expected_url = (
                "https://testrail.example.com/index.php?/api/v2/projects/get/123"
            )
            assert call_args[0][1] == expected_url

    def test_api_request_with_headers_kwarg_removal(self, base_api):
        """Test that headers kwarg is properly removed from kwargs."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            base_api._api_request("GET", "test/endpoint", headers={"X-Test": "value"})

            call_args = mock_request.call_args
            # headers should be merged with default headers
            expected_headers = {"Content-Type": "application/json", "X-Test": "value"}
            assert call_args[1]["headers"] == expected_headers
            assert call_args[1]["auth"] == ("testuser", "test_api_key")

    def test_api_request_logging_on_failure(self, base_api):
        """Test that failures are properly logged."""
        with (
            patch("requests.request") as mock_request,
            patch.object(base_api.logger, "error") as mock_error_logger,
            patch.object(base_api.logger, "warning") as mock_warning_logger,
        ):

            # API key fails with 401, password fails with 500
            mock_response_401 = Mock()
            mock_response_401.status_code = 401

            mock_response_500 = Mock()
            mock_response_500.status_code = 500
            mock_response_500.text = "Internal Server Error"

            mock_request.side_effect = [mock_response_401, mock_response_500]

            result = base_api._api_request("GET", "test/endpoint")

            # Should log warning for API key failure
            mock_warning_logger.assert_called_once_with(
                "API key authentication failed, trying password authentication"
            )

            # Should log error for password failure
            mock_error_logger.assert_called_with(
                "Failed to GET test/endpoint. Response: Internal Server Error"
            )

            assert result is None

    def test_api_request_no_auth_logging(self, base_api):
        """Test logging when no authentication methods are available."""
        base_api.client.api_key = None
        base_api.client.password = None

        with patch.object(base_api.logger, "error") as mock_error_logger:
            result = base_api._api_request("GET", "test/endpoint")

            mock_error_logger.assert_called_once_with(
                "No valid authentication method found. Please provide either an API key or password."
            )
            assert result is None

    @pytest.mark.parametrize("status_code", [400, 403, 404, 500, 502, 503])
    def test_api_request_various_error_status_codes(self, base_api, status_code):
        """Test API request with various error status codes."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.text = f"Error {status_code}"
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            assert result is None

    def test_api_request_json_decode_error(self, base_api):
        """Test API request when JSON response cannot be decoded."""
        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_request.return_value = mock_response

            # This should raise an exception when trying to decode JSON
            with pytest.raises(json.JSONDecodeError):
                base_api._api_request("GET", "test/endpoint")

    def test_api_request_requests_exception(self, base_api):
        """Test API request when requests library raises an exception."""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = Exception("Network error")

            # This should raise the exception
            with pytest.raises(Exception, match="Network error"):
                base_api._api_request("GET", "test/endpoint")

    def test_api_request_with_falsey_api_key(self, base_api):
        """Test API request when API key is falsey (empty string, etc.)."""
        base_api.client.api_key = ""

        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Should use password auth directly
            call_args = mock_request.call_args
            assert call_args[1]["auth"] == ("testuser", "test_password")
            assert result == {"success": True}

    def test_api_request_with_falsey_password(self, base_api):
        """Test API request when password is falsey (empty string, etc.)."""
        base_api.client.password = ""

        with patch("requests.request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response

            result = base_api._api_request("GET", "test/endpoint")

            # Should use API key auth
            call_args = mock_request.call_args
            assert call_args[1]["auth"] == ("testuser", "test_api_key")
            assert result == {"success": True}
