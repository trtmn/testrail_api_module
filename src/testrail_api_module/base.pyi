from typing import Any, Optional, Dict, List

class BaseAPI:
    """
    Base class for all TestRail API modules.
    This class provides the core functionality for making API requests to TestRail.
    It can be inherited by custom API modules to extend the package's functionality.
    """
    client: Any
    logger: Any
    def __init__(self, client: Any) -> None:
        """
        Initialize the base API class with a client instance.
        
        Args:
            client: The TestRailAPI client instance
        """
    def _api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """
        Make an API request to TestRail. Supports both API key and password authentication.
        Will try API key first, then fall back to password if API key fails.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            data (dict, optional): The data to send with the request, if any.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API if the request is successful.
            None: If the request fails with both authentication methods.
        """
