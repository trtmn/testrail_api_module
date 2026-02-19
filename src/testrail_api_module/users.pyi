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
    def add_user(
        self,
        name: str,
        email: str,
        password: str,
        role_id: int | None = None,
        is_active: bool = True,
    ) -> dict[str, Any] | None:
        """
        Add a new user.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The password for the user.
            role_id (int, optional): The ID of the role to assign to the user.
            is_active (bool, optional): Whether the user is active.

        Returns:
            dict: The created user data if successful, None otherwise.
        """
    def update_user(
        self, user_id: int, **kwargs: Any
    ) -> dict[str, Any] | None:
        """
        Update a user.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The fields to update (name, email, password, role_id, is_active).

        Returns:
            dict: The updated user data if successful, None otherwise.
        """
    def delete_user(self, user_id: int) -> dict[str, Any] | None:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_user_activity(self, user_id: int) -> list[dict[str, Any]] | None:
        """
        Get the activity log for a user.

        Args:
            user_id (int): The ID of the user to get activity for.

        Returns:
            list: List of activity entries if successful, None otherwise.
        """
    def get_user_projects(self, user_id: int) -> list[dict[str, Any]] | None:
        """
        Get all projects a user has access to.

        Args:
            user_id (int): The ID of the user to get projects for.

        Returns:
            list: List of projects if successful, None otherwise.
        """
    def get_user_roles(self, user_id: int) -> list[dict[str, Any]] | None:
        """
        Get all roles assigned to a user.

        Args:
            user_id (int): The ID of the user to get roles for.

        Returns:
            list: List of roles if successful, None otherwise.
        """
