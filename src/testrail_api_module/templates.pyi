from .base import BaseAPI as BaseAPI
from typing import Any

class TemplatesAPI(BaseAPI):
    """
    API for managing TestRail templates.
    """
    def get_template(self, template_id: int) -> dict[str, Any] | None:
        """
        Get a template by ID.
        
        Args:
            template_id (int): The ID of the template to retrieve.
            
        Returns:
            dict: The template data if successful, None otherwise.
        """
    def get_templates(self, project_id: int) -> list[dict[str, Any]] | None:
        """
        Get all templates for a project.
        
        Args:
            project_id (int): The ID of the project to get templates for.
            
        Returns:
            list: List of templates if successful, None otherwise.
        """
    def add_template(self, project_id: int, name: str, description: str | None = None, fields: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
        """
        Add a new template.
        
        Args:
            project_id (int): The ID of the project to add the template to.
            name (str): The name of the template.
            description (str, optional): The description of the template.
            fields (list, optional): List of template fields, each containing:
                - name (str): The name of the field
                - type (str): The type of the field
                - required (bool): Whether the field is required
                - default_value (str, optional): The default value for the field
                - options (list, optional): List of options for select/multi-select fields
                
        Returns:
            dict: The created template data if successful, None otherwise.
        """
    def update_template(self, template_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a template.
        
        Args:
            template_id (int): The ID of the template to update.
            **kwargs: The fields to update (name, description, fields).
            
        Returns:
            dict: The updated template data if successful, None otherwise.
        """
    def delete_template(self, template_id: int) -> dict[str, Any] | None:
        """
        Delete a template.
        
        Args:
            template_id (int): The ID of the template to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def get_template_fields(self, template_id: int) -> list[dict[str, Any]] | None:
        """
        Get all fields in a template.
        
        Args:
            template_id (int): The ID of the template to get fields for.
            
        Returns:
            list: List of template fields if successful, None otherwise.
        """
    def add_template_field(self, template_id: int, name: str, field_type: str, required: bool = False, default_value: str | None = None, options: list[str] | None = None) -> dict[str, Any] | None:
        """
        Add a field to a template.
        
        Args:
            template_id (int): The ID of the template to add the field to.
            name (str): The name of the field.
            field_type (str): The type of the field:
                - text: Single-line text
                - textarea: Multi-line text
                - select: Single-select dropdown
                - multiselect: Multi-select dropdown
                - number: Numeric value
                - date: Date value
                - checkbox: Boolean value
            required (bool, optional): Whether the field is required.
            default_value (str, optional): The default value for the field.
            options (list, optional): List of options for select/multi-select fields.
                
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def update_template_field(self, template_id: int, field_id: int, **kwargs) -> dict[str, Any] | None:
        """
        Update a field in a template.
        
        Args:
            template_id (int): The ID of the template containing the field.
            field_id (int): The ID of the field to update.
            **kwargs: The fields to update (name, type, required, default_value, options).
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
    def delete_template_field(self, template_id: int, field_id: int) -> dict[str, Any] | None:
        """
        Delete a field from a template.
        
        Args:
            template_id (int): The ID of the template containing the field.
            field_id (int): The ID of the field to delete.
            
        Returns:
            dict: The response data if successful, None otherwise.
        """
