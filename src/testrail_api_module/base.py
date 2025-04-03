"""
This module provides the base API class for the TestRail API package.
The BaseAPI class serves as the foundation for all TestRail API modules and can be used
to create custom API modules that extend the functionality of the package.
"""
import requests
import json
import os
import logging

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

    def _api_request(self, method, endpoint, data=None, **kwargs):
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
        url = f"{self.client.base_url}/index.php?/api/v2/{endpoint}"
        headers = {"Content-Type": "application/json"}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
            
        # Try API key authentication first
        if hasattr(self.client, 'api_key') and self.client.api_key:
            auth = (self.client.username, self.client.api_key)
            response = requests.request(
                method,
                url,
                headers=headers,
                data=json.dumps(data) if data else None,
                auth=auth,
                **kwargs
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                self.logger.warning("API key authentication failed, trying password authentication")
            else:
                self.logger.error(f"Failed to {method} {endpoint}. Response: {response.text}")
                return None
        
        # Fall back to password authentication
        if hasattr(self.client, 'password') and self.client.password:
            auth = (self.client.username, self.client.password)
            response = requests.request(
                method,
                url,
                headers=headers,
                data=json.dumps(data) if data else None,
                auth=auth,
                **kwargs
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to {method} {endpoint}. Response: {response.text}")
                return None
        
        self.logger.error("No valid authentication method found. Please provide either an API key or password.")
        return None 