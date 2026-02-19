"""
Tests for the CasesAPI module.

This module contains comprehensive tests for all methods in the CasesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.cases import CasesAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestCasesAPI:
    """Test suite for CasesAPI class."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        # Minimal module mocks used by CasesAPI validation.
        client.sections = Mock()
        client.sections.get_section.return_value = {
            "id": 1,
            "project_id": 1,
            "suite_id": None,
        }
        client.templates = Mock()
        client.templates.get_templates.return_value = [
            {"id": 1, "is_default": True}
        ]
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
            "postconditions": "Postconditions text",
        }

    def test_init(self, mock_client):
        """Test CasesAPI initialization."""
        api = CasesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_case(self, cases_api: CasesAPI) -> None:
        """Test get_case method."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = {"id": 1, "title": "Test Case"}

            result = cases_api.get_case(case_id=1)

            mock_get.assert_called_once_with("get_case/1")
            assert result == {"id": 1, "title": "Test Case"}

    def test_get_cases_minimal(self, cases_api: CasesAPI) -> None:
        """Test get_cases with minimal required parameters."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"},
            ]

            result = cases_api.get_cases(project_id=1)

            mock_get.assert_called_once_with("get_cases/1", params={})
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_cases_with_all_parameters(self, cases_api: CasesAPI) -> None:
        """Test get_cases with all optional parameters."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "title": "Case 1"}]

            cases_api.get_cases(
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
                offset=0,
            )

            expected_params = {
                "suite_id": 2,
                "section_id": 3,
                "created_after": 1000000,
                "created_before": 2000000,
                "created_by": [1, 2],
                "milestone_id": [1, 2],
                "priority_id": [1, 2],
                "type_id": [1, 2],
                "updated_after": 1000000,
                "updated_before": 2000000,
                "updated_by": [1, 2],
                "limit": 10,
                "offset": 0,
            }
            mock_get.assert_called_once_with(
                "get_cases/1", params=expected_params
            )

    def test_get_cases_with_single_ids(self, cases_api: CasesAPI) -> None:
        """Test get_cases with single integer IDs instead of lists."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            cases_api.get_cases(
                project_id=1,
                created_by=1,
                milestone_id=1,
                priority_id=1,
                type_id=1,
                updated_by=1,
            )

            expected_params = {
                "created_by": 1,
                "milestone_id": 1,
                "priority_id": 1,
                "type_id": 1,
                "updated_by": 1,
            }
            mock_get.assert_called_once_with(
                "get_cases/1", params=expected_params
            )

    def test_add_case_minimal(self, cases_api: CasesAPI) -> None:
        """Test add_case with minimal required parameters."""
        with (
            patch.object(cases_api, "_post") as mock_post,
            patch.object(cases_api, "get_case_fields") as mock_get_fields,
        ):
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            # Mock get_case_fields to return minimal field info (title is
            # always required)
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

            result = cases_api.add_case(section_id=1, title="Test Case")

            expected_data = {"title": "Test Case"}
            mock_post.assert_called_once_with("add_case/1", data=expected_data)
            assert result == {"id": 1, "title": "Test Case"}

    def test_add_case_with_all_parameters(
        self, cases_api: CasesAPI, sample_case_data: dict
    ) -> None:
        """Test add_case with all optional parameters."""
        with (
            patch.object(cases_api, "_post") as mock_post,
            patch.object(cases_api, "get_case_fields") as mock_get_fields,
        ):
            mock_post.return_value = sample_case_data
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

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
                postconditions="Postconditions text",
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
                "postconditions": "Postconditions text",
            }
            mock_post.assert_called_once_with("add_case/1", data=expected_data)
            assert result == sample_case_data

    def test_add_case_with_none_values(self, cases_api: CasesAPI) -> None:
        """Test add_case with None values for optional parameters."""
        with (
            patch.object(cases_api, "_post") as mock_post,
            patch.object(cases_api, "get_case_fields") as mock_get_fields,
        ):
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

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
                custom_fields=None,
            )

            expected_data = {"title": "Test Case"}
            mock_post.assert_called_once_with("add_case/1", data=expected_data)
            assert result == {"id": 1, "title": "Test Case"}

    def test_add_case_with_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test add_case with custom fields."""
        with (
            patch.object(cases_api, "_post") as mock_post,
            patch.object(cases_api, "get_case_fields") as mock_get_fields,
        ):
            mock_post.return_value = {"id": 1, "title": "Test Case"}
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1},
                {
                    "system_name": "custom_field1",
                    "is_required": False,
                    "type_id": 1,
                },
                {
                    "system_name": "custom_field2",
                    "is_required": False,
                    "type_id": 2,
                },
            ]

            custom_fields = {"custom1": "value1", "custom2": "value2"}
            cases_api.add_case(
                section_id=1, title="Test Case", custom_fields=custom_fields
            )

            expected_data = {
                "title": "Test Case",
                "custom1": "value1",
                "custom2": "value2",
            }
            mock_post.assert_called_once_with("add_case/1", data=expected_data)

    def test_update_case_minimal(self, cases_api: CasesAPI) -> None:
        """Test update_case with minimal parameters (only case_id)."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Existing Title"}

            result = cases_api.update_case(case_id=1)

            expected_data = {}
            mock_post.assert_called_once_with(
                "update_case/1", data=expected_data
            )
            assert result == {"id": 1, "title": "Existing Title"}

    def test_update_case_with_all_parameters(
        self, cases_api: CasesAPI
    ) -> None:
        """Test update_case with all optional parameters."""
        with patch.object(cases_api, "_post") as mock_post:
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
                postconditions="Updated postconditions",
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
                "postconditions": "Updated postconditions",
            }
            mock_post.assert_called_once_with(
                "update_case/1", data=expected_data
            )
            assert result == {"id": 1, "title": "Updated Title"}

    def test_update_case_with_none_values(self, cases_api: CasesAPI) -> None:
        """Test update_case with None values for optional parameters."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1}

            cases_api.update_case(
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
                custom_fields=None,
            )

            expected_data = {}
            mock_post.assert_called_once_with(
                "update_case/1", data=expected_data
            )

    def test_update_case_with_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test update_case with custom fields."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1}

            custom_fields = {"custom1": "value1", "custom2": "value2"}
            cases_api.update_case(
                case_id=1, title="Updated Title", custom_fields=custom_fields
            )

            expected_data = {
                "title": "Updated Title",
                "custom1": "value1",
                "custom2": "value2",
            }
            mock_post.assert_called_once_with(
                "update_case/1", data=expected_data
            )

    def test_delete_case(self, cases_api: CasesAPI) -> None:
        """Test delete_case method."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = cases_api.delete_case(case_id=1)

            mock_post.assert_called_once_with("delete_case/1")
            assert result == {}

    def test_get_case_fields(self, cases_api: CasesAPI) -> None:
        """Test get_case_fields method."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "field1", "type": "string"},
                {"id": 2, "name": "field2", "type": "integer"},
            ]

            result = cases_api.get_case_fields()

            mock_get.assert_called_once_with("get_case_fields")
            assert len(result) == 2
            assert result[0]["name"] == "field1"

    def test_get_case_types(self, cases_api: CasesAPI) -> None:
        """Test get_case_types method."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Other"},
                {"id": 2, "name": "Functional"},
            ]

            result = cases_api.get_case_types()

            mock_get.assert_called_once_with("get_case_types")
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_history_for_case(self, cases_api: CasesAPI) -> None:
        """Test get_history_for_case method."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [
                {"id": 1, "user": "user1", "created_on": 1000000},
                {"id": 2, "user": "user2", "created_on": 2000000},
            ]

            result = cases_api.get_history_for_case(case_id=1)

            mock_get.assert_called_once_with("get_history_for_case/1")
            assert len(result) == 2
            assert result[0]["user"] == "user1"

    def test_copy_cases_to_section(self, cases_api: CasesAPI) -> None:
        """Test copy_cases_to_section method."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"},
            ]

            result = cases_api.copy_cases_to_section(
                case_ids=[1, 2, 3], section_id=5
            )

            expected_data = {"case_ids": [1, 2, 3]}
            mock_post.assert_called_once_with(
                "copy_cases_to_section/5", data=expected_data
            )
            assert len(result) == 2

    def test_move_cases_to_section(self, cases_api: CasesAPI) -> None:
        """Test move_cases_to_section method."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"},
            ]

            result = cases_api.move_cases_to_section(
                case_ids=[1, 2, 3], section_id=5
            )

            expected_data = {"case_ids": [1, 2, 3]}
            mock_post.assert_called_once_with(
                "move_cases_to_section/5", data=expected_data
            )
            assert len(result) == 2

    def test_api_request_failure(self, cases_api: CasesAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                cases_api.get_case(case_id=1)

    def test_authentication_error(self, cases_api: CasesAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                cases_api.get_case(case_id=1)

    def test_rate_limit_error(self, cases_api: CasesAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                cases_api.get_case(case_id=1)

    def test_custom_fields_override(self, cases_api: CasesAPI) -> None:
        """Test that custom_fields properly override explicit parameters."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Custom Title"}

            custom_fields = {
                "title": "Custom Title",  # This should override the explicit title
                "custom_field": "custom_value",
            }

            cases_api.add_case(
                section_id=1,
                title="Original Title",
                custom_fields=custom_fields,
                validate_required=False,
            )

            expected_data = {
                "title": "Custom Title",  # Should be from custom_fields, overriding explicit title
                "custom_field": "custom_value",
            }
            mock_post.assert_called_once_with("add_case/1", data=expected_data)

    @pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
    def test_different_type_ids(
        self, cases_api: CasesAPI, type_id: int
    ) -> None:
        """Test add_case with different type IDs."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "type_id": type_id}

            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                type_id=type_id,
                validate_required=False,
            )

            expected_data = {"title": "Test Case", "type_id": type_id}
            mock_post.assert_called_once_with("add_case/1", data=expected_data)
            assert result["type_id"] == type_id

    @pytest.mark.parametrize("priority_id", [1, 2, 3, 4])
    def test_different_priority_ids(
        self, cases_api: CasesAPI, priority_id: int
    ) -> None:
        """Test add_case with different priority IDs."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "priority_id": priority_id}

            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                priority_id=priority_id,
                validate_required=False,
            )

            expected_data = {"title": "Test Case", "priority_id": priority_id}
            mock_post.assert_called_once_with("add_case/1", data=expected_data)
            assert result["priority_id"] == priority_id

    def test_large_case_and_section_ids(self, cases_api: CasesAPI) -> None:
        """Test with large case and section IDs."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}

            cases_api.add_case(
                section_id=999999, title="Test Case", validate_required=False
            )

            mock_post.assert_called_once_with(
                "add_case/999999", data={"title": "Test Case"}
            )

    def test_empty_case_ids_list(self, cases_api: CasesAPI) -> None:
        """Test copy_cases_to_section with empty case_ids list."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = []

            result = cases_api.copy_cases_to_section(case_ids=[], section_id=1)

            expected_data = {"case_ids": []}
            mock_post.assert_called_once_with(
                "copy_cases_to_section/1", data=expected_data
            )
            assert result == []

    def test_complex_custom_fields(self, cases_api: CasesAPI) -> None:
        """Test with complex custom fields data."""
        with patch.object(cases_api, "_post") as mock_post:
            mock_post.return_value = {"id": 1, "title": "Test Case"}

            complex_custom_fields = {
                "string_field": "test_value",
                "number_field": 42,
                "boolean_field": True,
                "null_field": None,
                "list_field": [1, 2, 3],
                "nested_dict": {"key": "value"},
            }

            cases_api.add_case(
                section_id=1,
                title="Test Case",
                custom_fields=complex_custom_fields,
                validate_required=False,
            )

            expected_data = {"title": "Test Case", **complex_custom_fields}
            mock_post.assert_called_once_with("add_case/1", data=expected_data)

    def test_get_cases_pagination(self, cases_api: CasesAPI) -> None:
        """Test get_cases with pagination parameters."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            cases_api.get_cases(project_id=1, limit=50, offset=100)

            expected_params = {"limit": 50, "offset": 100}
            mock_get.assert_called_once_with(
                "get_cases/1", params=expected_params
            )

    def test_get_cases_timestamp_filters(self, cases_api: CasesAPI) -> None:
        """Test get_cases with timestamp filters."""
        with patch.object(cases_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1}]

            cases_api.get_cases(
                project_id=1,
                created_after=1000000,
                created_before=2000000,
                updated_after=1500000,
                updated_before=2500000,
            )

            expected_params = {
                "created_after": 1000000,
                "created_before": 2000000,
                "updated_after": 1500000,
                "updated_before": 2500000,
            }
            mock_get.assert_called_once_with(
                "get_cases/1", params=expected_params
            )

    def test_add_case_validate_only_success(self, cases_api: CasesAPI) -> None:
        """Test add_case with validate_only=True when all fields are valid."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            # Mock get_case_fields to return required fields
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1},
                {
                    "system_name": "custom_field1",
                    "is_required": True,
                    "type_id": 1,
                },
            ]

            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                custom_fields={"custom_field1": "value1"},
                validate_only=True,
            )

            # Should return validation result, not make API call
            assert result["valid"] is True
            assert "All" in result["message"]
            assert len(result["missing_fields"]) == 0
            assert len(result["provided_fields"]) == 1  # custom_field1

    def test_add_case_validate_only_missing_fields(
        self, cases_api: CasesAPI
    ) -> None:
        """Test add_case with validate_only=True when required fields are missing."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            # Mock get_case_fields to return required fields
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1},
                {
                    "system_name": "custom_field1",
                    "is_required": True,
                    "type_id": 1,
                },
                {
                    "system_name": "custom_steps_separated",
                    "is_required": True,
                    "type_id": 12,
                },
            ]

            result = cases_api.add_case(
                section_id=1, title="Test Case", validate_only=True
            )

            # Should return validation result showing missing fields
            assert result["valid"] is False
            assert "Missing" in result["message"]
            # custom_field1 and custom_steps_separated
            assert len(result["missing_fields"]) == 2
            assert len(result["provided_fields"]) == 0
            assert "'custom_field1'" in result["missing_fields"][0]
            assert "'custom_steps_separated'" in result["missing_fields"][1]

    def test_case_fields_caching(self, cases_api: CasesAPI) -> None:
        """Test that case fields are cached after first fetch."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

            # First call should fetch from API
            fields1 = cases_api._get_required_case_fields()
            assert mock_get_fields.call_count == 1

            # Second call should use cache
            fields2 = cases_api._get_required_case_fields()
            assert mock_get_fields.call_count == 1  # Still 1, not 2

            # Should return same data
            assert fields1 == fields2

    def test_clear_case_fields_cache(self, cases_api: CasesAPI) -> None:
        """Test clearing the case fields cache."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

            # First call caches data
            cases_api._get_required_case_fields()
            assert mock_get_fields.call_count == 1

            # Clear cache
            cases_api.clear_case_fields_cache()

            # Next call should fetch again
            cases_api._get_required_case_fields()
            assert (
                mock_get_fields.call_count == 2
            )  # Called again after cache clear

    def test_case_fields_cache_bypass(self, cases_api: CasesAPI) -> None:
        """Test bypassing the cache with use_cache=False."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {"system_name": "title", "is_required": True, "type_id": 1}
            ]

            # First call caches data
            cases_api._get_required_case_fields()
            assert mock_get_fields.call_count == 1

            # Call with use_cache=False should fetch fresh data
            cases_api._get_required_case_fields(use_cache=False)
            assert mock_get_fields.call_count == 2  # Called again

    def test_required_fields_from_configs_array(
        self, cases_api: CasesAPI
    ) -> None:
        """Test that required fields are detected from configs array (project-specific)."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            # Simulate TestRail API response with configs array
            mock_get_fields.return_value = [
                {
                    "system_name": "title",
                    "is_required": True,  # Top-level flag
                    "type_id": 1,
                },
                {
                    "system_name": "custom_automation_type",
                    "is_required": False,  # Top-level is False
                    "type_id": 1,
                    "configs": [  # But required in config!
                        {
                            "context": {
                                "is_global": False,
                                "project_ids": [123],
                            },
                            "options": {
                                "is_required": True  # Required for project 123
                            },
                        }
                    ],
                },
                {
                    "system_name": "custom_steps_separated",
                    "is_required": False,
                    "type_id": 12,
                    "configs": [
                        {
                            "context": {"is_global": True},
                            "options": {
                                "is_required": True  # Required globally
                            },
                        }
                    ],
                },
                {
                    "system_name": "custom_optional_field",
                    "is_required": False,
                    "type_id": 1,
                    "configs": [
                        {
                            "context": {
                                "is_global": False,
                                "project_ids": [456],
                            },
                            "options": {
                                "is_required": False  # Not required
                            },
                        }
                    ],
                },
            ]

            # Get required fields
            required = cases_api._get_required_case_fields()

            # Should find 3 required fields:
            # 1. title (top-level is_required=True)
            # 2. custom_automation_type (required in config for project 123)
            # 3. custom_steps_separated (required in global config)
            # Should NOT include custom_optional_field (not required)
            assert len(required) == 3

            field_names = [f.get("system_name") for f in required]
            assert "title" in field_names
            assert "custom_automation_type" in field_names
            assert "custom_steps_separated" in field_names
            assert "custom_optional_field" not in field_names


class TestGetRequiredCaseFields:
    """Test suite for get_required_case_fields() method."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        client.sections = Mock()
        client.sections.get_section.return_value = {
            "id": 1,
            "project_id": 1,
            "suite_id": None,
        }
        client.templates = Mock()
        client.templates.get_templates.return_value = [
            {"id": 1, "is_default": True}
        ]
        return client

    @pytest.fixture
    def cases_api(self, mock_client):
        """Create a CasesAPI instance with mocked client."""
        return CasesAPI(mock_client)

    def test_get_required_case_fields_all_projects(
        self, cases_api: CasesAPI
    ) -> None:
        """Test get_required_case_fields without project filter returns all required fields."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "custom_automation_type",
                    "label": "Automation Type",
                    "type_id": 1,
                    "is_required": False,
                    "description": "Type of automation",
                    "configs": [
                        {
                            "context": {
                                "is_global": True,
                                "project_ids": None,
                            },
                            "options": {"is_required": True},
                        }
                    ],
                },
                {
                    "system_name": "custom_steps_separated",
                    "label": "Steps",
                    "type_id": 12,
                    "is_required": False,
                    "description": "Test steps",
                    "configs": [
                        {
                            "context": {
                                "is_global": False,
                                "project_ids": [1, 2, 3],
                            },
                            "options": {"is_required": True},
                        }
                    ],
                },
                {
                    "system_name": "custom_optional",
                    "label": "Optional Field",
                    "type_id": 1,
                    "is_required": False,
                    "configs": [
                        {
                            "context": {
                                "is_global": True,
                                "project_ids": None,
                            },
                            "options": {"is_required": False},
                        }
                    ],
                },
            ]

            result = cases_api.get_required_case_fields()

            # Verify response structure
            assert "required_fields" in result
            assert "field_count" in result
            assert "project_filtered" in result
            assert "cache_used" in result

            # Should have 2 required fields
            assert result["field_count"] == 2
            assert result["project_filtered"] is False

            # Verify fields are properly formatted
            fields = result["required_fields"]
            assert len(fields) == 2

            # Check first field (global)
            field1 = next(
                f
                for f in fields
                if f["system_name"] == "custom_automation_type"
            )
            assert field1["label"] == "Automation Type"
            assert field1["type_id"] == 1
            assert field1["type_name"] == "String"
            assert field1["type_hint"] == "string"
            assert field1["is_global"] is True
            assert field1["project_ids"] is None
            assert field1["description"] == "Type of automation"

            # Check second field (project-specific)
            field2 = next(
                f
                for f in fields
                if f["system_name"] == "custom_steps_separated"
            )
            assert field2["label"] == "Steps"
            assert field2["type_id"] == 12
            assert field2["type_name"] == "Stepped"
            assert "array of step objects" in field2["type_hint"]
            assert field2["is_global"] is False
            assert field2["project_ids"] == [1, 2, 3]

    def test_get_required_case_fields_with_project_filter(
        self, cases_api: CasesAPI
    ) -> None:
        """Test get_required_case_fields with project_id filters correctly."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "custom_global",
                    "label": "Global Field",
                    "type_id": 1,
                    "is_required": False,
                    "configs": [
                        {
                            "context": {
                                "is_global": True,
                                "project_ids": None,
                            },
                            "options": {"is_required": True},
                        }
                    ],
                },
                {
                    "system_name": "custom_project_1",
                    "label": "Project 1 Field",
                    "type_id": 5,
                    "is_required": False,
                    "configs": [
                        {
                            "context": {
                                "is_global": False,
                                "project_ids": [1, 2],
                            },
                            "options": {"is_required": True},
                        }
                    ],
                },
                {
                    "system_name": "custom_project_3",
                    "label": "Project 3 Field",
                    "type_id": 6,
                    "is_required": False,
                    "configs": [
                        {
                            "context": {
                                "is_global": False,
                                "project_ids": [3, 4],
                            },
                            "options": {"is_required": True},
                        }
                    ],
                },
            ]

            # Filter for project 1
            result = cases_api.get_required_case_fields(project_id=1)

            # Should have 2 fields: global + project 1 specific
            assert result["field_count"] == 2
            assert result["project_filtered"] is True

            field_names = [f["system_name"] for f in result["required_fields"]]
            assert "custom_global" in field_names  # Global field included
            assert (
                "custom_project_1" in field_names
            )  # Project 1 field included
            assert (
                "custom_project_3" not in field_names
            )  # Project 3 field excluded

    def test_get_required_case_fields_no_cache(
        self, cases_api: CasesAPI
    ) -> None:
        """Test get_required_case_fields with use_cache=False."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "custom_field",
                    "label": "Field",
                    "type_id": 1,
                    "is_required": True,
                    "configs": [],
                }
            ]

            # First call with cache
            result1 = cases_api.get_required_case_fields(use_cache=True)
            assert result1["cache_used"] is False  # First call, no cache yet

            # Second call with cache
            result2 = cases_api.get_required_case_fields(use_cache=True)
            assert result2["cache_used"] is True  # Should use cache

            # Third call without cache
            result3 = cases_api.get_required_case_fields(use_cache=False)
            assert result3["cache_used"] is False  # Bypassed cache

            # get_case_fields should be called twice (first and third)
            assert mock_get_fields.call_count == 2

    def test_get_required_case_fields_empty_result(
        self, cases_api: CasesAPI
    ) -> None:
        """Test get_required_case_fields when no required fields exist."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "custom_optional",
                    "label": "Optional",
                    "type_id": 1,
                    "is_required": False,
                    "configs": [
                        {
                            "context": {
                                "is_global": True,
                                "project_ids": None,
                            },
                            "options": {"is_required": False},
                        }
                    ],
                }
            ]

            result = cases_api.get_required_case_fields()

            assert result["field_count"] == 0
            assert result["required_fields"] == []

    def test_get_required_case_fields_top_level_required(
        self, cases_api: CasesAPI
    ) -> None:
        """Test get_required_case_fields with top-level is_required flag."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "title",
                    "label": "Title",
                    "type_id": 1,
                    "is_required": True,  # Top-level flag
                    "configs": [],  # No configs
                }
            ]

            result = cases_api.get_required_case_fields()

            assert result["field_count"] == 1
            field = result["required_fields"][0]
            assert field["system_name"] == "title"
            assert field["is_global"] is None  # No config context
            assert field["project_ids"] is None

    def test_get_required_case_fields_type_mapping(
        self, cases_api: CasesAPI
    ) -> None:
        """Test that type IDs are correctly mapped to type names."""
        with patch.object(cases_api, "get_case_fields") as mock_get_fields:
            mock_get_fields.return_value = [
                {
                    "system_name": "field_checkbox",
                    "type_id": 5,
                    "is_required": True,
                    "configs": [],
                },
                {
                    "system_name": "field_multiselect",
                    "type_id": 11,
                    "is_required": True,
                    "configs": [],
                },
                {
                    "system_name": "custom_steps_separated",
                    "type_id": 12,
                    "is_required": True,
                    "configs": [],
                },
            ]

            result = cases_api.get_required_case_fields()

            fields_by_name = {
                f["system_name"]: f for f in result["required_fields"]
            }

            assert fields_by_name["field_checkbox"]["type_name"] == "Checkbox"
            assert (
                fields_by_name["field_checkbox"]["type_hint"]
                == "boolean (True/False)"
            )

            assert (
                fields_by_name["field_multiselect"]["type_name"]
                == "Multi-select"
            )
            assert (
                fields_by_name["field_multiselect"]["type_hint"]
                == "array of IDs (numbers or strings)"
            )

            assert (
                fields_by_name["custom_steps_separated"]["type_name"]
                == "Stepped"
            )
            assert (
                "array of step objects"
                in fields_by_name["custom_steps_separated"]["type_hint"]
            )
