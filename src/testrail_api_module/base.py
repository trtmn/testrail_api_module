"""
This module provides the base API class for the TestRail API package.
The BaseAPI class serves as the foundation for all TestRail API modules and can be used
to create custom API modules that extend the functionality of the package.
"""
import requests
import json
import time
import logging
from typing import Dict, Any, Optional, Union, List
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class BaseAPI:
    """
    Base class for all TestRail API modules.
    This class provides the core functionality for making API requests to TestRail.
    It can be inherited by custom API modules to extend the package's functionality.
    """
    
    def __init__(self, client):
        """
        Initialize the base API class with a client instance.
        
        Args:
            client: The TestRailAPI client instance
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
        
        # Set up session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the complete URL for an API request.
        
        Args:
            endpoint: The API endpoint path
            params: Optional query parameters
            
        Returns:
            Complete URL string
        """
        url = f"{self.client.base_url}/index.php?/api/v2/{endpoint}"
        if params:
            # Filter out None values and convert to strings
            filtered_params = {k: str(v) for k, v in params.items() if v is not None}
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
        if hasattr(self.client, 'api_key') and self.client.api_key:
            return (self.client.username, self.client.api_key)
        elif hasattr(self.client, 'password') and self.client.password:
            return (self.client.username, self.client.password)
        else:
            raise TestRailAuthenticationError(
                "No valid authentication method found. Please provide either an API key or password."
            )

    def _handle_response(self, response: requests.Response) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
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
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise TestRailAPIException(f"Invalid JSON response: {e}")
        
        elif response.status_code == 401:
            raise TestRailAuthenticationError("Authentication failed. Please check your credentials.")
        
        elif response.status_code == 429:
            # Rate limit exceeded
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                raise TestRailRateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds.")
            else:
                raise TestRailRateLimitError("Rate limit exceeded.")
        
        elif response.status_code >= 400:
            error_message = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_message = error_data['error']
            except json.JSONDecodeError:
                error_message = response.text or error_message
            
            raise TestRailAPIException(
                error_message, 
                status_code=response.status_code,
                response_text=response.text
            )
        
        else:
            raise TestRailAPIException(f"Unexpected response status: {response.status_code}")

    def _api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
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
        url = self._build_url(endpoint, params)
        headers = {"Content-Type": "application/json"}
        
        # Update headers with any additional headers from kwargs
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
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
                timeout=self.client.timeout if hasattr(self.client, 'timeout') else 30,
                **kwargs
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.RequestException as e:
            raise TestRailAPIException(f"Request failed: {e}")
        except TestRailAPIError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            raise TestRailAPIException(f"Unexpected error: {e}")

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a GET request to the TestRail API."""
        return self._api_request('GET', endpoint, params=params, **kwargs)

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a POST request to the TestRail API."""
        return self._api_request('POST', endpoint, data=data, **kwargs) 