"""
This module provides functionality for managing users in TestRail.
Users are the people who can access and interact with TestRail.
"""

from typing import Any

from .base import BaseAPI


class UsersAPI(BaseAPI):
    """
    API for managing TestRail users.
    """

    def get_user(self, user_id: int) -> dict[str, Any] | None:
        """
        Get a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: The user data if successful, None otherwise.
        """
        return self._api_request("GET", f"get_user/{user_id}")

    def get_users(self) -> list[dict[str, Any]] | None:
        """
        Get all users.

        Returns:
            list: List of users if successful, None otherwise.
        """
        return self._api_request("GET", "get_users")

    def get_current_user(self) -> dict[str, Any] | None:
        """
        Get the currently authenticated user.

        Requires TestRail 6.6+.

        Returns:
            Dict containing the current user data.
        """
        return self._api_request("GET", "get_current_user")

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        """
        Get a user by email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            dict: The user data if successful, None otherwise.
        """
        return self._api_request("GET", f"get_user_by_email&email={email}")
