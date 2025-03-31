"""
`_common.py` serves as a foundational module for the TestRail API package, providing a base class for API requests and a function to set API credentials.
"""
import requests
import json
import os

class ApiConstructor:
    """
    A class to construct and make API requests to TestRail.
    """

    def __init__(self) -> object:
        """
        Initializes the ApiConstructor with default values for run_id, case_id, project_id,
        baseurl, username, and password.
        """
        self.run_id = None  # Actual run id in demo project
        """The run ID for the TestRail run. This is required."""
        
        self.case_id = None  # Actual case id in demo project
        """The case ID for the TestRail case. This is required."""
        
        self.project_id = None
        """The project ID for the TestRail project. This is required."""
        
        self.baseurl = None #Required!
        """The base URL for the TestRail API (e.g., "https://your_testrail_instance.testrail.io"). This is required.
        Can be set in the constructor or as an environment variable.
        use {your_instance}.set_testrail_api_credentials()"""
        
        self.username = None #Required!
        """The username for TestRail API authentication. This is required.
        Can be set in the constructor or as an environment variable.
        use {your_instance}.set_testrail_api_credentials()"""
        
        self.password = None
        """The password for TestRail API authentication. This is required.
        Can be set in the constructor or as an environment variable.
        use {your_instance}.set_testrail_api_credentials()"""

    def set_testrail_api_credentials(self, baseurl=None, username=None, password=None):
        """
        Set the TestRail API credentials as environment variables.

        Args:
            baseurl (str): The base URL for the TestRail API.
            username (str): The username for TestRail API authentication.
            password (str): The password for TestRail API authentication.
        """
        if baseurl is not None:
            self.baseurl = baseurl
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password

    def fetch_testrail_api_credentials(self):
        """
        Fetch the TestRail API credentials from the environment variables.

        Returns:
            tuple: A tuple containing the base URL, username, and password for the TestRail API.
        """

        os.environ['TESTRAIL_API_BASEURL'] = self.baseurl
        os.environ['TESTRAIL_API_USERNAME'] = self.username
        os.environ['TESTRAIL_API_PASSWORD'] = self.password

        return self.baseurl, self.username, self.password


    def api_request(self, method, endpoint, data=None):
                """
                Make an API request to TestRail.

                Args:
                    method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
                    endpoint (str): The API endpoint to send the request to.
                    data (dict, optional): The data to send with the request, if any.

                Returns:
                    dict: The JSON response from the API if the request is successful.
                    None: If the request fails.
                """
                # Confirm that all 3 required variables are set
                if not self.baseurl:
                    raise ValueError("The base URL for the TestRail API is required. See documentation for more info")
                if not self.username:
                    raise ValueError("The username for TestRail API authentication is required. See documentation for more info")
                if not self.password:
                    raise ValueError("The password for TestRail API authentication is required. See documentation for more info")

                url = f"{self.baseurl}/index.php?/api/v2/{endpoint}"
                headers = {"Content-Type": "application/json"}
                response = requests.request(method, url, headers=headers, data=json.dumps(data), auth=(self.username, self.password))
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Failed to {method} {endpoint}. Response:", response.text)
                    return None

