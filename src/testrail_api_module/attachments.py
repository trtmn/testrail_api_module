"""
This module provides functionalities to interact with attachments in TestRail.
"""
from ._common import BaseAPI

class AttachmentsAPI(BaseAPI):
    """
    Class for interacting with TestRail attachments API.
    """
    def add_attachment_to_case(self, case_id, file_path):
        """
        Add an attachment to a specific test case.

        Args:
            case_id (str): The ID of the test case.
            file_path (str): The path to the file to be attached.

        Returns:
            dict: The response from the API.
        """
        files = {'attachment': open(file_path, 'rb')}
        headers = {'Content-Type': 'multipart/form-data'}
        return self._api_request('POST', f'add_attachment_to_case/{case_id}', files=files, headers=headers)

    def add_attachment_to_plan(self, plan_id, file_path):
        """
        Add an attachment to a specific test plan.

        Args:
            plan_id (str): The ID of the test plan.
            file_path (str): The path to the file to be attached.

        Returns:
            dict: The response from the API.
        """
        files = {'attachment': open(file_path, 'rb')}
        headers = {'Content-Type': 'multipart/form-data'}
        return self._api_request('POST', f'add_attachment_to_plan/{plan_id}', files=files, headers=headers)

    def add_attachment_to_plan_entry(self, plan_id, entry_id, file_path):
        """
        Add an attachment to a specific test plan entry.

        Args:
            plan_id (str): The ID of the test plan.
            entry_id (str): The ID of the test plan entry.
            file_path (str): The path to the file to be attached.

        Returns:
            dict: The response from the API.
        """
        files = {'attachment': open(file_path, 'rb')}
        headers = {'Content-Type': 'multipart/form-data'}
        return self._api_request('POST', f'add_attachment_to_plan_entry/{plan_id}/{entry_id}', files=files, headers=headers)

    def add_attachment_to_result(self, result_id, file_path):
        """
        Add an attachment to a specific test result.

        Args:
            result_id (str): The ID of the test result.
            file_path (str): The path to the file to be attached.

        Returns:
            dict: The response from the API.
        """
        files = {'attachment': open(file_path, 'rb')}
        headers = {'Content-Type': 'multipart/form-data'}
        return self._api_request('POST', f'add_attachment_to_result/{result_id}', files=files, headers=headers)

    def add_attachment_to_run(self, run_id, file_path):
        """
        Add an attachment to a specific test run.

        Args:
            run_id (str): The ID of the test run.
            file_path (str): The path to the file to be attached.

        Returns:
            dict: The response from the API.
        """
        files = {'attachment': open(file_path, 'rb')}
        headers = {'Content-Type': 'multipart/form-data'}
        return self._api_request('POST', f'add_attachment_to_run/{run_id}', files=files, headers=headers)

    def get_attachments_for_case(self, case_id, limit=250, offset=0):
        """
        Get all attachments for a specific test case.

        Args:
            case_id (str): The ID of the test case.
            limit (int, optional): The maximum number of attachments to return (default is 250).
            offset (int, optional): The number of attachments to skip before starting to collect the result set (default is 0).

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachments_for_case/{case_id}&limit={limit}&offset={offset}')

    def get_attachments_for_plan(self, plan_id, limit=250, offset=0):
        """
        Get all attachments for a specific test plan.

        Args:
            plan_id (str): The ID of the test plan.
            limit (int, optional): The maximum number of attachments to return (default is 250).
            offset (int, optional): The number of attachments to skip before starting to collect the result set (default is 0).

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachments_for_plan/{plan_id}&limit={limit}&offset={offset}')

    def get_attachments_for_plan_entry(self, plan_id, entry_id, limit=250, offset=0):
        """
        Get all attachments for a specific test plan entry.

        Args:
            plan_id (str): The ID of the test plan.
            entry_id (str): The ID of the test plan entry.
            limit (int, optional): The maximum number of attachments to return (default is 250).
            offset (int, optional): The number of attachments to skip before starting to collect the result set (default is 0).

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachments_for_plan_entry/{plan_id}/{entry_id}&limit={limit}&offset={offset}')

    def get_attachments_for_run(self, run_id, limit=250, offset=0):
        """
        Get all attachments for a specific test run.

        Args:
            run_id (str): The ID of the test run.
            limit (int, optional): The maximum number of attachments to return (default is 250).
            offset (int, optional): The number of attachments to skip before starting to collect the result set (default is 0).

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachments_for_run/{run_id}?limit={limit}&offset={offset}')

    def get_attachments_for_test(self, test_id):
        """
        Get all attachments for a specific test.

        Args:
            test_id (str): The ID of the test.

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachments_for_test/{test_id}')

    def get_attachment(self, attachment_id):
        """
        Get details of a specific attachment.

        Args:
            attachment_id (str): The ID of the attachment.

        Returns:
            dict: The response from the API.
        """
        return self._api_request('GET', f'get_attachment/{attachment_id}')

    def delete_attachment(self, attachment_id):
        """
        Delete a specific attachment.

        Args:
            attachment_id (str): The ID of the attachment.

        Returns:
            dict: The response from the API.
        """
        return self._api_request('POST', f'delete_attachment/{attachment_id}')