"""
Tests for the AttachmentsAPI module.

This module contains comprehensive tests for all methods in the AttachmentsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import TYPE_CHECKING

from testrail_api_module.attachments import AttachmentsAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestAttachmentsAPI:
    """Test suite for AttachmentsAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def attachments_api(self, mock_client: Mock) -> AttachmentsAPI:
        """Create an AttachmentsAPI instance with mocked client."""
        return AttachmentsAPI(mock_client)

    def test_init(self, mock_client: Mock) -> None:
        """Test AttachmentsAPI initialization."""
        api = AttachmentsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_attachment(self, attachments_api: AttachmentsAPI) -> None:
        """Test get_attachment method."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "file.txt"}

            result = attachments_api.get_attachment(attachment_id=1)

            mock_request.assert_called_once_with('GET', 'get_attachment/1')
            assert result == {"id": 1, "name": "file.txt"}

    def test_get_attachments(self, attachments_api: AttachmentsAPI) -> None:
        """Test get_attachments method."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = [
                {"id": 1, "name": "file1.txt"},
                {"id": 2, "name": "file2.txt"}
            ]

            result = attachments_api.get_attachments(
                entity_type="case", entity_id=1)

            mock_request.assert_called_once_with(
                'GET', 'get_attachments/case/1')
            assert len(result) == 2

    @pytest.mark.parametrize("entity_type", ["case", "run", "plan", "project"])
    def test_get_attachments_different_entity_types(
            self, attachments_api: AttachmentsAPI, entity_type: str) -> None:
        """Test get_attachments with different entity types."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = [{"id": 1}]

            attachments_api.get_attachments(
                entity_type=entity_type, entity_id=1)

            mock_request.assert_called_once_with(
                'GET', f'get_attachments/{entity_type}/1')

    def test_add_attachment_minimal(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test add_attachment with minimal required parameters."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "file.txt"}

            result = attachments_api.add_attachment(
                entity_type="case",
                entity_id=1,
                file_path="/path/to/file.txt"
            )

            expected_data = {"file": "/path/to/file.txt"}
            mock_request.assert_called_once_with(
                'POST', 'add_attachment/case/1', data=expected_data)
            assert result == {"id": 1, "name": "file.txt"}

    def test_add_attachment_with_description(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test add_attachment with description."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1, "name": "file.txt"}

            attachments_api.add_attachment(
                entity_type="case",
                entity_id=1,
                file_path="/path/to/file.txt",
                description="Test file"
            )

            expected_data = {
                "file": "/path/to/file.txt",
                "description": "Test file"
            }
            mock_request.assert_called_once_with(
                'POST', 'add_attachment/case/1', data=expected_data)

    def test_add_attachment_without_description(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test add_attachment without description."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = {"id": 1}

            attachments_api.add_attachment(
                entity_type="run",
                entity_id=1,
                file_path="/path/to/file.txt",
                description=None
            )

            expected_data = {"file": "/path/to/file.txt"}
            mock_request.assert_called_once_with(
                'POST', 'add_attachment/run/1', data=expected_data)

    def test_delete_attachment(self, attachments_api: AttachmentsAPI) -> None:
        """Test delete_attachment method."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = {}

            result = attachments_api.delete_attachment(attachment_id=1)

            mock_request.assert_called_once_with('POST', 'delete_attachment/1')
            assert result == {}

    def test_get_attachment_content(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test get_attachment_content method."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.return_value = b"file content"

            result = attachments_api.get_attachment_content(attachment_id=1)

            mock_request.assert_called_once_with(
                'GET', 'get_attachment_content/1')
            assert result == b"file content"

    def test_api_request_failure(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                attachments_api.get_attachment(attachment_id=1)

    def test_authentication_error(
            self, attachments_api: AttachmentsAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError(
                "Authentication failed")

            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                attachments_api.get_attachment(attachment_id=1)

    def test_rate_limit_error(self, attachments_api: AttachmentsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(attachments_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError(
                "Rate limit exceeded")

            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                attachments_api.get_attachment(attachment_id=1)
