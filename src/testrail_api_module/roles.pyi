from .base import BaseAPI as BaseAPI
from typing import Any

class RolesAPI(BaseAPI):
    """
    API for managing TestRail roles.
    """
    def get_role(self, role_id: int) -> dict[str, Any] | None:
        """
        Get a role by ID.
        
        Args:
            role_id (int): The ID of the role to retrieve.
            
        Returns:
            dict: The role data if successful, None otherwise.
        """
    def get_roles(self) -> list[dict[str, Any]] | None:
        """
        Get all roles.
        
        Returns:
            list: List of roles if successful, None otherwise.
        """
    def add_role(self, name: str, description: str | None = None, permissions: dict[str, bool] | None = None) -> dict[str, Any] | None:
        """
        Add a new role.
        
        Args:
            name (str): The name of the role.
            description (str, optional): The description of the role.
            permissions (dict, optional): Dictionary of permission flags:
                - view_test_cases (bool): Can view test cases
                - edit_test_cases (bool): Can edit test cases
                - delete_test_cases (bool): Can delete test cases
                - view_test_suites (bool): Can view test suites
                - edit_test_suites (bool): Can edit test suites
                - delete_test_suites (bool): Can delete test suites
                - view_test_runs (bool): Can view test runs
                - edit_test_runs (bool): Can edit test runs
                - delete_test_runs (bool): Can delete test runs
                - view_test_plans (bool): Can view test plans
                - edit_test_plans (bool): Can edit test plans
                - delete_test_plans (bool): Can delete test plans
                - view_milestones (bool): Can view milestones
                - edit_milestones (bool): Can edit milestones
                - delete_milestones (bool): Can delete milestones
                - view_reports (bool): Can view reports
                - view_dashboard (bool): Can view dashboard
                - view_users (bool): Can view users
                - edit_users (bool): Can edit users
                - delete_users (bool): Can delete users
                - view_roles (bool): Can view roles
                - edit_roles (bool): Can edit roles
                - delete_roles (bool): Can delete roles
                - view_projects (bool): Can view projects
                - edit_projects (bool): Can edit projects
                - delete_projects (bool): Can delete projects
                
        Returns:
            dict: The created role data if successful, None otherwise.
        """
    def update_role(self, role_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a role.
        
        Args:
            role_id (int): The ID of the role to update.
            **kwargs: The fields to update (name, description, permissions).
            
        Returns:
            dict: The updated role data if successful, None otherwise.
        """
    def delete_role(self, role_id: int) -> dict[str, Any] | None:
        """
        Delete a role.
        
        Args:
            role_id (int): The ID of the role to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
