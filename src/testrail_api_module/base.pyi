import logging
from typing import Any, Literal, overload

import requests
from urllib3.util.retry import Retry

class TestRailAPIError(Exception):
    """Base exception class for TestRail API errors."""

class TestRailAuthenticationError(TestRailAPIError):
    """Raised when authentication fails."""

class TestRailRateLimitError(TestRailAPIError):
    """Raised when rate limit is exceeded."""

class TestRailAPIException(TestRailAPIError):
    """Raised for general API errors."""

    status_code: int | None
    response_text: str | None
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_text: str | None = None,
    ) -> None: ...

class _TestRailRetry(Retry):
    """Retry policy tailored to the TestRail API."""

    def _is_method_retryable(self, method: str) -> bool: ...
    def is_retry(
        self, method: str, status_code: int, has_retry_after: bool = False
    ) -> bool: ...

def _create_session() -> requests.Session:
    """Create a requests.Session with the TestRail retry policy."""

def _serialize_param_value(value: Any) -> str:
    """Serialize a single query parameter value for the TestRail API."""

class BaseAPI:
    """
    Base class for all TestRail API modules.
    This class provides the core functionality for making API requests to TestRail.
    It can be inherited by custom API modules to extend the package's functionality.
    """

    client: Any
    logger: logging.Logger
    session: requests.Session
    def __init__(self, client: Any) -> None:
        """
        Initialize the base API class with a client instance.

        Args:
            client: The TestRailAPI client instance
        """
    def _build_url(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> str:
        """
        Build the complete URL for an API request.

        Args:
            endpoint: The API endpoint path
            params: Optional query parameters

        Returns:
            Complete URL string
        """
    def _get_auth(self) -> tuple[str, str]:
        """
        Get authentication credentials.

        Returns:
            Tuple of (username, password_or_api_key)

        Raises:
            TestRailAuthenticationError: If no valid authentication is available
        """
    @overload
    def _handle_response(
        self, response: requests.Response, raw: Literal[False] = False
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    @overload
    def _handle_response(
        self, response: requests.Response, raw: Literal[True]
    ) -> bytes: ...
    @overload
    def _api_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        raw: Literal[False] = False,
        **kwargs: Any,
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    @overload
    def _api_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        raw: Literal[True],
        **kwargs: Any,
    ) -> bytes: ...
    @overload
    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        raw: Literal[False] = False,
        **kwargs: Any,
    ) -> dict[str, Any] | list[dict[str, Any]]: ...
    @overload
    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        raw: Literal[True],
        **kwargs: Any,
    ) -> bytes: ...
    def _post(
        self, endpoint: str, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make a POST request to the TestRail API."""
    def _post_multipart(
        self, endpoint: str, file_path: str, **kwargs: Any
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make a multipart/form-data POST request uploading a file."""
