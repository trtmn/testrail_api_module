"""
Tests for the TemplatesAPI module.

This module contains comprehensive tests for all methods in the TemplatesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.templates import TemplatesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestTemplatesAPI:
    """Test suite for TemplatesAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def templates_api(self, mock_client: Mock) -> TemplatesAPI:
        """Create a TemplatesAPI instance with mocked client."""
        return TemplatesAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test TemplatesAPI initialization."""
        api = TemplatesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_template(self, templates_api: TemplatesAPI) -> None:
        """Test get_template method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Template 1"}
            
            result = templates_api.get_template(template_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_template/1')
            assert result == {"id": 1, "name": "Template 1"}

    def test_get_templates(self, templates_api: TemplatesAPI) -> None:
        """Test get_templates method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Template 1"},
                {"id": 2, "name": "Template 2"}
            ]
            
            result = templates_api.get_templates(project_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_templates/1')
            assert len(result) == 2

    def test_add_template_minimal(self, templates_api: TemplatesAPI) -> None:
        """Test add_template with minimal required parameters."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Template"}
            
            result = templates_api.add_template(project_id=1, name="New Template")
            
            expected_data = {"name": "New Template"}
            mock_request.assert_called_once_with('POST', 'add_template/1', data=expected_data)
            assert result == {"id": 1, "name": "New Template"}

    def test_add_template_with_all_parameters(self, templates_api: TemplatesAPI) -> None:
        """Test add_template with all optional parameters."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Template"}
            
            fields = [
                {"name": "field1", "type": "text", "required": True}
            ]
            
            result = templates_api.add_template(
                project_id=1,
                name="New Template",
                description="Template description",
                fields=fields
            )
            
            expected_data = {
                "name": "New Template",
                "description": "Template description",
                "fields": fields
            }
            mock_request.assert_called_once_with('POST', 'add_template/1', data=expected_data)

    def test_update_template(self, templates_api: TemplatesAPI) -> None:
        """Test update_template method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated Template"}
            
            result = templates_api.update_template(
                template_id=1,
                name="Updated Template",
                description="Updated description"
            )
            
            expected_data = {
                "name": "Updated Template",
                "description": "Updated description"
            }
            mock_request.assert_called_once_with('POST', 'update_template/1', data=expected_data)

    def test_delete_template(self, templates_api: TemplatesAPI) -> None:
        """Test delete_template method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = templates_api.delete_template(template_id=1)
            
            mock_request.assert_called_once_with('POST', 'delete_template/1')
            assert result == {}

    def test_get_template_fields(self, templates_api: TemplatesAPI) -> None:
        """Test get_template_fields method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "field1"},
                {"id": 2, "name": "field2"}
            ]
            
            result = templates_api.get_template_fields(template_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_template_fields/1')
            assert len(result) == 2

    def test_add_template_field_minimal(self, templates_api: TemplatesAPI) -> None:
        """Test add_template_field with minimal required parameters."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Field"}
            
            result = templates_api.add_template_field(
                template_id=1,
                name="New Field",
                field_type="text"
            )
            
            expected_data = {
                "name": "New Field",
                "type": "text",
                "required": False
            }
            mock_request.assert_called_once_with('POST', 'add_template_field/1', data=expected_data)

    def test_add_template_field_with_all_parameters(self, templates_api: TemplatesAPI) -> None:
        """Test add_template_field with all optional parameters."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Field"}
            
            result = templates_api.add_template_field(
                template_id=1,
                name="New Field",
                field_type="select",
                required=True,
                default_value="default",
                options=["option1", "option2"]
            )
            
            expected_data = {
                "name": "New Field",
                "type": "select",
                "required": True,
                "default_value": "default",
                "options": ["option1", "option2"]
            }
            mock_request.assert_called_once_with('POST', 'add_template_field/1', data=expected_data)

    def test_update_template_field(self, templates_api: TemplatesAPI) -> None:
        """Test update_template_field method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1}
            
            result = templates_api.update_template_field(
                template_id=1,
                field_id=2,
                name="Updated Field"
            )
            
            expected_data = {"name": "Updated Field"}
            mock_request.assert_called_once_with('POST', 'update_template_field/1/2', data=expected_data)

    def test_delete_template_field(self, templates_api: TemplatesAPI) -> None:
        """Test delete_template_field method."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.return_value = {}
            
            result = templates_api.delete_template_field(template_id=1, field_id=2)
            
            mock_request.assert_called_once_with('POST', 'delete_template_field/1/2')
            assert result == {}

    def test_api_request_failure(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                templates_api.get_template(template_id=1)

    def test_authentication_error(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                templates_api.get_template(template_id=1)

    def test_rate_limit_error(self, templates_api: TemplatesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(templates_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                templates_api.get_template(template_id=1)






