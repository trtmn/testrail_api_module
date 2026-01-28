"""
Tests for the SectionsAPI module.

This module contains comprehensive tests for all methods in the SectionsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.sections import SectionsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestSectionsAPI:
    """Test suite for SectionsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def sections_api(self, mock_client: Mock) -> SectionsAPI:
        """Create a SectionsAPI instance with mocked client."""
        return SectionsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test SectionsAPI initialization."""
        api = SectionsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_section(self, sections_api: SectionsAPI) -> None:
        """Test get_section method."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.return_value = {"id": 1, "name": "Test Section"}

            result = result = sections_api.get_section(section_id=1)
            mock_get.assert_called_once_with('get_section/1')
            assert result == {"id": 1, "name": "Test Section"}

    def test_get_sections_minimal(self, sections_api: SectionsAPI) -> None:
        """Test get_sections with minimal required parameters."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "name": "Section 1"},
                {"id": 2, "name": "Section 2"}
            ]

            result = sections_api.get_sections(project_id=1)

            mock_get.assert_called_once_with(
                'get_sections/1',
                params={}
            )
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_sections_with_suite_id(
            self, sections_api: SectionsAPI) -> None:
        """Test get_sections with suite_id parameter."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.return_value = [{"id": 1, "name": "Section 1"}]

            sections_api.get_sections(project_id=1, suite_id=2)

            expected_params = {'suite_id': 2}
            mock_get.assert_called_once_with(
                'get_sections/1',
                params=expected_params
            )

    def test_add_section_minimal(self, sections_api: SectionsAPI) -> None:
        """Test add_section with minimal required parameters."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Section"}

            result = sections_api.add_section(
                project_id=1,
                name="New Section"
            )

            expected_data = {"name": "New Section"}
            mock_post.assert_called_once_with(
                'add_section/1',
                data=expected_data
            )
            assert result == {"id": 1, "name": "New Section"}

    def test_add_section_with_all_parameters(
            self, sections_api: SectionsAPI) -> None:
        """Test add_section with all optional parameters."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Section"}

            sections_api.add_section(
                project_id=1,
                name="New Section",
                description="Section description",
                suite_id=2,
                parent_id=3
            )

            expected_data = {
                "name": "New Section",
                "description": "Section description",
                "suite_id": 2,
                "parent_id": 3
            }
            mock_post.assert_called_once_with(
                'add_section/1',
                data=expected_data
            )

    def test_add_section_with_none_values(
            self, sections_api: SectionsAPI) -> None:
        """Test add_section with None values for optional parameters."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "New Section"}

            sections_api.add_section(
                project_id=1,
                name="New Section",
                description=None,
                suite_id=None,
                parent_id=None
            )

            expected_data = {"name": "New Section"}
            mock_post.assert_called_once_with(
                'add_section/1',
                data=expected_data
            )

    def test_update_section_minimal(self, sections_api: SectionsAPI) -> None:
        """Test update_section with minimal parameters (only section_id)."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1}

            result = sections_api.update_section(section_id=1)

            expected_data = {}
            mock_post.assert_called_once_with(
                'update_section/1',
                data=expected_data
            )
            assert result == {"id": 1}

    def test_update_section_with_all_parameters(
            self, sections_api: SectionsAPI) -> None:
        """Test update_section with all optional parameters."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1, "name": "Updated Section"}

            sections_api.update_section(
                section_id=1,
                name="Updated Section",
                description="Updated description",
                parent_id=2
            )

            expected_data = {
                "name": "Updated Section",
                "description": "Updated description",
                "parent_id": 2
            }
            mock_post.assert_called_once_with(
                'update_section/1',
                data=expected_data
            )

    def test_update_section_with_none_values(
            self, sections_api: SectionsAPI) -> None:
        """Test update_section with None values."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {"id": 1}

            sections_api.update_section(
                section_id=1,
                name=None,
                description=None,
                parent_id=None
            )

            expected_data = {}
            mock_post.assert_called_once_with(
                'update_section/1',
                data=expected_data
            )

    def test_delete_section(self, sections_api: SectionsAPI) -> None:
        """Test delete_section method."""
        with patch.object(sections_api, '_post') as mock_post:
            mock_post.return_value = {}

            result = sections_api.delete_section(section_id=1)
            mock_post.assert_called_once_with('delete_section/1')
            assert result == {}

    def test_get_section_cases(self, sections_api: SectionsAPI) -> None:
        """Test get_section_cases method."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.return_value = [
                {"id": 1, "title": "Case 1"},
                {"id": 2, "title": "Case 2"}
            ]

            result = sections_api.get_section_cases(section_id=1)

            mock_get.assert_called_once_with('get_section_cases/1')
            assert len(result) == 2
            assert result[0]["id"] == 1

    def test_get_section_stats(self, sections_api: SectionsAPI) -> None:
        """Test get_section_stats method."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.return_value = {
                "total": 10,
                "passed": 8,
                "failed": 2
            }

            result = sections_api.get_section_stats(section_id=1)
            mock_get.assert_called_once_with('get_section_stats/1')
            assert result["total"] == 10

    def test_api_request_failure(self, sections_api: SectionsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                sections_api.get_section(section_id=1)

    def test_authentication_error(self, sections_api: SectionsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed")

            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                sections_api.get_section(section_id=1)

    def test_rate_limit_error(self, sections_api: SectionsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(sections_api, '_get') as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded")

            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                sections_api.get_section(section_id=1)
