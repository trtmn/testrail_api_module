from typing import Any

from .base import BaseAPI as BaseAPI

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
    def get_users(self) -> list[dict[str, Any]] | None:
        """
        Get all users.

        Returns:
            list: List of users if successful, None otherwise.
        """
    def get_current_user(self) -> dict[str, Any] | None:
        """Get the currently authenticated user. Requires TestRail 6.6+."""
    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        """
        Get a user by email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            dict: The user data if successful, None otherwise.
        """
