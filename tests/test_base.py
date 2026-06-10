"""
Tests for the base module.

This module contains comprehensive tests for the BaseAPI class and exception classes,
including edge cases, error handling, and proper API request formatting.
"""

import json
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest
import requests

from testrail_api_module.base import (
    BaseAPI,
    TestRailAPIError,
    TestRailAPIException,
    TestRailAuthenticationError,
    TestRailRateLimitError,
    _TestRailRetry,
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
            "Error message", status_code=500, response_text="Server error"
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
        assert hasattr(api, "logger")
        assert hasattr(api, "session")
        assert api.session is not None

    def test_init_session_mounting(self, mock_client: Mock) -> None:
        """Test BaseAPI initialization sets up session with retry strategy."""
        api = BaseAPI(mock_client)

        # Verify session was created
        assert api.session is not None
        # Verify adapters were mounted (http and https)
        # The session should have adapters mounted
        assert hasattr(api.session, "adapters")
        # Check that adapters exist for both http and https
        # session.adapters is an OrderedDict with protocol prefixes as keys
        assert "http://" in api.session.adapters
        assert "https://" in api.session.adapters

    def test_init_shares_client_session(self) -> None:
        """Test BaseAPI reuses the client's requests.Session when provided."""
        shared_session = requests.Session()
        client = Mock()
        client.session = shared_session
        api = BaseAPI(client)
        assert api.session is shared_session
        shared_session.close()

    def test_init_creates_own_session_without_client_session(
        self, mock_client: Mock
    ) -> None:
        """Test BaseAPI creates its own session when the client has none.

        A Mock attribute is not a real requests.Session, so standalone
        usage falls back to creating a configured session.
        """
        api = BaseAPI(mock_client)
        assert isinstance(api.session, requests.Session)
        assert api.session is not mock_client.session

    def test_session_retry_configuration(self, base_api: BaseAPI) -> None:
        """Test the mounted adapter uses the TestRail retry policy."""
        adapter = base_api.session.get_adapter("https://testrail.example.com")
        retry = adapter.max_retries
        assert isinstance(retry, _TestRailRetry)
        assert retry.total == 3
        assert retry.backoff_factor == 1
        assert retry.raise_on_status is False
        assert retry.allowed_methods is None
        assert set(retry.status_forcelist) == {429, 500, 502, 503, 504}

    def test_retry_policy_get_retries_on_429_and_5xx(self) -> None:
        """Test the retry policy retries GETs on 429 and 5xx statuses."""
        retry = _TestRailRetry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=None,
            raise_on_status=False,
        )
        assert retry.is_retry("GET", 429) is True
        assert retry.is_retry("GET", 500) is True
        assert retry.is_retry("GET", 503) is True
        assert retry.is_retry("GET", 200) is False
        assert retry._is_method_retryable("GET") is True

    def test_retry_policy_post_retries_only_on_429(self) -> None:
        """Test the retry policy retries POSTs on 429 only (writes are
        not idempotent in TestRail, so 5xx must not be replayed)."""
        retry = _TestRailRetry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=None,
            raise_on_status=False,
        )
        assert retry.is_retry("POST", 429) is True
        assert retry.is_retry("POST", 500) is False
        assert retry.is_retry("POST", 502) is False
        assert retry.is_retry("POST", 503) is False
        assert retry.is_retry("POST", 503, has_retry_after=True) is False
        assert retry.is_retry("post", 500) is False
        # Read errors (request may have reached the server) must not
        # be retried for POSTs either.
        assert retry._is_method_retryable("POST") is False

    def test_retry_policy_survives_increment(self) -> None:
        """Test the retry policy class is preserved across increment()
        (urllib3 creates a new Retry instance per attempt)."""
        retry = _TestRailRetry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=None,
            raise_on_status=False,
        )
        bumped = retry.increment(
            method="GET", url="/", response=None, error=None
        )
        assert isinstance(bumped, _TestRailRetry)
        assert bumped.total == 2
        assert bumped.is_retry("POST", 500) is False

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
        # Lists are comma-joined ("," url-encodes to %2C)
        assert "ids=1%2C2%2C3" in url
        assert "name=test+case" in url

    def test_build_url_serializes_true_as_1(self, base_api: BaseAPI) -> None:
        """Test _build_url serializes True as 1 (TestRail's PHP backend
        treats "True" as 0, silently inverting filters)."""
        url = base_api._build_url("get_runs/1", params={"is_completed": True})
        assert "is_completed=1" in url
        assert "True" not in url

    def test_build_url_serializes_false_as_0(self, base_api: BaseAPI) -> None:
        """Test _build_url serializes False as 0."""
        url = base_api._build_url("get_runs/1", params={"is_completed": False})
        assert "is_completed=0" in url
        assert "False" not in url

    def test_build_url_serializes_list_as_comma_joined(
        self, base_api: BaseAPI
    ) -> None:
        """Test _build_url comma-joins list filter values."""
        url = base_api._build_url("get_cases/1", params={"created_by": [1, 2]})
        assert "created_by=1%2C2" in url
        assert "%5B" not in url  # no "[" from a Python repr

    def test_build_url_serializes_tuple_as_comma_joined(
        self, base_api: BaseAPI
    ) -> None:
        """Test _build_url comma-joins tuple filter values."""
        url = base_api._build_url(
            "get_cases/1", params={"priority_id": (4, 5)}
        )
        assert "priority_id=4%2C5" in url

    def test_build_url_preserves_prejoined_string(
        self, base_api: BaseAPI
    ) -> None:
        """Test _build_url leaves pre-joined string filters intact
        (results.py/tests.py already comma-join their list params)."""
        url = base_api._build_url(
            "get_results/1", params={"status_id": "1,2,3"}
        )
        assert "status_id=1%2C2%2C3" in url

    def test_build_url_serializes_bools_inside_lists(
        self, base_api: BaseAPI
    ) -> None:
        """Test _build_url serializes booleans inside list values."""
        url = base_api._build_url(
            "get_cases/1", params={"flags": [True, False]}
        )
        assert "flags=1%2C0" in url

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
        client = Mock(spec=["username", "password"])
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
        with pytest.raises(
            TestRailAuthenticationError,
            match="No valid authentication method found",
        ):
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
        client = Mock(spec=["username", "password"])
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
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with response body containing only whitespace."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.text = "   \n\t  "  # Only whitespace

        result = base_api._handle_response(response)
        # Whitespace-only responses should be treated as empty
        assert result == {}

    def test_handle_response_201_created(self, base_api: BaseAPI) -> None:
        """Test _handle_response accepts 201 as success."""
        response = Mock(spec=requests.Response)
        response.status_code = 201
        response.text = '{"id": 1}'
        response.json.return_value = {"id": 1}

        result = base_api._handle_response(response)
        assert result == {"id": 1}

    def test_handle_response_204_no_content(self, base_api: BaseAPI) -> None:
        """Test _handle_response accepts 204 with empty body as success."""
        response = Mock(spec=requests.Response)
        response.status_code = 204
        response.text = ""

        result = base_api._handle_response(response)
        assert result == {}

    def test_handle_response_raw_returns_bytes(
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with raw=True returns response.content."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b"\x89PNG binary data"

        result = base_api._handle_response(response, raw=True)
        assert result == b"\x89PNG binary data"

    def test_handle_response_raw_skips_json_parsing(
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with raw=True never parses JSON, so
        non-JSON bodies (e.g. .feature files) succeed."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.content = b"Feature: Login"
        response.json.side_effect = json.JSONDecodeError(
            "Invalid JSON", "Feature: Login", 0
        )

        result = base_api._handle_response(response, raw=True)
        assert result == b"Feature: Login"
        response.json.assert_not_called()

    def test_handle_response_raw_error_still_raises(
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with raw=True still maps error codes."""
        response = Mock(spec=requests.Response)
        response.status_code = 401

        with pytest.raises(TestRailAuthenticationError):
            base_api._handle_response(response, raw=True)

    def test_handle_response_invalid_json(self, base_api: BaseAPI) -> None:
        """Test _handle_response with invalid JSON (non-empty but malformed)."""
        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.text = "not valid json"  # Non-empty but invalid JSON
        response.json.side_effect = json.JSONDecodeError(
            "Invalid JSON", "not valid json", 0
        )

        with pytest.raises(
            TestRailAPIException, match="Invalid JSON response"
        ):
            base_api._handle_response(response)

    def test_handle_response_401(self, base_api: BaseAPI) -> None:
        """Test _handle_response with 401 (authentication error)."""
        response = Mock(spec=requests.Response)
        response.status_code = 401

        with pytest.raises(
            TestRailAuthenticationError, match="Authentication failed"
        ):
            base_api._handle_response(response)

    def test_handle_response_429_with_retry_after(
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with 429 (rate limit) with Retry-After header."""
        response = Mock(spec=requests.Response)
        response.status_code = 429
        response.headers = {"Retry-After": "60"}

        with pytest.raises(
            TestRailRateLimitError, match="Retry after 60 seconds"
        ):
            base_api._handle_response(response)

    def test_handle_response_429_without_retry_after(
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with 429 (rate limit) without Retry-After header."""
        response = Mock(spec=requests.Response)
        response.status_code = 429
        response.headers = {}

        with pytest.raises(
            TestRailRateLimitError, match="Rate limit exceeded"
        ):
            base_api._handle_response(response)

    def test_handle_response_400_with_error_in_json(
        self, base_api: BaseAPI
    ) -> None:
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
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with 400+ status, valid JSON but no 'error' key."""
        response = Mock(spec=requests.Response)
        response.status_code = 400
        response.json.return_value = {"message": "Bad request", "code": 400}
        response.text = '{"message": "Bad request", "code": 400}'

        with pytest.raises(TestRailAPIException) as exc_info:
            base_api._handle_response(response)
        assert exc_info.value.status_code == 400
        assert (
            exc_info.value.response_text
            == '{"message": "Bad request", "code": 400}'
        )
        # Should use default error message when 'error' key not present
        assert "API request failed with status 400" in str(exc_info.value)

    def test_handle_response_500_without_error_in_json(
        self, base_api: BaseAPI
    ) -> None:
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
        self, base_api: BaseAPI
    ) -> None:
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
        self, base_api: BaseAPI
    ) -> None:
        """Test _handle_response with unexpected status code."""
        response = Mock(spec=requests.Response)
        response.status_code = 100

        with pytest.raises(
            TestRailAPIException, match="Unexpected response status: 100"
        ):
            base_api._handle_response(response)

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    @patch("testrail_api_module.base.BaseAPI._handle_response")
    def test_api_request_get_success(
        self, mock_handle, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request with successful GET request."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        result = base_api._api_request("GET", "get_case/1")

        assert result == {"id": 1}
        base_api.session.request.assert_called_once()
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["method"] == "GET"
        assert call_kwargs["headers"]["Content-Type"] == "application/json"

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    @patch("testrail_api_module.base.BaseAPI._handle_response")
    def test_api_request_post_with_data(
        self, mock_handle, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request with POST request and data."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/add_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._api_request("POST", "add_case/1", data=data)

        assert result == {"id": 1}
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["method"] == "POST"
        assert call_kwargs["json"] == data

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    @patch("testrail_api_module.base.BaseAPI._handle_response")
    def test_api_request_post_with_explicit_none_data(
        self, mock_handle, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request with POST request and data=None explicitly."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/add_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)
        mock_handle.return_value = {"id": 1}

        result = base_api._api_request("POST", "add_case/1", data=None)

        assert result == {"id": 1}
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["method"] == "POST"
        assert call_kwargs["json"] is None

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_with_custom_headers(
        self, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request with custom headers in kwargs."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)

        custom_headers = {"X-Custom-Header": "value"}
        base_api._api_request("GET", "get_case/1", headers=custom_headers)

        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["headers"]["Content-Type"] == "application/json"
        assert call_kwargs["headers"]["X-Custom-Header"] == "value"

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_with_timeout(
        self, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request uses client timeout."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        base_api.session.request = Mock(return_value=mock_response)

        base_api._api_request("GET", "get_case/1")

        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["timeout"] == 30

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_without_timeout_attribute(
        self, mock_auth, mock_build
    ) -> None:
        """Test _api_request uses default timeout when client has no timeout attribute."""
        client = Mock(spec=["base_url", "username", "api_key"])
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        # No timeout attribute - use spec to prevent auto-creation
        api = BaseAPI(client)

        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        api.session.request = Mock(return_value=mock_response)

        api._api_request("GET", "get_case/1")

        call_kwargs = api.session.request.call_args[1]
        assert call_kwargs["timeout"] == 30  # Default timeout

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_with_request_exception(
        self, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request handles RequestException."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        base_api.session.request = Mock(
            side_effect=requests.exceptions.RequestException(
                "Connection error"
            )
        )

        with pytest.raises(
            TestRailAPIException, match="Request failed: Connection error"
        ):
            base_api._api_request("GET", "get_case/1")

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_re_raises_testrail_errors(
        self, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request re-raises TestRailAPIError exceptions."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        mock_response = Mock(spec=requests.Response)
        base_api.session.request = Mock(return_value=mock_response)

        # Simulate _handle_response raising TestRailAPIError
        with patch.object(
            base_api,
            "_handle_response",
            side_effect=TestRailAPIError("API error"),
        ):
            with pytest.raises(TestRailAPIError, match="API error"):
                base_api._api_request("GET", "get_case/1")

    @patch("testrail_api_module.base.BaseAPI._build_url")
    @patch("testrail_api_module.base.BaseAPI._get_auth")
    def test_api_request_with_unexpected_exception(
        self, mock_auth, mock_build, base_api: BaseAPI
    ) -> None:
        """Test _api_request handles unexpected exceptions."""
        mock_build.return_value = (
            "https://testrail.example.com/index.php?/api/v2/get_case/1"
        )
        mock_auth.return_value = ("user", "key")
        base_api.session.request = Mock(
            side_effect=ValueError("Unexpected error")
        )

        with pytest.raises(
            TestRailAPIException, match="Unexpected error: Unexpected error"
        ):
            base_api._api_request("GET", "get_case/1")

    @patch.object(BaseAPI, "_api_request")
    def test_get_method(self, mock_api_request, base_api: BaseAPI) -> None:
        """Test _get method."""
        mock_api_request.return_value = {"id": 1}

        result = base_api._get("get_case/1", params={"limit": 10})

        mock_api_request.assert_called_once_with(
            "GET", "get_case/1", params={"limit": 10}, raw=False
        )
        assert result == {"id": 1}

    @patch.object(BaseAPI, "_api_request")
    def test_get_method_raw(self, mock_api_request, base_api: BaseAPI) -> None:
        """Test _get method passes raw=True through to _api_request."""
        mock_api_request.return_value = b"Feature: Login"

        result = base_api._get("get_bdd/1", raw=True)

        mock_api_request.assert_called_once_with(
            "GET", "get_bdd/1", params=None, raw=True
        )
        assert result == b"Feature: Login"

    @patch.object(BaseAPI, "_api_request")
    def test_post_method(self, mock_api_request, base_api: BaseAPI) -> None:
        """Test _post method."""
        mock_api_request.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._post("add_case/1", data=data)

        mock_api_request.assert_called_once_with(
            "POST", "add_case/1", data=data
        )
        assert result == {"id": 1}

    @patch.object(BaseAPI, "_api_request")
    def test_get_method_with_kwargs(
        self, mock_api_request, base_api: BaseAPI
    ) -> None:
        """Test _get method with additional kwargs."""
        mock_api_request.return_value = {"id": 1}

        result = base_api._get("get_case/1", params={"limit": 10}, timeout=60)

        mock_api_request.assert_called_once_with(
            "GET", "get_case/1", params={"limit": 10}, raw=False, timeout=60
        )
        assert result == {"id": 1}

    @patch.object(BaseAPI, "_api_request")
    def test_post_method_with_kwargs(
        self, mock_api_request, base_api: BaseAPI
    ) -> None:
        """Test _post method with additional kwargs."""
        mock_api_request.return_value = {"id": 1}

        data = {"title": "Test Case"}
        result = base_api._post("add_case/1", data=data, timeout=60)

        mock_api_request.assert_called_once_with(
            "POST", "add_case/1", data=data, timeout=60
        )
        assert result == {"id": 1}

    def test_api_request_raw_returns_bytes(self, base_api: BaseAPI) -> None:
        """Test _api_request with raw=True returns raw bytes and does
        not forward 'raw' to the session request."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.content = b"binary content"
        base_api.session.request = Mock(return_value=mock_response)

        result = base_api._api_request("GET", "get_attachment/1", raw=True)

        assert result == b"binary content"
        call_kwargs = base_api.session.request.call_args[1]
        assert "raw" not in call_kwargs
        assert call_kwargs["method"] == "GET"

    def test_post_multipart_success(self, base_api: BaseAPI, tmp_path) -> None:
        """Test _post_multipart uploads the opened file in an
        'attachment' form field without the JSON Content-Type header."""
        file_path = tmp_path / "evidence.png"
        file_path.write_bytes(b"\x89PNG fake image bytes")

        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = '{"attachment_id": 443}'
        mock_response.json.return_value = {"attachment_id": 443}
        base_api.session.request = Mock(return_value=mock_response)

        result = base_api._post_multipart(
            "add_attachment_to_case/1", str(file_path)
        )

        assert result == {"attachment_id": 443}
        call_kwargs = base_api.session.request.call_args[1]
        assert call_kwargs["method"] == "POST"
        assert "add_attachment_to_case/1" in call_kwargs["url"]
        assert call_kwargs["auth"] == ("testuser", "test_api_key")
        assert call_kwargs["timeout"] == 30
        # The file handle must be sent as the 'attachment' form field
        assert "attachment" in call_kwargs["files"]
        assert call_kwargs["files"]["attachment"].name == str(file_path)
        # No JSON Content-Type header: requests must generate the
        # multipart boundary header itself
        assert "headers" not in call_kwargs
        assert "json" not in call_kwargs

    def test_post_multipart_missing_file(self, base_api: BaseAPI) -> None:
        """Test _post_multipart raises FileNotFoundError for a missing
        file (not a wrapped TestRailAPIException)."""
        base_api.session.request = Mock()

        with pytest.raises(FileNotFoundError):
            base_api._post_multipart(
                "add_attachment_to_case/1", "/nonexistent/file.png"
            )
        base_api.session.request.assert_not_called()

    def test_post_multipart_authentication_error(
        self, base_api: BaseAPI, tmp_path
    ) -> None:
        """Test _post_multipart maps 401 to TestRailAuthenticationError."""
        file_path = tmp_path / "evidence.png"
        file_path.write_bytes(b"data")

        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 401
        base_api.session.request = Mock(return_value=mock_response)

        with pytest.raises(
            TestRailAuthenticationError, match="Authentication failed"
        ):
            base_api._post_multipart(
                "add_attachment_to_case/1", str(file_path)
            )

    def test_post_multipart_rate_limit_error(
        self, base_api: BaseAPI, tmp_path
    ) -> None:
        """Test _post_multipart maps 429 to TestRailRateLimitError."""
        file_path = tmp_path / "evidence.png"
        file_path.write_bytes(b"data")

        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.headers = {}
        base_api.session.request = Mock(return_value=mock_response)

        with pytest.raises(
            TestRailRateLimitError, match="Rate limit exceeded"
        ):
            base_api._post_multipart(
                "add_attachment_to_case/1", str(file_path)
            )

    def test_post_multipart_request_exception(
        self, base_api: BaseAPI, tmp_path
    ) -> None:
        """Test _post_multipart wraps RequestException."""
        file_path = tmp_path / "evidence.png"
        file_path.write_bytes(b"data")

        base_api.session.request = Mock(
            side_effect=requests.exceptions.RequestException(
                "Connection error"
            )
        )

        with pytest.raises(
            TestRailAPIException, match="Request failed: Connection error"
        ):
            base_api._post_multipart(
                "add_attachment_to_case/1", str(file_path)
            )
