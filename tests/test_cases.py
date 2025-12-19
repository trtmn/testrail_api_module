"""
Tests for the CasesAPI module.

This module contains comprehensive tests for all methods in the CasesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.cases import CasesAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestCasesAPI:
    """Test suite for CasesAPI class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def cases_api(self, mock_client):
        """Create a CasesAPI instance with mocked client."""
        return CasesAPI(mock_client)

    @pytest.fixture
    def sample_case_data(self):
        """Sample test case data for testing."""
        return {
            "id": 1,
            "title": "Test Case Title",
            "section_id": 1,
            "template_id": 1,
            "type_id": 2,
            "priority_id": 2,
            "estimate": "30s",
            "milestone_id": 1,
            "refs": "REF-123",
            "description": "Test case description",
            "preconditions": "Preconditions text",
            "postconditions": "Postconditions text"
        }

    def test_init(self, mock_client):
        """Test CasesAPI initialization."""
        api = CasesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_case(self, cases_api: CasesAPI) -> None:
        """Test get_case method."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = {"id": 1, "title": "Test Case"}
            
            result = cases_api.get_case(case_id=1)
            
            mock_get.assert_called_once_with('get_case/1')
            assert result == {"id": 1, "title": "Test Case"}

    def test_get_cases_minimal(self, cases_api: CasesAPI) -> None:
        """Test get_cases with minimal required parameters."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]
            
            result = cases_api.get_cases(project_id=1)
            
            mock_get.assert_called_once_with(
                'get_cases/1',
                params={}
            )
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_cases_with_all_parameters(self, cases_api: CasesAPI) -> None:
        """Test get_cases with all optional parameters."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1, "title": "Case 1"}]
            
            result = cases_api.get_cases(
                project_id=1,
                suite_id=2,
                section_id=3,
                created_after=1000000,
                created_before=2000000,
                created_by=[1, 2],
                milestone_id=[1, 2],
                priority_id=[1, 2],
                type_id=[1, 2],
                updated_after=1000000,
                updated_before=2000000,
                updated_by=[1, 2],
                limit=10,
                offset=0
            )
            
            expected_params = {
                'suite_id': 2,
                'section_id': 3,
                'created_after': 1000000,
                'created_before': 2000000,
                'created_by': [1, 2],
                'milestone_id': [1, 2],
                'priority_id': [1, 2],
                'type_id': [1, 2],
                'updated_after': 1000000,
                'updated_before': 2000000,
                'updated_by': [1, 2],
                'limit': 10,
                'offset': 0
            }
            mock_get.assert_called_once_with(
                'get_cases/1',
                params=expected_params
            )

    def test_get_cases_with_single_ids(self, cases_api: CasesAPI) -> None:
        """Test get_cases with single integer IDs instead of lists."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = cases_api.get_cases(
                project_id=1,
                created_by=1,
                milestone_id=1,
                priority_id=1,
                type_id=1,
                updated_by=1
            )
            
            expected_params = {
                'created_by': 1,
                'milestone_id': 1,
                'priority_id': 1,
                'type_id': 1,
                'updated_by': 1
            }
            mock_get.assert_called_once_with(
                'get_cases/1',
                params=expected_params
            )

    def test_add_case_minimal(self, cases_api: CasesAPI) -> None:
        """Test add_case with minimal required parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case"
            )
            
            expected_data = {"title": "Test Case"}
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )
            assert result == {"id": 1, "title": "Test Case"}

    def test_add_case_with_all_parameters(self, cases_api: CasesAPI,
                                         sample_case_data: dict) -> None:
        """Test add_case with all optional parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = sample_case_data
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case Title",
                template_id=1,
                type_id=2,
                priority_id=2,
                estimate="30s",
                milestone_id=1,
                refs="REF-123",
                description="Test case description",
                preconditions="Preconditions text",
                postconditions="Postconditions text"
            )
            
            expected_data = {
                "title": "Test Case Title",
                "template_id": 1,
                "type_id": 2,
                "priority_id": 2,
                "estimate": "30s",
                "milestone_id": 1,
                "refs": "REF-123",
                "description": "Test case description",
                "preconditions": "Preconditions text",
                "postconditions": "Postconditions text"
            }
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )
            assert result == sample_case_data

    def test_add_case_with_none_values(self, cases_api: CasesAPI) -> None:
        """Test add_case with None values for optional parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                template_id=None,
                type_id=None,
                priority_id=None,
                estimate=None,
                milestone_id=None,
                refs=None,
                description=None,
                preconditions=None,
                postconditions=None,
                custom_fields=None
            )
            
            expected_data = {"title": "Test Case"}
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )
            assert result == {"id": 1, "title": "Test Case"}

    def test_add_case_with_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test add_case with custom fields."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            
            custom_fields = {"custom1": "value1", "custom2": "value2"}
            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                custom_fields=custom_fields
            )
            
            expected_data = {
                "title": "Test Case",
                "custom1": "value1",
                "custom2": "value2"
            }
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )

    def test_update_case_minimal(self, cases_api: CasesAPI) -> None:
        """Test update_case with minimal parameters (only case_id)."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Existing Title"}
            
            result = cases_api.update_case(case_id=1)
            
            expected_data = {}
            mock_post.assert_called_once_with(
                'update_case/1',
                data=expected_data
            )
            assert result == {"id": 1, "title": "Existing Title"}

    def test_update_case_with_all_parameters(self, cases_api: CasesAPI) -> None:
        """Test update_case with all optional parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Updated Title"}
            
            result = cases_api.update_case(
                case_id=1,
                title="Updated Title",
                template_id=1,
                type_id=2,
                priority_id=2,
                estimate="30s",
                milestone_id=1,
                refs="REF-123",
                description="Updated description",
                preconditions="Updated preconditions",
                postconditions="Updated postconditions"
            )
            
            expected_data = {
                "title": "Updated Title",
                "template_id": 1,
                "type_id": 2,
                "priority_id": 2,
                "estimate": "30s",
                "milestone_id": 1,
                "refs": "REF-123",
                "description": "Updated description",
                "preconditions": "Updated preconditions",
                "postconditions": "Updated postconditions"
            }
            mock_post.assert_called_once_with(
                'update_case/1',
                data=expected_data
            )
            assert result == {"id": 1, "title": "Updated Title"}

    def test_update_case_with_none_values(self, cases_api: CasesAPI) -> None:
        """Test update_case with None values for optional parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1}
            
            result = cases_api.update_case(
                case_id=1,
                title=None,
                template_id=None,
                type_id=None,
                priority_id=None,
                estimate=None,
                milestone_id=None,
                refs=None,
                description=None,
                preconditions=None,
                postconditions=None,
                custom_fields=None
            )
            
            expected_data = {}
            mock_post.assert_called_once_with(
                'update_case/1',
                data=expected_data
            )

    def test_update_case_with_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test update_case with custom fields."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1}
            
            custom_fields = {"custom1": "value1", "custom2": "value2"}
            result = cases_api.update_case(
                case_id=1,
                title="Updated Title",
                custom_fields=custom_fields
            )
            
            expected_data = {
                "title": "Updated Title",
                "custom1": "value1",
                "custom2": "value2"
            }
            mock_post.assert_called_once_with(
                'update_case/1',
                data=expected_data
            )

    def test_delete_case(self, cases_api: CasesAPI) -> None:
        """Test delete_case method."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {}
            
            result = cases_api.delete_case(case_id=1)
            
            mock_post.assert_called_once_with('delete_case/1')
            assert result == {}

    def test_get_case_fields(self, cases_api: CasesAPI) -> None:
        """Test get_case_fields method."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "field1", "type": "string"},
                {"id": 2, "name": "field2", "type": "integer"}
            ]
            
            result = cases_api.get_case_fields()
            
            mock_get.assert_called_once_with('get_case_fields')
            assert len(result) == 2
            assert result[0]["name"] == "field1"

    def test_get_case_types(self, cases_api: CasesAPI) -> None:
        """Test get_case_types method."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Other"},
                {"id": 2, "name": "Functional"}
            ]
            
            result = cases_api.get_case_types()
            
            mock_get.assert_called_once_with('get_case_types')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_case_history(self, cases_api: CasesAPI) -> None:
        """Test get_case_history method."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "user": "user1", "created_on": 1000000},
                {"id": 2, "user": "user2", "created_on": 2000000}
            ]
            
            result = cases_api.get_case_history(case_id=1)
            
            mock_get.assert_called_once_with('get_case_history/1')
            assert len(result) == 2
            assert result[0]["user"] == "user1"

    def test_copy_cases_to_section(self, cases_api: CasesAPI) -> None:
        """Test copy_cases_to_section method."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]
            
            result = cases_api.copy_cases_to_section(
                case_ids=[1, 2, 3],
                section_id=5
            )
            
            expected_data = {"case_ids": [1, 2, 3]}
            mock_post.assert_called_once_with(
                'copy_cases_to_section/5',
                data=expected_data
            )
            assert len(result) == 2

    def test_move_cases_to_section(self, cases_api: CasesAPI) -> None:
        """Test move_cases_to_section method."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]
            
            result = cases_api.move_cases_to_section(
                case_ids=[1, 2, 3],
                section_id=5
            )
            
            expected_data = {"case_ids": [1, 2, 3]}
            mock_post.assert_called_once_with(
                'move_cases_to_section/5',
                data=expected_data
            )
            assert len(result) == 2

    def test_api_request_failure(self, cases_api: CasesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                cases_api.get_case(case_id=1)

    def test_authentication_error(self, cases_api: CasesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                cases_api.get_case(case_id=1)

    def test_rate_limit_error(self, cases_api: CasesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                cases_api.get_case(case_id=1)

    def test_custom_fields_override(self, cases_api: CasesAPI) -> None:
        """Test that custom_fields properly override explicit parameters."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Custom Title"}
            
            custom_fields = {
                "title": "Custom Title",  # This should override the explicit title
                "custom_field": "custom_value"
            }
            
            result = cases_api.add_case(
                section_id=1,
                title="Original Title",
                custom_fields=custom_fields
            )
            
            expected_data = {
                "title": "Custom Title",  # Should be from custom_fields, overriding explicit title
                "custom_field": "custom_value"
            }
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )

    @pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
    def test_different_type_ids(self, cases_api: CasesAPI, type_id: int) -> None:
        """Test add_case with different type IDs."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "type_id": type_id}
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                type_id=type_id
            )
            
            expected_data = {"title": "Test Case", "type_id": type_id}
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )
            assert result["type_id"] == type_id

    @pytest.mark.parametrize("priority_id", [1, 2, 3, 4])
    def test_different_priority_ids(self, cases_api: CasesAPI, priority_id: int) -> None:
        """Test add_case with different priority IDs."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "priority_id": priority_id}
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                priority_id=priority_id
            )
            
            expected_data = {"title": "Test Case", "priority_id": priority_id}
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )
            assert result["priority_id"] == priority_id

    def test_large_case_and_section_ids(self, cases_api: CasesAPI) -> None:
        """Test with large case and section IDs."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            
            result = cases_api.add_case(
                section_id=999999,
                title="Test Case"
            )
            
            mock_post.assert_called_once_with(
                'add_case/999999',
                data={"title": "Test Case"}
            )

    def test_empty_case_ids_list(self, cases_api: CasesAPI) -> None:
        """Test copy_cases_to_section with empty case_ids list."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = []
            
            result = cases_api.copy_cases_to_section(
                case_ids=[],
                section_id=1
            )
            
            expected_data = {"case_ids": []}
            mock_post.assert_called_once_with(
                'copy_cases_to_section/1',
                data=expected_data
            )
            assert result == []

    def test_complex_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test with complex custom fields data."""
        with patch.object(cases_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            
            complex_custom_fields = {
                "string_field": "test_value",
                "number_field": 42,
                "boolean_field": True,
                "null_field": None,
                "list_field": [1, 2, 3],
                "nested_dict": {"key": "value"}
            }
            
            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                custom_fields=complex_custom_fields
            )
            
            expected_data = {
                "title": "Test Case",
                **complex_custom_fields
            }
            mock_post.assert_called_once_with(
                'add_case/1',
                data=expected_data
            )

    def test_get_cases_pagination(self, cases_api: CasesAPI) -> None:
        """Test get_cases with pagination parameters."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = cases_api.get_cases(
                project_id=1,
                limit=50,
                offset=100
            )
            
            expected_params = {
                'limit': 50,
                'offset': 100
            }
            mock_get.assert_called_once_with(
                'get_cases/1',
                params=expected_params
            )

    def test_get_cases_timestamp_filters(self, cases_api: CasesAPI) -> None:
        """Test get_cases with timestamp filters."""
        with patch.object(cases_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1}]
            
            result = cases_api.get_cases(
                project_id=1,
                created_after=1000000,
                created_before=2000000,
                updated_after=1500000,
                updated_before=2500000
            )
            
            expected_params = {
                'created_after': 1000000,
                'created_before': 2000000,
                'updated_after': 1500000,
                'updated_before': 2500000
            }
            mock_get.assert_called_once_with(
                'get_cases/1',
                params=expected_params
            )








