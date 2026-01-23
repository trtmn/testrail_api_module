import requests
from typing import Any, Optional, Dict, List
from typing import Any

class TestRailAPIError(Exception):
    """Base exception class for TestRail API errors."""
class TestRailAuthenticationError(TestRailAPIError):
    """Raised when authentication fails."""
class TestRailRateLimitError(TestRailAPIError):
    """Raised when rate limit is exceeded."""

class TestRailAPIException(TestRailAPIError):
    """Raised for general API errors."""
    status_code: Any
    response_text: Any
    def __init__(self, message: str, status_code: int | None = None, response_text: str | None = None) -> None: ...

class BaseAPI:
    """
    Base class for all TestRail API modules.
    This class provides the core functionality for making API requests to TestRail.
    It can be inherited by custom API modules to extend the package's functionality.
    """
    client: Any
    logger: Any
    session: Any
    def __init__(self, client: Any) -> None:
        """
        Initialize the base API class with a client instance.
        
        Args:
            client: The TestRailAPI client instance
        """
    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
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
    def _handle_response(self, response: requests.Response) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: The HTTP response object
            
        Returns:
            Parsed JSON response data
            
        Raises:
            TestRailRateLimitError: If rate limit is exceeded
            TestRailAPIException: For other API errors
        """
    def _api_request(self, method: str, endpoint: str, data: dict[str, Any] | None = None, params: dict[str, Any] | None = None, **kwargs) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Make an API request to TestRail following official patterns.

        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint: The API endpoint to send the request to.
            data: The data to send with the request, if any.
            params: Query parameters for the request.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            Parsed JSON response from the API.

        Raises:
            TestRailAPIError: For various API-related errors
        """
    def _get(self, endpoint: str, params: dict[str, Any] | None = None, **kwargs) -> dict[str, Any] | list[dict[str, Any]]:
        """Make a GET request to the TestRail API."""
    def _post(self, endpoint: str, data: dict[str, Any] | None = None, **kwargs) -> dict[str, Any] | list[dict[str, Any]]:
        """Make a POST request to the TestRail API."""
