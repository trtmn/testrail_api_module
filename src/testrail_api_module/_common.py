"""
`_common.py` serves as a foundational module for the TestRail API package, providing a base class for API requests.
"""
import requests
import json
import os

class BaseAPI:
    """
    Base class for all TestRail API modules.
    """
    def __init__(self, client):
        """
        Initialize the base API class with a client instance.
        
        Args:
            client: The TestRailAPI client instance
        """
        self.client = client

    def _api_request(self, method, endpoint, data=None, **kwargs):
        """
        Make an API request to TestRail.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            data (dict, optional): The data to send with the request, if any.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            dict: The JSON response from the API if the request is successful.
            None: If the request fails.
        """
        url = f"{self.client.base_url}/index.php?/api/v2/{endpoint}"
        headers = {"Content-Type": "application/json"}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
            
        response = requests.request(
            method,
            url,
            headers=headers,
            data=json.dumps(data) if data else None,
            auth=(self.client.username, self.client.api_key),
            **kwargs
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to {method} {endpoint}. Response:", response.text)
            return None

