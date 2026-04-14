"""
This module provides functionality for managing users in TestRail.
Users are the people who can access and interact with TestRail.
"""

from typing import Any

from .base import BaseAPI

__all__ = ["UsersAPI"]


class UsersAPI(BaseAPI):
    """
    API for managing TestRail users.

    This class provides methods to retrieve user information,
    including looking up users by ID, email, or getting the
    currently authenticated user.
    """

    def get_user(self, user_id: int) -> dict[str, Any]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            Dict containing the user data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_user/{user_id}")

    def get_users(self) -> list[dict[str, Any]]:
        """
        Get all users.

        Returns:
            List of dictionaries containing user data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", "get_users")

    def get_current_user(self) -> dict[str, Any]:
        """
        Get the currently authenticated user.

        Requires TestRail 6.6+.

        Returns:
            Dict containing the current user data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", "get_current_user")

    def get_user_by_email(self, email: str) -> dict[str, Any]:
        """
        Get a user by email address.

        Args:
            email: The email address of the user to retrieve.

        Returns:
            Dict containing the user data.

        Raises:
            TestRailAPIError: If the API request fails.
        """
        return self._api_request("GET", f"get_user_by_email&email={email}")
