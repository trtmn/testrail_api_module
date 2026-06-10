"""
This module provides the base API class for the TestRail API package.
The BaseAPI class serves as the foundation for all TestRail API modules and can be used
to create custom API modules that extend the functionality of the package.
"""

import json
import logging
from typing import Any
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

__all__ = [
    "BaseAPI",
    "TestRailAPIError",
    "TestRailAuthenticationError",
    "TestRailRateLimitError",
    "TestRailAPIException",
]


class TestRailAPIError(Exception):
    """Base exception class for TestRail API errors."""

    pass


class TestRailAuthenticationError(TestRailAPIError):
    """Raised when authentication fails."""

    pass


class TestRailRateLimitError(TestRailAPIError):
    """Raised when rate limit is exceeded."""

    pass


class TestRailAPIException(TestRailAPIError):
    """Raised for general API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_text: str | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class _TestRailRetry(Retry):
    """
    Retry policy tailored to the TestRail API.

    TestRail performs *all* write operations (including deletes) via
    POST, and those writes are not idempotent. Replaying a POST whose
    request may already have reached the server could duplicate data,
    so POSTs are only retried when it is safe to do so:

    - 429 responses (the server refused the request without acting
      on it)
    - connection errors (the request never reached the server)

    All other methods (reads) retry on connection errors, read errors,
    and the configured ``status_forcelist`` (429/5xx).
    """

    def _is_method_retryable(self, method: str) -> bool:
        # Gates read-error retries: a read error means the request may
        # have been received by the server, so never replay a POST.
        if method.upper() == "POST":
            return False
        return super()._is_method_retryable(method)

    def is_retry(
        self, method: str, status_code: int, has_retry_after: bool = False
    ) -> bool:
        # Gates status-based retries: POSTs are only safe to retry on
        # 429, where the server rejected the request without acting.
        if method.upper() == "POST":
            return status_code == 429
        return super().is_retry(method, status_code, has_retry_after)


def _create_session() -> requests.Session:
    """
    Create a ``requests.Session`` configured with the TestRail retry
    policy (3 retries, backoff factor 1, ``raise_on_status=False`` so
    the final response always flows into ``_handle_response`` for
    correct exception mapping).

    Returns:
        A configured ``requests.Session``.
    """
    session = requests.Session()
    retry_strategy = _TestRailRetry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=None,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _serialize_param_value(value: Any) -> str:
    """
    Serialize a single query parameter value for the TestRail API.

    Booleans become ``"1"``/``"0"`` (TestRail's PHP backend treats
    ``"True"`` as 0, silently inverting filters) and lists/tuples
    become comma-separated strings as required by multi-value filters.

    Args:
        value: The parameter value to serialize.

    Returns:
        The serialized string value.
    """
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, list | tuple):
        return ",".join(_serialize_param_value(item) for item in value)
    return str(value)


class BaseAPI:
    """
    Base class for all TestRail API modules.
    This class provides the core functionality for making API requests to TestRail.
    It can be inherited by custom API modules to extend the package's functionality.
    """

    def __init__(self, client: Any) -> None:
        """
        Initialize the base API class with a client instance.

        If the client provides a ``requests.Session`` (as
        ``TestRailAPI`` does), it is shared so that all submodules use
        a single connection pool. Otherwise (standalone usage) a new
        session with the TestRail retry policy is created.

        Args:
            client: The TestRailAPI client instance
        """
        self.client = client
        self.logger = logging.getLogger(__name__)

        client_session = getattr(client, "session", None)
        if isinstance(client_session, requests.Session):
            self.session = client_session
        else:
            self.session = _create_session()

    def _build_url(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> str:
        """
        Build the complete URL for an API request.

        Booleans are rendered as ``1``/``0`` and lists/tuples as
        comma-separated values, as expected by the TestRail API.

        Args:
            endpoint: The API endpoint path
            params: Optional query parameters

        Returns:
            Complete URL string
        """
        url = f"{self.client.base_url}/index.php?/api/v2/{endpoint}"
        if params:
            # Filter out None values and serialize the rest
            filtered_params = {
                k: _serialize_param_value(v)
                for k, v in params.items()
                if v is not None
            }
            if filtered_params:
                url += f"&{urlencode(filtered_params)}"
        return url

    def _get_auth(self) -> tuple[str, str]:
        """
        Get authentication credentials.

        Returns:
            Tuple of (username, password_or_api_key)

        Raises:
            TestRailAuthenticationError: If no valid authentication is available
        """
        if hasattr(self.client, "api_key") and self.client.api_key:
            return (self.client.username, self.client.api_key)
        elif hasattr(self.client, "password") and self.client.password:
            return (self.client.username, self.client.password)
        else:
            raise TestRailAuthenticationError(
                "No valid authentication method found. Please provide either an API key or password."
            )

    def _handle_response(
        self, response: requests.Response, raw: bool = False
    ) -> Any:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: The HTTP response object
            raw: If True, return the raw response body as bytes on
                success instead of parsing it as JSON (for binary
                endpoints such as ``get_attachment`` and ``get_bdd``).

        Returns:
            Parsed JSON response data, or raw bytes when ``raw=True``

        Raises:
            TestRailRateLimitError: If rate limit is exceeded
            TestRailAPIException: For other API errors
        """
        if 200 <= response.status_code < 300:
            if raw:
                return response.content

            # Handle empty responses (common for delete operations)
            response_text = response.text.strip()
            if not response_text:
                # Empty response is valid for delete operations - return empty dict
                # This matches the expected behavior for delete operations in
                # TestRail
                return {}

            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise TestRailAPIException(
                    f"Invalid JSON response: {e}"
                ) from e

        elif response.status_code == 401:
            raise TestRailAuthenticationError(
                "Authentication failed. Please check your credentials."
            )

        elif response.status_code == 429:
            # Rate limit exceeded
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                raise TestRailRateLimitError(
                    f"Rate limit exceeded. Retry after {retry_after} seconds."
                )
            else:
                raise TestRailRateLimitError("Rate limit exceeded.")

        elif response.status_code >= 400:
            error_message = (
                f"API request failed with status {response.status_code}"
            )
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_message = error_data["error"]
            except json.JSONDecodeError:
                error_message = response.text or error_message

            raise TestRailAPIException(
                error_message,
                status_code=response.status_code,
                response_text=response.text,
            )

        else:
            raise TestRailAPIException(
                f"Unexpected response status: {response.status_code}"
            )

    def _api_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        raw: bool = False,
        **kwargs: Any,
    ) -> Any:
        """
        Make an API request to TestRail following official patterns.

        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint: The API endpoint to send the request to.
            data: The data to send with the request, if any.
            params: Query parameters for the request.
            raw: If True, return the raw response body as bytes
                instead of parsing it as JSON.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Parsed JSON response from the API, or raw bytes when
            ``raw=True``.

        Raises:
            TestRailAPIError: For various API-related errors
        """
        url = self._build_url(endpoint, params)
        headers = {"Content-Type": "application/json"}

        # Update headers with any additional headers from kwargs
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        # Get authentication credentials
        auth = self._get_auth()

        # Prepare request data
        json_data = None
        if data is not None:
            json_data = data

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                auth=auth,
                json=json_data,
                timeout=self.client.timeout
                if hasattr(self.client, "timeout")
                else 30,
                **kwargs,
            )

            return self._handle_response(response, raw=raw)

        except requests.exceptions.RequestException as e:
            raise TestRailAPIException(f"Request failed: {e}") from e
        except TestRailAPIError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            raise TestRailAPIException(f"Unexpected error: {e}") from e

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        *,
        raw: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Make a GET request to the TestRail API."""
        return self._api_request(
            "GET", endpoint, params=params, raw=raw, **kwargs
        )

    def _post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Make a POST request to the TestRail API."""
        return self._api_request("POST", endpoint, data=data, **kwargs)

    def _post_multipart(
        self,
        endpoint: str,
        file_path: str,
        **kwargs: Any,
    ) -> Any:
        """
        Make a multipart/form-data POST request uploading a file.

        TestRail's file-upload endpoints (``add_attachment_to_*`` and
        ``add_bdd``) expect the file bytes in an ``attachment`` form
        field. The JSON Content-Type header must not be set so that
        requests can generate the multipart boundary header.

        Args:
            endpoint: The API endpoint to send the request to.
            file_path: Path to the file to upload.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Parsed JSON response from the API.

        Raises:
            FileNotFoundError: If ``file_path`` does not exist.
            TestRailAPIError: For various API-related errors
        """
        url = self._build_url(endpoint)
        auth = self._get_auth()
        timeout = (
            self.client.timeout if hasattr(self.client, "timeout") else 30
        )

        with open(file_path, "rb") as attachment:
            try:
                response = self.session.request(
                    method="POST",
                    url=url,
                    auth=auth,
                    files={"attachment": attachment},
                    timeout=timeout,
                    **kwargs,
                )

                return self._handle_response(response)

            except requests.exceptions.RequestException as e:
                raise TestRailAPIException(f"Request failed: {e}") from e
            except TestRailAPIError:
                # Re-raise our custom exceptions
                raise
            except Exception as e:
                raise TestRailAPIException(f"Unexpected error: {e}") from e
