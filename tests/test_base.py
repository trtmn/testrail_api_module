"""
Tests for the base module.

This module contains comprehensive tests for the BaseAPI class and exception classes,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
import json
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING
import requests

from testrail_api_module.base import (
    BaseAPI,
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
    TestRailAPIException
)

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestExceptionClasses:
    """Test suite for exception classes."""

    def test_testrail_api_error(self) -> None:
        """Test TestRailAPIError exception."""
        error = TestRailAPIError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_testrail_authentication_error(self) -> None:
        """Test TestRailAuthenticationError exception."""
        error = TestRailAuthenticationError("Auth failed")
        assert str(error) == "Auth failed"
        assert isinstance(error, TestRailAPIError)

    def test_testrail_rate_limit_error(self) -> None:
        """Test TestRailRateLimitError exception."""
        error = TestRailRateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert isinstance(error, TestRailAPIError)

    def test_testrail_api_exception_with_status_code(self) -> None:
        """Test TestRailAPIException with status_code."""
        error = TestRailAPIException("Error", status_code=404)
        assert str(error) == "Error"
        assert error.status_code == 404
        assert error.response_text is None
        assert isinstance(error, TestRailAPIError)

    def test_testrail_api_exception_with_all_attributes(self) -> None:
        """Test TestRailAPIException with all attributes."""
        error = TestRailAPIException(
            "Error message",
            status_code=500,
            response_text="Server error"
        )
        assert str(error) == "Error message"
        assert error.status_code == 500
        assert error.response_text == "Server error"


class TestBaseAPI:
    """Test suite for BaseAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        client.timeout = 30
        return client

    @pytest.fixture
    def base_api(self, mock_client: Mock) -> BaseAPI:
        """Create a BaseAPI instance with mocked client."""
        return BaseAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test BaseAPI initialization."""
        api = BaseAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')
        assert hasattr(api, 'session')
        assert api.session is not None

    def test_init_session_mounting(self, mock_client: Mock) -> None:
        """Test BaseAPI initialization sets up session with retry strategy."""
        api = BaseAPI(mock_client)

        # Verify session was created
        assert api.session is not None
        # Verify adapters were mounted (http and https)
        # The session should have adapters mounted
        assert hasattr(api.session, 'adapters')
        # Check that adapters exist for both http and https
        # session.adapters is an OrderedDict with protocol prefixes as keys
        assert 'http://' in api.session.adapters
        assert 'https://' in api.session.adapters

    def test_build_url_without_params(self, base_api: BaseAPI) -> None:
        """Test _build_url without parameters."""
        url = base_api._build_url("get_case/1")
        expected = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        assert url == expected

    def test_build_url_with_params(self, base_api: BaseAPI) -> None:
        """Test _build_url with parameters."""
        params = {"limit": 10, "offset": 0}
        url = base_api._build_url("get_cases/1", params=params)
        assert "limit=10" in url
        assert "offset=0" in url
        assert "get_cases/1" in url

    def test_build_url_with_none_params(self, base_api: BaseAPI) -> None:
        """Test _build_url with None values in params."""
        params = {"limit": 10, "offset": None, "filter": "test"}
        url = base_api._build_url("get_cases/1", params=params)
        assert "limit=10" in url
        assert "filter=test" in url
        assert "offset" not in url  # None values should be filtered out

    def test_build_url_with_empty_params(self, base_api: BaseAPI) -> None:
        """Test _build_url with empty params dict."""
        url = base_api._build_url("get_cases/1", params={})
        expected = "https://testrail.example.com/index.php?/api/v2/get_cases/1"
        assert url == expected

    def test_build_url_with_complex_params(self, base_api: BaseAPI) -> None:
        """Test _build_url with complex parameter values."""
        params = {"ids": [1, 2, 3], "name": "test case"}
        url = base_api._build_url("get_cases/1", params=params)
        # All values should be converted to strings
        assert "ids" in url
        assert "name" in url

    def test_build_url_with_all_none_params(self, base_api: BaseAPI) -> None:
        """Test _build_url when all params are None (edge case)."""
        params = {"limit": None, "offset": None, "filter": None}
        url = base_api._build_url("get_cases/1", params=params)
        # Should not add query parameters when all are None
        expected = "https://testrail.example.com/index.php?/api/v2/get_cases/1"
        assert url == expected

    def test_get_auth_with_api_key(self, base_api: BaseAPI) -> None:
        """Test _get_auth with API key."""
        auth = base_api._get_auth()
        assert auth == ("testuser", "test_api_key")

    def test_get_auth_with_password(self) -> None:
        """Test _get_auth with password."""
        client = Mock(spec=['username', 'password'])
        client.username = "testuser"
        client.password = "test_password"
        api = BaseAPI(client)
        auth = api._get_auth()
        assert auth == ("testuser", "test_password")

    def test_get_auth_prefers_api_key_over_password(self) -> None:
        """Test _get_auth prefers API key over password."""
        client = Mock()
        client.username = "testuser"
        client.api_key = "test_api_key"
        client.password = "test_password"
        api = BaseAPI(client)
        auth = api._get_auth()
        assert auth == ("testuser", "test_api_key")

    def test_get_auth_no_credentials(self) -> None:
        """Test _get_auth raises error when no credentials provided."""
        # Use a simple object instead of Mock to avoid auto-attribute creation
        class SimpleClient:
            def __init__(self):
                self.username = "testuser"
                # No api_key or password attributes

        client = SimpleClient()
        api = BaseAPI(client)
        with pytest.raises(TestRailAuthenticationError, match="No valid authentication method found"):
            api._get_auth()

    def test_get_auth_with_empty_api_key(self) -> None:
        """Test _get_auth when api_key is empty string."""
        client = Mock()
        client.username = "testuser"
        client.api_key = ""  # Empty string
        client.password = "test_password"
        api = BaseAPI(client)
        # Should fall back to password when api_key is empty
        auth = api._get_auth()
        assert auth == ("testuser", "test_password")

    def test_get_auth_with_none_api_key(self) -> None:
        """Test _get_auth when api_key is None."""
        client = Mock()
        client.username = "testuser"
        client.api_key = None
        client.password = "test_password"
        api = BaseAPI(client)
        # Should fall back to password when api_key is None
        auth = api._get_auth()
        assert auth == ("testuser", "test_password")

    def test_get_auth_with_empty_password(self) -> None:
        """Test _get_auth when password is empty string."""
        client = Mock()
        client.username = "testuser"
        client.api_key = "test_api_key"
        client.password = ""  # Empty string
        api = BaseAPI(client)
        # Should use api_key when password is empty
        auth = api._get_auth()
        assert auth == ("testuser", "test_api_key")

    def test_get_auth_no_api_key_attribute(self) -> None:
        """Test _get_auth when client has no api_key attribute."""
        client = Mock(spec=['username', 'password'])
        client.username = "testuser"
        # No api_key attribute at all - use spec to prevent auto-creation
        client.password = "test_password"
        api = BaseAPI(client)
        auth = api._get_auth()
        assert auth == ("testuser", "test_password")

    def test_handle_response_success(self, base_api: BaseAPI) -> None:
        """Test _handle_response with successful response (200)."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = {"id": 1, "name": "Test"}

        result = base_api._handle_response(response)
        assert result == {"id": 1, "name": "Test"}

    def test_handle_response_success_list(self, base_api: BaseAPI) -> None:
        """Test _handle_response with successful list response (200)."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.json.return_value = [{"id": 1}, {"id": 2}]

        result = base_api._handle_response(response)
        assert result == [{"id": 1}, {"id": 2}]

    def test_handle_response_empty_body(self, base_api: BaseAPI) -> None:
        """Test _handle_response with empty response body (common for delete operations)."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.text = ""  # Empty response body

        result = base_api._handle_response(response)
        # Empty responses should return empty dict for delete operations
        assert result == {}

    def test_handle_response_empty_body_with_whitespace(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with response body containing only whitespace."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.text = "   \n\t  "  # Only whitespace

        result = base_api._handle_response(response)
        # Whitespace-only responses should be treated as empty
        assert result == {}

    def test_handle_response_invalid_json(self, base_api: BaseAPI) -> None:
        """Test _handle_response with invalid JSON (non-empty but malformed)."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.text = "not valid json"  # Non-empty but invalid JSON
        response.json.side_effect = json.JSONDecodeError(
            "Invalid JSON", "not valid json", 0)

        with pytest.raises(TestRailAPIException, match="Invalid JSON response"):
            base_api._handle_response(response)

    def test_handle_response_401(self, base_api: BaseAPI) -> None:
        """Test _handle_response with 401 (authentication error)."""
        response = Mock(spec=requests.Response)
        response.status_code = 401

        with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
            base_api._handle_response(response)

    def test_handle_response_429_with_retry_after(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 429 (rate limit) with Retry-After header."""
        response = Mock(spec=requests.Response)
        response.status_code = 429
        response.headers = {"Retry-After": "60"}

        with pytest.raises(TestRailRateLimitError, match="Retry after 60 seconds"):
            base_api._handle_response(response)

    def test_handle_response_429_without_retry_after(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 429 (rate limit) without Retry-After header."""
        response = Mock(spec=requests.Response)
        response.status_code = 429
        response.headers = {}

        with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
            base_api._handle_response(response)

    def test_handle_response_400_with_error_in_json(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 400+ status and error in JSON."""
        response = Mock(spec=requests.Response)
        response.status_code = 400
        response.json.return_value = {"error": "Bad request error"}
        response.text = '{"error": "Bad request error"}'

        with pytest.raises(TestRailAPIException) as exc_info:
            base_api._handle_response(response)
        assert exc_info.value.status_code == 400
        assert exc_info.value.response_text == '{"error": "Bad request error"}'
        assert "Bad request error" in str(exc_info.value)

    def test_handle_response_400_with_json_but_no_error_key(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 400+ status, valid JSON but no 'error' key."""
        response = Mock(spec=requests.Response)
        response.status_code = 400
        response.json.return_value = {"message": "Bad request", "code": 400}
        response.text = '{"message": "Bad request", "code": 400}'

        with pytest.raises(TestRailAPIException) as exc_info:
            base_api._handle_response(response)
        assert exc_info.value.status_code == 400
        assert exc_info.value.response_text == '{"message": "Bad request", "code": 400}'
        # Should use default error message when 'error' key not present
        assert "API request failed with status 400" in str(exc_info.value)

    def test_handle_response_500_without_error_in_json(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 500+ status without error in JSON."""
        response = Mock(spec=requests.Response)
        response.status_code = 500
        response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        response.text = "Internal Server Error"

        with pytest.raises(TestRailAPIException) as exc_info:
            base_api._handle_response(response)
        assert exc_info.value.status_code == 500
        assert exc_info.value.response_text == "Internal Server Error"
        # When response.text is not empty, it uses response.text as the error
        # message
        assert "Internal Server Error" in str(exc_info.value)

    def test_handle_response_500_with_empty_text(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with 500+ status with empty text."""
        response = Mock(spec=requests.Response)
        response.status_code = 500
        response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        response.text = ""

        with pytest.raises(TestRailAPIException) as exc_info:
            base_api._handle_response(response)
        assert exc_info.value.status_code == 500
        assert "API request failed with status 500" in str(exc_info.value)

    def test_handle_response_unexpected_status(
            self, base_api: BaseAPI) -> None:
        """Test _handle_response with unexpected status code."""
        response = Mock(spec=requests.Response)
        response.status_code = 100

        with pytest.raises(TestRailAPIException, match="Unexpected response status: 100"):
            base_api._handle_response(response)

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    @patch('testrail_api_module.base.BaseAPI._handle_response')
    def test_api_request_get_success(
            self,
            mock_handle,
            mock_auth,
            mock_build,
            base_api: BaseAPI) -> None:
        """Test _api_request with successful GET request."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        result = base_api._api_request('GET', 'get_case/1')

        assert result == {"id": 1}
        base_api.session.request.assert_called_once()
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs['method'] == 'GET'
        assert call_kwargs['headers']['Content-Type'] == 'application/json'

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    @patch('testrail_api_module.base.BaseAPI._handle_response')
    def test_api_request_post_with_data(
            self,
            mock_handle,
            mock_auth,
            mock_build,
            base_api: BaseAPI) -> None:
        """Test _api_request with POST request and data."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/add_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._api_request('POST', 'add_case/1', data=data)

        assert result == {"id": 1}
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs['method'] == 'POST'
        assert call_kwargs['json'] == data

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    @patch('testrail_api_module.base.BaseAPI._handle_response')
    def test_api_request_post_with_explicit_none_data(
            self, mock_handle, mock_auth, mock_build, base_api: BaseAPI) -> None:
        """Test _api_request with POST request and data=None explicitly."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/add_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        result = base_api._api_request('POST', 'add_case/1', data=None)

        assert result == {"id": 1}
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs['method'] == 'POST'
        assert call_kwargs['json'] is None

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_with_custom_headers(
            self, mock_auth, mock_build, base_api: BaseAPI) -> None:
        """Test _api_request with custom headers in kwargs."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)

        custom_headers = {"X-Custom-Header": "value"}
        base_api._api_request('GET', 'get_case/1', headers=custom_headers)

        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs['headers']['Content-Type'] == 'application/json'
        assert call_kwargs['headers']['X-Custom-Header'] == 'value'

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_with_timeout(
            self,
            mock_auth,
            mock_build,
            base_api: BaseAPI) -> None:
        """Test _api_request uses client timeout."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)

        base_api._api_request('GET', 'get_case/1')

        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs['timeout'] == 30

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_without_timeout_attribute(
            self, mock_auth, mock_build) -> None:
        """Test _api_request uses default timeout when client has no timeout attribute."""
        client = Mock(spec=['base_url', 'username', 'api_key'])
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        # No timeout attribute - use spec to prevent auto-creation
        api = BaseAPI(client)

        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        api.session.request = Mock(return_value=mock_response)

        api._api_request('GET', 'get_case/1')

        call_kwargs = api.session.request.call_args[1]
        assert call_kwargs['timeout'] == 30  # Default timeout

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_with_request_exception(
            self, mock_auth, mock_build, base_api: BaseAPI) -> None:
        """Test _api_request handles RequestException."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        base_api.session.request = Mock(
            side_effect=requests.exceptions.RequestException("Connection error"))

        with pytest.raises(TestRailAPIException, match="Request failed: Connection error"):
            base_api._api_request('GET', 'get_case/1')

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_re_raises_testrail_errors(
            self, mock_auth, mock_build, base_api: BaseAPI) -> None:
        """Test _api_request re-raises TestRailAPIError exceptions."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)

        # Simulate _handle_response raising TestRailAPIError
        with patch.object(base_api, '_handle_response', side_effect=TestRailAPIError("API error")):
            with pytest.raises(TestRailAPIError, match="API error"):
                base_api._api_request('GET', 'get_case/1')

    @patch('testrail_api_module.base.BaseAPI._build_url')
    @patch('testrail_api_module.base.BaseAPI._get_auth')
    def test_api_request_with_unexpected_exception(
            self, mock_auth, mock_build, base_api: BaseAPI) -> None:
        """Test _api_request handles unexpected exceptions."""
        mock_build.return_value = "https://testrail.example.com/index.php?/api/v2/get_case/1"
        mock_auth.return_value = ("user", "key")
        base_api.session.request = Mock(
            side_effect=ValueError("Unexpected error"))

        with pytest.raises(TestRailAPIException, match="Unexpected error: Unexpected error"):
            base_api._api_request('GET', 'get_case/1')

    @patch.object(BaseAPI, '_api_request')
    def test_get_method(self, mock_api_request, base_api: BaseAPI) -> None:
        """Test _get method."""
        mock_api_request.return_value = {"id": 1}

        result = base_api._get('get_case/1', params={"limit": 10})

        mock_api_request.assert_called_once_with(
            'GET', 'get_case/1', params={"limit": 10})
        assert result == {"id": 1}

    @patch.object(BaseAPI, '_api_request')
    def test_post_method(self, mock_api_request, base_api: BaseAPI) -> None:
        """Test _post method."""
        mock_api_request.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._post('add_case/1', data=data)

        mock_api_request.assert_called_once_with(
            'POST', 'add_case/1', data=data)
        assert result == {"id": 1}

    @patch.object(BaseAPI, '_api_request')
    def test_get_method_with_kwargs(
            self,
            mock_api_request,
            base_api: BaseAPI) -> None:
        """Test _get method with additional kwargs."""
        mock_api_request.return_value = {"id": 1}

        result = base_api._get('get_case/1', params={"limit": 10}, timeout=60)

        mock_api_request.assert_called_once_with(
            'GET', 'get_case/1', params={"limit": 10}, timeout=60)
        assert result == {"id": 1}

    @patch.object(BaseAPI, '_api_request')
    def test_post_method_with_kwargs(
            self,
            mock_api_request,
            base_api: BaseAPI) -> None:
        """Test _post method with additional kwargs."""
        mock_api_request.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._post('add_case/1', data=data, timeout=60)

        mock_api_request.assert_called_once_with(
            'POST', 'add_case/1', data=data, timeout=60)
        assert result == {"id": 1}
