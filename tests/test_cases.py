"""
Tests for the CasesAPI module.

This module contains comprehensive tests for all methods in the CasesAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch

from testrail_api_module.cases import CasesAPI


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
            "priority_id": 3,
            "estimate": "1h",
            "milestone_id": 1,
            "refs": "REQ-123",
            "description": "Test case description",
            "preconditions": "Test preconditions",
            "postconditions": "Test postconditions",
        }

    def test_init(self, mock_client):
        """Test CasesAPI initialization."""
        api = CasesAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_case(self, cases_api, sample_case_data):
        """Test get_case method."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = sample_case_data

            result = cases_api.get_case(case_id=1)

            mock_request.assert_called_once_with("GET", "get_case/1")
            assert result == sample_case_data

    def test_get_case_with_large_id(self, cases_api):
        """Test get_case with a large case ID."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 999999, "title": "Large ID Case"}

            result = cases_api.get_case(case_id=999999)

            mock_request.assert_called_once_with("GET", "get_case/999999")
            assert result == {"id": 999999, "title": "Large ID Case"}

    def test_get_cases_project_only(self, cases_api):
        """Test get_cases with only project_id."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1}, {"id": 2}]

            result = cases_api.get_cases(project_id=1)

            mock_request.assert_called_once_with("GET", "get_cases/1")
            assert result == [{"id": 1}, {"id": 2}]

    def test_get_cases_with_suite_id(self, cases_api):
        """Test get_cases with project_id and suite_id."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1, "suite_id": 1}]

            result = cases_api.get_cases(project_id=1, suite_id=1)

            mock_request.assert_called_once_with("GET", "get_cases/1&suite_id=1")
            assert result == [{"id": 1, "suite_id": 1}]

    def test_get_cases_with_section_id(self, cases_api):
        """Test get_cases with project_id and section_id."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1, "section_id": 1}]

            result = cases_api.get_cases(project_id=1, section_id=1)

            mock_request.assert_called_once_with("GET", "get_cases/1&section_id=1")
            assert result == [{"id": 1, "section_id": 1}]

    def test_get_cases_with_both_suite_and_section(self, cases_api):
        """Test get_cases with project_id, suite_id, and section_id."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = [{"id": 1, "suite_id": 1, "section_id": 1}]

            result = cases_api.get_cases(project_id=1, suite_id=1, section_id=1)

            mock_request.assert_called_once_with(
                "GET", "get_cases/1&suite_id=1&section_id=1"
            )
            assert result == [{"id": 1, "suite_id": 1, "section_id": 1}]

    def test_add_case_minimal(self, cases_api, sample_case_data):
        """Test add_case with minimal required parameters."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = sample_case_data

            result = cases_api.add_case(section_id=1, title="Test Case Title")

            expected_data = {"title": "Test Case Title"}
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == sample_case_data

    def test_add_case_with_all_parameters(self, cases_api, sample_case_data):
        """Test add_case with all optional parameters."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = sample_case_data

            result = cases_api.add_case(
                section_id=1,
                title="Test Case Title",
                template_id=1,
                type_id=2,
                priority_id=3,
                estimate="1h",
                milestone_id=1,
                refs="REQ-123",
                description="Test case description",
                preconditions="Test preconditions",
                postconditions="Test postconditions",
                custom_fields={"custom1": "value1", "custom2": "value2"},
            )

            expected_data = {
                "title": "Test Case Title",
                "template_id": 1,
                "type_id": 2,
                "priority_id": 3,
                "estimate": "1h",
                "milestone_id": 1,
                "refs": "REQ-123",
                "description": "Test case description",
                "preconditions": "Test preconditions",
                "postconditions": "Test postconditions",
                "custom1": "value1",
                "custom2": "value2",
            }
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == sample_case_data

    def test_add_case_with_none_values(self, cases_api):
        """Test add_case with None values for optional parameters."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "title": "Test Case"}

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
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "title": "Test Case"}

    def test_add_case_with_empty_strings(self, cases_api):
        """Test add_case with empty strings for optional parameters."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "title": "Test Case"}

            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                template_id=0,
                type_id=0,
                priority_id=0,
                estimate="",
                milestone_id=0,
                refs="",
                description="",
                preconditions="",
                postconditions="",
                custom_fields={},
            )

            expected_data = {"title": "Test Case"}
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "title": "Test Case"}

    def test_update_case(self, cases_api, sample_case_data):
        """Test update_case method."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = sample_case_data

            result = cases_api.update_case(
                case_id=1,
                title="Updated Title",
                priority_id=2,
                description="Updated description",
            )

            expected_data = {
                "title": "Updated Title",
                "priority_id": 2,
                "description": "Updated description",
            }
            mock_request.assert_called_once_with(
                "POST", "update_case/1", data=expected_data
            )
            assert result == sample_case_data

    def test_update_case_with_custom_fields(self, cases_api):
        """Test update_case with custom fields."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "custom_field": "value"}

            result = cases_api.update_case(
                case_id=1, title="Updated Title", custom_field="value"
            )

            expected_data = {"title": "Updated Title", "custom_field": "value"}
            mock_request.assert_called_once_with(
                "POST", "update_case/1", data=expected_data
            )
            assert result == {"id": 1, "custom_field": "value"}

    def test_delete_case(self, cases_api):
        """Test delete_case method."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"success": True}

            result = cases_api.delete_case(case_id=1)

            mock_request.assert_called_once_with("POST", "delete_case/1")
            assert result == {"success": True}

    def test_delete_case_with_large_id(self, cases_api):
        """Test delete_case with a large case ID."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"success": True}

            result = cases_api.delete_case(case_id=999999)

            mock_request.assert_called_once_with("POST", "delete_case/999999")
            assert result == {"success": True}

    def test_get_case_fields(self, cases_api):
        """Test get_case_fields method."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "Title", "type_id": 1},
                {"id": 2, "name": "Description", "type_id": 2},
                {"id": 3, "name": "Priority", "type_id": 3},
            ]

            result = cases_api.get_case_fields()

            mock_request.assert_called_once_with("GET", "get_case_fields")
            assert result == [
                {"id": 1, "name": "Title", "type_id": 1},
                {"id": 2, "name": "Description", "type_id": 2},
                {"id": 3, "name": "Priority", "type_id": 3},
            ]

    def test_api_request_failure(self, cases_api):
        """Test API request failure handling."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = None

            result = cases_api.get_case(case_id=1)

            assert result is None

    @pytest.mark.parametrize("type_id", [1, 2, 3, 4, 5, 6])
    def test_different_type_ids(self, cases_api, type_id):
        """Test add_case with different type_id values."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "type_id": type_id}

            result = cases_api.add_case(
                section_id=1, title="Test Case", type_id=type_id
            )

            expected_data = {"title": "Test Case", "type_id": type_id}
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "type_id": type_id}

    @pytest.mark.parametrize("priority_id", [1, 2, 3, 4])
    def test_different_priority_ids(self, cases_api, priority_id):
        """Test add_case with different priority_id values."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "priority_id": priority_id}

            result = cases_api.add_case(
                section_id=1, title="Test Case", priority_id=priority_id
            )

            expected_data = {"title": "Test Case", "priority_id": priority_id}
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "priority_id": priority_id}

    def test_large_section_id(self, cases_api):
        """Test add_case with a large section ID."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "section_id": 999999}

            result = cases_api.add_case(section_id=999999, title="Test Case")

            expected_data = {"title": "Test Case"}
            mock_request.assert_called_once_with(
                "POST", "add_case/999999", data=expected_data
            )
            assert result == {"id": 1, "section_id": 999999}

    def test_complex_custom_fields(self, cases_api):
        """Test add_case with complex custom fields."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "custom_complex": "value"}

            custom_fields = {
                "custom_complex": "value",
                "custom_number": 42,
                "custom_boolean": True,
                "custom_list": ["item1", "item2"],
                "custom_dict": {"key": "value"},
            }

            result = cases_api.add_case(
                section_id=1, title="Test Case", custom_fields=custom_fields
            )

            expected_data = {
                "title": "Test Case",
                "custom_complex": "value",
                "custom_number": 42,
                "custom_boolean": True,
                "custom_list": ["item1", "item2"],
                "custom_dict": {"key": "value"},
            }
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "custom_complex": "value"}

    def test_empty_cases_list(self, cases_api):
        """Test get_cases returning empty list."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = []

            result = cases_api.get_cases(project_id=1)

            mock_request.assert_called_once_with("GET", "get_cases/1")
            assert result == []

    def test_zero_values_handling(self, cases_api):
        """Test handling of zero values for optional parameters."""
        with patch.object(cases_api, "_api_request") as mock_request:
            mock_request.return_value = {"id": 1, "title": "Test Case"}

            result = cases_api.add_case(
                section_id=1,
                title="Test Case",
                template_id=0,
                type_id=0,
                priority_id=0,
                milestone_id=0,
            )

            expected_data = {"title": "Test Case"}
            mock_request.assert_called_once_with(
                "POST", "add_case/1", data=expected_data
            )
            assert result == {"id": 1, "title": "Test Case"}
