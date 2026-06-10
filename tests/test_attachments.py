"""
Tests for the AttachmentsAPI module.

This module contains comprehensive tests for all methods in the AttachmentsAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.attachments import AttachmentsAPI
from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)

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

    @pytest.fixture
    def sample_attachment_data(self) -> dict:
        """Sample attachment data returned by upload endpoints."""
        return {"attachment_id": 443}

    def test_init(self, mock_client: Mock) -> None:
        """Test AttachmentsAPI initialization."""
        api = AttachmentsAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_add_attachment_to_case(
        self,
        attachments_api: AttachmentsAPI,
        sample_attachment_data: dict,
    ) -> None:
        """Test add_attachment_to_case uploads via multipart."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.return_value = sample_attachment_data

            result = attachments_api.add_attachment_to_case(
                case_id=1, file_path="/path/to/file.png"
            )

            mock_multipart.assert_called_once_with(
                "add_attachment_to_case/1", "/path/to/file.png"
            )
            assert result == {"attachment_id": 443}

    def test_add_attachment_to_plan(
        self,
        attachments_api: AttachmentsAPI,
        sample_attachment_data: dict,
    ) -> None:
        """Test add_attachment_to_plan uploads via multipart."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.return_value = sample_attachment_data

            result = attachments_api.add_attachment_to_plan(
                plan_id=2, file_path="/path/to/file.png"
            )

            mock_multipart.assert_called_once_with(
                "add_attachment_to_plan/2", "/path/to/file.png"
            )
            assert result == {"attachment_id": 443}

    def test_add_attachment_to_plan_entry(
        self,
        attachments_api: AttachmentsAPI,
        sample_attachment_data: dict,
    ) -> None:
        """Test add_attachment_to_plan_entry uses both plan and entry IDs."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.return_value = sample_attachment_data

            result = attachments_api.add_attachment_to_plan_entry(
                plan_id=2, entry_id=7, file_path="/path/to/file.png"
            )

            mock_multipart.assert_called_once_with(
                "add_attachment_to_plan_entry/2/7", "/path/to/file.png"
            )
            assert result == {"attachment_id": 443}

    def test_add_attachment_to_result(
        self,
        attachments_api: AttachmentsAPI,
        sample_attachment_data: dict,
    ) -> None:
        """Test add_attachment_to_result uploads via multipart."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.return_value = sample_attachment_data

            result = attachments_api.add_attachment_to_result(
                result_id=3, file_path="/path/to/file.png"
            )

            mock_multipart.assert_called_once_with(
                "add_attachment_to_result/3", "/path/to/file.png"
            )
            assert result == {"attachment_id": 443}

    def test_add_attachment_to_run(
        self,
        attachments_api: AttachmentsAPI,
        sample_attachment_data: dict,
    ) -> None:
        """Test add_attachment_to_run uploads via multipart."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.return_value = sample_attachment_data

            result = attachments_api.add_attachment_to_run(
                run_id=4, file_path="/path/to/file.png"
            )

            mock_multipart.assert_called_once_with(
                "add_attachment_to_run/4", "/path/to/file.png"
            )
            assert result == {"attachment_id": 443}

    def test_add_attachment_file_not_found(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test upload methods propagate FileNotFoundError."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.side_effect = FileNotFoundError("missing")

            with pytest.raises(FileNotFoundError):
                attachments_api.add_attachment_to_case(
                    case_id=1, file_path="/nonexistent/file.png"
                )

    def test_get_attachments_for_case_minimal(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_case with minimal parameters."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 1, "name": "file.png"}]

            result = attachments_api.get_attachments_for_case(case_id=1)

            mock_get.assert_called_once_with(
                "get_attachments_for_case/1", params={}
            )
            assert result == [{"id": 1, "name": "file.png"}]

    def test_get_attachments_for_case_all_params(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_case with limit and offset."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = {
                "offset": 50,
                "limit": 25,
                "size": 25,
                "attachments": [{"id": 1}],
            }

            result = attachments_api.get_attachments_for_case(
                case_id=1, limit=25, offset=50
            )

            mock_get.assert_called_once_with(
                "get_attachments_for_case/1",
                params={"limit": 25, "offset": 50},
            )
            assert result["attachments"] == [{"id": 1}]

    def test_get_attachments_for_case_none_params(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_case excludes None parameters."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = []

            result = attachments_api.get_attachments_for_case(
                case_id=1, limit=None, offset=None
            )

            mock_get.assert_called_once_with(
                "get_attachments_for_case/1", params={}
            )
            assert result == []

    def test_get_attachments_for_plan_minimal(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_plan with minimal parameters."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 2}]

            result = attachments_api.get_attachments_for_plan(plan_id=2)

            mock_get.assert_called_once_with(
                "get_attachments_for_plan/2", params={}
            )
            assert result == [{"id": 2}]

    def test_get_attachments_for_plan_all_params(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_plan with limit and offset."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 2}]

            result = attachments_api.get_attachments_for_plan(
                plan_id=2, limit=10, offset=20
            )

            mock_get.assert_called_once_with(
                "get_attachments_for_plan/2",
                params={"limit": 10, "offset": 20},
            )
            assert result == [{"id": 2}]

    def test_get_attachments_for_plan_entry(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_plan_entry uses both IDs."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 3}]

            result = attachments_api.get_attachments_for_plan_entry(
                plan_id=2, entry_id=7
            )

            mock_get.assert_called_once_with(
                "get_attachments_for_plan_entry/2/7"
            )
            assert result == [{"id": 3}]

    def test_get_attachments_for_run_minimal(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_run with minimal parameters."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 4}]

            result = attachments_api.get_attachments_for_run(run_id=4)

            mock_get.assert_called_once_with(
                "get_attachments_for_run/4", params={}
            )
            assert result == [{"id": 4}]

    def test_get_attachments_for_run_all_params(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_run with limit and offset."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 4}]

            result = attachments_api.get_attachments_for_run(
                run_id=4, limit=5, offset=0
            )

            mock_get.assert_called_once_with(
                "get_attachments_for_run/4",
                params={"limit": 5, "offset": 0},
            )
            assert result == [{"id": 4}]

    def test_get_attachments_for_test(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachments_for_test method."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = [{"id": 5}]

            result = attachments_api.get_attachments_for_test(test_id=5)

            mock_get.assert_called_once_with("get_attachments_for_test/5")
            assert result == [{"id": 5}]

    def test_get_attachment_int_id(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachment downloads raw bytes with an integer ID."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = b"\x89PNG binary data"

            result = attachments_api.get_attachment(attachment_id=1)

            mock_get.assert_called_once_with("get_attachment/1", raw=True)
            assert result == b"\x89PNG binary data"

    def test_get_attachment_uuid_id(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test get_attachment with a UUID string ID (newer TestRail)."""
        uuid = "5c5e8b3a-21c7-4f73-a0ef-d09e9f1b8c19"
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.return_value = b"binary"

            result = attachments_api.get_attachment(attachment_id=uuid)

            mock_get.assert_called_once_with(
                f"get_attachment/{uuid}", raw=True
            )
            assert result == b"binary"

    def test_delete_attachment_int_id(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test delete_attachment with an integer ID."""
        with patch.object(attachments_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = attachments_api.delete_attachment(attachment_id=1)

            mock_post.assert_called_once_with("delete_attachment/1")
            assert result == {}

    def test_delete_attachment_uuid_id(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test delete_attachment with a UUID string ID (newer TestRail)."""
        uuid = "5c5e8b3a-21c7-4f73-a0ef-d09e9f1b8c19"
        with patch.object(attachments_api, "_post") as mock_post:
            mock_post.return_value = {}

            result = attachments_api.delete_attachment(attachment_id=uuid)

            mock_post.assert_called_once_with(f"delete_attachment/{uuid}")
            assert result == {}

    def test_api_request_failure(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test behavior when API request fails."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                attachments_api.get_attachment(attachment_id=1)

    def test_authentication_error(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test behavior when authentication fails."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                attachments_api.get_attachment(attachment_id=1)

    def test_rate_limit_error(self, attachments_api: AttachmentsAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(attachments_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                attachments_api.get_attachment(attachment_id=1)

    def test_upload_authentication_error(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test upload methods propagate authentication errors."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                attachments_api.add_attachment_to_case(
                    case_id=1, file_path="/path/to/file.png"
                )

    def test_upload_rate_limit_error(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test upload methods propagate rate limit errors."""
        with patch.object(
            attachments_api, "_post_multipart"
        ) as mock_multipart:
            mock_multipart.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                attachments_api.add_attachment_to_run(
                    run_id=1, file_path="/path/to/file.png"
                )

    def test_removed_generic_methods_are_gone(
        self, attachments_api: AttachmentsAPI
    ) -> None:
        """Test the fabricated generic methods were removed (they called
        endpoints that do not exist in any TestRail version)."""
        assert not hasattr(attachments_api, "get_attachments")
        assert not hasattr(attachments_api, "add_attachment")
